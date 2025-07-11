"""
Main widget coordinator for the Weather Dashboard application.

This module provides the primary widget coordination class that manages
all UI components including control widgets, metric displays, charts,
and tabbed interfaces. Orchestrates widget initialization, updates,
and event handling throughout the application.

Classes:
    WeatherDashboardWidgets: Main widget coordinator and manager
"""

from typing import Dict, Any, Callable, List, Optional
import tkinter as tk
from tkinter import ttk, messagebox

from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.widgets.title_widgets import TitleWidget
from WeatherDashboard.widgets.control_widgets import ControlWidgets
from WeatherDashboard.widgets.metric_widgets import MetricDisplayWidgets
from WeatherDashboard.widgets.chart_widgets import ChartWidgets
from WeatherDashboard.widgets.tabbed_widgets import TabbedDisplayWidgets
from WeatherDashboard.widgets.status_bar_widgets import StatusBarWidgets

class WeatherDashboardWidgets:
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
    def __init__(self, frames: Dict[str, ttk.Frame], state: Any, update_cb: Callable, clear_cb: Callable, dropdown_cb: Callable) -> None:
        """Initialize the widget coordinator with all UI components.
        
        Sets up all widget managers and connects them to the application state
        and callback functions for proper event handling.
        
        Args:
            frames: Dictionary of UI frame containers
            state: Application state manager
            update_cb: Callback function for update button events
            clear_cb: Callback function for clear/reset button events
            dropdown_cb: Callback function for dropdown change events
        """
        self.frames = frames
        self.state = state
        
        # Callback mapping for cleaner organization
        self.callbacks = {
            'update': update_cb,
            'reset': clear_cb,
            'dropdown_update': dropdown_cb
        }
        
        # Widget component references
        self.title_widget: Optional[TitleWidget] = None
        self.control_widgets: Optional[ControlWidgets] = None
        self.tabbed_widgets: Optional[TabbedDisplayWidgets] = None
        self.status_bar_widgets: Optional[StatusBarWidgets] = None
        
        self._initialize_all_widgets()
    
    def _initialize_all_widgets(self) -> None:
        """Initialize all widget components with proper error handling.
        
        Creates all widget sections in the correct order with comprehensive
        error handling. If any widget creation fails, displays appropriate
        error messages and re-raises the exception.
        
        Raises:
            tk.TclError: If GUI widget creation fails
            Exception: For other unexpected errors during setup
        """
        try:
            self._create_title_section()
            self._create_control_section()
            self._create_tabbed_section()
            self._create_status_bar_section()
            
        except tk.TclError as e:
            Logger.error(f"GUI widget creation failed: {e}")
            messagebox.showerror("GUI Error", f"Failed to create interface: {e}")
            raise
        except Exception as e:
            Logger.error(f"Unexpected error during GUI setup: {e}")
            messagebox.showerror("Setup Error", f"Failed to initialize dashboard: {e}")
            raise
    
    def _create_title_section(self) -> None:
        """Create the title widget section.
        
        Initializes the title display widget in the title frame for
        showing the application header and branding.
        """
        self.title_widget = TitleWidget(self.frames["title"])
    
    def _create_control_section(self) -> None:
        """Create the control widgets section.
        
        Initializes the control panel with input fields, buttons, and
        dropdowns, connecting them to the appropriate callback functions.
        """
        self.control_widgets = ControlWidgets(
            self.frames["control"], 
            self.state, 
            self.callbacks
        )
    
    def _create_tabbed_section(self) -> None:
        """Create the control widgets section.
        
        Initializes the control panel with input fields, buttons, and
        dropdowns, connecting them to the appropriate callback functions.
        """
        self.tabbed_widgets = TabbedDisplayWidgets(
            self.frames["tabbed"], 
            self.state
        )

    def _create_status_bar_section(self) -> None:
        """Create the control widgets section.
        
        Initializes the control panel with input fields, buttons, and
        dropdowns, connecting them to the appropriate callback functions.
        """
        self.status_bar_widgets = StatusBarWidgets(
            self.frames["status_bar"],
            self.state
        )
    
    # DELEGATION METHODS    
    def update_chart_display(self, x_vals: List[str], y_vals: List[Any], metric_key: str, city: str, unit_system: str, fallback: bool = False) -> None:
        """Update the chart display with new data.
        
        Delegates chart rendering to the chart widget manager with proper
        error handling and fallback indication.
        
        Args:
            x_vals: X-axis values (typically dates)
            y_vals: Y-axis values (metric data)
            metric_key: Weather metric being charted
            city: City name for chart title
            unit: Unit system for axis labeling
            fallback: True if using fallback/simulated data
        """
        if self.chart_widgets:  # Uses the property accessor
            self.chart_widgets.update_chart_display(
                x_vals, y_vals, metric_key, city, unit_system, fallback
            )
    
    # For backward compatibility
    @property
    def metric_widgets(self):
        """Create the control widgets section.
        
        Initializes the control panel with input fields, buttons, and
        dropdowns, connecting them to the appropriate callback functions.
        """
        if self.tabbed_widgets:
            return self.tabbed_widgets.get_metric_widgets()
        return None

    @property
    def chart_widgets(self):
        """Access to chart widgets through tabbed interface.
        
        Returns:
            Chart widget manager from the tabbed interface, or None if not available
        """
        if self.tabbed_widgets:
            return self.tabbed_widgets.get_chart_widgets()
        return None