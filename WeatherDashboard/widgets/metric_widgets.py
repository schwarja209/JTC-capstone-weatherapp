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
    
    def _create_all_metrics(self) -> None:
        """Create all metric display widgets in organized sections.
        
        Orchestrates the creation of city/date headers, weather metric displays,
        alert status indicators, and registers all widgets with state manager
        for coordinated updates and visibility management.
        """
        self._create_header_info()
        self._create_weather_metrics()
        self._create_alert_status()
        self._register_with_state()
    
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
        for i, metric_key in enumerate(config.KEY_TO_DISPLAY):
            row = 0 + i
            
            # Create label and value widgets
            name_label = ttk.Label(self.parent, text=f"{config.KEY_TO_DISPLAY[metric_key]}:", style="LabelName.TLabel")
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
    
    def _register_with_state(self) -> None:
        """Register widget references with the state manager."""
        self.state.metric_labels = self.metric_labels
        self.state.city_label = self.city_label
        self.state.date_label = self.date_label
        self.state.alert_status_widget = self.alert_status_widget
        self.state.alert_text_label = self.alert_text_label