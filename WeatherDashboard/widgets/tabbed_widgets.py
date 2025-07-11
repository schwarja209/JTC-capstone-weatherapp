"""
Tabbed interface for metrics and chart display.

This module provides a tabbed notebook widget that organizes the weather
dashboard display into separate tabs for current weather metrics and
historical weather trend charts. Manages tab switching, content widgets,
and user interaction events.

Classes:
    TabbedDisplayWidgets: Main tabbed interface manager with metrics and chart tabs
"""

from typing import Any
import tkinter as tk
from tkinter import ttk

from WeatherDashboard.widgets.metric_widgets import MetricDisplayWidgets
from WeatherDashboard.widgets.chart_widgets import ChartWidgets

class TabbedDisplayWidgets:
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
        """Initialize the tabbed display interface.
        
        Creates the notebook widget, sets up individual tabs for metrics and charts,
        initializes content widgets for each tab, and binds tab change events for
        future enhancements and state tracking.
        
        Args:
            parent_frame: Parent TTK frame to contain the tabbed interface
            state: Application state manager for widget coordination and data updates
        """
        self.parent = parent_frame
        self.state = state
        
        # Create notebook (tab container)
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tab frames
        self.metrics_frame = ttk.Frame(self.notebook)
        self.chart_frame = ttk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.metrics_frame, text="Current Weather")
        self.notebook.add(self.chart_frame, text="Weather Trends")
        
        # Initialize tab content widgets
        self.metric_widgets = MetricDisplayWidgets(self.metrics_frame, state)
        self.chart_widgets = ChartWidgets(self.chart_frame, state)
        
        # Bind tab change event for future enhancements
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
        """Return current active tab name."""
        current_tab = self.notebook.select()
        current_tab_widget = self.notebook.nametowidget(current_tab)
        
        if current_tab_widget == self.metrics_frame:
            return "metrics"
        elif current_tab_widget == self.chart_frame:
            return "chart"
        return "unknown"
    
    def _on_tab_changed(self, event):
        """Handle tab change events and coordinate tab-specific actions.
        
        Called automatically when user switches between tabs. Currently serves
        as a placeholder for future enhancements like refreshing chart data when
        switching to the chart tab or updating metric displays when switching
        to the metrics tab.
        
        Args:
            event: TTK NotebookTabChanged event object containing tab change details
        """
        current_tab = self.get_current_tab()
        # Could add logic here like refreshing chart when switching to chart tab
        # For now, just a placeholder for future features
        pass