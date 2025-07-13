"""
Metric display widgets for current weather data.

This module provides comprehensive metric display widgets for showing current
weather information including city/date headers, weather metrics with visibility
controls, and integrated weather alert status indicators. Manages dynamic
metric visibility and alert notifications.

Classes:
    MetricDisplayWidgets: Main metric display manager with alerts integration
"""

from typing import Dict, Any, Optional
import tkinter as tk
from tkinter import ttk

from WeatherDashboard import config
from WeatherDashboard.features.alerts.alert_display import AlertStatusIndicator
from WeatherDashboard.utils.logger import Logger


class MetricDisplayWidgets:
    """Manages the display of current weather metrics and alert status.
    
    Creates and manages the current weather display tab including city/date
    headers, dynamic weather metric displays with visibility controls, and
    integrated weather alert status indicators. Coordinates with the state
    manager for metric visibility and provides alert notifications.
    
    Attributes:
        parent: Parent frame container
        state: Application state manager
        metric_labels: Dictionary of metric display widgets by metric key
        city_label: City name display label
        date_label: Date/time display label
        alert_status_widget: Alert status indicator widget
        alert_text_label: Alert text notification label
    """
    def __init__(self, parent_frame: ttk.Frame, state: Any) -> None:
        """Initialize the metric display widgets.
        
        Creates city/date headers, weather metric displays with visibility
        controls, alert status indicators, and registers all widgets with
        the state manager for coordinated updates.
        
        Args:
            parent_frame: Parent TTK frame to contain the metric displays
            state: Application state manager for widget coordination
        """
        self.parent = parent_frame
        self.state = state
        
        # Widget references
        self.metric_labels: Dict[str, Dict[str, ttk.Label]] = {}
        self.city_label: Optional[ttk.Label] = None
        self.date_label: Optional[ttk.Label] = None

        # Alert status widget
        self.alert_status_widget: Optional[AlertStatusIndicator] = None
        
        self._create_all_metrics()
    
    def update_metric_display(self, metric_displays: Dict[str, str]) -> None:
        """Update metric displays using centralized configuration."""
        # Clear all existing displays first
        for metric_key in config.METRICS:
            if metric_key in self.metric_labels:
                widgets = self.metric_labels[metric_key]
                widgets['label'].grid_forget()
                widgets['value'].grid_forget()
        
        # Define display order for each column section
        left_column_order = ['conditions', 'temperature', 'humidity', 'rain', 'snow', 'precipitation_probability', 'wind_chill', 'heat_index', 'weather_comfort_score']
        right_column_order = ['cloud_cover', 'temp_min', 'wind_speed', 'pressure', 'visibility', 'dew_point', 'uv_index', 'air_quality_description']

        left_row = 0
        right_row = 0
        
        # Process left column metrics (columns 2-3)
        for display_metric in left_column_order:
            if self._is_metric_visible(display_metric):
                should_display = True
                label = ""
                value = ""

                # Determine display data and label
                if display_metric == 'temperature':
                    label = 'Temperature:'
                    value = metric_displays.get('enhanced_temperature', '--')
                elif display_metric == 'conditions':
                    label = 'Conditions:'
                    value = metric_displays.get('enhanced_conditions', '--')
                elif display_metric in ['rain', 'snow']:
                    label = f"{config.METRICS[display_metric]['label']}:"
                    value = metric_displays.get(display_metric, '--')
                    if value == '--' or value == '0.0 mm' or value == '0.0 in':
                        should_display = False # Skip if no precipitation
                elif display_metric in ['wind_chill', 'heat_index', 'weather_comfort_score', 'precipitation_probability']:
                    label = f"{config.METRICS[display_metric]['label']}:"
                    value = metric_displays.get(display_metric, '--')
                    # Skip wind chill and heat index if they're None (not applicable)
                    if display_metric in ['wind_chill', 'heat_index'] and value == '--':
                        should_display = False
                else:
                    # Standard individual metric
                    label = f"{config.METRICS[display_metric]['label']}:"
                    value = metric_displays.get(display_metric, '--')
                
                if should_display:
                    self._show_metric_at_position(display_metric, label, value, left_row, 2, 3)
                    left_row += 1
        
        # Process right column metrics (columns 4-5)  
        for display_metric in right_column_order:
            if self._is_metric_visible(display_metric):
                # Determine display data and label
                if display_metric == 'temp_min':
                    label = "Today's Range:"
                    value = metric_displays.get('temp_range', '--')
                elif display_metric == 'wind_speed':
                    label = 'Wind:'
                    value = metric_displays.get('enhanced_wind', '--')
                elif display_metric in ['dew_point', 'uv_index', 'air_quality_description']:
                    label = f"{config.METRICS[display_metric]['label']}:"
                    value = metric_displays.get(display_metric, '--')
                else:
                    # Standard individual metric
                    label = f"{config.METRICS[display_metric]['label']}:"
                    value = metric_displays.get(display_metric, '--')
                
                self._show_metric_at_position(display_metric, label, value, right_row, 4, 5)
                right_row += 1

    def _show_metric_at_position(self, metric_key: str, label_text: str, value_text: str, row: int, label_col: int, value_col: int) -> None:
        """Helper method to show a metric at specific grid position."""
        if metric_key in self.metric_labels:
            widgets = self.metric_labels[metric_key]
            widgets['label'].configure(text=label_text)
            widgets['value'].configure(text=value_text)
            
            # Add extra padding for column 4 (right section)
            padx = (20, 0) if label_col == 4 else (0, 0)
            
            widgets['label'].grid(row=row, column=label_col, sticky=tk.W, pady=5, padx=padx)
            widgets['value'].grid(row=row, column=value_col, sticky=tk.W, pady=5)

    def _is_metric_visible(self, metric_key: str) -> bool:
        """Check if a specific metric is currently visible using standardized access."""
        try:
            return self.state.visibility.get(metric_key, tk.BooleanVar()).get()
        except (AttributeError, KeyError) as e:
            Logger.warn(f"Failed to check visibility for metric '{metric_key}': {e}")
            return False
    
    def _create_all_metrics(self) -> None:
        """Create all metric display widgets in organized sections.
        
        Orchestrates the creation of city/date headers, weather metric displays,
        and alert status indicators for coordinated updates and visibility management.
        """
        self._create_header_info()
        self._create_weather_metrics()
        self._create_alert_status()
    
    def _create_header_info(self) -> None:
        """Create city and date display headers.
        
        Creates labeled display widgets for city name and date/time information
        positioned at the top of the metrics display area.
        """
        # City label
        ttk.Label(self.parent, text="City:", style="LabelName.TLabel").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.city_label = ttk.Label(self.parent, text="--", width=15, style="LabelValue.TLabel")
        self.city_label.grid(row=0, column=1, sticky=tk.W, pady=5)

        # Date label
        ttk.Label(self.parent, text="Date:", style="LabelName.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.date_label = ttk.Label(self.parent, text="--", width=15, style="LabelValue.TLabel")
        self.date_label.grid(row=1, column=1, sticky=tk.W, pady=5)
    
    def _create_weather_metrics(self) -> None:
        """Create weather metric display widgets with visibility controls.
        
        Creates label/value widget pairs for each weather metric defined in
        configuration. Widgets are initially positioned but their visibility
        is managed dynamically by the state manager based on user preferences.
        """
        for i, metric_key in enumerate(config.METRICS):
            row = 0 + i
            
            # Create label and value widgets
            name_label = ttk.Label(self.parent, text=f"{config.METRICS[metric_key]['label']}:", style="LabelName.TLabel")
            value_label = ttk.Label(self.parent, text="--", style="LabelValue.TLabel")
            
            # Position them (initially visible, will be managed by state)
            name_label.grid(row=row, column=2, sticky=tk.W, pady=5)
            value_label.grid(row=row, column=3, sticky=tk.W, pady=5)
            
            # Store references
            self.metric_labels[metric_key] = {
                "label": name_label, 
                "value": value_label
            }
    
    def _create_alert_status(self) -> None:
        """Create alert status indicator and notification widgets.
        
        Creates an alert status frame containing both a clickable alert icon
        widget and a text label for alert notifications. The alert widget
        provides visual indication of weather alerts and allows user interaction.
        """
        # Create a frame to hold both alert widget and text
        alert_frame = ttk.Frame(self.parent)
        alert_frame.grid(row=2, column=0, columnspan=2, padx=5, sticky=tk.W)
        
        # Alert widget
        self.alert_status_widget = AlertStatusIndicator(alert_frame)
        self.alert_status_widget.pack(side=tk.LEFT)
        
        # Alert text label (initially hidden)
        self.alert_text_label = ttk.Label(
            alert_frame, 
            text="", 
            style="LabelValue.TLabel",
            foreground="red",
            font=("Arial", 9, "bold")
        )
        self.alert_text_label.pack(side=tk.LEFT, padx=(5, 0))
    
    def update_alert_display(self, alerts) -> None:
        """Update both alert widget and text label."""
        if self.alert_status_widget:
            self.alert_status_widget.update_status(alerts)
        
        # Update text label based on alerts
        if self.alert_text_label:
            if alerts:
                # Count alerts by severity
                warnings = len([a for a in alerts if a.severity == 'warning'])
                if warnings > 0:
                    self.alert_text_label.configure(text="Alert!", foreground="red")
                else:
                    self.alert_text_label.configure(text="Information", foreground="orange")
            else:
                self.alert_text_label.configure(text="", foreground="gray")