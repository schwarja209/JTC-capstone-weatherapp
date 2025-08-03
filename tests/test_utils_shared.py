"""
Shared test utilities for WeatherDashboard test suite.

This module provides common test fixtures, utilities, and helper functions
to reduce duplication and improve maintainability across the test suite.
"""

import unittest
import tkinter as tk
from unittest.mock import Mock, patch
from contextlib import contextmanager


class SharedTestUtils:
    """Shared test utilities for common test operations."""
    
    @staticmethod
    def create_mock_state_manager():
        """Create a mock state manager with common configuration."""
        mock_state = Mock()
        mock_state.get_current_unit_system.return_value = "metric"
        mock_state.get_current_city.return_value = "New York"
        mock_state.get_current_chart_range.return_value = "Last 7 Days"
        mock_state.get_current_chart_metric.return_value = "Temperature"
        mock_state.get_current_range.return_value = "Last 7 Days"
        
        # Mock visibility state
        mock_visibility = {}
        for metric in ['temperature', 'humidity', 'wind_speed', 'pressure']:
            mock_var = Mock()
            mock_var.get.return_value = True  # All metrics visible by default
            mock_visibility[metric] = mock_var
        mock_state.visibility = mock_visibility
        
        return mock_state
    
    @staticmethod
    def create_mock_thresholds():
        """Create mock alert thresholds."""
        return {
            'temperature_high': 35.0,
            'temperature_low': -10.0,
            'wind_speed_high': 15.0,
            'pressure_low': 980.0,
            'humidity_high': 85.0,
            'humidity_low': 15.0
        }
    
    @staticmethod
    def create_mock_weather_data():
        """Create mock weather data for testing."""
        return {
            'temperature': 25.0,
            'humidity': 60.0,
            'wind_speed': 5.0,
            'pressure': 1013.0,
            'conditions': 'Clear'
        }
    
    @staticmethod
    def create_mock_color_ranges():
        """Create mock color ranges for testing."""
        return {
            'temperature': {
                'ranges': [
                    (-20, '#2C3E50'), (-10, '#34495E'), (5, '#3498DB'),
                    (15, '#27AE60'), (25, '#E67E22'), (35, '#E74C3C'), (45, '#C0392B')
                ],
                'unit_dependent': True,
                'imperial_ranges': [
                    (-10, '#2C3E50'), (15, '#34495E'), (40, '#3498DB'),
                    (60, '#27AE60'), (80, '#E67E22'), (95, '#E74C3C'), (110, '#C0392B')
                ]
            },
            'humidity': {
                'ranges': [
                    (0, '#E67E22'), (20, '#F39C12'), (40, '#27AE60'),
                    (70, '#3498DB'), (85, '#2980B9'), (100, '#2C3E50')
                ],
                'unit_dependent': False
            },
            'wind_speed': {
                'ranges': [
                    (0, '#95A5A6'), (5, '#27AE60'), (15, '#F39C12'),
                    (25, '#E67E22'), (35, '#E74C3C')
                ],
                'unit_dependent': False
            },
            'pressure': {
                'ranges': [
                    (980, '#E74C3C'), (1000, '#E67E22'), (1013, '#27AE60'),
                    (1030, '#3498DB'), (1050, '#2980B9')
                ],
                'unit_dependent': False
            }
        }


class TkinterTestMixin:
    """Mixin for tests that need Tkinter functionality."""
    
    @classmethod
    def setUpClass(cls):
        """Set up Tkinter root window once for the entire test class."""
        cls.root = tk.Tk()
        cls.root.withdraw()  # Hide the window during tests

    @classmethod
    def tearDownClass(cls):
        """Clean up Tkinter root window once."""
        if hasattr(cls, 'root') and cls.root:
            cls.root.destroy()

    def setUp(self):
        """Set up test fixtures for each test."""
        # Create common Tkinter variables
        self.temp_var = tk.BooleanVar(value=True)
        self.humidity_var = tk.BooleanVar(value=False)
        self.pressure_var = tk.BooleanVar(value=True)


class PerformanceTestMixin:
    """Mixin for performance testing utilities."""
    
    def assert_performance_acceptable(self, func, *args, iterations=1000, max_time=1.0, **kwargs):
        """Assert that a function performs within acceptable time limits."""
        import time
        
        start_time = time.time()
        for _ in range(iterations):
            func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        self.assertLess(execution_time, max_time, 
                       f"Function took {execution_time:.3f}s, expected < {max_time}s")


class ErrorHandlingTestMixin:
    """Mixin for error handling test utilities."""
    
    def assert_graceful_error_handling(self, func, *args, expected_exception=None, **kwargs):
        """Assert that a function handles errors gracefully."""
        if expected_exception:
            with self.assertRaises(expected_exception):
                func(*args, **kwargs)
        else:
            # Should not raise any exception
            try:
                result = func(*args, **kwargs)
                # Function should return a reasonable result or None
                self.assertIsNotNone(result)
            except Exception as e:
                self.fail(f"Function should handle errors gracefully, but raised: {e}")


@contextmanager
def mock_config(config_dict):
    """Context manager for mocking configuration."""
    with patch('WeatherDashboard.config') as mock_config:
        for key, value in config_dict.items():
            setattr(mock_config, key, value)
        yield mock_config


@contextmanager
def mock_styles(styles_dict):
    """Context manager for mocking styles."""
    with patch('WeatherDashboard.styles') as mock_styles:
        for key, value in styles_dict.items():
            setattr(mock_styles, key, value)
        yield mock_styles


def create_test_widgets(root):
    """Create common test widgets."""
    frame = tk.Frame(root)
    label = tk.Label(frame, text="Test Label")
    value = tk.Label(frame, text="Test Value")
    return frame, label, value


def assert_widget_positioned_correctly(widget, expected_row, expected_column):
    """Assert that a widget is positioned correctly in the grid."""
    grid_info = widget.grid_info()
    if grid_info:
        actual_row = int(grid_info.get('row', -1))
        actual_column = int(grid_info.get('column', -1))
        return actual_row == expected_row and actual_column == expected_column
    return False


def create_mock_alert(alert_type="temperature_high", severity="warning", 
                     title="Test Alert", message="Test message", 
                     icon="🔥", value=38.0, threshold=35.0):
    """Create a mock alert for testing."""
    from WeatherDashboard.features.alerts.alert_manager import WeatherAlert
    return WeatherAlert(
        alert_type=alert_type,
        severity=severity,
        title=title,
        message=message,
        icon=icon,
        value=value,
        threshold=threshold
    )


class TestBase(unittest.TestCase, PerformanceTestMixin, ErrorHandlingTestMixin):
    """Base test class with common functionality."""
    
    def setUp(self):
        """Set up common test fixtures."""
        self.utils = SharedTestUtils()
    
    def assert_almost_equal_with_tolerance(self, actual, expected, tolerance=0.1):
        """Assert that values are almost equal with a tolerance."""
        self.assertAlmostEqual(actual, expected, delta=tolerance)
    
    def assert_is_valid_color(self, color):
        """Assert that a color value is valid."""
        # Check if it's a valid hex color or named color
        if isinstance(color, str):
            if color.startswith('#'):
                # Hex color
                self.assertTrue(len(color) in [4, 7, 9], f"Invalid hex color: {color}")
                self.assertTrue(all(c in '0123456789ABCDEFabcdef' for c in color[1:]))
            else:
                # Named color - just check it's a string
                self.assertIsInstance(color, str)
        else:
            self.fail(f"Color should be a string, got: {type(color)}")


if __name__ == '__main__':
    unittest.main() 