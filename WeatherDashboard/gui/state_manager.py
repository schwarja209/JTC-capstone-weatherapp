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

import tkinter as tk
from typing import List

from WeatherDashboard import config, styles
from WeatherDashboard.utils.preferences_utils import PreferencesService


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
        # Direct imports for stable utilities
        self.config = config
        self.styles = styles

        # Initialize preferences service
        self.preferences_service = PreferencesService()

        # Create the tkinter variables
        self.city = tk.StringVar(value=self.config.DEFAULTS["city"])
        self.unit = tk.StringVar(value=self.config.DEFAULTS["unit"])
        self.range = tk.StringVar(value=self.config.DEFAULTS["range"])
        self.chart = tk.StringVar(value=self.config.DEFAULTS["chart"])
        self.visibility = {
            key: tk.BooleanVar(value=val)
            for key, val in self.config.DEFAULTS["visibility"].items()
        }

        # Load preferences on startup
        self._load_preferences()

        # Add automatic preference saving on state changes
        self._setup_automatic_preference_saving()
        
    # STATE ACCESS METHODS - These provide clean access to state values
    def get_current_city(self) -> str:
        """Get current city name from user input."""
        layout_config = self.styles.LAYOUT_CONFIG()
        state_config = layout_config['widget_positions'].get('state_access', {})
        
        # Use centralized state variable name or fallback
        city_var_name = state_config.get('city_variable', 'city')
        city_var = getattr(self, city_var_name, self.city)
        return city_var.get()
    
    def get_current_unit_system(self) -> str:
        """Get current unit system selection."""
        layout_config = self.styles.LAYOUT_CONFIG()
        state_config = layout_config['widget_positions'].get('state_access', {})
        
        # Use centralized state variable name or fallback
        unit_var_name = state_config.get('unit_variable', 'unit')
        unit_var = getattr(self, unit_var_name, self.unit)
        return unit_var.get()
    
    def get_current_range(self) -> str:
        """Get current date range selection for charts."""
        layout_config = self.styles.LAYOUT_CONFIG()
        state_config = layout_config['widget_positions'].get('state_access', {})
        
        # Use centralized state variable name or fallback
        range_var_name = state_config.get('range_variable', 'range')
        range_var = getattr(self, range_var_name, self.range)
        return range_var.get()
    
    def get_current_chart_metric(self) -> str:
        """Get current chart metric selection."""
        layout_config = self.styles.LAYOUT_CONFIG()
        state_config = layout_config['widget_positions'].get('state_access', {})
        
        # Use centralized state variable name or fallback
        chart_var_name = state_config.get('chart_variable', 'chart')
        chart_var = getattr(self, chart_var_name, self.chart)
        return chart_var.get()
    
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
        self.city.set(self.config.DEFAULTS["city"])
        self.unit.set(self.config.DEFAULTS["unit"])
        self.range.set(self.config.DEFAULTS["range"])
        self.chart.set(self.config.DEFAULTS["chart"])
        
        for key, var in self.visibility.items():
            var.set(self.config.DEFAULTS["visibility"].get(key, False))
    
    def _load_preferences(self) -> None:
        """Load user preferences and apply to state."""
        try:
            preferences = self.preferences_service.load_preferences()
            self.preferences_service.apply_preferences_to_state(preferences, self)
        except Exception as e:
            # Log error but continue with defaults
            print(f"Failed to load preferences: {e}")
    
    def save_preferences(self) -> None:
        """Save current state as user preferences."""
        try:
            # Get scheduler state from main window (will be passed in)
            scheduler_enabled = getattr(self, '_scheduler_enabled', self.config.SCHEDULER['enabled'])
            preferences = self.preferences_service.update_preferences_from_state(self, scheduler_enabled)
            self.preferences_service.save_preferences(preferences)
        except Exception as e:
            print(f"Failed to save preferences: {e}")

    def _setup_automatic_preference_saving(self) -> None:
        """Setup automatic preference saving when state variables change."""
        # Add trace callbacks for automatic preference saving
        self.city.trace_add('write', self._on_preference_changed)
        self.unit.trace_add('write', self._on_preference_changed)
        self.range.trace_add('write', self._on_preference_changed)
        self.chart.trace_add('write', self._on_preference_changed)
        
        # Add trace callbacks for visibility changes
        for var in self.visibility.values():
            var.trace_add('write', self._on_preference_changed)

    def _on_preference_changed(self, *args) -> None:
        """Handle preference changes and save automatically with debouncing."""
        try:
            # Only save preferences for non-text fields to avoid excessive saves
            # For text fields (like city), we'll save on button press instead
            pass
        except Exception as e:
            print(f"Failed to handle preference change: {e}")

    def save_preferences_debounced(self) -> None:
        """Save preferences immediately (debouncing removed due to root window access issue)."""
        self.save_preferences()
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        city = self.get_current_city()
        unit = self.get_current_unit_system()
        visible_count = len(self.get_visible_metrics())
        return f"WeatherDashboardState(city={city}, unit={unit}, visible_metrics={visible_count})"