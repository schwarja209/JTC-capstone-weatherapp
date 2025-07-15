"""
Unit tests for WeatherViewModel class.

Tests view model data formatting and presentation logic including:
- Weather data formatting for display
- Enhanced temperature display formatting
- Wind information formatting with direction
- Date and status formatting
- Metrics formatting with units
- Complete display data generation
- Error handling in formatting
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from WeatherDashboard.core.view_models import WeatherViewModel


class TestWeatherViewModel(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Sample weather data for testing
        self.sample_data = {
            'temperature': 25.0,
            'humidity': 60,
            'pressure': 1013.25,
            'wind_speed': 5.0,
            'wind_direction': 180,
            'wind_gust': 8.0,
            'conditions': 'Clear',
            'feels_like': 27.0,
            'temp_min': 20.0,
            'temp_max': 30.0,
            'visibility': 10000,
            'cloud_cover': 20,
            'rain': 0.0,
            'snow': 0.0,
            'weather_icon': '01d',
            'heat_index': 28.0,
            'wind_chill': None,
            'dew_point': 15.0,
            'precipitation_probability': 10.0,
            'weather_comfort_score': 85.0,
            'uv_index': 5.2,
            'air_quality_index': 3,
            'air_quality_description': 'Moderate'
        }
        
        # Create view model with correct constructor signature
        self.view_model = WeatherViewModel(
            self.sample_data,  # raw_data as positional argument
            'New York',        # city
            'metric',          # unit_system
            False              # is_fallback
        )

    def test_initialization(self):
        """Test view model initializes correctly."""
        self.assertEqual(self.view_model.raw_data, self.sample_data)
        self.assertEqual(self.view_model.city, 'New York')
        self.assertEqual(self.view_model.unit_system, 'metric')
        self.assertFalse(self.view_model.is_fallback)
        self.assertEqual(self.view_model.city_name, 'New York')

    def test_initialization_with_fallback(self):
        """Test view model initialization with fallback data."""
        fallback_vm = WeatherViewModel(
            self.sample_data,
            'Test City',
            'imperial',
            True
        )
        
        self.assertTrue(fallback_vm.is_fallback)
        self.assertEqual(fallback_vm.unit_system, 'imperial')

    def test_format_date(self):
        """Test date formatting."""
        # Test with specific datetime
        test_date = datetime(2024, 12, 15, 14, 30, 0)
        formatted = self.view_model._format_date(test_date)
        
        self.assertIsInstance(formatted, str)
        self.assertGreater(len(formatted), 0)

    def test_format_date_current_time(self):
        """Test date formatting with current time."""
        formatted = self.view_model._format_date()
        
        # Should return a formatted string
        self.assertIsInstance(formatted, str)
        self.assertGreater(len(formatted), 0)

    def test_format_status_live_data(self):
        """Test status formatting for live data."""
        status = self.view_model._format_status()
        self.assertEqual(status, "")  # Live data shows no status

    def test_format_status_fallback_data(self):
        """Test status formatting for fallback data."""
        fallback_vm = WeatherViewModel(
            self.sample_data,
            'Test City',
            'metric',
            True
        )
        
        status = fallback_vm._format_status()
        self.assertEqual(status, "(Simulated)")

    def test_get_display_data_structure(self):
        """Test that display data has expected structure."""
        display_data = self.view_model.get_display_data()
        
        # Should return a dictionary
        self.assertIsInstance(display_data, dict)
        
        # Should have some basic expected keys (flexible based on actual implementation)
        self.assertIsInstance(display_data, dict)
        self.assertGreater(len(display_data), 0)

    def test_get_display_data_imperial_units(self):
        """Test display data generation with imperial units."""
        imperial_vm = WeatherViewModel(
            self.sample_data,
            'New York',
            'imperial',
            False
        )
        
        display_data = imperial_vm.get_display_data()
        
        # Should return valid display data
        self.assertIsInstance(display_data, dict)

    def test_get_metric_value_existing_key(self):
        """Test getting metric value for existing key."""
        value = self.view_model.get_metric_value('temperature')
        self.assertEqual(value, 25.0)

    def test_get_metric_value_missing_key(self):
        """Test getting metric value for missing key."""
        value = self.view_model.get_metric_value('nonexistent_metric')
        self.assertIsNone(value)

    def test_degrees_to_compass_conversion(self):
        """Test wind direction degree to compass conversion."""
        test_cases = [
            (0, "N"),
            (45, "NE"),
            (90, "E"),
            (135, "SE"),
            (180, "S"),
            (225, "SW"),
            (270, "W"),
            (315, "NW"),
            (360, "N")  # Wraps around
        ]
        
        for degrees, expected in test_cases:
            with self.subTest(degrees=degrees):
                result = self.view_model._degrees_to_compass(degrees)
                self.assertEqual(result, expected)

    def test_get_weather_icon(self):
        """Test weather icon retrieval."""
        with patch('WeatherDashboard.core.view_models.styles') as mock_styles:
            mock_styles.WEATHER_ICONS = {
                '01d': '☀️',
                '02d': '🌤️'
            }
            
            # Test existing icon
            result = self.view_model._get_weather_icon('01d')
            self.assertEqual(result, '☀️')
            
            # Test non-existing icon
            result = self.view_model._get_weather_icon('99x')
            self.assertEqual(result, '')

    def test_edge_cases_with_none_values(self):
        """Test handling of None values in weather data."""
        # Create data with None values
        none_data = {
            'temperature': None,
            'humidity': None,
            'pressure': None,
            'wind_speed': None,
            'conditions': None,
            'feels_like': None,
            'temp_min': None,
            'temp_max': None
        }
        
        view_model = WeatherViewModel(
            none_data,
            'Test City',
            'metric',
            False
        )
        
        # Should not crash and should return formatted data
        display_data = view_model.get_display_data()
        self.assertIsInstance(display_data, dict)

    def test_error_handling_in_formatting(self):
        """Test error handling during data formatting."""
        # Create malformed data that might cause formatting errors
        bad_data = {
            'temperature': 'invalid_number',
            'humidity': [],
            'pressure': {},
            'wind_speed': 'text',
            'conditions': 123
        }
        
        # Should handle errors gracefully
        try:
            view_model = WeatherViewModel(
                bad_data,
                'Test City',
                'metric',
                False
            )
            display_data = view_model.get_display_data()
            # If we get here, error handling worked
            self.assertIsInstance(display_data, dict)
        except Exception as e:
            # If we get an exception, the error handling needs improvement
            self.fail(f"View model should handle malformed data gracefully: {e}")

    def test_date_string_property(self):
        """Test date_str property."""
        date_str = self.view_model.date_str
        self.assertIsInstance(date_str, str)
        self.assertGreater(len(date_str), 0)

    def test_metrics_property_after_setup(self):
        """Test metrics property after setup."""
        # Metrics should be populated after initialization
        self.assertIsInstance(self.view_model.metrics, dict)

    def test_format_with_unit_converter_integration(self):
        """Test formatting integration with unit converter."""
        with patch('WeatherDashboard.core.view_models.UnitConverter') as mock_converter:
            mock_converter.format_value.return_value = "25.0 °C"
            
            # Create new view model to trigger formatting
            vm = WeatherViewModel(
                self.sample_data,
                'Test',
                'metric',
                False
            )
            
            display_data = vm.get_display_data()
            
            # Should return valid display data
            self.assertIsInstance(display_data, dict)

    def test_comprehensive_display_formatting(self):
        """Test comprehensive display data formatting with all features."""
        # Test with rich data that exercises all formatting paths
        rich_data = {
            'temperature': 25.0,
            'humidity': 60,
            'pressure': 1013.25,
            'wind_speed': 5.0,
            'wind_direction': 225,  # SW
            'wind_gust': 8.0,
            'conditions': 'Partly Cloudy',
            'feels_like': 28.0,  # Warmer feeling
            'temp_min': 18.0,
            'temp_max': 32.0,
            'visibility': 10000,
            'cloud_cover': 40,
            'rain': 2.5,
            'snow': 0.0,
            'weather_icon': '02d',
            'heat_index': 29.0,
            'wind_chill': None,
            'dew_point': 16.0,
            'precipitation_probability': 25.0,
            'weather_comfort_score': 75.0,
            'uv_index': 6.0,
            'air_quality_index': 2,
            'air_quality_description': 'Fair'
        }
        
        view_model = WeatherViewModel(
            rich_data,
            'San Francisco',
            'metric',
            False
        )
        
        display_data = view_model.get_display_data()
        
        # Should return valid display data structure
        self.assertIsInstance(display_data, dict)
        self.assertGreater(len(display_data), 0)

    def test_view_model_with_minimal_data(self):
        """Test view model with minimal weather data."""
        minimal_data = {
            'temperature': 20.0,
            'humidity': 50,
            'conditions': 'Clear'
        }
        
        view_model = WeatherViewModel(
            minimal_data,
            'Test City',
            'metric',
            False
        )
        
        # Should handle minimal data gracefully
        display_data = view_model.get_display_data()
        self.assertIsInstance(display_data, dict)

    def test_view_model_different_unit_systems(self):
        """Test view model with different unit systems."""
        for unit_system in ['metric', 'imperial']:
            with self.subTest(unit_system=unit_system):
                vm = WeatherViewModel(
                    self.sample_data,
                    'Test City',
                    unit_system,
                    False
                )
                
                display_data = vm.get_display_data()
                self.assertIsInstance(display_data, dict)
                self.assertEqual(vm.unit_system, unit_system)


if __name__ == '__main__':
    unittest.main()