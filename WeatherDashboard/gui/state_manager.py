"""
Centralized state management for the Weather Dashboard application.
"""

import tkinter as tk
from WeatherDashboard import config


class WeatherDashboardState:
    """Centralized state management for the Weather Dashboard application.
    
    Replaces the gui_vars dictionary approach while maintaining the same interface
    and variable names where possible. Provides better organization for future
    state expansion.
    """
    
    def __init__(self):
        """Initialize all state variables matching the original gui_vars structure."""
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
        self.status_label = None
        self.chart_widget = None
        
        # Chart components (maintained from WeatherDashboardWidgets)
        self.chart_canvas = None
        self.chart_fig = None
        self.chart_ax = None
        
        # Application state (new additions for better state management)
        self.current_weather_data = None
        self.fallback_active = False
        self.last_update_time = None
    
    # BACKWARD COMPATIBILITY METHODS
    # These methods maintain the same interface as the original gui_vars dictionary
    def get(self, key):
        """Get method for backward compatibility with gui_vars['key'] access."""
        return getattr(self, key, None)
    
    def __getitem__(self, key):
        """Dictionary-style access for backward compatibility."""
        return getattr(self, key, None)
    
    def __setitem__(self, key, value):
        """Dictionary-style assignment for backward compatibility."""
        setattr(self, key, value)
    
    # STATE ACCESS METHODS
    # These provide cleaner access to state values
    def get_current_city(self):
        """Get current city name."""
        return self.city.get()
    
    def get_current_unit_system(self):
        """Get current unit system (metric/imperial)."""
        return self.unit.get()
    
    def get_current_range(self):
        """Get current date range selection."""
        return self.range.get()
    
    def get_current_chart_metric(self):
        """Get current chart metric selection."""
        return self.chart.get()
    
    def is_metric_visible(self, metric_key):
        """Check if a metric is currently visible."""
        var = self.visibility.get(metric_key)
        return var.get() if var else False
    
    def get_visible_metrics(self):
        """Get list of currently visible metric keys."""
        return [key for key, var in self.visibility.items() if var.get()]
    
    # STATE MODIFICATION METHODS    
    def reset_to_defaults(self):
        """Reset all input controls to default values (preserves original method name)."""
        self.city.set(config.DEFAULTS["city"])
        self.unit.set(config.DEFAULTS["unit"])
        self.range.set(config.DEFAULTS["range"])
        self.chart.set(config.DEFAULTS["chart"])
        
        for key, var in self.visibility.items():
            var.set(config.DEFAULTS["visibility"].get(key, False))
    
    def set_weather_data(self, weather_data, is_fallback=False):
        """Store current weather data (new functionality for better state management)."""
        self.current_weather_data = weather_data
        self.fallback_active = is_fallback
        self.last_update_time = weather_data.get('date') if weather_data else None
    
    def get_weather_data(self):
        """Get current weather data (new functionality)."""
        return self.current_weather_data
    
    def is_using_fallback(self):
        """Check if currently using fallback data (new functionality)."""
        return self.fallback_active
    
    # DISPLAY UPDATE METHODS
    # These encapsulate display logic that was previously scattered
    def update_city_display(self, city_name, date_str, status=""):
        """Update city-related display elements."""
        if self.city_label:
            self.city_label.config(text=city_name)
        
        if self.date_label:
            self.date_label.config(text=date_str)
        
        if self.status_label:
            self.status_label.config(text=status)
    
    def update_metric_display(self, metric_displays):
        """Update all metric displays based on visibility.
        
        Args:
            metric_displays: Dict of {metric_key: formatted_value}
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
    
    def update_chart_dropdown_options(self):
        """Update chart dropdown based on visible metrics."""
        if not self.chart_widget:
            return
        
        # Get display names of visible metrics
        visible_metrics = self.get_visible_metrics()
        visible_display_names = [
            config.KEY_TO_DISPLAY[key] for key in visible_metrics
        ]
        
        if not visible_display_names:
            self.chart_widget['values'] = ["No metrics selected"]
            self.chart.set("No metrics selected")
            self.chart_widget.configure(state="disabled")
        else:
            self.chart_widget['values'] = visible_display_names
            self.chart.set(visible_display_names[0])
            self.chart_widget.configure(state="readonly")
    
    # CHART METHODS
    def is_chart_available(self):
        """Check if chart widgets are available."""
        return self.chart_ax is not None
    
    def register_chart_widgets(self, canvas, figure, axes):
        """Register chart widgets with state."""
        self.chart_canvas = canvas
        self.chart_fig = figure
        self.chart_ax = axes
    
    # VALIDATION METHODS    
    def validate_current_state(self):
        """Validate current state and return any errors."""
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
    
    def get_current_settings_summary(self):
        """Get a summary of current settings for logging/debugging."""
        return {
            'city': self.get_current_city(),
            'unit_system': self.get_current_unit_system(),
            'date_range': self.get_current_range(),
            'chart_metric': self.get_current_chart_metric(),
            'visible_metrics': self.get_visible_metrics(),
            'fallback_active': self.is_using_fallback(),
        }
    
    def __repr__(self):
        """String representation for debugging."""
        summary = self.get_current_settings_summary()
        return f"WeatherDashboardState({summary})"