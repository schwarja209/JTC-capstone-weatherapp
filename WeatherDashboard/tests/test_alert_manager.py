"""
Unit tests for AlertManager and WeatherAlert classes.

Tests weather alert system functionality including:
- Alert generation based on weather thresholds
- Severity level assignment and calculation
- Unit conversion for alert thresholds
- Alert message formatting and templating
- Visibility-based alert filtering
- Alert history management
- Integration with configuration and styling systems
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import tkinter as tk

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from WeatherDashboard.features.alerts.alert_manager import WeatherAlert, AlertManager


class TestWeatherAlert(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.alert = WeatherAlert(
            alert_type="temperature_high",
            severity="warning",
            title="High Temperature Alert", 
            message="Temperature is very high: 38.0°C (threshold: 35.0°C)",
            icon="🔥",
            value=38.0,
            threshold=35.0
        )

    def test_weather_alert_initialization(self):
        """Test WeatherAlert object initialization."""
        self.assertEqual(self.alert.alert_type, "temperature_high")
        self.assertEqual(self.alert.severity, "warning")
        self.assertEqual(self.alert.title, "High Temperature Alert")
        self.assertIn("38.0°C", self.alert.message)
        self.assertEqual(self.alert.icon, "🔥")
        self.assertEqual(self.alert.value, 38.0)
        self.assertEqual(self.alert.threshold, 35.0)
        self.assertIsInstance(self.alert.timestamp, datetime)

    def test_weather_alert_string_representation(self):
        """Test WeatherAlert string representation."""
        repr_str = repr(self.alert)
        self.assertIn("WeatherAlert", repr_str)
        self.assertIn("warning", repr_str)
        self.assertIn("High Temperature Alert", repr_str)


class TestAlertManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures with mocked state manager."""
        # Create mock state manager
        self.mock_state = Mock()
        self.mock_state.get_current_unit_system.return_value = "metric"
        
        # Mock visibility state
        self.mock_visibility = {}
        for metric in ['temperature', 'humidity', 'wind_speed', 'pressure']:
            mock_var = Mock()
            mock_var.get.return_value = True  # All metrics visible by default
            self.mock_visibility[metric] = mock_var
        self.mock_state.visibility = self.mock_visibility
        
        # Create alert manager with mocked dependencies
        with patch('WeatherDashboard.features.alerts.alert_manager.config') as mock_config:
            mock_config.ALERT_THRESHOLDS = {
                'temperature_high': 35.0,
                'temperature_low': -10.0,
                'wind_speed_high': 15.0,
                'pressure_low': 980.0,
                'humidity_high': 85.0,
                'humidity_low': 15.0
            }
            self.alert_manager = AlertManager(self.mock_state)

    def test_alert_manager_initialization(self):
        """Test AlertManager initializes correctly."""
        self.assertEqual(self.alert_manager.state, self.mock_state)
        self.assertEqual(len(self.alert_manager.active_alerts), 0)
        self.assertEqual(len(self.alert_manager.alert_history), 0)
        self.assertIsNotNone(self.alert_manager.thresholds)

    def test_get_alert_definitions(self):
        """Test alert definitions retrieval."""
        with patch('WeatherDashboard.features.alerts.alert_manager.styles') as mock_styles:
            mock_styles.ALERT_DEFINITIONS = {
                'temperature_high': {
                    'threshold_key': 'temperature_high',
                    'check_function': lambda val, thresh: val > thresh,
                    'severity': 'warning',
                    'icon': '🔥',
                    'title': 'High Temperature Alert',
                    'message_template': 'Temperature is very high: {value:.1f}{unit}',
                    'unit_type': 'temperature'
                }
            }
            
            definitions = self.alert_manager._get_alert_definitions()
            self.assertIn('temperature_high', definitions)
            self.assertEqual(definitions['temperature_high']['severity'], 'warning')

    def test_check_weather_alerts_no_alerts(self):
        """Test weather alert checking with no alert conditions met."""
        # Weather data with normal conditions
        weather_data = {
            'temperature': 22.0,  # Normal temperature
            'humidity': 50.0,     # Normal humidity
            'wind_speed': 5.0,    # Normal wind speed
            'pressure': 1013.0    # Normal pressure
        }
        
        with patch.object(self.alert_manager, '_get_visible_metrics') as mock_visible:
            mock_visible.return_value = ['temperature', 'humidity', 'wind_speed', 'pressure']
            
            with patch.object(self.alert_manager, '_check_generic_alert') as mock_check:
                mock_check.return_value = []  # No alerts for any condition
                
                alerts = self.alert_manager.check_weather_alerts(weather_data)
                
                self.assertEqual(len(alerts), 0)
                self.assertEqual(len(self.alert_manager.active_alerts), 0)

    def test_check_weather_alerts_temperature_warning(self):
        """Test weather alert checking with high temperature warning."""
        # Weather data with high temperature
        weather_data = {
            'temperature': 38.0,  # Above threshold (35.0)
            'humidity': 50.0,
            'wind_speed': 5.0,
            'pressure': 1013.0
        }
        
        # Mock alert creation
        mock_alert = WeatherAlert(
            alert_type="temperature_high",
            severity="warning",
            title="High Temperature Alert",
            message="Temperature is very high: 38.0°C (threshold: 35.0°C)",
            icon="🔥",
            value=38.0,
            threshold=35.0
        )
        
        with patch.object(self.alert_manager, '_get_visible_metrics') as mock_visible:
            mock_visible.return_value = ['temperature']
            
            with patch.object(self.alert_manager, '_check_generic_alert') as mock_check:
                # Return alert only for temperature_high check
                def side_effect(alert_type, value, weather_data=None):
                    if alert_type == 'temperature_high' and value == 38.0:
                        return [mock_alert]
                    return []
                
                mock_check.side_effect = side_effect
                
                alerts = self.alert_manager.check_weather_alerts(weather_data)
                
                self.assertEqual(len(alerts), 1)
                self.assertEqual(alerts[0].alert_type, "temperature_high")
                self.assertEqual(alerts[0].severity, "warning")
                self.assertEqual(len(self.alert_manager.active_alerts), 1)

    def test_check_weather_alerts_multiple_conditions(self):
        """Test weather alert checking with multiple alert conditions."""
        # Weather data with multiple alert conditions
        weather_data = {
            'temperature': 38.0,  # High temperature
            'humidity': 90.0,     # High humidity
            'wind_speed': 20.0,   # High wind speed
            'pressure': 975.0     # Low pressure
        }
        
        # Mock multiple alerts
        mock_alerts = [
            WeatherAlert("temperature_high", "warning", "High Temp", "Hot", "🔥", 38.0, 35.0),
            WeatherAlert("humidity_high", "caution", "High Humidity", "Humid", "💧", 90.0, 85.0),
            WeatherAlert("wind_speed_high", "caution", "High Wind", "Windy", "💨", 20.0, 15.0),
            WeatherAlert("pressure_low", "watch", "Low Pressure", "Stormy", "⛈️", 975.0, 980.0)
        ]
        
        with patch.object(self.alert_manager, '_get_visible_metrics') as mock_visible:
            mock_visible.return_value = ['temperature', 'humidity', 'wind_speed', 'pressure']
            
            with patch.object(self.alert_manager, '_check_generic_alert') as mock_check:
                # Return different alerts for different checks
                def side_effect(alert_type, value, weather_data=None):
                    alert_map = {
                        'temperature_high': [mock_alerts[0]] if value == 38.0 else [],
                        'humidity_high': [mock_alerts[1]] if value == 90.0 else [],
                        'wind_speed_high': [mock_alerts[2]] if value == 20.0 else [],
                        'pressure_low': [mock_alerts[3]] if value == 975.0 else []
                    }
                    return alert_map.get(alert_type, [])
                
                mock_check.side_effect = side_effect
                
                alerts = self.alert_manager.check_weather_alerts(weather_data)
                
                self.assertEqual(len(alerts), 4)
                severities = [alert.severity for alert in alerts]
                self.assertIn("warning", severities)
                self.assertIn("caution", severities)
                self.assertIn("watch", severities)

    def test_check_generic_alert_basic_threshold(self):
        """Test generic alert checking with basic threshold comparison."""
        with patch.object(self.alert_manager, '_get_alert_definitions') as mock_definitions:
            mock_definitions.return_value = {
                'temperature_high': {
                    'threshold_key': 'temperature_high',
                    'check_function': lambda val, thresh: val > thresh,
                    'severity': 'warning',
                    'icon': '🔥',
                    'title': 'High Temperature Alert',
                    'message_template': 'Temperature is very high: {value:.1f}{unit} (threshold: {threshold:.1f}{unit})',
                    'unit_type': 'temperature'
                }
            }
            
            with patch.object(self.alert_manager, '_get_converted_threshold') as mock_threshold:
                mock_threshold.return_value = 35.0
                
                with patch.object(self.alert_manager, '_get_unit_for_alert_type') as mock_unit:
                    mock_unit.return_value = '°C'
                    
                    # Test value above threshold
                    alerts = self.alert_manager._check_generic_alert('temperature_high', 38.0)
                    
                    self.assertEqual(len(alerts), 1)
                    self.assertEqual(alerts[0].alert_type, 'temperature_high')
                    self.assertEqual(alerts[0].severity, 'warning')
                    self.assertIn('38.0', alerts[0].message)

    def test_check_generic_alert_severity_function(self):
        """Test generic alert checking with dynamic severity function."""
        with patch.object(self.alert_manager, '_get_alert_definitions') as mock_definitions:
            # Alert with severity function
            mock_definitions.return_value = {
                'wind_speed_high': {
                    'threshold_key': 'wind_speed_high',
                    'check_function': lambda val, thresh: val > thresh,
                    'severity_function': lambda val, thresh: 'warning' if val > thresh * 1.5 else 'caution',
                    'icon': '💨',
                    'title': 'High Wind Alert',
                    'message_template': 'Strong winds: {value:.1f} {unit}',
                    'unit_type': 'wind_speed'
                }
            }
            
            with patch.object(self.alert_manager, '_get_converted_threshold') as mock_threshold:
                mock_threshold.return_value = 15.0
                
                with patch.object(self.alert_manager, '_get_unit_for_alert_type') as mock_unit:
                    mock_unit.return_value = 'm/s'
                    
                    # Test moderate wind (caution level)
                    alerts = self.alert_manager._check_generic_alert('wind_speed_high', 18.0)
                    self.assertEqual(alerts[0].severity, 'caution')
                    
                    # Test high wind (warning level)
                    alerts = self.alert_manager._check_generic_alert('wind_speed_high', 25.0)
                    self.assertEqual(alerts[0].severity, 'warning')

    def test_get_converted_threshold_metric_to_imperial(self):
        """Test threshold conversion from metric to imperial units."""
        # Mock state to return imperial units
        self.mock_state.get_current_unit_system.return_value = "imperial"
        
        with patch('WeatherDashboard.features.alerts.alert_manager.UnitConverter') as mock_converter:
            mock_converter.convert_temperature.return_value = 95.0  # 35°C to °F
            
            # Test temperature threshold conversion
            result = self.alert_manager._get_converted_threshold('temperature_high', 'imperial')
            
            self.assertEqual(result, 95.0)
            mock_converter.convert_temperature.assert_called_once_with(35.0, '°C', '°F')

    def test_get_converted_threshold_metric_system(self):
        """Test threshold with metric system (no conversion needed)."""
        # State already returns metric
        result = self.alert_manager._get_converted_threshold('temperature_high', 'metric')
        
        # Should return original threshold value
        self.assertEqual(result, 35.0)

    def test_get_unit_for_alert_type(self):
        """Test unit label retrieval for different alert types."""
        test_cases = [
            ('temperature', 'metric', '°C'),
            ('temperature', 'imperial', '°F'),
            ('wind_speed', 'metric', 'm/s'),
            ('wind_speed', 'imperial', 'mph'),
            ('pressure', 'metric', 'hPa'),
            ('pressure', 'imperial', 'inHg'),
            ('percent', 'metric', '%'),
            ('index', 'metric', '')
        ]
        
        for unit_type, unit_system, expected in test_cases:
            with self.subTest(unit_type=unit_type, unit_system=unit_system):
                result = self.alert_manager._get_unit_for_alert_type(unit_type, unit_system)
                self.assertEqual(result, expected)

    def test_get_visible_metrics(self):
        """Test visible metrics retrieval from state."""
        # Configure some metrics as visible, others as not
        self.mock_visibility['temperature'].get.return_value = True
        self.mock_visibility['humidity'].get.return_value = False
        self.mock_visibility['wind_speed'].get.return_value = True
        self.mock_visibility['pressure'].get.return_value = False
        
        visible_metrics = self.alert_manager._get_visible_metrics()
        
        self.assertIn('temperature', visible_metrics)
        self.assertNotIn('humidity', visible_metrics)
        self.assertIn('wind_speed', visible_metrics)
        self.assertNotIn('pressure', visible_metrics)

    def test_get_visible_metrics_missing_state(self):
        """Test visible metrics retrieval with missing state attributes."""
        # Remove visibility attribute
        del self.mock_state.visibility
        
        visible_metrics = self.alert_manager._get_visible_metrics()
        
        # Should return empty list without error
        self.assertEqual(len(visible_metrics), 0)

    def test_get_active_alerts(self):
        """Test active alerts retrieval."""
        # Add some alerts to active list
        mock_alert1 = Mock()
        mock_alert2 = Mock()
        self.alert_manager.active_alerts = [mock_alert1, mock_alert2]
        
        active_alerts = self.alert_manager.get_active_alerts()
        
        # Should return copy of active alerts
        self.assertEqual(len(active_alerts), 2)
        self.assertIsNot(active_alerts, self.alert_manager.active_alerts)  # Should be a copy

    def test_get_alert_history(self):
        """Test alert history retrieval with limit."""
        # Add alerts to history
        mock_alerts = [Mock() for _ in range(25)]
        self.alert_manager.alert_history = mock_alerts
        
        # Test default limit
        history = self.alert_manager.get_alert_history()
        self.assertEqual(len(history), 20)  # Default limit
        
        # Test custom limit
        history = self.alert_manager.get_alert_history(10)
        self.assertEqual(len(history), 10)
        
        # Should return most recent alerts (last N items)
        self.assertEqual(history, mock_alerts[-10:])

    def test_clear_all_alerts(self):
        """Test clearing all active alerts."""
        # Add some alerts
        self.alert_manager.active_alerts = [Mock(), Mock(), Mock()]
        
        with patch('WeatherDashboard.features.alerts.alert_manager.Logger') as mock_logger:
            self.alert_manager.clear_all_alerts()
            
            # All alerts should be cleared
            self.assertEqual(len(self.alert_manager.active_alerts), 0)
            mock_logger.info.assert_called_once_with("All active alerts cleared")

    def test_alert_history_management(self):
        """Test alert history management and size limits."""
        # Create many alerts to test history limit
        weather_data = {'temperature': 40.0}  # High temperature
        
        mock_alert = WeatherAlert("temperature_high", "warning", "Hot", "Very hot", "🔥", 40.0, 35.0)
        
        with patch.object(self.alert_manager, '_get_visible_metrics') as mock_visible:
            mock_visible.return_value = ['temperature']
            
            with patch.object(self.alert_manager, '_check_generic_alert') as mock_check:
                mock_check.return_value = [mock_alert]
                
                # Add more than 100 alerts (history limit)
                for _ in range(105):
                    self.alert_manager.check_weather_alerts(weather_data)
                
                # History should be limited to 100 most recent
                self.assertEqual(len(self.alert_manager.alert_history), 100)

    def test_special_visibility_alert_handling(self):
        """Test special handling for visibility alerts with unit conversion."""
        # Mock low visibility conditions
        weather_data = {'visibility': 2000}  # 2km visibility
        
        with patch.object(self.alert_manager, '_get_visible_metrics') as mock_visible:
            mock_visible.return_value = ['visibility']
            
            # Mock metric system
            self.mock_state.get_current_unit_system.return_value = 'metric'
            
            with patch.object(self.alert_manager, '_get_converted_threshold') as mock_threshold:
                mock_threshold.return_value = 3000  # 3km threshold
                
                alerts = self.alert_manager._check_generic_alert('low_visibility', 2000.0, weather_data)
                
                # Should generate low visibility alert
                self.assertEqual(len(alerts), 1)
                self.assertEqual(alerts[0].alert_type, 'low_visibility')
                self.assertEqual(alerts[0].severity, 'caution')

    def test_alert_logging_integration(self):
        """Test that alerts are properly logged when generated."""
        weather_data = {'temperature': 38.0}
        mock_alert = WeatherAlert("temperature_high", "warning", "High Temp", "Hot weather", "🔥", 38.0, 35.0)
        
        with patch.object(self.alert_manager, '_get_visible_metrics') as mock_visible:
            mock_visible.return_value = ['temperature']
            
            with patch.object(self.alert_manager, '_check_generic_alert') as mock_check:
                mock_check.return_value = [mock_alert]
                
                with patch('WeatherDashboard.features.alerts.alert_manager.Logger') as mock_logger:
                    self.alert_manager.check_weather_alerts(weather_data)
                    
                    # Should log the alert
                    mock_logger.warn.assert_called()
                    log_call_args = mock_logger.warn.call_args[0][0]
                    self.assertIn("Weather alert", log_call_args)
                    self.assertIn("High Temp", log_call_args)


if __name__ == '__main__':
    unittest.main()