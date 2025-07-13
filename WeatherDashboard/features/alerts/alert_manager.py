"""
Weather alert management system.

This module provides comprehensive weather alert processing including
threshold monitoring, alert generation, severity assessment, and alert
status management. Supports configurable alert conditions and real-time
weather monitoring for user notifications.

Classes:
    AlertManager: Main alert processing and management system
"""

from typing import List, Dict, Any
from datetime import datetime

from WeatherDashboard import config
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.unit_converter import UnitConverter

class WeatherAlert:
    """Individual weather alert data structure.
    
    Represents a single weather alert with all relevant information including
    severity, messaging, thresholds, and timing data.
    
    Attributes:
        alert_type: Type/category of the alert
        severity: Alert severity level ('warning', 'caution', 'watch')
        title: Short descriptive title for the alert
        message: Detailed alert message for display
        icon: Emoji icon representing the alert type
        value: Current weather value that triggered the alert
        threshold: Threshold value that was exceeded
        timestamp: When the alert was generated
    """
    def __init__(self, alert_type: str, severity: str, title: str, message: str, icon: str, value: float, threshold: float):
        """Initialize a weather alert.
        
        Args:
            alert_type: Type/category of the alert
            severity: Alert severity level ('warning', 'caution', 'watch')
            title: Short descriptive title for the alert
            message: Detailed alert message for display
            icon: Emoji icon representing the alert type
            value: Current weather value that triggered the alert
            threshold: Threshold value that was exceeded
        """
        self.alert_type = alert_type
        self.severity = severity  # 'warning', 'caution', 'watch'
        self.title = title
        self.message = message
        self.icon = icon
        self.value = value
        self.threshold = threshold
        self.timestamp = datetime.now()
    
    def __repr__(self) -> str:
        """String representation for debugging.
        
        Returns:
            str: Formatted string showing alert severity and title
        """
        return f"WeatherAlert({self.severity}: {self.title})"

class AlertManager:
    """Manage weather alerts and threshold monitoring.
    
    Processes weather data against configurable thresholds to generate
    appropriate alerts for users. Handles alert severity assessment,
    storage of active alerts, and provides status information for UI display.
    
    Attributes:
        state: Application state manager for alert status updates
        active_alerts: List of currently active weather alerts
    """
    def __init__(self, state_manager):
        """Initialize the alert manager.
        
        Args:
            state: Application state manager for alert status updates
        """
        self.state = state_manager
        self.active_alerts: List[WeatherAlert] = []
        self.alert_history: List[WeatherAlert] = []
        
        # Get thresholds from config
        self.thresholds = config.ALERT_THRESHOLDS

    def _get_alert_definitions(self) -> Dict[str, Dict[str, Any]]:
        """Define all alert types with their configuration."""
        return {
            'temperature_high': {
                'threshold_key': 'temperature_high',
                'check_function': lambda val, thresh: val > thresh,
                'severity': 'warning',
                'icon': '🔥',
                'title': 'High Temperature Alert',
                'message_template': 'Temperature is very high: {value:.1f}{unit} (threshold: {threshold:.1f}{unit})',
                'unit_type': 'temperature'
            },
            'temperature_low': {
                'threshold_key': 'temperature_low',
                'check_function': lambda val, thresh: val < thresh,
                'severity': 'warning', 
                'icon': '🥶',
                'title': 'Low Temperature Alert',
                'message_template': 'Temperature is very low: {value:.1f}{unit} (threshold: {threshold:.1f}{unit})',
                'unit_type': 'temperature'
            },
            'wind_speed_high': {
                'threshold_key': 'wind_speed_high',
                'check_function': lambda val, thresh: val > thresh,
                'severity_function': lambda val, thresh: 'warning' if val > thresh * 1.5 else 'caution',
                'icon': '💨',
                'title': 'High Wind Alert', 
                'message_template': 'Strong winds detected: {value:.1f} {unit} (threshold: {threshold:.1f} {unit})',
                'unit_type': 'wind_speed'
            },
            'pressure_low': {
                'threshold_key': 'pressure_low',
                'check_function': lambda val, thresh: val < thresh,
                'severity': 'watch',
                'icon': '⛈️',
                'title': 'Low Pressure Alert',
                'message_template': 'Low pressure system detected: {value:.1f} {unit} (threshold: {threshold:.1f} {unit})',
                'unit_type': 'pressure'
            },
            'humidity_high': {
                'threshold_key': 'humidity_high',
                'check_function': lambda val, thresh: val > thresh,
                'severity': 'caution',
                'icon': '💧',
                'title': 'High Humidity Alert',
                'message_template': 'Very humid conditions: {value:.0f}% (threshold: {threshold:.0f}%)',
                'unit_type': 'percent'
            },
            'humidity_low': {
                'threshold_key': 'humidity_low',
                'check_function': lambda val, thresh: val < thresh,
                'severity': 'caution',
                'icon': '🏜️',
                'title': 'Low Humidity Alert',
                'message_template': 'Very dry conditions: {value:.0f}% (threshold: {threshold:.0f}%)',
                'unit_type': 'percent'
            },
            'heavy_rain': {
                'threshold_key': 'heavy_rain_threshold',
                'check_function': lambda val, thresh: val > thresh,
                'severity': 'warning',
                'icon': '🌧️',
                'title': 'Heavy Rain Alert',
                'message_template': 'Heavy rainfall detected: {value:.1f} {unit}/hour (threshold: {threshold:.1f} {unit})',
                'unit_type': 'precipitation'
            },
            'heavy_snow': {
                'threshold_key': 'heavy_snow_threshold',
                'check_function': lambda val, thresh: val > thresh,
                'severity': 'warning',
                'icon': '🌨️',
                'title': 'Heavy Snow Alert',
                'message_template': 'Heavy snowfall detected: {value:.1f} {unit}/hour (threshold: {threshold:.1f} {unit})',
                'unit_type': 'precipitation'
            },
            'low_visibility': {
                'threshold_key': 'low_visibility_metric',  # Will be handled specially
                'check_function': lambda val, thresh: val < thresh,
                'severity': 'caution',
                'icon': '🌫️',
                'title': 'Low Visibility Alert',
                'message_template': 'Reduced visibility: {value:.1f} {unit} (threshold: {threshold:.1f} {unit})',
                'unit_type': 'visibility'
            },
            'heat_index_high': {
                'threshold_key': 'heat_index_high',
                'check_function': lambda val, thresh: val > thresh,
                'severity': 'warning',
                'icon': '🔥',
                'title': 'Dangerous Heat Index',
                'message_template': 'Heat index is dangerously high: {value:.1f}{unit} (threshold: {threshold:.1f}{unit})',
                'unit_type': 'temperature'
            },
            'wind_chill_low': {
                'threshold_key': 'wind_chill_low',
                'check_function': lambda val, thresh: val < thresh,
                'severity': 'warning',
                'icon': '🥶',
                'title': 'Dangerous Wind Chill',
                'message_template': 'Wind chill is dangerously low: {value:.1f}{unit} (threshold: {threshold:.1f}{unit})',
                'unit_type': 'temperature'
            },
            'uv_index_high': {
                'threshold_key': 'uv_index_high',
                'check_function': lambda val, thresh: val > thresh,
                'severity': 'caution',
                'icon': '☀️',
                'title': 'High UV Index Alert',
                'message_template': 'Very high UV exposure: {value:.0f} (threshold: {threshold:.0f})',
                'unit_type': 'index'
            },
            'air_quality_poor': {
                'threshold_key': 'air_quality_poor',
                'check_function': lambda val, thresh: val >= thresh,
                'severity_function': lambda val, thresh: 'warning' if val == 5 else 'caution',
                'icon': '😷',
                'title': 'Poor Air Quality Alert',
                'message_template': 'Air quality is poor: AQI {value:.0f} (threshold: AQI {threshold:.0f})',
                'unit_type': 'index'
            }
        }
    
    def _check_generic_alert(self, alert_type: str, value: float, weather_data: Dict[str, Any] = None) -> List[WeatherAlert]:
        """Generic method to check any alert type using the definitions table.
        
        Args:
            alert_type: Type of alert to check (key from alert definitions)
            value: Current value to check against threshold
            weather_data: Full weather data dict (for special cases like precipitation)
            
        Returns:
            List of alerts generated
        """
        alert_def = self._get_alert_definitions().get(alert_type)
        if not alert_def:
            return []
        
        alerts = []
        unit_system = self.state.get_current_unit_system()
        
        # Handle special cases that need custom logic
        if alert_type == 'low_visibility':
            # Custom visibility handling (convert units for display)
            unit_system = self.state.get_current_unit_system()
            if unit_system == 'imperial':
                threshold_meters = self._get_converted_threshold('low_visibility_imperial', unit_system)
                vis_display = value * 0.000621371  # meters to miles
                threshold_display = threshold_meters * 0.000621371
                unit = 'mi'
            else:
                threshold_meters = self._get_converted_threshold('low_visibility_metric', unit_system)
                vis_display = value / 1000  # meters to kilometers  
                threshold_display = threshold_meters / 1000
                unit = 'km'
            
            if value < threshold_meters:
                alert = WeatherAlert(
                    alert_type='low_visibility',
                    severity='caution',
                    title='Low Visibility Alert',
                    message=f'Reduced visibility: {vis_display:.1f} {unit} (threshold: {threshold_display:.1f} {unit})',
                    icon='🌫️',
                    value=vis_display,
                    threshold=threshold_display
                )
                return [alert]
            return []
        
        # Get converted threshold
        threshold = self._get_converted_threshold(alert_def['threshold_key'], unit_system)
        
        # Check if alert condition is met
        if alert_def['check_function'](value, threshold):
            # Determine severity (use function if provided, otherwise use fixed severity)
            if 'severity_function' in alert_def:
                severity = alert_def['severity_function'](value, threshold)
            else:
                severity = alert_def['severity']
            
            # Get appropriate unit label
            unit = self._get_unit_for_alert_type(alert_def['unit_type'], unit_system)
            
            # Create alert
            alert = WeatherAlert(
                alert_type=alert_type,
                severity=severity,
                title=alert_def['title'],
                message=alert_def['message_template'].format(
                    value=value, 
                    threshold=threshold, 
                    unit=unit
                ),
                icon=alert_def['icon'],
                value=value,
                threshold=threshold
            )
            alerts.append(alert)
        
        return alerts

    def _get_unit_for_alert_type(self, unit_type: str, unit_system: str) -> str:
        """Get the appropriate unit label for an alert type."""
        unit_map = {
            'temperature': '°F' if unit_system == 'imperial' else '°C',
            'wind_speed': 'mph' if unit_system == 'imperial' else 'm/s',
            'pressure': 'inHg' if unit_system == 'imperial' else 'hPa',
            'precipitation': 'in' if unit_system == 'imperial' else 'mm',
            'visibility': 'mi' if unit_system == 'imperial' else 'km',
            'percent': '%',
            'index': ''
        }
        return unit_map.get(unit_type, '')

    def check_weather_alerts(self, weather_data: Dict[str, Any]) -> List[WeatherAlert]:
        """Check weather data against alert thresholds using the generic system."""
        new_alerts = []
        
        # Clear previous alerts
        self.active_alerts.clear()
        
        # Get visible metrics from state
        visible_metrics = self._get_visible_metrics()
        
        # Map visible metrics to alert types and values
        alert_checks = [
            ('temperature_high', weather_data.get('temperature', 0), 'temperature'),
            ('temperature_low', weather_data.get('temperature', 0), 'temperature'),
            ('wind_speed_high', weather_data.get('wind_speed', 0), 'wind_speed'),
            ('pressure_low', weather_data.get('pressure', 1013), 'pressure'),
            ('humidity_high', weather_data.get('humidity', 50), 'humidity'),
            ('humidity_low', weather_data.get('humidity', 50), 'humidity'),
            ('heavy_rain', weather_data.get('rain', 0) or 0, 'rain'),
            ('heavy_snow', weather_data.get('snow', 0) or 0, 'snow'),
            ('low_visibility', weather_data.get('visibility', 10000), 'visibility'),
            ('heat_index_high', weather_data.get('heat_index'), 'heat_index'),
            ('wind_chill_low', weather_data.get('wind_chill'), 'wind_chill'),
            ('uv_index_high', weather_data.get('uv_index'), 'uv_index'),
            ('air_quality_poor', weather_data.get('air_quality_index'), 'air_quality_index'),
        ]
        
        # Check each alert type if the corresponding metric is visible
        for alert_type, value, metric_key in alert_checks:
            if metric_key in visible_metrics and value is not None:
                new_alerts.extend(self._check_generic_alert(alert_type, value, weather_data))
        
        # Store active alerts and add to history
        self.active_alerts = new_alerts
        if new_alerts:
            self.alert_history.extend(new_alerts)
            
            # Keep history manageable (last 100 alerts)
            if len(self.alert_history) > 100:
                self.alert_history = self.alert_history[-100:]
            
            # Log all new alerts
            for alert in new_alerts:
                Logger.warn(f"Weather alert: {alert.title} - {alert.message}")
        
        return new_alerts

    def _get_converted_threshold(self, threshold_key: str, unit_system: str) -> float:
        """Get threshold converted to current unit system.
        
        Args:
            threshold_key: Configuration key for the threshold
            unit_system: Target unit system ('metric' or 'imperial')
            
        Returns:
            float: Threshold value converted to the specified unit system
        """
        threshold_value = self.thresholds[threshold_key]
        
        # Config thresholds are always in metric, convert if needed
        if unit_system == "metric":
            return threshold_value
        
        # Convert to imperial
        if threshold_key in ['temperature_high', 'temperature_low', 'heat_index_high', 'wind_chill_low']:
            return UnitConverter.convert_temperature(threshold_value, '°C', '°F')
        elif threshold_key == 'wind_speed_high':
            return UnitConverter.convert_wind_speed(threshold_value, 'm/s', 'mph')
        elif threshold_key == 'pressure_low':
            return UnitConverter.convert_pressure(threshold_value, 'hPa', 'inHg')
        elif threshold_key in ['heavy_rain_threshold', 'heavy_snow_threshold']:
            return UnitConverter.convert_precipitation(threshold_value, 'mm', 'in')
        else:
            return threshold_value  # humidity, etc. don't need conversion

    def _get_visible_metrics(self) -> List[str]:
        """Get list of currently visible metrics.
        
        Returns:
            List[str]: List of metric keys that are currently visible in the UI
        """
        visible = []
        if hasattr(self.state, 'visibility'):
            for metric_key, var in self.state.visibility.items():
                if hasattr(var, 'get') and var.get():
                    visible.append(metric_key)
        return visible
    
    def get_active_alerts(self) -> List[WeatherAlert]:
        """Get currently active alerts."""
        return self.active_alerts.copy()
    
    def get_alert_history(self, limit: int = 20) -> List[WeatherAlert]:
        """Get recent alert history."""
        return self.alert_history[-limit:]
    
    def clear_all_alerts(self) -> None:
        """Clear all active alerts."""
        self.active_alerts.clear()
        Logger.info("All active alerts cleared")