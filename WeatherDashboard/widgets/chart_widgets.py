"""
Chart widgets for displaying weather trends.
"""

from typing import List, Any, Optional
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from WeatherDashboard import config
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.unit_converter import UnitConverter
from WeatherDashboard.utils.utils import format_fallback_status


class ChartWidgets:
    """Manages matplotlib chart display for weather trends."""
    def __init__(self, parent_frame: ttk.Frame, state: Any) -> None:
        self.parent = parent_frame
        self.state = state
        
        # Chart components
        self.chart_canvas: Optional[FigureCanvasTkAgg] = None
        self.chart_fig: Optional[Figure] = None
        self.chart_ax: Optional[Any] = None
        
        self._create_chart()
    
    def _create_chart(self) -> None:
        """Creates the matplotlib chart display."""
        try:
            self._setup_matplotlib_components()
            self._configure_initial_chart()
            self._register_with_state()
            
        except Exception as e:
            Logger.error(f"Failed to create chart widgets: {e}")
            self._create_fallback_display()
    
    def _setup_matplotlib_components(self) -> None:
        """Sets up matplotlib Figure, Axes, and Canvas."""
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
        """Creates a simple fallback when matplotlib fails."""
        fallback_label = ttk.Label(self.parent, text="Chart unavailable")
        fallback_label.pack()
        
        # Set components to None
        self.chart_fig = None
        self.chart_ax = None
        self.chart_canvas = None
    
    def _register_with_state(self) -> None:
        """Registers chart components with the state manager."""
        self.state.register_chart_widgets(self.chart_canvas, self.chart_fig, self.chart_ax)
    
    def update_chart_display(self, x_vals: List[str], y_vals: List[Any], metric_key: str, city: str, unit_system: str, fallback: bool = False) -> None:
        """Updates the chart display with new data."""
        if not self.state.is_chart_available():
            Logger.warn("Chart display unavailable - matplotlib setup failed")
            return

        # Clear and plot new data
        self.chart_ax.clear()
        self.chart_ax.plot(x_vals, y_vals, marker="o")

        # Configure chart labels
        label = config.KEY_TO_DISPLAY.get(metric_key, metric_key.title())
        unit = UnitConverter.get_unit_label(metric_key, unit_system)

        self.chart_ax.set_title(f"{label} {format_fallback_status(fallback, 'display')} in {city}")
        self.chart_ax.set_xlabel("Date")
        self.chart_ax.set_ylabel(f"{label} ({unit})")

        # Format and draw
        self.chart_fig.autofmt_xdate(rotation=45)
        self.chart_fig.tight_layout()
        self.chart_canvas.draw()