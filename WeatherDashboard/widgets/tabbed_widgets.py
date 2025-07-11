"""
Tabbed interface for metrics and chart display.
"""

from typing import Any
import tkinter as tk
from tkinter import ttk

from WeatherDashboard.widgets.metric_widgets import MetricDisplayWidgets
from WeatherDashboard.widgets.chart_widgets import ChartWidgets

class TabbedDisplayWidgets:
    """Manages tabbed interface for metrics and chart display."""
    
    def __init__(self, parent_frame: ttk.Frame, state: Any) -> None:
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
        """Programmatically switch to metrics tab."""
        self.notebook.select(self.metrics_frame)
    
    def switch_to_chart_tab(self) -> None:
        """Programmatically switch to chart tab."""
        self.notebook.select(self.chart_frame)
    
    def get_current_tab(self) -> str:
        """Returns current active tab name."""
        current_tab = self.notebook.select()
        current_tab_widget = self.notebook.nametowidget(current_tab)
        
        if current_tab_widget == self.metrics_frame:
            return "metrics"
        elif current_tab_widget == self.chart_frame:
            return "chart"
        return "unknown"
    
    def _on_tab_changed(self, event):
        """Handle tab change events (for future enhancements)."""
        current_tab = self.get_current_tab()
        # Could add logic here like refreshing chart when switching to chart tab
        # For now, just a placeholder for future features
        pass