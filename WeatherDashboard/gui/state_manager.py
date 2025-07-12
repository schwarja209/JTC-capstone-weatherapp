"""
Centralized state management for the Weather Dashboard application.

This module provides comprehensive state management including UI variable tracking,
validation, display updates, and backward compatibility. Replaces the original
gui_vars dictionary approach with a more structured class-based system.

Classes:
    WeatherDashboardState: Central state manager for all application state
"""

from typing import List, Dict, Any, Optional, Tuple
import tkinter as tk
from WeatherDashboard import config


class WeatherDashboardState:
    """Centralized state management for the Weather Dashboard application.
    
    Manages all application state including user inputs, UI widget references,
    weather data, and display state. Provides validation, display updates, and
    backward compatibility with the original gui_vars interface.
    
    Attributes:
        city: StringVar for city name input
        unit: StringVar for unit system selection
        range: StringVar for date range selection  
        chart: StringVar for chart metric selection
        visibility: Dict of BooleanVars for metric visibility
        metric_labels: Dict of UI metric display widgets
        city_label: UI label for city display
        date_label: UI label for date display
        chart_widget: Chart display widget reference
        current_weather_data: Currently loaded weather data
        fallback_active: Flag indicating if using fallback data
        last_update_time: Timestamp of last data update
    """
    
    def __init__(self):
        """Initialize all state variables matching the original gui_vars structure.
        
        Sets up tkinter variables for user inputs, widget references for UI updates,
        and application state tracking variables.
        """
        # Create the same tkinter variables as before
        self.city = tk.StringVar(value=config.DEFAULTS["city"])
        self.unit = tk.StringVar(value=config.DEFAULTS["unit"])
        self.range = tk.StringVar(value=config.DEFAULTS["range"])
        self.chart = tk.StringVar(value=config.DEFAULTS["chart"])
        self.visibility = {
            key: tk.BooleanVar(value=val)
            for key, val in config.DEFAULTS["visibility"].items()
        }
        
        # Widget references (set by UI components during initialization)
        self.metric_labels = {}
        self.city_label = None
        self.date_label = None
        self.chart_widget = None
        
        # Chart components (maintained from WeatherDashboardWidgets)
        self.chart_canvas = None
        self.chart_fig = None
        self.chart_ax = None
        
        # Application state (new additions for better state management)
        self.current_weather_data = None
        self.fallback_active = False
        self.last_update_time = None
        
    # STATE ACCESS METHODS
    # These provide cleaner access to state values
    def get_current_city(self) -> str:
        """Get current city name from user input."""
        return self.city.get()
    
    def get_current_unit_system(self) -> str:
        """Get current unit system selection."""
        return self.unit.get()
    
    def get_current_range(self) -> str:
        """Get current date range selection for charts."""
        return self.range.get()
    
    def get_current_chart_metric(self) -> str:
        """Get current chart metric selection."""
        return self.chart.get()
    
    def is_metric_visible(self, metric_key: str) -> bool:
        """Check if a metric is currently visible in the UI."""
        var = self.visibility.get(metric_key)
        return var.get() if var else False
    
    def get_visible_metrics(self) -> List[str]:
        """Get list of currently visible metric keys."""
        return [key for key, var in self.visibility.items() if var.get()]
    
    # STATE MODIFICATION METHODS    
    def reset_to_defaults(self) -> None:
        """Reset all input controls to default values.
        
        Restores city, unit system, date range, chart metric, and visibility
        settings to their configured default values.
        """
        self.city.set(config.DEFAULTS["city"])
        self.unit.set(config.DEFAULTS["unit"])
        self.range.set(config.DEFAULTS["range"])
        self.chart.set(config.DEFAULTS["chart"])
        
        for key, var in self.visibility.items():
            var.set(config.DEFAULTS["visibility"].get(key, False))
    
    def set_weather_data(self, weather_data: Optional[Dict[str, Any]], is_fallback: bool = False) -> None:
        """Store current weather data for state management.
        
        Args:
            weather_data: Weather data dictionary to store, or None to clear
            is_fallback: True if this is fallback/simulated data
        """
        self.current_weather_data = weather_data
        self.fallback_active = is_fallback
        self.last_update_time = weather_data.get('date') if weather_data else None
    
    def get_current_weather_data(self) -> Optional[Dict[str, Any]]:
        """Get current weather data from state."""
        return self.current_weather_data
    
    def is_using_fallback(self) -> bool:
        """Check if currently using fallback/simulated data."""
        return self.fallback_active
    
    # DISPLAY UPDATE METHODS
    # These encapsulate display logic that was previously scattered
    def update_city_display(self, city_name: str, date_str: str, status: str = "") -> None:
        """Update city-related display elements.
        
        Args:
            city_name: City name to display
            date_str: Date string to display
            status: Optional status string (unused in current implementation)
        """
        if self.city_label:
            self.city_label.config(text=city_name)
        
        if self.date_label:
            self.date_label.config(text=date_str)
    
    def update_metric_display(self, metric_displays: Dict[str, str]) -> None:
        """Update all metric displays based on visibility settings.
        
        Shows or hides metric widgets based on current visibility settings and
        updates displayed values with formatted metric data.
        
        Args:
            metric_displays: Dict mapping metric keys to formatted display values
        """
        row_counter = 0
        for metric_key in config.KEY_TO_DISPLAY:
            if metric_key not in self.metric_labels:
                continue
            
            widgets = self.metric_labels[metric_key]
            is_visible = self.is_metric_visible(metric_key)

            # Hide all widgets first
            widgets['label'].grid_forget()
            widgets['value'].grid_forget()

            # Show and update if visible
            if is_visible and metric_key in metric_displays:
                widgets['label'].grid(row=row_counter, column=2, sticky=tk.W, pady=5)
                widgets['value'].grid(row=row_counter, column=3, sticky=tk.W, pady=5)
                widgets['value'].config(text=metric_displays[metric_key])
                row_counter += 1

    def get_current_chart_dropdown_data(self) -> Tuple[List[str], bool]:
        """Get data for chart dropdown update in UI-agnostic format.
        
        Returns:
            Tuple containing:
                - List[str]: Display names of visible metrics
                - bool: True if any metrics are visible
        """
        visible_metrics = self.get_visible_metrics()
        visible_display_names = [
            config.KEY_TO_DISPLAY[key] for key in visible_metrics
        ]
        
        has_metrics = bool(visible_display_names)
        return visible_display_names, has_metrics
    
    def update_status_bar_system(self, message: str, status_type: str = "info") -> None:
        """Update system status message in status bar.
        
        Args:
            message: Status message to display
            status_type: Type of status ('info', 'warning', 'error', 'loading')
        """
        if hasattr(self, 'system_status_label') and self.system_status_label:
            colors = {
                "info": "green",
                "warning": "orange", 
                "error": "red",
                "loading": "blue"
            }
            self.system_status_label.configure(
                text=message,
                foreground=colors.get(status_type, "green")
            )

    def update_status_bar_data(self, message: str) -> None:
        """Update data source status in status bar.
        
        Args:
            message: Data status message to display
        """
        if hasattr(self, 'data_status_label') and self.data_status_label:
            self.data_status_label.configure(text=message)
    
    # CHART METHODS
    def is_chart_available(self) -> bool:
        """Check if chart widgets are available for rendering."""
        return self.chart_ax is not None
    
    # VALIDATION METHODS    
    def validate_current_state(self) -> List[str]:
        """Validate current state and return any errors.
        
        Checks city name, unit system, and visible metrics for validity.
        
        Returns:
            List[str]: List of validation error messages, empty if valid
        """
        errors = []
        
        city = self.get_current_city()
        if not city or not city.strip():
            errors.append("City name cannot be empty")
        
        unit_system = self.get_current_unit_system()
        if unit_system not in ['metric', 'imperial']:
            errors.append(f"Invalid unit system: {unit_system}")
        
        if not self.get_visible_metrics():
            errors.append("At least one metric must be visible")
        
        return errors
    
    def get_current_settings_summary(self) -> Dict[str, Any]:
        """Get a summary of current settings for logging/debugging.
        
        Returns:
            Dict[str, Any]: Dictionary containing all current state values
        """
        return {
            'city': self.get_current_city(),
            'unit_system': self.get_current_unit_system(),
            'date_range': self.get_current_range(),
            'chart_metric': self.get_current_chart_metric(),
            'visible_metrics': self.get_visible_metrics(),
            'fallback_active': self.is_using_fallback(),
        }
    
    def __repr__(self) -> str:
        """String representation for debugging.
        
        Returns:
            str: Formatted string showing current state summary
        """
        summary = self.get_current_settings_summary()
        return f"WeatherDashboardState({summary})"