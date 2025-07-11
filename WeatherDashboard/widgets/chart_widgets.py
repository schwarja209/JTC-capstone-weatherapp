"""
Chart widgets for displaying weather trends.

This module provides matplotlib-based chart widgets for displaying weather
trend data and historical analysis. Handles chart creation, data visualization,
error recovery, and integrates with the application state for dynamic updates.
Includes fallback handling for matplotlib initialization failures.

Classes:
    ChartWidgets: Matplotlib chart manager with error handling and fallback support
"""

from typing import List, Any, Optional, Dict
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from WeatherDashboard import config
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.unit_converter import UnitConverter
from WeatherDashboard.utils.utils import format_fallback_status


class ChartWidgets:
    """Manages matplotlib chart display for weather trends and historical data.
    
    Creates and manages matplotlib Figure, Axes, and Canvas components for
    displaying weather trend charts. Handles chart initialization, data
    visualization, error recovery, and provides fallback displays when
    matplotlib fails to load. Integrates with state manager for chart
    component coordination.
    
    Attributes:
        parent: Parent frame container
        state: Application state manager
        chart_canvas: Matplotlib canvas widget (None if failed)
        chart_fig: Matplotlib figure object (None if failed)
        chart_ax: Matplotlib axes object (None if failed)
        fallback_label: Fallback label widget when matplotlib fails
    """
    def __init__(self, parent_frame: ttk.Frame, state: Any) -> None:
        """Initialize the chart widgets with matplotlib integration.
        
        Attempts to create matplotlib components (Figure, Axes, Canvas) for
        chart display. If matplotlib initialization fails, creates a fallback
        display and registers None values with state manager to indicate
        chart unavailability.
        
        Args:
            parent_frame: Parent TTK frame to contain the chart display
            state: Application state manager for chart component registration
        """
        self.parent = parent_frame
        self.state = state
        
        # Chart components
        self.chart_canvas: Optional[FigureCanvasTkAgg] = None
        self.chart_fig: Optional[Figure] = None
        self.chart_ax: Optional[Any] = None
        
        self._create_chart()
    
    def _create_chart(self) -> None:
        """Create matplotlib chart display with comprehensive error handling.
        
        Attempts to initialize matplotlib components and configure the chart display.
        If any step fails, creates a fallback display and registers None values
        with state manager to indicate chart unavailability to other components.
        """
        try:
            self._setup_matplotlib_components()
            self._configure_initial_chart()
            self._register_with_state()
            
        except Exception as e:
            Logger.error(f"Failed to create chart widgets: {e}")
            self._create_fallback_display()
            # Register None values to indicate chart is unavailable
            self.state.register_chart_widgets(None, None, None)
    
    def _setup_matplotlib_components(self) -> None:
        """Set up matplotlib Figure, Axes, and Canvas components.
        
        Creates the matplotlib Figure with specified dimensions, adds a subplot
        for chart rendering, and creates the Tkinter canvas widget for embedding
        the chart in the GUI.
        """
        self.chart_fig = Figure(figsize=(8, 3), dpi=100)
        self.chart_ax = self.chart_fig.add_subplot(111)
        self.chart_canvas = FigureCanvasTkAgg(self.chart_fig, master=self.parent)
    
    def _configure_initial_chart(self) -> None:
        """Configures the initial empty chart."""
        if self.chart_ax:
            self.chart_ax.set_title("")
            self.chart_ax.set_xlabel("")
            self.chart_ax.set_ylabel("")
        
        if self.chart_canvas:
            self.chart_canvas.draw()
            self.chart_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def _create_fallback_display(self) -> None:
        """Create fallback display when matplotlib initialization fails.
        
        Creates a simple text label indicating chart unavailability and sets
        all chart components to None to signal to other parts of the application
        that chart functionality is not available.
        """
        # Create a simple fallback label
        self.fallback_label = ttk.Label(self.parent, text="Chart unavailable - matplotlib failed to load")
        self.fallback_label.pack(expand=True)
        
        # Set components to None to indicate unavailability
        self.chart_fig = None
        self.chart_ax = None
        self.chart_canvas = None
    
    def _register_with_state(self) -> None:
        """Register chart components with the state manager."""
        self.state.register_chart_widgets(self.chart_canvas, self.chart_fig, self.chart_ax)
    
    def _format_chart_labels(self, metric_key: str, city: str, unit_system: str, fallback: bool) -> Dict[str, str]:
        """Formats chart labels based on metric and settings."""
        label = config.KEY_TO_DISPLAY.get(metric_key, metric_key.title())
        unit = UnitConverter.get_unit_label(metric_key, unit_system)
        
        return {
            'title': f"{label} {format_fallback_status(fallback, 'display')} in {city}",
            'xlabel': "Date", 
            'ylabel': f"{label} ({unit})"
        }

    def update_chart_display(self, x_vals: List[str], y_vals: List[Any], metric_key: str, city: str, unit_system: str, fallback: bool = False) -> None:
        """Updates the chart display with new data."""
        if not self.state.is_chart_available():
            Logger.warn("Chart display unavailable - matplotlib setup failed")
            return

        # Clear and plot new data
        self.chart_ax.clear()
        self.chart_ax.plot(x_vals, y_vals, marker="o")

        # Get formatted labels
        labels = self._format_chart_labels(metric_key, city, unit_system, fallback)
        self.chart_ax.set_title(labels['title'])
        self.chart_ax.set_xlabel(labels['xlabel'])
        self.chart_ax.set_ylabel(labels['ylabel'])

        # Format and draw
        self.chart_fig.autofmt_xdate(rotation=45)
        self.chart_fig.tight_layout()
        self.chart_canvas.draw()