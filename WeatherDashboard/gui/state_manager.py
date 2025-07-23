"""
Centralized state management for the Weather Dashboard application.

This module provides UI state management including user input variables,
metric visibility settings, state validation, and clean access methods.
Uses direct tkinter variable coupling for reactive UI updates per ADR-033.

The state manager is intentionally coupled to tkinter to enable direct widget
binding and automatic UI updates, trading testability for simplicity and
maintainability in this desktop GUI application.

Classes:
    WeatherDashboardState: UI state manager with validation and access methods
"""

from typing import List
import tkinter as tk

from WeatherDashboard import config


class WeatherDashboardState:
    """Centralized state management for the Weather Dashboard application.
    
    Manages UI state variables including user inputs, metric visibility settings,
    and provides clean access methods. Handles state validation and reset functionality.
    
    Attributes:
        city: StringVar for city name input
        unit: StringVar for unit system selection
        range: StringVar for date range selection  
        chart: StringVar for chart metric selection
        visibility: Dict of BooleanVars for metric visibility
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
        
    # STATE ACCESS METHODS - These provide cleaner access to state values
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
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        city = self.get_current_city()
        unit = self.get_current_unit_system()
        visible_count = len(self.get_visible_metrics())
        return f"WeatherDashboardState(city={city}, unit={unit}, visible_metrics={visible_count})"