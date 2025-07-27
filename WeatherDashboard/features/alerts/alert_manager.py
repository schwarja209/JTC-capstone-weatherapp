"""
Weather alert management system.

This module provides comprehensive weather alert processing including
threshold monitoring, alert generation, severity assessment, and alert
status management. Supports configurable alert conditions and real-time
weather monitoring for user notifications.

Classes:
    AlertManager: Main alert processing and management system
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from WeatherDashboard.utils.logger import Logger
from WeatherDashboard import config, styles
from WeatherDashboard.utils.unit_converter import UnitConverter
from WeatherDashboard.utils.state_utils import StateUtils


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
    def __init__(self, alert_type: str, severity: str, title: str, message: str, icon: str, value: float, threshold: float) -> None:
        """Initialize a weather alert."""
        self.alert_type = alert_type
        self.severity = severity # 'warning', 'caution', 'watch'
        self.title = title
        self.message = message
        self.icon = icon
        self.value = value
        self.threshold = threshold
        self.timestamp = datetime.now()
    
    def __repr__(self) -> str:
        """String representation for debugging."""
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
    def __init__(self, state_manager: Any, thresholds: Optional[Dict[str, Any]]) -> None:
        """Initialize the alert manager."""
        # Direct imports for stable utilities
        self.logger = Logger()
        self.config = config
        self.styles = styles
        self.unit_converter = UnitConverter()
        self.state_utils = StateUtils()
        
        # Injected dependencies for testable components
        self.state = state_manager
        self.active_alerts: List[WeatherAlert] = []
        self.alert_history: List[WeatherAlert] = []
        
        # Initialize dependencies with injection
        self.thresholds = thresholds or self.config.ALERT_THRESHOLDS

    def _get_alert_definitions(self) -> Dict[str, Dict[str, Any]]:
        """Return alert definitions from centralized styling configuration."""
        return self.styles.ALERT_DEFINITIONS
    
    def _check_generic_alert(self, alert_type: str, value: float, weather_data: Dict[str, Any] = None) -> List[WeatherAlert]:
        """Check alert condition using configurable definitions and create alerts.
    
        Retrieves alert definition, converts thresholds for current unit system,
        applies check function, determines severity (static or dynamic), and
        creates appropriate alert objects with formatted messages.
        
        Args:
            alert_type: Type of alert to check (key from alert definitions)
            value: Current value to check against threshold
            weather_data: Full weather data dict (for special cases like precipitation)
            
        Returns:
            List of WeatherAlert objects if conditions met, empty list otherwise
        """
        alert_def = self._get_alert_definitions().get(alert_type)
        if not alert_def:
            return []
        
        alerts = []
        unit_system = self.state.get_current_unit_system()
        
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
        """Check weather data against alert thresholds and generate appropriate alerts.

        Processes current weather data against all configured alert thresholds,
        generates alerts for exceeded conditions, manages alert history, and
        returns active alerts for UI display. Only checks metrics that are
        currently visible to the user.

        Args:
            weather_data: Dictionary containing current weather measurements
            
        Returns:
            List[WeatherAlert]: Currently active weather alerts
        """
        new_alerts = []
        
        # Clear previous alerts
        self.active_alerts.clear()
        
        # Get visible metrics from state
        visible_metrics = self.state_utils.get_visible_metrics(self.state)
        
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
            if len(self.alert_history) > self.config.MEMORY['max_alert_history_size']:
                self.alert_history = self.alert_history[-self.config.MEMORY['max_alert_history_size']:]
            
            # Log all new alerts
            for alert in new_alerts:
                self.logger.warn(f"Weather alert: {alert.title} - {alert.message}")
        
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
            return self.unit_converter.convert_temperature(threshold_value, '°C', '°F')
        elif threshold_key == 'wind_speed_high':
            return self.unit_converter.convert_wind_speed(threshold_value, 'm/s', 'mph')
        elif threshold_key == 'pressure_low':
            return self.unit_converter.convert_pressure(threshold_value, 'hPa', 'inHg')
        elif threshold_key in ['heavy_rain_threshold', 'heavy_snow_threshold']:
            return self.unit_converter.convert_precipitation(threshold_value, 'mm', 'in')
        else:
            return threshold_value  # humidity, etc. don't need conversion
    
    def get_active_alerts(self) -> List[WeatherAlert]:
        """Get currently active alerts."""
        return self.active_alerts.copy()
    
    def get_alert_history(self, limit: int = 20) -> List[WeatherAlert]:
        """Get recent alert history."""
        return self.alert_history[-limit:]
    
    def clear_all_alerts(self) -> None:
        """Clear all active alerts."""
        self.active_alerts.clear()
        self.logger.info("All active alerts cleared")