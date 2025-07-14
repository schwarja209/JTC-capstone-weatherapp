"""
Metric display widgets for current weather data.

This module provides comprehensive metric display widgets for showing current
weather information including city/date headers, weather metrics with visibility
controls, and integrated weather alert status indicators. Manages dynamic
metric visibility and alert notifications.

Classes:
    MetricDisplayWidgets: Main metric display manager with alerts integration
"""

from typing import Dict, Any, Optional, List
import tkinter as tk
from tkinter import ttk

from WeatherDashboard import config, styles
from WeatherDashboard.features.alerts.alert_display import AlertStatusIndicator
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.color_utils import get_metric_color, get_enhanced_temperature_color, extract_numeric_value


# ================================
# 1. INITIALIZATION & SETUP
# ================================
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
        and alert status indicators for coordinated updates and visibility management.
        """
        self._create_header_info()
        self._create_weather_metrics()
        self._create_alert_status()    

# ================================  
# 2. METRIC DISPLAY UPDATES
# ================================
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

    def update_alert_display(self, alerts) -> None:
        """Update both alert widget and text label with enhanced styling."""
        if self.alert_status_widget:
            self.alert_status_widget.update_status(alerts)
        
        # Update text label with enhanced information
        if self.alert_text_label:
            if alerts:
                # Count alerts by severity with enhanced display
                warnings = len([a for a in alerts if a.severity == 'warning'])
                cautions = len([a for a in alerts if a.severity == 'caution'])
                watches = len([a for a in alerts if a.severity == 'watch'])
                
                # Create enhanced status text
                status_parts = []
                if warnings > 0:
                    status_parts.append(f"{warnings} Critical")
                if cautions > 0:
                    status_parts.append(f"{cautions} Caution")
                if watches > 0:
                    status_parts.append(f"{watches} Watch")
                
                status_text = " | ".join(status_parts)
                self.alert_text_label.configure(text=status_text)
            else:
                self.alert_text_label.configure(text="")

# ================================
# 3. WIDGET CREATION METHODS
# ================================    
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
            style="AlertText.TLabel"
        )
        self.alert_text_label.pack(side=tk.LEFT, padx=(5, 0))

# ================================
# 4. METRIC POSITIONING & DISPLAY
# ================================
    def _show_metric_at_position(self, metric_key: str, label_text: str, value_text: str, row: int, label_col: int, value_col: int) -> None:
        """Helper method to show a metric at specific grid position with color coding."""
        if metric_key in self.metric_labels:
            widgets = self.metric_labels[metric_key]
            widgets['label'].configure(text=label_text)
            
            # Set padding for column positioning (moved to top)
            padx = styles.ALERT_DISPLAY_CONFIG['column_padding']['right_section'] if label_col == 4 else styles.ALERT_DISPLAY_CONFIG['column_padding']['left_section']
            
            # Special handling for comfort score - show progress bar instead of text
            if metric_key == 'weather_comfort_score' and value_text != '--':
                # Extract numeric value for progress bar
                raw_value = extract_numeric_value(value_text)
                if raw_value is not None:
                    # Clear the value label and add progress bar
                    widgets['value'].configure(text="")
                    
                    # Remove existing progress bar if any
                    for child in widgets['value'].winfo_children():
                        child.destroy()
                    
                    # Create and pack custom progress bar
                    progress_bar = self._create_comfort_progress_bar(widgets['value'], raw_value)
                    progress_bar.pack(pady=2)
                else:
                    widgets['value'].configure(text=value_text, foreground="darkslategray")
            else:
                # Standard metric display with color coding
                widgets['value'].configure(text=value_text)
                
                # Clear any existing alert badges
                for child in widgets['value'].winfo_children():
                    if isinstance(child, tk.Label):  # Remove old badges
                        child.destroy()
                
                # Add color coding based on metric value
                unit_system = self.state.get_current_unit_system()

                # Special color logic for enhanced temperature display
                if metric_key == 'temperature' and 'feels' in value_text:
                    color = get_enhanced_temperature_color(value_text, unit_system)
                    # Check alerts for enhanced temperature (use base temperature)
                    raw_value = extract_numeric_value(value_text)
                else:
                    # Standard color logic for other metrics
                    raw_value = extract_numeric_value(value_text)
                    color = get_metric_color(metric_key, raw_value, unit_system)

                widgets['value'].configure(foreground=color)
                
                # Add alert badges if metric has alerts (simplified for now - will integrate with alert manager)
                if raw_value is not None:
                    # TODO: Integrate with centralized alert manager for metric-specific alerts
                    # For now, skip individual metric badges to avoid duplication
                    pass
            
            # Grid positioning (always executed, uses padx defined at top)
            widgets['label'].grid(row=row, column=label_col, sticky=tk.W, pady=5, padx=padx)
            widgets['value'].grid(row=row, column=value_col, sticky=tk.W, pady=5)

    def _create_comfort_progress_bar(self, parent: ttk.Frame, comfort_score: float) -> tk.Canvas:
        """Create a colored progress bar using Canvas for better color control.
        
        Args:
            parent: Parent frame to contain the progress bar
            comfort_score: Current comfort score (0-100)
            
        Returns:
            tk.Canvas: Canvas widget displaying colored progress bar
        """
        # Get color using the same logic as text metrics
        color = get_metric_color('weather_comfort_score', comfort_score, 'metric')
        
        # Create canvas for custom progress bar using configured dimensions
        layout = styles.WIDGET_LAYOUT['comfort_progress_bar']
        canvas = tk.Canvas(parent, width=layout['width'], height=layout['height'], highlightthickness=0)

        # Draw background
        canvas.create_rectangle(0, 0, layout['width'], layout['height'], fill='lightgray', outline='gray')

        # Draw progress bar
        border_allowance = layout['width'] - (2 * layout['border_width'])  # Leave border space
        progress_width = int((comfort_score / 100) * border_allowance)
        if progress_width > 0:
            canvas.create_rectangle(1, 1, progress_width + 1, 14, fill=color, outline='')
        
        return canvas

# ================================
# 5. UTILITY & HELPER METHODS
# ================================
    def _is_metric_visible(self, metric_key: str) -> bool:
        """Check if a specific metric is currently visible using standardized access."""
        try:
            return self.state.visibility.get(metric_key, tk.BooleanVar()).get()
        except (AttributeError, KeyError) as e:
            Logger.warn(f"Failed to check visibility for metric '{metric_key}': {e}")
            return False