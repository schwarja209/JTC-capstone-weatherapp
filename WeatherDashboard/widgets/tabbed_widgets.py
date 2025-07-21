"""
Tabbed interface for metrics and chart display.

This module provides a tabbed notebook widget that organizes the weather
dashboard display into separate tabs for current weather metrics and
historical weather trend charts. Manages tab switching, content widgets,
and user interaction events.

Classes:
    TabbedDisplayWidgets: Main tabbed interface manager with metrics and chart tabs
"""

from typing import Any, Optional
import tkinter as tk
from tkinter import ttk

from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.widgets.base_widgets import BaseWidgetManager, SafeWidgetCreator, widget_error_handler
from WeatherDashboard.widgets.metric_widgets import MetricDisplayWidgets
from WeatherDashboard.widgets.chart_widgets import ChartWidgets


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
    def __init__(self, parent_frame: ttk.Frame, state: Any) -> None:
        """Initialize the tabbed display interface with error handling
        
        Creates the notebook widget, sets up individual tabs for metrics and charts,
        initializes content widgets for each tab, and binds tab change events for
        future enhancements and state tracking.
        
        Args:
            parent_frame: Parent TTK frame to contain the tabbed interface
            state: Application state manager for widget coordination and data updates
        """        
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
            Logger.warn("Tabbed display widgets created with errors - some functionality may be limited")
    
    def _create_widgets(self) -> None:
        """Create tabbed interface with notebook and content widgets.

        Creates TTK Notebook, sets up individual tab frames, adds tabs with
        appropriate labels, initializes content widgets for each tab, and
        binds event handlers for tab switching.
        """
        # Create notebook (tab container)
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tab frames using SafeWidgetCreator
        self.metrics_frame = SafeWidgetCreator.create_frame(self.notebook)
        self.chart_frame = SafeWidgetCreator.create_frame(self.notebook)
        
        # Add tabs to notebook
        if self.metrics_frame:
            self.notebook.add(self.metrics_frame, text="Current Weather")
        if self.chart_frame:
            self.notebook.add(self.chart_frame, text="Weather Trends")
        
        # Initialize tab content widgets
        self.metric_widgets = MetricDisplayWidgets(self.metrics_frame, self.state)
        self.chart_widgets = ChartWidgets(self.chart_frame, self.state)

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
    
    @widget_error_handler("tab change")
    def _on_tab_changed(self, event):
        """Handle tab change events (placeholder for future features)."""
        current_tab = self.get_current_tab()
        # Could add logic here like refreshing chart when switching to chart tab
        # For now, just a placeholder for future features
        pass