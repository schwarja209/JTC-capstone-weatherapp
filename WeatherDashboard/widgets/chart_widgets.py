"""
Chart widgets for displaying weather trends.

This module provides matplotlib-based chart widgets for displaying weather
trend data and historical analysis. Handles chart creation, data visualization,
error recovery, and integrates with the application state for dynamic updates.
Includes fallback handling for matplotlib initialization failures.

Classes:
    ChartWidgets: Matplotlib chart manager with error handling and fallback support
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Any, Optional, Dict

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from WeatherDashboard import config, styles
from WeatherDashboard.utils.utils import Utils
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.unit_converter import UnitConverter

from .base_widgets import BaseWidgetManager, SafeWidgetCreator, widget_error_handler
from .widget_interface import IWeatherDashboardWidgets


class ChartWidgets(BaseWidgetManager, IWeatherDashboardWidgets):
    """Manages matplotlib chart display for weather trends and historical data.
    
    Creates and manages matplotlib Figure, Axes, and Canvas components for
    displaying weather trend charts. Handles chart initialization, data
    visualization, error recovery, and provides fallback displays when
    matplotlib fails to load. Integrates with state manager for chart
    component coordination and inherits standardized error handling.
    
    Attributes:
        parent: Parent frame container
        state: Application state manager
        chart_canvas: Matplotlib canvas widget (None if initialization failed)
        chart_fig: Matplotlib figure object (None if initialization failed)
        chart_ax: Matplotlib axes object (None if initialization failed)
        chart_error: Error message if chart creation failed
        fallback_label: Fallback label widget displayed when matplotlib fails
    """

    def __init__(self, parent_frame: ttk.Frame, state: Any) -> None:
        """Initialize the chart widgets with error handling.
        
        Attempts to create matplotlib components (Figure, Axes, Canvas) for
        chart display. If matplotlib initialization fails, creates a fallback
        display and registers None values with state manager to indicate
        chart unavailability.
        
        Args:
            parent_frame: Parent TTK frame to contain the chart display
            state: Application state manager for chart component registration
        """
        # Direct imports for stable utilities
        self.logger = Logger()
        self.config = config
        self.styles = styles
        self.utils = Utils()
        self.unit_converter = UnitConverter()

        # Injected dependencies for testable components
        self.parent_frame = parent_frame
        self.state = state

        # Chart components
        self.chart_canvas: Optional[FigureCanvasTkAgg] = None
        self.chart_fig: Optional[Figure] = None
        self.chart_ax: Optional[Any] = None
        self.chart_error: Optional[str] = None
        self.fallback_label: Optional[ttk.Label] = None
        
        # Initialize base class with error handling
        super().__init__(parent_frame, state, "chart widgets")
        
        # Create widgets with standardized error handling
        if not self.safe_create_widgets():
            self.logger.warn("Chart widgets created with errors - fallback display active")
     
    def _create_widgets(self) -> None:
        """Create matplotlib chart display with comprehensive error handling.
        
        Attempts to initialize matplotlib components and configure the chart display.
        If any step fails, creates a fallback display and registers None values
        with state manager to indicate chart unavailability to other components.
        """
        try:
            self._setup_matplotlib_components()
            self._configure_initial_chart()
            self.chart_error = None  # Clear any previous errors
            
        except Exception as e:
            self.logger.error(self.config.ERROR_MESSAGES['config_error'].format(section="chart initialization", reason=str(e)))
            self._create_fallback_display()
            # Store error state for controller to check later
            self.chart_error = str(e)
    
    def _setup_matplotlib_components(self) -> None:
        """Set up matplotlib Figure, Axes, and Canvas components."""
        # Get parent dimensions for ratio-based sizing
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()

        if parent_width <= 0 or parent_height <= 0:  # Handle case where parent hasn't been sized yet
            parent_width = 800  # Default fallback
            parent_height = 600  # Default fallback

        # Calculate figure size using ratios (convert pixels to inches)
        # Assume 100 DPI for conversion
        dpi = self.config.CHART['chart_dpi']
        fig_width = max(4, int(parent_width * 0.8 / dpi))  # 80% of parent width, minimum 4 inches
        fig_height = max(2, int(parent_height * 0.6 / dpi))  # 60% of parent height, minimum 2 inches

        self.chart_fig = Figure(figsize=(fig_width, fig_height), dpi=dpi)
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
            layout_config = self.styles.LAYOUT_CONFIG
            chart_config = layout_config['widget_positions'].get('chart_display', {})
            
            # Use centralized pack configuration or fallback to default
            pack_config = chart_config.get('pack', {'side': 'top', 'fill': 'both', 'expand': True})
            self.chart_canvas.get_tk_widget().pack(**pack_config)
    
    @widget_error_handler("fallback display")
    def _create_fallback_display(self) -> None:
        """Create fallback display when matplotlib initialization fails.
        
        Creates a simple text label indicating chart unavailability and sets
        all chart components to None to signal to other parts of the application
        that chart functionality is not available.
        """
        layout_config = self.styles.LAYOUT_CONFIG
        fallback_config = layout_config['widget_positions'].get('chart_fallback', {})
        
        self.fallback_label = SafeWidgetCreator.create_label(self.parent, "Chart unavailable - matplotlib failed to load")
        
        # Use centralized pack configuration or fallback to default
        pack_config = fallback_config.get('pack', {'expand': True})
        self.fallback_label.pack(**pack_config)
    
    def _format_chart_labels(self, metric_key: str, city: str, unit_system: str, fallback: bool) -> Dict[str, str]:
        """Formats chart labels based on metric and settings."""
        label = self.config.METRICS.get(metric_key, {}).get('label', metric_key.title())
        unit = self.unit_converter.get_unit_label(metric_key, unit_system)
        
        return {
            'title': f"{label} {self.utils.format_fallback_status(fallback, 'display')} in {city}",
            'xlabel': "Date", 
            'ylabel': f"{label} ({unit})"
        }

    def update_chart_display(self, x_vals: List[str], y_vals: List[Any], metric_key: str, city: str, unit_system: str, fallback: bool = False) -> None:
        """Updates the chart display with new data.
        
        Args:
            x_vals: X-axis values (typically dates)
            y_vals: Y-axis values (metric data points)
            metric_key: Weather metric being charted
            city: City name for chart title
            unit_system: Unit system for axis labeling
            fallback: Whether data comes from fallback/simulated source
        """
        if not (hasattr(self, 'chart_canvas') and hasattr(self, 'chart_ax') and self.chart_ax is not None):
            self.logger.warn(self.config.ERROR_MESSAGES['config_error'].format(section="chart display", reason="matplotlib setup failed"))
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
        self.chart_fig.autofmt_xdate(rotation=self.config.CHART['chart_rotation_degrees'])
        self.chart_fig.tight_layout()
        self.chart_canvas.draw()

    def clear_chart_with_error_message(self) -> None:
        """Clear the chart widget and display a fallback error message.

        Side Effects:
            Clears the chart display and shows an error message in the chart area.
            Logs an error if the chart cannot be cleared.
        """
        try:
            if self.chart_ax:
                self.chart_ax.clear()
                self.chart_ax.text(
                    0.5, 0.5,
                    'Chart unavailable\nPlease check settings',
                    ha='center', va='center',
                    transform=self.chart_ax.transAxes
                )
                if self.chart_canvas:
                    self.chart_canvas.draw()

            elif self.fallback_label:
                self.fallback_label.configure(text="Chart unavailable\nPlease check settings")
        
        except Exception as recovery_error:
            self.logger.error(f"Failed to clear chart after error: {recovery_error}")