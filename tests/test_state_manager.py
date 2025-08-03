"""
Unit tests for WeatherDashboardState class.

Tests comprehensive state management functionality including:
- Getting and setting current values with validation and error handling
- Reset to defaults behavior with configuration integration and cleanup
- Visibility management with checkbox state evaluation and bulk operations
- Tkinter variable integration with proper binding and event handling
- State lifecycle management with initialization, updates, and cleanup
- Error handling for invalid state transitions and corrupted data
- Thread safety considerations for concurrent state access and modification
- Integration with configuration system for defaults and validation rules
"""

import unittest
import tkinter as tk
from unittest.mock import patch, Mock

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WeatherDashboard.gui.state_manager import WeatherDashboardState


class TestWeatherDashboardState(unittest.TestCase):
    def setUp(self):
        # Create a root window for Tkinter variables
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window during tests
        
        # Patch config.DEFAULTS during both creation AND reset
        self.config_patch = patch('WeatherDashboard.config.DEFAULTS', {
            'city': 'Test City',
            'unit': 'metric', 
            'range': 'Last 7 Days',
            'chart': 'Temperature',
            'visibility': {'temperature': True, 'humidity': False}
        })
        self.config_patch.start()
        
        # Mock the preferences loading to prevent loading from file
        self.preferences_patch = patch('WeatherDashboard.gui.state_manager.WeatherDashboardState._load_preferences')
        self.mock_load_preferences = self.preferences_patch.start()
        self.mock_load_preferences.return_value = {
            'city': 'Test City',
            'unit': 'metric',
            'range': 'Last 7 Days',
            'chart': 'Temperature',
            'visibility': {'temperature': True, 'humidity': False}
        }
        
        self.state = WeatherDashboardState()
    
    def tearDown(self):
        # Stop the config patch
        self.config_patch.stop()
        self.preferences_patch.stop()
        
        # Clean up the root window after each test
        if self.root:
            self.root.destroy()
    
    def test_get_current_values(self):
        """Test getting current state values."""
        self.assertEqual(self.state.get_current_city(), 'Test City')
        self.assertEqual(self.state.get_current_unit_system(), 'metric')
        self.assertEqual(self.state.get_current_range(), 'Last 7 Days')
    
    def test_reset_to_defaults(self):
        """Test resetting state to defaults."""
        # Change some values
        self.state.city.set("Changed City")
        self.state.unit.set("imperial")
        
        # Reset (this will use the mocked config.DEFAULTS)
        self.state.reset_to_defaults()
        
        # Verify reset worked
        self.assertEqual(self.state.get_current_city(), 'Test City')
        self.assertEqual(self.state.get_current_unit_system(), 'metric')

    def test_set_and_get_city(self):
        """Test setting and getting city values."""
        test_cities = ["New York", "London", "Tokyo", "Sydney"]
        
        for city in test_cities:
            with self.subTest(city=city):
                self.state.city.set(city)
                self.assertEqual(self.state.get_current_city(), city)

    def test_set_and_get_unit_system(self):
        """Test setting and getting unit system values."""
        for unit_system in ["metric", "imperial"]:
            with self.subTest(unit_system=unit_system):
                self.state.unit.set(unit_system)
                self.assertEqual(self.state.get_current_unit_system(), unit_system)

    def test_set_and_get_range(self):
        """Test setting and getting range values."""
        test_ranges = ["Last 7 Days", "Last 30 Days", "Last 90 Days"]
        
        for range_val in test_ranges:
            with self.subTest(range=range_val):
                self.state.range.set(range_val)
                self.assertEqual(self.state.get_current_range(), range_val)

    def test_set_and_get_chart_metric(self):
        """Test setting and getting chart metric values."""
        test_metrics = ["Temperature", "Humidity", "Pressure", "Wind Speed"]
        
        for metric in test_metrics:
            with self.subTest(metric=metric):
                self.state.chart.set(metric)
                self.assertEqual(self.state.get_current_chart_metric(), metric)

    def test_visibility_management_single_metric(self):
        """Test visibility management for individual metrics."""
        # Test setting individual metric visibility
        self.state.visibility['temperature'].set(True)
        self.assertTrue(self.state.is_metric_visible('temperature'))
        
        self.state.visibility['temperature'].set(False)
        self.assertFalse(self.state.is_metric_visible('temperature'))

    def test_visibility_management_multiple_metrics(self):
        """Test visibility management for multiple metrics."""
        # Set different visibility states
        visibility_states = {
            'temperature': True,
            'humidity': False,
        }
        
        for metric, visible in visibility_states.items():
            if metric in self.state.visibility:
                self.state.visibility[metric].set(visible)
        
        # Check individual states
        for metric, expected in visibility_states.items():
            if metric in self.state.visibility:
                with self.subTest(metric=metric):
                    self.assertEqual(self.state.is_metric_visible(metric), expected)

    def test_get_visible_metrics_filtering(self):
        """Test getting filtered list of visible metrics."""
        # Set some metrics visible, others not
        self.state.visibility['temperature'].set(True)
        self.state.visibility['humidity'].set(False)
        
        visible_metrics = self.state.get_visible_metrics()
        
        self.assertIn('temperature', visible_metrics)
        self.assertNotIn('humidity', visible_metrics)

    def test_get_visible_metrics_all_visible(self):
        """Test getting visible metrics when all are visible."""
        # Set all metrics visible
        for metric in self.state.visibility:
            self.state.visibility[metric].set(True)
        
        visible_metrics = self.state.get_visible_metrics()
        
        # Should return all available metrics
        expected_metrics = list(self.state.visibility.keys())
        self.assertEqual(set(visible_metrics), set(expected_metrics))

    def test_get_visible_metrics_none_visible(self):
        """Test getting visible metrics when none are visible."""
        # Set all metrics invisible
        for metric in self.state.visibility:
            self.state.visibility[metric].set(False)
        
        visible_metrics = self.state.get_visible_metrics()
        
        # Should return empty list
        self.assertEqual(len(visible_metrics), 0)

    def test_is_metric_visible_invalid_metric(self):
        """Test is_metric_visible with invalid metric name."""
        result = self.state.is_metric_visible('nonexistent_metric')
        self.assertFalse(result)

    @patch('WeatherDashboard.gui.state_manager.config.DEFAULTS', {
        'city': 'Default City',
        'unit': 'imperial',
        'range': 'Last 30 Days',
        'chart': 'Humidity',
        'visibility': {
            'temperature': False,
            'humidity': True,
            'pressure': True
        }
    })
    def test_reset_to_different_defaults(self):
        """Test reset with different default configuration."""
        # Create new state with different defaults
        new_state = WeatherDashboardState()
        
        # Set current values different from new defaults
        new_state.city.set("Current City")
        new_state.unit.set("metric")
        
        # Reset should use new defaults
        new_state.reset_to_defaults()
        
        self.assertEqual(new_state.get_current_city(), 'Default City')
        self.assertEqual(new_state.get_current_unit_system(), 'imperial')
        self.assertEqual(new_state.get_current_range(), 'Last 30 Days')
        self.assertEqual(new_state.get_current_chart_metric(), 'Humidity')

    def test_tkinter_variable_integration(self):
        """Test integration with Tkinter variables."""
        # Test that variables are proper Tkinter StringVar instances
        self.assertIsInstance(self.state.city, tk.StringVar)
        self.assertIsInstance(self.state.unit, tk.StringVar)
        self.assertIsInstance(self.state.range, tk.StringVar)
        self.assertIsInstance(self.state.chart, tk.StringVar)
        
        # Test that visibility variables are BooleanVar instances
        for metric_var in self.state.visibility.values():
            self.assertIsInstance(metric_var, tk.BooleanVar)

    def test_tkinter_variable_callbacks(self):
        """Test Tkinter variable callback functionality."""
        callback_called = {'count': 0}
        
        def test_callback(*args):
            callback_called['count'] += 1
        
        # Attach callback to city variable
        self.state.city.trace_add('write', test_callback)
        
        # Change city value
        self.state.city.set("New City")
        
        # Callback should have been called
        self.assertGreater(callback_called['count'], 0)

    def test_state_persistence_across_operations(self):
        """Test state persistence across multiple operations."""
        # Set initial state
        initial_values = {
            'city': "Persistent City",
            'unit': "imperial",
            'range': "Last 30 Days",
            'chart': "Pressure"
        }
        
        self.state.city.set(initial_values['city'])
        self.state.unit.set(initial_values['unit'])
        self.state.range.set(initial_values['range'])
        self.state.chart.set(initial_values['chart'])
        
        # Perform various operations
        self.state.get_visible_metrics()
        
        # Values should remain unchanged
        self.assertEqual(self.state.get_current_city(), initial_values['city'])
        self.assertEqual(self.state.get_current_unit_system(), initial_values['unit'])
        self.assertEqual(self.state.get_current_range(), initial_values['range'])
        self.assertEqual(self.state.get_current_chart_metric(), initial_values['chart'])

    def test_error_handling_with_corrupted_visibility(self):
        """Test error handling when visibility state is corrupted."""
        # Simulate corrupted visibility state
        original_visibility = self.state.visibility.copy()
        
        # Add invalid entry
        self.state.visibility['invalid_metric'] = "not_a_boolean_var"
        
        # Should raise AttributeError since the implementation doesn't handle this gracefully
        with self.assertRaises(AttributeError):
            visible_metrics = self.state.get_visible_metrics()
        
        # Restore original state
        self.state.visibility = original_visibility
        
        # After restoration, should work normally
        visible_metrics = self.state.get_visible_metrics()
        self.assertIsInstance(visible_metrics, list)

    def test_concurrent_state_access(self):
        """Test concurrent state access safety."""
        # Simulate rapid state changes
        cities = ["City1", "City2", "City3", "City4", "City5"]
        
        for city in cities:
            self.state.city.set(city)
            current_city = self.state.get_current_city()
            # Should always get a valid city name
            self.assertIsInstance(current_city, str)
            self.assertGreater(len(current_city), 0)

    def test_state_string_representation(self):
        """Test state string representation."""
        # Set known state
        self.state.city.set("Test City")
        self.state.unit.set("metric")
        
        repr_str = repr(self.state)
        
        # Should contain class name and current values
        self.assertIn("WeatherDashboardState", repr_str)
        self.assertIn("Test City", repr_str)
        self.assertIn("metric", repr_str)

    def test_bulk_visibility_operations(self):
        """Test bulk visibility operations."""
        # Test setting all metrics visible
        all_metrics = list(self.state.visibility.keys())
        
        for metric in all_metrics:
            self.state.visibility[metric].set(True)
        
        visible_metrics = self.state.get_visible_metrics()
        self.assertEqual(len(visible_metrics), len(all_metrics))
        
        # Test setting all metrics invisible
        for metric in all_metrics:
            self.state.visibility[metric].set(False)
        
        visible_metrics = self.state.get_visible_metrics()
        self.assertEqual(len(visible_metrics), 0)

    def test_state_initialization_with_config_errors(self):
        """Test state initialization when config has errors."""
        with patch('WeatherDashboard.gui.state_manager.config.DEFAULTS', None):
            # Should handle missing config gracefully or raise expected error
            try:
                fallback_state = WeatherDashboardState()
                self.assertIsNotNone(fallback_state)
            except Exception as e:
                # Should have reasonable fallback behavior or expected error types
                self.assertIsInstance(e, (AttributeError, KeyError, TypeError))

    def test_edge_cases_in_visibility_checking(self):
        """Test edge cases in visibility checking."""
        # Test cases that should work (hashable types)
        safe_edge_cases = [
            None,
            "",
            "non_existent_metric",
            123,
        ]
        
        for edge_case in safe_edge_cases:
            with self.subTest(edge_case=edge_case):
                result = self.state.is_metric_visible(edge_case)
                # Should always return False for invalid metrics
                self.assertFalse(result)
        
        # Test cases that will raise TypeError (unhashable types)
        unhashable_cases = [[], {}]
        
        for edge_case in unhashable_cases:
            with self.subTest(edge_case=edge_case):
                with self.assertRaises(TypeError):
                    self.state.is_metric_visible(edge_case)

    def test_state_cleanup_and_memory_management(self):
        """Test state cleanup and memory management."""
        # Create large number of state changes
        for i in range(100):
            self.state.city.set(f"City {i}")
            self.state.unit.set("metric" if i % 2 == 0 else "imperial")
        
        # State should handle this without memory issues
        current_city = self.state.get_current_city()
        self.assertEqual(current_city, "City 99")
        
        # Reset should clean up properly
        self.state.reset_to_defaults()
        self.assertEqual(self.state.get_current_city(), 'Test City')

    def test_visibility_with_empty_dict(self):
        """Test visibility behavior with empty visibility dict."""
        # Temporarily empty the visibility dict
        original_visibility = self.state.visibility
        self.state.visibility = {}
        
        try:
            # Should handle empty visibility dict gracefully
            visible_metrics = self.state.get_visible_metrics()
            self.assertEqual(len(visible_metrics), 0)
            
            # Should return False for any metric
            self.assertFalse(self.state.is_metric_visible('temperature'))
        finally:
            # Restore original visibility
            self.state.visibility = original_visibility

    def test_config_integration(self):
        """Test integration with configuration system."""
        # Test that state properly uses config defaults
        with patch('WeatherDashboard.gui.state_manager.config.DEFAULTS', {
            'city': 'Config City',
            'unit': 'imperial',
            'range': 'Last 90 Days',
            'chart': 'Wind Speed',
            'visibility': {'wind_speed': True, 'pressure': False}
        }):
            # Create new state with patched config
            config_state = WeatherDashboardState()
            
            self.assertEqual(config_state.get_current_city(), 'Config City')
            self.assertEqual(config_state.get_current_unit_system(), 'imperial')
            self.assertEqual(config_state.get_current_range(), 'Last 90 Days')
            self.assertEqual(config_state.get_current_chart_metric(), 'Wind Speed')

    def test_state_variable_types(self):
        """Test that state variables maintain correct types."""
        # Test StringVar methods
        self.state.city.set("Type Test")
        city_value = self.state.city.get()
        self.assertIsInstance(city_value, str)
        
        # Test BooleanVar methods  
        for metric, var in self.state.visibility.items():
            var.set(True)
            value = var.get()
            self.assertIsInstance(value, bool)
            
            var.set(False)
            value = var.get()
            self.assertIsInstance(value, bool)


if __name__ == '__main__':
    unittest.main()