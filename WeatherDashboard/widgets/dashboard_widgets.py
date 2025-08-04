"""
Main widget coordinator for the Weather Dashboard application.

This module provides the primary widget coordination class that manages
all UI components including control widgets, metric displays, charts,
and tabbed interfaces. Orchestrates widget initialization, updates,
and event handling throughout the application.

Classes:
    WeatherDashboardWidgets: Main widget coordinator and manager
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Callable, Optional, List

from WeatherDashboard import config, styles, dialog
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.widget_utils import WidgetUtils

from .widget_interface import IWeatherDashboardWidgets
from .base_widgets import BaseWidgetManager, widget_error_handler
from .widget_registry import WidgetRegistry
from .title_widgets import TitleWidget
from .control_widgets import ControlWidgets
from .tabbed_widgets import TabbedDisplayWidgets
from .metric_widgets import MetricDisplayWidgets
from .chart_widgets import ChartWidgets
from .status_bar_widgets import StatusBarWidgets


class WeatherDashboardWidgets(BaseWidgetManager, IWeatherDashboardWidgets):
    """Manage all widget components and UI updates for the Weather Dashboard.
    
    Coordinates the initialization and management of all UI components including
    control widgets, metric displays, chart widgets, and tabbed interfaces.
    Provides a unified interface for widget updates and event handling.
    
    Attributes:
        frames: Dictionary of UI frame containers
        state: Application state manager
        update_callback: Callback function for update button events
        clear_callback: Callback function for clear/reset button events
        dropdown_callback: Callback function for dropdown change events
        control_widgets: Control panel widget manager
        metric_widgets: Metric display widget manager
        chart_widgets: Chart display widget manager
    """

    def __init__(self, frames: Dict[str, ttk.Frame], state: Any, update_cb: Callable, clear_cb: Callable,
                 dropdown_cb: Callable, cancel_cb: Callable = None, scheduler_cb: Callable = None,
                 theme_cb: Callable = None) -> None:
        """Initialize the widget coordinator with error handling.
        
        Sets up all widget managers and connects them to the application state
        and callback functions for proper event handling.
        
        Args:
            frames: Dictionary of UI frame containers
            state: Application state manager
            update_cb: Callback function for update button events
            clear_cb: Callback function for clear/reset button events
            dropdown_cb: Callback function for dropdown change events
            cancel_cb: Callback function for operation cancellation
            scheduler_cb: Scheduler toggle callback
            theme_cb: Theme change callback
        """
        # Direct imports for stable utilities
        self.logger = Logger()
        self.config = config
        self.styles = styles
        self.dialog = dialog
        self.widget_utils = WidgetUtils()

        # Injected dependencies for testable components
        self.frames = frames
        self.state = state
        
        # Callback mapping for cleaner organization
        self.callbacks = {
            'update': update_cb,
            'reset': clear_cb,
            'dropdown_update': dropdown_cb,
            'cancel': cancel_cb,
        }
        # Separate because in title frame
        self.scheduler_callback = scheduler_cb
        self.theme_callback = theme_cb
        
        # Widget component references
        self.title_widget: Optional[TitleWidget] = None
        self.control_widgets: Optional[ControlWidgets] = None
        self.tabbed_widgets: Optional[TabbedDisplayWidgets] = None
        self.status_bar_widgets: Optional[StatusBarWidgets] = None

        # Add convenience properties for accessing nested widgets
        self._metric_widgets: Optional[MetricDisplayWidgets] = None
        self._chart_widgets: Optional[ChartWidgets] = None

        # Initialize widget registry
        self.widget_registry = WidgetRegistry()
        # Register all frames with the registry
        for frame_id, frame in frames.items():
            self.widget_registry.register_frame(frame_id, frame)
        
        # Initialize base class with error handling
        super().__init__(None, state, "dashboard widgets")
        
        # Create widgets with standardized error handling
        if not self.safe_create_widgets():
            self.logger.warn("Dashboard widgets created with errors - some functionality may be limited")
    
    def _create_widgets(self) -> None:
        """Initialize all widget components base class error handling.
        
        Creates all widget sections in the correct order with comprehensive
        error handling. If any widget creation fails, displays appropriate
        error messages and re-raises the exception.
        
        Raises:
            tk.TclError: If GUI widget creation fails
            Exception: For other unexpected errors during setup
        """
        layout_config = self.styles.LAYOUT_CONFIG()
        dashboard_config = layout_config['widget_positions'].get('dashboard_sections', {})

        try:
            self.logger.info("Creating dashboard widgets")
            
            # Use centralized frame assignments
            title_frame = self.frames[dashboard_config.get('title_frame', 'title')]
            control_frame = self.frames[dashboard_config.get('control_frame', 'control')]
            tabbed_frame = self.frames[dashboard_config.get('tabbed_frame', 'tabbed')]
            status_frame = self.frames[dashboard_config.get('status_frame', 'status_bar')]
            
            self._create_title_section(title_frame)
            self._create_control_section(control_frame)
            self._create_tabbed_section(tabbed_frame)
            self._create_status_bar_section(status_frame)
            
            self.logger.info("Dashboard widgets created successfully")

        except tk.TclError as e:
            self.logger.error(f"GUI widget creation failed: {e}")
            self.dialog.dialog_manager.show_error("GUI Error", f"Failed to create interface: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during GUI setup: {e}")
            self.dialog.dialog_manager.show_error("Setup Error", f"Failed to initialize dashboard: {e}")
            raise
    
    @widget_error_handler("title section")
    def _create_title_section(self, title_frame: ttk.Frame) -> None:
        """Create the title widget section."""
        self.title_widget = TitleWidget(
            title_frame, 
            scheduler_callback=self.scheduler_callback,
            theme_callback=self.theme_callback
        )

        # Register title widget with registry
        self.widget_registry.register_widget(
            widget_id='title_widget',
            widget=self.title_widget,
            widget_type='title',
            parent_frame=title_frame,
            position={'pack': {'fill': 'x', 'padx': self.styles.CONTROL_PANEL_CONFIG()['padding']['standard'], 'pady': self.styles.CONTROL_PANEL_CONFIG()['padding']['standard']}},
            style='Title.TFrame'
        )
    
    @widget_error_handler("control section")
    def _create_control_section(self, control_frame: ttk.Frame) -> None:
        """Create the control widgets section."""
        self.control_widgets = ControlWidgets(control_frame, self.state, self.callbacks)

        self.widget_registry.register_widget(
            widget_id='control_widgets',
            widget=self.control_widgets,
            widget_type='control',
            parent_frame=control_frame,
            position={'pack': {'fill': 'x', 'padx': self.styles.CONTROL_PANEL_CONFIG()['padding']['standard'], 'pady': self.styles.CONTROL_PANEL_CONFIG()['padding']['standard']}},
            style='Control.TFrame'
        )
    
    @widget_error_handler("tabbed section")
    def _create_tabbed_section(self, tabbed_frame: ttk.Frame) -> None:
        """Create the tabbed display section."""
        self.tabbed_widgets = TabbedDisplayWidgets(tabbed_frame, self.state, self.widget_registry)
        
        self.widget_registry.register_widget(
            widget_id='tabbed_widgets',
            widget=self.tabbed_widgets,
            widget_type='tabbed',
            parent_frame=tabbed_frame,
            position={'pack': {'fill': 'both', 'expand': True}},
            style='Tabbed.TFrame'
        )

    @widget_error_handler("status bar section")
    def _create_status_bar_section(self, status_frame: ttk.Frame) -> None:
        """Create the status bar section."""
        self.status_bar_widgets = StatusBarWidgets(status_frame, self.state)

        # Register status bar widgets with registry
        self.widget_registry.register_widget(
            widget_id='status_bar_widgets',
            widget=self.status_bar_widgets,
            widget_type='status',
            parent_frame=status_frame,
            position={'pack': {'fill': 'x', 'side': 'bottom'}},
            style='Status.TFrame'
        )

    @property
    def metric_widgets(self) -> Optional[MetricDisplayWidgets]:
        """Get metric widgets from tabbed widgets."""
        if self.tabbed_widgets and hasattr(self.tabbed_widgets, 'get_metric_widgets'):
            return self.tabbed_widgets.get_metric_widgets()
        return None

    @property
    def chart_widgets(self) -> Optional[ChartWidgets]:
        """Get chart widgets from tabbed widgets."""
        if self.tabbed_widgets and hasattr(self.tabbed_widgets, 'get_chart_widgets'):
            return self.tabbed_widgets.get_chart_widgets()
        return None
        
    # DELEGATION METHODS
    def is_ready(self) -> bool:
        """Return True if all sub-widgets are ready."""
        return all([
            (self.metric_widgets and self.metric_widgets.is_ready()),
            (self.status_bar_widgets and self.status_bar_widgets.is_ready()),
            (self.chart_widgets and self.chart_widgets.is_ready()) if self.chart_widgets else True,
            (self.control_widgets and self.control_widgets.is_ready()) if self.control_widgets else True,
        ])

    def get_creation_error(self) -> Optional[str]:
        """Return the first creation error from sub-widgets, or None."""
        for w in [self.metric_widgets, self.status_bar_widgets, self.chart_widgets, self.control_widgets]:
            if w and w.get_creation_error():
                return w.get_creation_error()
        return None

    def update_metric_display(self, metrics: Dict[str, str]) -> None:
        """Delegate metric display update to metric_widgets."""
        if self.metric_widgets:
            self.metric_widgets.update_metric_display(metrics)

    def update_chart_display(self, x_vals: List[str], y_vals: List[Any], metric_key: str, city: str, unit_system: str) -> None:
        """Delegate chart display update to chart_widgets."""
        if self.chart_widgets:
            self.chart_widgets.update_chart_display(x_vals, y_vals, metric_key, city, unit_system)

    def clear_chart_with_error_message(self) -> None:
        """Delegate chart clearing to chart_widgets."""
        if self.chart_widgets:
            self.chart_widgets.clear_chart_with_error_message()

    def update_status_bar(self, city_name: str, error_exception: Optional[Exception], simulated: bool=False) -> None:
        """Delegate status bar update to status_bar_widgets."""
        if self.status_bar_widgets:
            self.status_bar_widgets.update_status_bar(city_name, error_exception, simulated)

    def update_alerts(self, raw_data: Dict[str, Any]) -> None:
        """Delegate alert update to metric_widgets."""
        if self.metric_widgets:
            self.metric_widgets.update_alerts(raw_data)

    def get_alert_popup_parent(self) -> Any:
        """Return the alert popup parent from metric_widgets."""
        if self.metric_widgets:
            return self.metric_widgets.get_alert_popup_parent()
        return None

    def get_registry(self) -> WidgetRegistry:
        """Get the widget registry for direct access."""
        return self.widget_registry

    def apply_style_to_widget(self, widget_id: str, style: str) -> bool:
        """Apply a style to a specific widget through the registry."""
        return self.widget_registry.apply_style_to_widget(widget_id, style)

    def apply_style_to_type(self, widget_type: str, style: str) -> int:
        """Apply a style to all widgets of a specific type through the registry."""
        return self.widget_registry.apply_style_to_type(widget_type, style)

    def move_widget(self, widget_id: str, new_frame_id: str, new_position: Dict[str, Any]) -> bool:
        """Move a widget to a different frame and position through the registry."""
        return self.widget_registry.move_widget(widget_id, new_frame_id, new_position)

    def show_widget(self, widget_id: str) -> bool:
        """Show a widget through the registry."""
        return self.widget_registry.show_widget(widget_id)

    def hide_widget(self, widget_id: str) -> bool:
        """Hide a widget through the registry."""
        return self.widget_registry.hide_widget(widget_id)