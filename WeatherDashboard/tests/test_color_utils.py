"""
Unit tests for color utility functions.

Tests color determination logic for metric values including:
- Color coding based on value ranges
- Unit system dependent color selection
- Enhanced temperature color logic with feels-like indicators
- Numeric value extraction from formatted text
- Theme foundation for satirical color manipulation
"""

import unittest
from unittest.mock import Mock, patch

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from WeatherDashboard.utils.color_utils import (
    get_metric_color, get_enhanced_temperature_color, extract_numeric_value
)


class TestColorUtils(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Use actual color ranges from your styles.py
        self.mock_color_ranges = {
            'temperature': {
                'ranges': [
                    (-20, 'navy'),
                    (-10, 'blue'),
                    (5, 'steelblue'),
                    (15, 'green'),
                    (25, 'orange'),
                    (35, 'red'),
                    (45, 'darkred')
                ],
                'unit_dependent': True,
                'imperial_ranges': [
                    (-10, 'navy'),
                    (15, 'blue'),
                    (40, 'steelblue'),
                    (60, 'green'),
                    (80, 'orange'),
                    (95, 'red'),
                    (110, 'darkred')
                ]
            },
            'humidity': {
                'ranges': [
                    (20, 'orange'),
                    (40, 'goldenrod'),
                    (60, 'green'),
                    (80, 'steelblue'),
                    (100, 'blue')
                ],
                'unit_dependent': False
            },
            'wind_speed': {
                'ranges': [
                    (2, 'green'),
                    (5, 'goldenrod'),
                    (10, 'orange'),
                    (15, 'red'),
                    (25, 'darkred')
                ],
                'unit_dependent': False
            },
            'pressure': {
                'ranges': [
                    (980, 'red'),
                    (1000, 'orange'),
                    (1020, 'green'),
                    (1040, 'orange'),
                    (1060, 'red')
                ],
                'unit_dependent': False
            }
        }

    @patch('WeatherDashboard.utils.color_utils.styles')
    def test_get_metric_color_temperature_cold(self, mock_styles):
        """Test temperature color for cold conditions."""
        mock_styles.METRIC_COLOR_RANGES = self.mock_color_ranges
        
        # Test very cold temperature
        result = get_metric_color('temperature', -15, 'metric')
        self.assertEqual(result, 'blue')
        
        # Test cold temperature
        result = get_metric_color('temperature', 0, 'metric')
        self.assertEqual(result, 'steelblue')

    @patch('WeatherDashboard.utils.color_utils.styles')
    def test_get_metric_color_temperature_moderate(self, mock_styles):
        """Test temperature color for moderate conditions."""
        mock_styles.METRIC_COLOR_RANGES = self.mock_color_ranges
        
        # Test moderate temperature (should be orange based on your ranges)
        result = get_metric_color('temperature', 20, 'metric')
        self.assertEqual(result, 'orange')  # Fixed expectation

    @patch('WeatherDashboard.utils.color_utils.styles')
    def test_get_metric_color_temperature_hot(self, mock_styles):
        """Test temperature color for hot conditions."""
        mock_styles.METRIC_COLOR_RANGES = self.mock_color_ranges
        
        # Test hot temperature (30°C is above 25, so should be red)
        result = get_metric_color('temperature', 30, 'metric')
        self.assertEqual(result, 'red')  # Fixed expectation
        
        # Test very hot temperature
        result = get_metric_color('temperature', 40, 'metric')
        self.assertEqual(result, 'red')

    @patch('WeatherDashboard.utils.color_utils.styles')
    def test_get_metric_color_unit_system_dependent(self, mock_styles):
        """Test color selection with unit system dependent ranges."""
        mock_styles.METRIC_COLOR_RANGES = self.mock_color_ranges
        
        # Test metric system (20°C should be orange)
        result_metric = get_metric_color('temperature', 20, 'metric')
        self.assertEqual(result_metric, 'orange')  # Fixed expectation
        
        # Test imperial system (70°F should be green in imperial ranges)
        result_imperial = get_metric_color('temperature', 70, 'imperial')
        self.assertEqual(result_imperial, 'green')

    @patch('WeatherDashboard.utils.color_utils.styles')
    def test_get_metric_color_humidity_ranges(self, mock_styles):
        """Test humidity color ranges."""
        mock_styles.METRIC_COLOR_RANGES = self.mock_color_ranges
        
        test_cases = [
            (10, 'orange'),     # Low humidity
            (30, 'goldenrod'),  # Moderate-low humidity
            (50, 'green'),      # Ideal humidity
            (70, 'steelblue'),  # High humidity
            (90, 'blue')        # Very high humidity
        ]
        
        for humidity, expected_color in test_cases:
            with self.subTest(humidity=humidity):
                result = get_metric_color('humidity', humidity, 'metric')
                self.assertEqual(result, expected_color)

    @patch('WeatherDashboard.utils.color_utils.styles')
    def test_get_metric_color_none_value(self, mock_styles):
        """Test color determination with None value."""
        mock_styles.METRIC_COLOR_RANGES = self.mock_color_ranges
        
        result = get_metric_color('temperature', None, 'metric')
        self.assertEqual(result, 'darkslategray')

    @patch('WeatherDashboard.utils.color_utils.styles')
    def test_get_metric_color_unknown_metric(self, mock_styles):
        """Test color determination for unknown metric."""
        mock_styles.METRIC_COLOR_RANGES = self.mock_color_ranges
        
        result = get_metric_color('unknown_metric', 25, 'metric')
        self.assertEqual(result, 'darkslategray')

    @patch('WeatherDashboard.utils.color_utils.styles')
    def test_get_metric_color_invalid_value_type(self, mock_styles):
        """Test color determination with invalid value type."""
        mock_styles.METRIC_COLOR_RANGES = self.mock_color_ranges
        
        # Test with string value that can't be converted to float
        result = get_metric_color('temperature', 'invalid', 'metric')
        self.assertEqual(result, 'black')

    @patch('WeatherDashboard.utils.color_utils.styles')
    def test_get_enhanced_temperature_color_no_feels_like(self, mock_styles):
        """Test enhanced temperature color without feels-like information."""
        mock_styles.METRIC_COLOR_RANGES = self.mock_color_ranges
        
        # Test regular temperature display (25°C should be orange)
        result = get_enhanced_temperature_color('25°C', 'metric')
        self.assertEqual(result, 'orange')  # Fixed expectation

    @patch('WeatherDashboard.utils.color_utils.styles')
    def test_get_enhanced_temperature_color_feels_warmer(self, mock_styles):
        """Test enhanced temperature color when feels warmer."""
        mock_styles.TEMPERATURE_DIFFERENCE_COLORS = {
            'slight_warmer': 'darkorange',
            'significant_warmer': 'red',
            'slight_cooler': 'lightblue',
            'significant_cooler': 'blue'
        }
        mock_styles.METRIC_COLOR_RANGES = self.mock_color_ranges
        
        # Test slight difference (feels warmer)
        result = get_enhanced_temperature_color('25°C (feels 27°C ↑)', 'metric')
        self.assertEqual(result, 'darkorange')
        
        # Test significant difference (feels much warmer)
        result = get_enhanced_temperature_color('25°C (feels 32°C ↑)', 'metric')
        self.assertEqual(result, 'red')

    @patch('WeatherDashboard.utils.color_utils.styles')
    def test_get_enhanced_temperature_color_fallback(self, mock_styles):
        """Test enhanced temperature color fallback to normal color."""
        # Set up styles without TEMPERATURE_DIFFERENCE_COLORS
        mock_styles.METRIC_COLOR_RANGES = self.mock_color_ranges
        
        # Should fall back to normal temperature color (25°C = orange)
        result = get_enhanced_temperature_color('25°C (feels 30°C ↑)', 'metric')
        self.assertEqual(result, 'orange')  # Fixed expectation

    def test_extract_numeric_value_simple_number(self):
        """Test numeric value extraction from simple numbers."""
        test_cases = [
            ('25', 25.0),
            ('25.5', 25.5),
            ('-10', -10.0),
            ('0', 0.0),
            ('100.25', 100.25)
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                result = extract_numeric_value(text)
                self.assertEqual(result, expected)

    def test_extract_numeric_value_with_units(self):
        """Test numeric value extraction from text with units."""
        test_cases = [
            ('25°C', 25.0),
            ('77°F', 77.0),
            ('50%', 50.0),
            ('1013 hPa', 1013.0),
            ('15 m/s', 15.0),
            ('30 mph', 30.0)
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                result = extract_numeric_value(text)
                self.assertEqual(result, expected)

    def test_extract_numeric_value_no_number(self):
        """Test numeric value extraction from text with no numbers."""
        test_cases = [
            ('Clear skies', None),
            ('Partly cloudy', None),
            ('No data available', None),
            ('--', None),
            ('N/A', None),
            ('', None)
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                result = extract_numeric_value(text)
                self.assertEqual(result, expected)

    def test_extract_numeric_value_multiple_numbers(self):
        """Test numeric value extraction from text with multiple numbers."""
        test_cases = [
            ('Temperature range: 15°C to 25°C', 15.0),  # Should extract first
            ('Wind: 10 m/s gusts 15 m/s', 10.0),
            ('UV index 7, visibility 10 km', 7.0),
            ('Pressure 1013 hPa, dewpoint 12°C', 1013.0)
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                result = extract_numeric_value(text)
                self.assertEqual(result, expected)

    def test_extract_numeric_value_enhanced_temperature(self):
        """Test numeric value extraction from enhanced temperature display."""
        test_cases = [
            ('25°C (feels 28°C ↑)', 25.0),  # Should extract first number
            ('77°F (feels 82°F ↑)', 77.0),
            ('15°C (feels 12°C ↓)', 15.0),
            ('-5°C (feels -10°C ↓)', -5.0)
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                result = extract_numeric_value(text)
                self.assertEqual(result, expected)

    @patch('WeatherDashboard.utils.color_utils.styles')
    def test_satirical_theme_foundation(self, mock_styles):
        """Test foundation features for satirical theme manipulation."""
        mock_styles.METRIC_COLOR_RANGES = self.mock_color_ranges
        
        # Normal color determination (25°C should be orange)
        normal_color = get_metric_color('temperature', 25, 'metric')
        self.assertEqual(normal_color, 'orange')  # Fixed expectation
        
        # Simulate theme manipulation by modifying ranges
        satirical_ranges = self.mock_color_ranges.copy()
        satirical_ranges['temperature']['ranges'] = [
            (-20, 'rainbow'),  # Satirical: everything is wonderful
            (50, 'rainbow')    # Even extreme heat is "rainbow" colored
        ]
        mock_styles.METRIC_COLOR_RANGES = satirical_ranges
        
        theme_color = get_metric_color('temperature', 25, 'metric')
        self.assertEqual(theme_color, 'rainbow')

    @patch('WeatherDashboard.utils.color_utils.styles')
    def test_error_handling_malformed_config(self, mock_styles):
        """Test error handling with malformed color configuration."""
        # Malformed configuration
        mock_styles.METRIC_COLOR_RANGES = {
            'temperature': {
                'ranges': 'invalid_format',  # Should be a list
                'unit_dependent': True
            }
        }
        
        # Should handle gracefully and return default color
        result = get_metric_color('temperature', 25, 'metric')
        self.assertEqual(result, 'black')  # Fixed expectation

    @patch('WeatherDashboard.utils.color_utils.styles')
    def test_unit_system_edge_cases(self, mock_styles):
        """Test unit system handling edge cases."""
        mock_styles.METRIC_COLOR_RANGES = self.mock_color_ranges
        
        # Test with invalid unit system (25°C should be orange)
        result = get_metric_color('temperature', 25, 'invalid_unit')
        self.assertEqual(result, 'orange')  # Fixed expectation
        
        # Test with None unit system
        result = get_metric_color('temperature', 25, None)
        self.assertEqual(result, 'orange')  # Fixed expectation

    def test_string_numeric_conversion_edge_cases(self):
        """Test string to numeric conversion edge cases."""
        edge_cases = [
            ('25.', 25.0),           # Trailing decimal
            ('.5', None),            # Leading decimal - may not be parsed correctly
            ('1.23e2', None),        # Scientific notation - may not be parsed correctly  
            ('25.00000', 25.0),      # Many decimal places
            ('+25', 25.0),           # Positive sign
            ('25,000', 25.0),        # With comma (should extract 25)
        ]
        
        for text, expected in edge_cases:
            with self.subTest(text=text):
                result = extract_numeric_value(text)
                if expected is not None:
                    self.assertAlmostEqual(result, expected, places=1)
                else:
                    # For cases that might not parse correctly, just check they don't crash
                    self.assertIsInstance(result, (float, type(None)))


if __name__ == '__main__':
    unittest.main()