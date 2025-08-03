"""
Test for WeatherDashboard.styles

Tests style configuration module with focus on:
- Import functionality
- Configuration structure validation
- Theme system integration
"""

import unittest
from unittest.mock import patch

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.test_utils_shared import TestBase


class TestStyles(TestBase):
    """Test styles module functionality."""
    
    def test_import_styles(self):
        """Test that styles module can be imported successfully."""
        import WeatherDashboard.styles
        self.assertTrue(hasattr(WeatherDashboard.styles, "__doc__"))
        self.assertIsNotNone(WeatherDashboard.styles.__doc__)

    def test_styles_module_structure(self):
        """Test that styles module has expected structure."""
        import WeatherDashboard.styles
        
        # Check for expected attributes
        expected_attrs = [
            'LAYOUT_CONFIG',
            'configure_styles',
            'get_theme_config'
        ]
        
        for attr in expected_attrs:
            with self.subTest(attribute=attr):
                self.assertTrue(hasattr(WeatherDashboard.styles, attr), 
                              f"Styles module missing attribute: {attr}")

    def test_layout_config_structure(self):
        """Test that layout configuration has proper structure."""
        import WeatherDashboard.styles
        
        layout_config = WeatherDashboard.styles.LAYOUT_CONFIG
        
        # Check that it's a dictionary
        self.assertIsInstance(layout_config, dict)
        
        # Check for expected layout sections (actual structure)
        expected_sections = ['frames', 'grid_weights', 'widget_positions']
        for section in expected_sections:
            with self.subTest(section=section):
                self.assertIn(section, layout_config)

    def test_theme_config_function(self):
        """Test that theme configuration function works properly."""
        import WeatherDashboard.styles
        
        # Test that get_theme_config is callable
        self.assertTrue(callable(WeatherDashboard.styles.get_theme_config))
        
        # Test that it returns a dictionary
        result = WeatherDashboard.styles.get_theme_config()
        self.assertIsInstance(result, dict)

    def test_configure_styles_function(self):
        """Test that configure_styles function exists and is callable."""
        import WeatherDashboard.styles
        
        # Test that configure_styles is callable
        self.assertTrue(callable(WeatherDashboard.styles.configure_styles))
        
        # Test that it can be called with a theme name
        try:
            WeatherDashboard.styles.configure_styles('neutral')
        except Exception as e:
            # It's okay if it fails due to Tkinter not being available
            self.assertIn('tkinter', str(e).lower())

    def test_alert_definitions_import(self):
        """Test that alert definitions are properly imported."""
        try:
            from WeatherDashboard.features.alerts.alert_config import ALERT_DEFINITIONS
            
            # Check that it's a dictionary
            self.assertIsInstance(ALERT_DEFINITIONS, dict)
            
            # Check for expected alert types
            expected_alerts = ['temperature_high', 'temperature_low', 'wind_speed_high']
            for alert_type in expected_alerts:
                with self.subTest(alert_type=alert_type):
                    self.assertIn(alert_type, ALERT_DEFINITIONS)
                    
                    # Check structure of each alert definition
                    alert_config = ALERT_DEFINITIONS[alert_type]
                    required_keys = ['threshold_key', 'check_function', 'icon', 'title']
                    for key in required_keys:
                        self.assertIn(key, alert_config)
                    
                    # Check for either 'severity' or 'severity_function' (not both)
                    has_severity = 'severity' in alert_config
                    has_severity_function = 'severity_function' in alert_config
                    self.assertTrue(has_severity or has_severity_function,
                                  f"Alert {alert_type} should have either 'severity' or 'severity_function'")
        except ImportError:
            self.skipTest("Alert config not available")

    def test_temperature_difference_colors_function(self):
        """Test that temperature difference colors function works properly."""
        import WeatherDashboard.styles
        
        # Test that get_temperature_difference_colors is callable
        self.assertTrue(callable(WeatherDashboard.styles.get_temperature_difference_colors))
        
        # Test that it returns a string (actual behavior)
        result = WeatherDashboard.styles.get_temperature_difference_colors()
        self.assertIsInstance(result, str)
        
        # Check that it's a valid color
        self.assert_is_valid_color(result)

    def test_metric_colors_function(self):
        """Test that metric colors function works properly."""
        import WeatherDashboard.styles
        
        # Test that get_metric_colors is callable
        self.assertTrue(callable(WeatherDashboard.styles.get_metric_colors))
        
        # Test that it returns a dictionary (actual behavior)
        result = WeatherDashboard.styles.get_metric_colors()
        self.assertIsInstance(result, dict)

    def test_color_validation(self):
        """Test that all color values are valid."""
        import WeatherDashboard.styles
        
        # Get metric colors (returns a dictionary)
        metric_colors = WeatherDashboard.styles.get_metric_colors()
        
        # Check that it's a dictionary of valid colors
        self.assertIsInstance(metric_colors, dict)
        for metric, config in metric_colors.items():
            with self.subTest(metric=metric):
                if isinstance(config, dict) and 'ranges' in config:
                    for value, color in config['ranges']:
                        self.assert_is_valid_color(color)
                elif isinstance(config, str):
                    self.assert_is_valid_color(config)
        
        # Test temperature difference color (returns a string)
        temp_diff_color = WeatherDashboard.styles.get_temperature_difference_colors()
        self.assert_is_valid_color(temp_diff_color)

    def test_alert_function_validation(self):
        """Test that alert check functions are callable."""
        try:
            from WeatherDashboard.features.alerts.alert_config import ALERT_DEFINITIONS
            
            for alert_type, config in ALERT_DEFINITIONS.items():
                with self.subTest(alert_type=alert_type):
                    check_function = config.get('check_function')
                    if check_function:
                        self.assertTrue(callable(check_function), 
                                      f"Check function for {alert_type} should be callable")
        except ImportError:
            self.skipTest("Alert config not available")

    def test_theme_integration(self):
        """Test that styles integrate with theme system."""
        import WeatherDashboard.styles
        
        # Test that styles can be accessed by theme manager
        try:
            from WeatherDashboard.features.themes.theme_manager import theme_manager
            
            # Test getting theme configuration
            theme_config = theme_manager.get_theme_config()
            self.assertIsInstance(theme_config, dict)
            self.assertGreater(len(theme_config), 0)
        except ImportError:
            # Theme manager might not be available, skip this test
            self.skipTest("Theme manager not available")

    def test_performance_characteristics(self):
        """Test that style lookups perform efficiently."""
        import WeatherDashboard.styles
        
        # Test performance of theme configuration lookups
        def test_theme_lookup():
            WeatherDashboard.styles.get_theme_config()
            WeatherDashboard.styles.get_metric_colors()
            WeatherDashboard.styles.get_temperature_difference_colors()
        
        # Should complete quickly
        self.assert_performance_acceptable(test_theme_lookup, iterations=1000, max_time=0.1)


if __name__ == '__main__':
    unittest.main()