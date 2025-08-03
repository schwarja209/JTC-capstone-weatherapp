"""
Metric display widgets for current weather data.

This module provides comprehensive metric display widgets for showing current
weather information including city/date headers, weather metrics with visibility
controls, and integrated weather alert status indicators. Implements lazy widget
creation for improved startup performance and eliminates widget flash issues.

Features include dynamic color coding based on metric values and unit systems,
custom progress bar display for comfort scores, enhanced temperature displays
with feels-like indicators, and integrated alert status with clickable indicators.

Classes:
    MetricDisplayWidgets: Main metric display manager with alerts integration
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, List

from WeatherDashboard import config, styles
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.color_utils import ColorUtils
from WeatherDashboard.utils.state_utils import StateUtils
from WeatherDashboard.utils.widget_utils import WidgetUtils
from WeatherDashboard.features.alerts.alert_display import AlertStatusIndicator

from .base_widgets import BaseWidgetManager, SafeWidgetCreator, widget_error_handler
from .widget_interface import IWeatherDashboardWidgets


# ================================
# 1. INITIALIZATION & SETUP
# ================================
class MetricDisplayWidgets(BaseWidgetManager, IWeatherDashboardWidgets):
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
        # Direct imports for stable utilities
        self.logger = Logger()
        self.config = config
        self.styles = styles
        self.color_utils = ColorUtils()
        self.state_utils = StateUtils()
        self.widget_utils = WidgetUtils()

        # Injected dependencies for testable components
        self.parent_frame = parent_frame
        self.state = state

        # Widget references
        self.metric_labels: Dict[str, Dict[str, ttk.Label]] = {}
        self.city_label: Optional[ttk.Label] = None
        self.date_label: Optional[ttk.Label] = None
        self.alert_status_widget: Optional[AlertStatusIndicator] = None

        # Initialize base class with error handling
        super().__init__(parent_frame, state, "metric display widgets")
        
        # Create widgets with standardized error handling
        if not self.safe_create_widgets():
            self.logger.warn("Metric display widgets created with errors - some functionality may be limited")
    
    def _create_widgets(self) -> None:
        """Create all metric display widgets with base class error handling."""
        self._create_header_info()
        self._create_weather_metrics()
        self._create_alert_status()    

# ================================  
# 2. METRIC DISPLAY UPDATES
# ================================
    def update_metric_display(self, metric_displays: Dict[str, str]) -> None:
        """Update metric displays based on visibility settings and formatted data.

        Clears existing displays, processes metrics in defined column order,
        applies visibility filtering, and positions widgets with proper styling.
        Handles special cases for enhanced temperature, precipitation, and wind displays.

        Args:
            metric_displays: Dictionary of formatted metric data for display
        """
        layout_config = self.styles.LAYOUT_CONFIG
        metric_config = layout_config['widget_positions']['metric_display']
        left_col_config = metric_config['left_column']
        right_col_config = metric_config['right_column']

        # Clear all existing displays first using centralized utility
        for metric_key in self.config.METRICS:
            if metric_key in self.metric_labels:
                widgets = self.metric_labels[metric_key]
                self.widget_utils.safe_grid_forget(widgets['label'])
                self.widget_utils.safe_grid_forget(widgets['value'])
        
        # Update city and date labels
        if self.city_label and "city" in metric_displays:
            self.city_label.configure(text=metric_displays["city"])
        if self.date_label and "date" in metric_displays:
            self.date_label.configure(text=metric_displays["date"])

        # Define display order for each column section
        left_column_order = ['conditions', 'temperature', 'humidity', 'rain', 'snow', 'precipitation_probability', 'wind_chill', 'heat_index', 'weather_comfort_score']
        right_column_order = ['cloud_cover', 'temp_min', 'wind_speed', 'pressure', 'visibility', 'dew_point', 'uv_index', 'air_quality_description']

        left_row = 0
        right_row = 0
        
        # Process left column metrics (columns 2-3)
        for display_metric in left_column_order:
            if self.state_utils.is_metric_visible(self.state, display_metric):
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
                    label = f"{self.config.METRICS[display_metric]['label']}:"
                    value = metric_displays.get(display_metric, '--')
                    if value == '--' or value == '0.0 mm' or value == '0.0 in':
                        should_display = False # Skip if no precipitation
                elif display_metric in ['wind_chill', 'heat_index', 'weather_comfort_score', 'precipitation_probability']:
                    label = f"{self.config.METRICS[display_metric]['label']}:"
                    value = metric_displays.get(display_metric, '--')
                    # Skip wind chill and heat index if they're None (not applicable)
                    if display_metric in ['wind_chill', 'heat_index'] and value == '--':
                        should_display = False
                else:
                    # Standard individual metric
                    label = f"{self.config.METRICS[display_metric]['label']}:"
                    value = metric_displays.get(display_metric, '--')
                
                if should_display:
                    self._show_metric_at_position(
                        display_metric, label, value, left_row, 
                        left_col_config['start_col'], left_col_config['end_col']
                    )
                    left_row += 1
        
        # Process right column metrics (columns 4-5)  
        for display_metric in right_column_order:
            if self.state_utils.is_metric_visible(self.state, display_metric):
                # Determine display data and label
                if display_metric == 'temp_min':
                    label = "Today's Range:"
                    value = metric_displays.get('temp_range', '--')
                elif display_metric == 'wind_speed':
                    label = 'Wind:'
                    value = metric_displays.get('enhanced_wind', '--')
                elif display_metric in ['dew_point', 'uv_index', 'air_quality_description']:
                    label = f"{self.config.METRICS[display_metric]['label']}:"
                    value = metric_displays.get(display_metric, '--')
                else:
                    # Standard individual metric
                    label = f"{self.config.METRICS[display_metric]['label']}:"
                    value = metric_displays.get(display_metric, '--')
                
                self._show_metric_at_position(
                    display_metric, label, value, right_row,
                    right_col_config['start_col'], right_col_config['end_col']
                )
                right_row += 1

    def update_alert_display(self, alerts: List[Any]) -> None:
        """Update both alert widget and text label with enhanced styling.
        
        Updates the alert status indicator widget and text label to display
        current weather alerts with severity-based styling and count information.
        
        Args:
            alerts: List of weather alert objects with severity attributes
        """
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
    
    def update_alerts(self, raw_data: Dict[str, Any]) -> None:
        """Update the alert display widgets with the provided raw weather data."""
        if not self.is_ready():
            self.logger.warn("Cannot update alerts: widgets not ready")
            return
        
        if not isinstance(raw_data, dict):
            self.logger.error(f"Update alerts - raw_data is not a dict: {type(raw_data)}")
            return

        # Extract alerts from raw_data and update the alert widgets
        alerts = raw_data.get("alerts", []) if isinstance(raw_data, dict) else []
        if self.alert_status_widget:
            self.alert_status_widget.update_status(alerts)
        
        if hasattr(self, "alert_text_label") and self.alert_text_label:
            if alerts:
                self.alert_text_label.configure(text=f"{len(alerts)} Alerts")
            else:
                self.alert_text_label.configure(text="")

# ================================
# 3. WIDGET CREATION METHODS
# ================================
    @widget_error_handler("header info")    
    def _create_header_info(self) -> None:
        """Create city and date display headers with error handling."""
        # Get parent dimensions for ratio-based sizing
        parent_width = self.parent.winfo_width()
        if parent_width <= 0:  # Handle case where parent hasn't been sized yet
            parent_width = 300  # Default fallback

        # Calculate width using ratio (e.g., 10% of parent width)
        label_width = max(10, int(0.1 * parent_width))  # Minimum 10 characters

        # City label
        city_label, self.city_label = self.widget_utils.create_label_value_pair(self.parent, "City:", "--", value_style="LabelValue.TLabel")
        self.city_label.configure(width=label_width)
        self.widget_utils.position_widget_pair(self.parent, city_label, self.city_label, 0, 0, 1)

        # Date label  
        date_label, self.date_label = self.widget_utils.create_label_value_pair(self.parent, "Date:", "--", value_style="LabelValue.TLabel")
        self.date_label.configure(width=label_width)
        self.widget_utils.position_widget_pair(self.parent, date_label, self.date_label, 1, 0, 1)
    
    @widget_error_handler("weather metrics")
    def _create_weather_metrics(self) -> None:
        """Initialize metric widgets storage. Widgets created on-demand."""
        # Just initialize the storage - widgets created when first needed
        self.metric_labels = {}

    @widget_error_handler("metric widget")
    def _get_or_create_metric_widget(self, metric_key: str) -> Dict[str, ttk.Label]:
        """Get existing widget or create new one for the metric with error handling."""
        if not isinstance(metric_key, str) or not metric_key.strip():
            raise ValueError(f"Invalid metric_key: {metric_key}")

        if metric_key not in self.metric_labels:
            # Create widgets using centralized utility
            label_text = f"{self.config.METRICS[metric_key]['label']}:"
            name_label, value_label = self.widget_utils.create_label_value_pair(self.parent, label_text, "--")
            
            # Store references
            self.metric_labels[metric_key] = {
                "label": name_label, 
                "value": value_label
            }
            
        return self.metric_labels[metric_key]
    
    @widget_error_handler("alert status")
    def _create_alert_status(self) -> None:
        """Create alert status indicator and notification widgets.
        
        Creates an alert status frame containing both a clickable alert icon
        widget and a text label for alert notifications. The alert widget
        provides visual indication of weather alerts and allows user interaction.
        """
        # Create a frame to hold both alert widget and text
        alert_frame = SafeWidgetCreator.create_frame(self.parent)
        alert_frame.grid(row=2, column=0, columnspan=2, padx=self.styles.CONTROL_PANEL_CONFIG()['padding']['standard'], sticky=tk.W)
        
        # Alert widget
        self.alert_status_widget = AlertStatusIndicator(alert_frame)
        self.alert_status_widget.pack(side=tk.LEFT)
        
        # Alert text label using SafeWidgetCreator
        self.alert_text_label = SafeWidgetCreator.create_label(alert_frame, "", "AlertText.TLabel")
        self.alert_text_label.pack(side=tk.LEFT, padx=(self.styles.CONTROL_PANEL_CONFIG()['padding']['standard'], 0))

# ================================
# 4. METRIC POSITIONING & DISPLAY
# ================================
    def _show_metric_at_position(self, metric_key: str, label_text: str, value_text: str, row: int, label_col: int, value_col: int) -> None:
        """Display metric at specific grid position with dynamic color coding and special formatting.
    
        Creates or retrieves metric widget, applies color coding based on values,
        handles special comfort score progress bar display, and positions widgets
        in the specified grid location.
        
        Args:
            metric_key: Weather metric identifier for widget lookup
            label_text: Display text for the metric label
            value_text: Formatted value text for display
            row: Grid row position
            label_col: Grid column for label widget
            value_col: Grid column for value widget
        """
        # Get or create widget on-demand
        widgets = self._get_or_create_metric_widget(metric_key)
        widgets['label'].configure(text=label_text)
        
        # Set padding for column positioning (moved to top)
        padx = self.styles.ALERT_DISPLAY_CONFIG['column_padding']['right_section'] if label_col == 4 else self.styles.ALERT_DISPLAY_CONFIG['column_padding']['left_section']
        
        # Special handling for comfort score - show progress bar instead of text
        if metric_key == 'weather_comfort_score' and value_text != '--':
            # Extract numeric value for progress bar
            raw_value = self.color_utils.extract_numeric_value(value_text)
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
                color = self.color_utils.get_enhanced_temperature_color(value_text, unit_system)
                # Check alerts for enhanced temperature (use base temperature)
                raw_value = self.color_utils.extract_numeric_value(value_text)
            else:
                # Standard color logic for other metrics
                raw_value = self.color_utils.extract_numeric_value(value_text)
                color = self.color_utils.get_metric_color(metric_key, raw_value, unit_system)

            widgets['value'].configure(foreground=color)
            
            # Add alert badges if metric has alerts (simplified for now - will integrate with alert manager)
            if raw_value is not None:
                # TODO: Integrate with centralized alert manager for metric-specific alerts
                # For now, skip individual metric badges to avoid duplication
                pass
        
        # Grid positioning (always executed, uses padx defined at top)
        self.widget_utils.position_widget_pair(self.parent, widgets['label'], widgets['value'], row, label_col, value_col, label_text)

    def _create_comfort_progress_bar(self, parent: ttk.Frame, comfort_score: float) -> tk.Canvas:
        """Create a colored progress bar using Canvas for better color control.
        
        Args:
            parent: Parent frame to contain the progress bar
            comfort_score: Current comfort score (0-100)
            
        Returns:
            tk.Canvas: Canvas widget displaying colored progress bar
        """
        # Get parent dimensions
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # Get theme configuration
        theme_config = self.styles.get_theme_config()
        progress_config = theme_config['dimensions']['progress_bar']
        
        # Calculate dimensions using ratios
        bar_width = int(progress_config['width_ratio'] * parent_width)
        bar_height = int(progress_config['height_ratio'] * parent_height)
        border_width = progress_config['border_width']

        # Get color using the same logic as text metrics
        color = self.color_utils.get_metric_color('weather_comfort_score', comfort_score, 'metric')
        
        # Create canvas for custom progress bar using calculated dimensions
        canvas = tk.Canvas(parent, width=bar_width, height=bar_height, highlightthickness=0)

        # Draw background
        canvas.create_rectangle(0, 0, bar_width, bar_height, fill='lightgray', outline='gray')

        # Draw progress bar
        border_allowance = bar_width - (2 * border_width)  # Leave border space
        progress_width = int((comfort_score / 100) * border_allowance)
        if progress_width > 0:
            canvas.create_rectangle(1, 1, progress_width + 1, bar_height - 1, fill=color, outline='')
        
        return canvas