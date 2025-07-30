"""
Tabbed interface for metrics and chart display.

This module provides a tabbed notebook widget that organizes the weather
dashboard display into separate tabs for current weather metrics and
historical weather trend charts. Manages tab switching, content widgets,
and user interaction events.

Classes:
    TabbedDisplayWidgets: Main tabbed interface manager with metrics and chart tabs
"""

import tkinter as tk
from tkinter import ttk
from typing import Any, Optional

from WeatherDashboard import styles
from WeatherDashboard.utils.logger import Logger

from .base_widgets import BaseWidgetManager, SafeWidgetCreator, widget_error_handler
from .widget_registry import WidgetRegistry
from .metric_widgets import MetricDisplayWidgets
from .chart_widgets import ChartWidgets


class TabbedDisplayWidgets(BaseWidgetManager):
    """Manages tabbed interface for metrics and chart display.
    
    Creates and manages a notebook widget with two main tabs:
    - Current Weather: Displays real-time weather metrics and alert status
    - Weather Trends: Shows historical weather charts and trend analysis
    
    Handles tab switching, widget initialization, and provides access to
    individual tab content widgets for external updates and interaction.
    
    Attributes:
        parent: Parent frame container
        state: Application state manager
        notebook: TTK Notebook widget for tab management
        metrics_frame: Frame containing current weather metrics
        chart_frame: Frame containing weather trend charts
        metric_widgets: Widget manager for metrics tab content
        chart_widgets: Widget manager for chart tab content
    """

    def __init__(self, parent_frame: ttk.Frame, state: Any, widget_registry: WidgetRegistry = None) -> None:
        """Initialize the tabbed display interface with error handling
        
        Creates the notebook widget, sets up individual tabs for metrics and charts,
        initializes content widgets for each tab, and binds tab change events for
        future enhancements and state tracking.
        
        Args:
            parent_frame: Parent TTK frame to contain the tabbed interface
            state: Application state manager for widget coordination and data updates
        """
        # Direct imports for stable utilities
        self.logger = Logger()
        self.styles = styles

        # Injected dependencies for testable components
        self.parent_frame = parent_frame
        self.state = state
        self.widget_registry = widget_registry

        # Widget references
        self.notebook: Optional[ttk.Notebook] = None
        self.metrics_frame: Optional[ttk.Frame] = None
        self.chart_frame: Optional[ttk.Frame] = None
        self.metric_widgets: Optional[MetricDisplayWidgets] = None
        self.chart_widgets: Optional[ChartWidgets] = None
        
        # Initialize base class with error handling
        super().__init__(parent_frame, state, "tabbed display widgets")
        
        # Create widgets with standardized error handling
        if not self.safe_create_widgets():
            self.logger.warn("Tabbed display widgets created with errors - some functionality may be limited")
    
    def _create_widgets(self) -> None:
        """Create tabbed interface with notebook and content widgets.

        Creates TTK Notebook, sets up individual tab frames, adds tabs with
        appropriate labels, initializes content widgets for each tab, and
        binds event handlers for tab switching.
        """
        layout_config = self.styles.LAYOUT_CONFIG
        tabbed_config = layout_config['widget_positions'].get('tabbed_display', {})
    
        # Create notebook (tab container)
        self.notebook = ttk.Notebook(self.parent)

        # Use centralized pack configuration or fallback to default
        pack_config = tabbed_config.get('notebook_pack', {'fill': 'BOTH', 'expand': True})
        self.notebook.pack(**pack_config)
        
        # Create tab frames using SafeWidgetCreator
        self.metrics_frame = SafeWidgetCreator.create_frame(self.notebook)
        self.chart_frame = SafeWidgetCreator.create_frame(self.notebook)

        # Add tabs to notebook with centralized text configuration
        tab_texts = tabbed_config.get('tab_texts', {
            'metrics': 'Current Weather',
            'chart': 'Weather Trends'
        })
        if self.metrics_frame:
            self.notebook.add(self.metrics_frame, text="Current Weather")
        if self.chart_frame:
            self.notebook.add(self.chart_frame, text="Weather Trends")
        
        # Initialize tab content widgets
        self.metric_widgets = MetricDisplayWidgets(self.metrics_frame, self.state)
        self.chart_widgets = ChartWidgets(self.chart_frame, self.state)

        if self.widget_registry:
            self._register_sub_widgets()

        # Bind events
        self._bind_events()

    @widget_error_handler("event binding")
    def _bind_events(self) -> None:
        """Bind tab change events with error handling."""
        if self.notebook:
            self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def get_metric_widgets(self) -> MetricDisplayWidgets:
        """Returns metric widgets for external access."""
        return self.metric_widgets
    
    def get_chart_widgets(self) -> ChartWidgets:
        """Returns chart widgets for external access."""
        return self.chart_widgets
    
    def switch_to_metrics_tab(self) -> None:
        """Switch to metrics tab."""
        self.notebook.select(self.metrics_frame)
    
    def switch_to_chart_tab(self) -> None:
        """Switch to chart tab."""
        self.notebook.select(self.chart_frame)
    
    def get_current_tab(self) -> str:
        """Return current active tab identifier."""
        current_tab = self.notebook.select()
        current_tab_widget = self.notebook.nametowidget(current_tab)
        
        if current_tab_widget == self.metrics_frame:
            return "metrics"
        elif current_tab_widget == self.chart_frame:
            return "chart"
        return "unknown"
    
    def _register_sub_widgets(self) -> None:
        """Register metric and chart widgets with the registry.
        
        Registers the metric_widgets and chart_widgets with the widget registry
        so they can be accessed and manipulated at runtime.
        """
        if self.metric_widgets and self.metrics_frame:
            self.widget_registry.register_widget(
                widget_id='metric_widgets',
                widget=self.metric_widgets,
                widget_type='metric',
                parent_frame=self.metrics_frame,
                position={'pack': {'fill': 'both', 'expand': True}},
                style='Metric.TFrame'
            )
            self.logger.info("Registered metric widgets with registry")
        
        if self.chart_widgets and self.chart_frame:
            self.widget_registry.register_widget(
                widget_id='chart_widgets',
                widget=self.chart_widgets,
                widget_type='chart',
                parent_frame=self.chart_frame,
                position={'pack': {'fill': 'both', 'expand': True}},
                style='Chart.TFrame'
            )
            self.logger.info("Registered chart widgets with registry")
    
    @widget_error_handler("tab change")
    def _on_tab_changed(self, event) -> None:
        """Handle tab change events (placeholder for future features)."""
        current_tab = self.get_current_tab()
        # Could add logic here like refreshing chart when switching to chart tab
        # For now, just a placeholder for future features
        pass