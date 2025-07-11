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
        self.thresholds = config.DEFAULTS["alert_thresholds"]
        
    def check_weather_alerts(self, weather_data: Dict[str, Any]) -> List[WeatherAlert]:
        """Check weather data against alert thresholds and return any alerts.
        
        Evaluates current weather conditions against configured alert thresholds
        and generates appropriate alerts with severity levels and descriptions.
        
        Args:
            weather_data: Current weather data to evaluate
            
        Returns:
            List[Dict[str, Any]]: List of generated alerts with severity and descriptions
        """
        new_alerts = []
        
        # Clear previous alerts
        self.active_alerts.clear()
        
        # Get visible metrics from state
        visible_metrics = self._get_visible_metrics()
        
        # Check alerts only for visible metrics
        if 'temperature' in visible_metrics:
            temp = weather_data.get('temperature', 0)
            new_alerts.extend(self._check_temperature_alerts(temp))
        
        if 'wind_speed' in visible_metrics:
            wind_speed = weather_data.get('wind_speed', 0)
            new_alerts.extend(self._check_wind_alerts(wind_speed))
        
        if 'pressure' in visible_metrics:
            pressure = weather_data.get('pressure', 1013)
            new_alerts.extend(self._check_pressure_alerts(pressure))
        
        if 'humidity' in visible_metrics:
            humidity = weather_data.get('humidity', 50)
            new_alerts.extend(self._check_humidity_alerts(humidity))
        
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
        if threshold_key in ['temperature_high', 'temperature_low']:
            return UnitConverter.convert_temperature(threshold_value, '°C', '°F')
        elif threshold_key == 'wind_speed_high':
            return UnitConverter.convert_wind_speed(threshold_value, 'm/s', 'mph')
        elif threshold_key == 'pressure_low':
            return UnitConverter.convert_pressure(threshold_value, 'hPa', 'inHg')
        else:
            return threshold_value  # humidity doesn't need conversion

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
    
    def _check_temperature_alerts(self, temperature: float) -> List[WeatherAlert]:
        """Check for temperature-based alerts.
        
        Args:
            temperature: Current temperature value to evaluate
            
        Returns:
            List[WeatherAlert]: List of temperature-related alerts generated
        """
        alerts = []

        # Get current unit system from state
        unit_system = self.state.get_current_unit_system()

        high_threshold = self._get_converted_threshold('temperature_high', unit_system)
        low_threshold = self._get_converted_threshold('temperature_low', unit_system)
        
        # Determine temperature unit for display
        temp_unit = '°F' if unit_system == 'imperial' else '°C'
        
        if temperature > high_threshold:
            alert = WeatherAlert(
                alert_type='temperature_high',
                severity='warning',
                title='High Temperature Alert',
                message=f'Temperature is very high: {temperature:.1f}{temp_unit} (threshold: {high_threshold}{temp_unit})',
                icon='🔥',
                value=temperature,
                threshold=high_threshold
            )
            alerts.append(alert)
            
        elif temperature < low_threshold:
            alert = WeatherAlert(
                alert_type='temperature_low', 
                severity='warning',
                title='Low Temperature Alert',
                message=f'Temperature is very low: {temperature:.1f}{temp_unit} (threshold: {low_threshold}{temp_unit})',
                icon='🥶',
                value=temperature,
                threshold=low_threshold
            )
            alerts.append(alert)
            
        return alerts
    
    def _check_wind_alerts(self, wind_speed: float) -> List[WeatherAlert]:
        """Check for wind-based alerts.
        
        Args:
            wind_speed: Current wind speed value to evaluate
            
        Returns:
            List[WeatherAlert]: List of wind-related alerts generated
        """
        alerts = []
        
        # Get current unit system from state
        unit_system = self.state.get_current_unit_system()
        
        threshold = self._get_converted_threshold('wind_speed_high', unit_system)
        
        # Determine wind speed unit for display
        wind_unit = 'mph' if unit_system == 'imperial' else 'm/s'
        
        if wind_speed > threshold:
            # Determine severity based on wind speed
            if wind_speed > threshold * 1.5:
                severity = 'warning'
            else:
                severity = 'caution'
                
            alert = WeatherAlert(
                alert_type='wind_speed',
                severity=severity,
                title='High Wind Alert',
                message=f'Strong winds detected: {wind_speed:.1f} {wind_unit} (threshold: {threshold} {wind_unit})',
                icon='💨',
                value=wind_speed,
                threshold=threshold
            )
            alerts.append(alert)
            
        return alerts
    
    def _check_pressure_alerts(self, pressure: float) -> List[WeatherAlert]:
        """Check for pressure-based alerts indicating storm systems.
        
        Args:
            pressure: Current atmospheric pressure value to evaluate
            
        Returns:
            List[WeatherAlert]: List of pressure-related alerts generated
        """
        alerts = []
        
        # Get current unit system from state
        unit_system = self.state.get_current_unit_system()
        
        threshold = self._get_converted_threshold('pressure_low', unit_system)
        
        # Determine pressure unit for display
        pressure_unit = 'inHg' if unit_system == 'imperial' else 'hPa'
        
        if pressure < threshold:
            alert = WeatherAlert(
                alert_type='pressure_low',
                severity='watch',
                title='Low Pressure Alert', 
                message=f'Low pressure system detected: {pressure:.1f} {pressure_unit} (threshold: {threshold} {pressure_unit})',
                icon='⛈️',
                value=pressure,
                threshold=threshold
            )
            alerts.append(alert)
            
        return alerts
    
    def _check_humidity_alerts(self, humidity: float) -> List[WeatherAlert]:
        """Check for humidity-based alerts.
        
        Args:
            humidity: Current humidity percentage to evaluate
            
        Returns:
            List[WeatherAlert]: List of humidity-related alerts generated
        """
        alerts = []
        
        high_threshold = self.thresholds['humidity_high']
        low_threshold = self.thresholds['humidity_low']
        
        if humidity > high_threshold:
            alert = WeatherAlert(
                alert_type='humidity_high',
                severity='caution',
                title='High Humidity Alert',
                message=f'Very humid conditions: {humidity}% (threshold: {high_threshold}%)',
                icon='💧',
                value=humidity,
                threshold=high_threshold
            )
            alerts.append(alert)
            
        elif humidity < low_threshold:
            alert = WeatherAlert(
                alert_type='humidity_low',
                severity='caution', 
                title='Low Humidity Alert',
                message=f'Very dry conditions: {humidity}% (threshold: {low_threshold}%)',
                icon='🏜️',
                value=humidity,
                threshold=low_threshold
            )
            alerts.append(alert)
            
        return alerts
    
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