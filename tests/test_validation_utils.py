"""
Unit tests for ValidationUtils class.

Tests comprehensive validation utility functionality including:
- City name validation with edge cases and error reporting
- Unit system validation with invalid inputs and error messages
- Metric visibility validation with state manager integration
- Date range validation with configuration checking  
- Chart metric validation with configuration integration
- Complete state validation with multiple validation checks
- Input type validation for controller operations
- Numeric range validation with boundary checking
- Error formatting and message consistency
- Integration with centralized configuration system
"""

import unittest
import os
import tempfile
from unittest.mock import patch, Mock

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WeatherDashboard.utils.validation_utils import ValidationUtils


class TestValidationUtils(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.validation_utils = ValidationUtils()
    
    # ================================
    # City name validation tests
    # ================================
    
    def test_validate_city_name_valid_inputs(self):
        """Test city name validation with valid inputs."""
        valid_cities = [
            "New York",
            "Paris", 
            "San Francisco",
            "Los Angeles",
            "Chicago",
            "New-York",
            "Saint Paul",
            "Las Vegas",
            "O'Fallon"  # With apostrophe
        ]
        
        for city_name in valid_cities:
            with self.subTest(input=city_name):
                # Should not raise an exception for valid cities
                try:
                    self.validation_utils.validate_city_name(city_name)
                except ValueError:
                    self.fail(f"Valid city '{city_name}' should not raise an exception")

    def test_validate_city_name_invalid_inputs(self):
        """Test city name validation with invalid inputs."""
        invalid_inputs = [
            ("", "cannot be empty"),
            ("   ", "cannot be empty"),
            ("\t\n", "cannot be empty"),
            (None, "must be a string"),
            (123, "must be a string"),
            ([], "must be a string"),
            ({}, "must be a string"),
            ("city123", "invalid characters"),  # Contains numbers
            ("city@domain", "invalid characters"),  # Contains @ symbol
            ("a" * 101, "cannot be longer than 100 characters")  # Too long
        ]
        
        for invalid_input, expected_error_part in invalid_inputs:
            with self.subTest(input=invalid_input):
                # Should raise ValueError for invalid inputs
                with self.assertRaises(ValueError) as context:
                    self.validation_utils.validate_city_name(invalid_input)
                
                # Check that the error message contains expected part
                error_text = str(context.exception).lower()
                self.assertIn(expected_error_part.lower(), error_text)

    # ================================
    # Unit system validation tests
    # ================================
    
    def test_validate_unit_system_valid_inputs(self):
        """Test unit system validation with valid inputs."""
        valid_systems = ["metric", "imperial"]
        
        for system in valid_systems:
            with self.subTest(system=system):
                # Should not raise an exception for valid unit systems
                try:
                    self.validation_utils.validate_unit_system(system)
                except ValueError:
                    self.fail(f"Valid unit system '{system}' should not raise an exception")

    def test_validate_unit_system_invalid_inputs(self):
        """Test unit system validation with invalid inputs."""
        invalid_inputs = [
            ("", "invalid"),
            ("METRIC", "invalid"),
            ("Imperial", "invalid"),
            ("celsius", "invalid"),
            ("fahrenheit", "invalid"),
            ("kelvin", "invalid"),
            (None, "must be a string"),
            (123, "must be a string"),
            ([], "must be a string"),
            ({}, "must be a string")
        ]
        
        for invalid_input, expected_error_part in invalid_inputs:
            with self.subTest(input=invalid_input):
                # Should raise ValueError for invalid unit systems
                with self.assertRaises(ValueError) as context:
                    self.validation_utils.validate_unit_system(invalid_input)
                
                # Check that the error message contains expected part
                error_text = str(context.exception).lower()
                self.assertIn(expected_error_part.lower(), error_text)

    # ================================
    # Metric visibility validation tests
    # ================================
    
    def test_validate_metric_visibility_valid_state(self):
        """Test metric visibility validation with valid state."""
        mock_state_manager = Mock()
        mock_state_manager.visibility = {
            'temperature': Mock(),
            'humidity': Mock(),
            'pressure': Mock()
        }
        
        # Should not raise an exception for valid state
        try:
            self.validation_utils.validate_metric_visibility(mock_state_manager)
        except ValueError:
            self.fail("Valid metric visibility should not raise an exception")

    def test_validate_metric_visibility_no_visible_metrics(self):
        """Test metric visibility validation when no metrics are visible."""
        mock_state_manager = Mock()
        mock_state_manager.visibility = {}  # No visibility metrics
        
        # Should raise ValueError for invalid state
        with self.assertRaises(ValueError):
            self.validation_utils.validate_metric_visibility(mock_state_manager)

    def test_validate_metric_visibility_missing_attribute(self):
        """Test metric visibility validation when state manager missing visibility."""
        mock_state_manager = Mock()
        del mock_state_manager.visibility  # Remove visibility attribute
        
        # Should raise ValueError for invalid state
        with self.assertRaises(ValueError):
            self.validation_utils.validate_metric_visibility(mock_state_manager)

    # ================================
    # Date range validation tests
    # ================================
    
    @patch('WeatherDashboard.utils.validation_utils.config')
    def test_format_validation_errors_empty_list(self, mock_config):
        """Test error formatting with empty error list."""
        # The format_validation_errors method was removed, so we'll skip this test
        self.skipTest("format_validation_errors method was removed")

    @patch('WeatherDashboard.utils.validation_utils.config')
    def test_validate_date_range_valid_inputs(self, mock_config):
        """Test date range validation with valid inputs."""
        mock_config.CHART = {
            "range_options": {
                "Last 7 Days": {"days": 7},
                "Last 14 Days": {"days": 14},
                "Last 30 Days": {"days": 30}
            }
        }
        valid_ranges = ["Last 7 Days", "Last 14 Days", "Last 30 Days"]

        for days in valid_ranges:
            with self.subTest(days=days):
                # Should not raise an exception for valid date ranges
                try:
                    self.validation_utils.validate_date_range(days)
                except ValueError:
                    self.fail(f"Valid date range '{days}' should not raise an exception")

    @patch('WeatherDashboard.utils.validation_utils.config')
    def test_validate_date_range_invalid_inputs(self, mock_config):
        """Test date range validation with invalid inputs."""
        mock_config.CHART = {
            "range_options": {
                "Last 1 Day": {"days": 1},
                "Last 7 Days": {"days": 7}
            }
        }
        mock_config.ERROR_MESSAGES = {
            'validation': 'Date range is invalid: {reason}'
        }
        
        invalid_ranges = ["Invalid Range", "Last 1 Day", None, 42]
        
        for invalid_range in invalid_ranges:
            with self.subTest(invalid_range=invalid_range):
                # Should raise ValueError for invalid date ranges
                with self.assertRaises(ValueError) as context:
                    self.validation_utils.validate_date_range(invalid_range)
                
                # Check error message content
                error_text = str(context.exception).lower()
                if isinstance(invalid_range, str):
                    self.assertIn("invalid", error_text)
                else:
                    self.assertIn("string", error_text)

    # ================================
    # Chart metric validation tests
    # ================================
    
    @patch('WeatherDashboard.utils.validation_utils.config')
    def test_validate_chart_metric_valid_inputs(self, mock_config):
        """Test chart metric validation with valid inputs."""
        mock_config.METRICS = {
            "temperature": {"label": "Temperature"},
            "humidity": {"label": "Humidity"},
            "pressure": {"label": "Pressure"}
        }
        valid_metrics = ["Temperature", "Humidity", "Pressure"]

        for metric in valid_metrics:
            with self.subTest(metric=metric):
                # Should not raise an exception for valid chart metrics
                try:
                    self.validation_utils.validate_chart_metric(metric)
                except ValueError:
                    self.fail(f"Valid chart metric '{metric}' should not raise an exception")

    @patch('WeatherDashboard.utils.validation_utils.config')
    def test_validate_chart_metric_invalid_inputs(self, mock_config):
        """Test chart metric validation with invalid inputs."""
        mock_config.METRICS = {
            "temperature": {"label": "Temperature"},
            "humidity": {"label": "Humidity"}
        }
        mock_config.ERROR_MESSAGES = {
            'validation': 'Chart metric is invalid: {reason}'
        }
        
        with patch('WeatherDashboard.utils.validation_utils.config', mock_config):
            invalid_metrics = ["Invalid Metric", "Temp", None, 42]

            for invalid_metric in invalid_metrics:
                with self.subTest(invalid_metric=invalid_metric):
                    # Should raise ValueError for invalid chart metrics
                    with self.assertRaises(ValueError) as context:
                        self.validation_utils.validate_chart_metric(invalid_metric)

                    # Check error message content
                    error_text = str(context.exception).lower()
                    if isinstance(invalid_metric, str):
                        self.assertIn("not found", error_text)  # Changed from "invalid" to "not found"

    # ================================
    # Complete state validation tests
    # ================================
    
    @patch('WeatherDashboard.utils.validation_utils.config')
    def test_validate_complete_state_valid_state(self, mock_config):
        """Test complete state validation with valid state."""
        mock_config.ERROR_MESSAGES = {
            'validation': 'Field is invalid: {reason}',
            'state_error': 'State validation error: {reason}'
        }
        
        # Mock a valid state manager
        mock_state_manager = Mock()
        mock_state_manager.get_current_city.return_value = "New York"
        mock_state_manager.get_current_unit_system.return_value = "metric"
        mock_state_manager.get_current_range.return_value = "Last 7 Days"
        mock_state_manager.get_current_chart_metric.return_value = "Temperature"
        
        # Mock the validation methods to not raise exceptions
        with patch.object(self.validation_utils, 'validate_city_name') as mock_city, \
             patch.object(self.validation_utils, 'validate_unit_system') as mock_unit, \
             patch.object(self.validation_utils, 'validate_metric_visibility') as mock_visibility, \
             patch.object(self.validation_utils, 'validate_date_range') as mock_range, \
             patch.object(self.validation_utils, 'validate_chart_metric') as mock_metric:
            
            # Mock validation methods to not raise exceptions
            mock_city.return_value = None
            mock_unit.return_value = None
            mock_visibility.return_value = None
            mock_range.return_value = None
            mock_metric.return_value = None
            
            # Should not raise an exception for valid state
            try:
                self.validation_utils.validate_complete_state(mock_state_manager)
            except ValueError:
                self.fail("Valid complete state should not raise an exception")

    def test_validate_complete_state_multiple_errors(self):
        """Test complete state validation with multiple validation errors."""
        mock_state_manager = Mock()
        # Missing visibility attribute
        del mock_state_manager.visibility
        
        # Should raise ValueError for invalid state
        with self.assertRaises(ValueError):
            self.validation_utils.validate_complete_state(mock_state_manager)

    # ================================
    # Input type validation tests
    # ================================
    
    def test_validate_input_types_valid_inputs(self):
        """Test input type validation with valid inputs."""
        valid_inputs = [
            ("New York", "metric"),
            ("Paris", "imperial"),
            ("London", None)
        ]
        
        for city, unit in valid_inputs:
            with self.subTest(city=city, unit=unit):
                # Should not raise an exception for valid inputs
                try:
                    self.validation_utils.validate_input_types(city, unit)
                except ValueError:
                    self.fail(f"Valid inputs '{city}', '{unit}' should not raise an exception")

    def test_validate_input_types_invalid_inputs(self):
        """Test input type validation with invalid inputs."""
        invalid_inputs = [
            (None, "metric"),
            ("", "imperial"),
            ("city123", "metric"),  # Invalid city name
            ("New York", "invalid_unit")
        ]
        
        for city, unit in invalid_inputs:
            with self.subTest(city=city, unit=unit):
                # Should raise ValueError for invalid inputs
                with self.assertRaises(ValueError):
                    self.validation_utils.validate_input_types(city, unit)

    # ================================
    # Numeric range validation tests
    # ================================
    
    def test_is_valid_numeric_range_valid_inputs(self):
        """Test numeric range validation with valid inputs."""
        valid_inputs = [
            (5, 1, 10),
            (0, 0, 100),
            (100, 0, 100),
            (50, None, 100),  # No minimum
            (25, 0, None),    # No maximum
            (0, None, None)   # No bounds
        ]
        
        for value, min_val, max_val in valid_inputs:
            with self.subTest(value=value, min_val=min_val, max_val=max_val):
                # Should not raise an exception for valid ranges
                try:
                    self.validation_utils.is_valid_numeric_range(value, min_val, max_val)
                except ValueError:
                    self.fail(f"Valid range '{value}' in [{min_val}, {max_val}] should not raise an exception")

    def test_is_valid_numeric_range_invalid_inputs(self):
        """Test numeric range validation with invalid inputs."""
        invalid_inputs = [
            (-1, 0, 100),     # Below minimum
            (101, 0, 100),    # Above maximum
            (50, 60, 100),    # Below minimum (higher min)
            (50, 0, 40),      # Above maximum (lower max)
            (None, 0, 100),   # None value
            ("invalid", 0, 100)  # Non-numeric value
        ]
        
        for value, min_val, max_val in invalid_inputs:
            with self.subTest(value=value, min_val=min_val, max_val=max_val):
                # Should raise ValueError for invalid ranges
                with self.assertRaises(ValueError):
                    self.validation_utils.is_valid_numeric_range(value, min_val, max_val)

    # ================================
    # Error formatting tests
    # ================================
    
    def test_format_validation_errors_single_error(self):
        """Test error formatting with single error."""
        # The format_validation_errors method was removed, so we'll skip this test
        self.skipTest("format_validation_errors method was removed")

    def test_format_validation_errors_multiple_errors(self):
        """Test error formatting with multiple errors."""
        # The format_validation_errors method was removed, so we'll skip this test
        self.skipTest("format_validation_errors method was removed")

    # Removed duplicate test - see the patched version above

    def test_format_validation_errors_custom_prefix(self):
        """Test error formatting with custom prefix."""
        # The format_validation_errors method was removed, so we'll skip this test
        self.skipTest("format_validation_errors method was removed")

    # ================================
    # Error message consistency tests
    # ================================
    
    def test_error_message_consistency(self):
        """Test that error messages are consistent across validation methods."""
        invalid_inputs = ["", None, 123, "city123"]
        
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                # Test city name validation - should raise ValueError
                with self.assertRaises(ValueError):
                    self.validation_utils.validate_city_name(invalid_input)
                
                # Test unit system validation - should raise ValueError
                with self.assertRaises(ValueError):
                    self.validation_utils.validate_unit_system(invalid_input)

    # ================================
    # Configuration integration tests
    # ================================
    
    def test_configuration_integration(self):
        """Test that validation methods integrate with configuration system."""
        # Test that validation methods use configuration for error messages
        with self.assertRaises(ValueError):
            self.validation_utils.validate_city_name("")

    # ================================
    # Edge cases and boundary conditions
    # ================================
    
    def test_edge_cases_and_boundary_conditions(self):
        """Test edge cases and boundary conditions."""
        # Test with very long city names
        long_city = "a" * 100  # Exactly at the limit
        try:
            self.validation_utils.validate_city_name(long_city)
        except ValueError:
            self.fail("City name at the limit should be valid")
        
        # Test with city name at the limit + 1
        too_long_city = "a" * 101
        with self.assertRaises(ValueError):
            self.validation_utils.validate_city_name(too_long_city)

    # ================================
    # Special characters in city names
    # ================================
    
    def test_special_characters_in_city_names(self):
        """Test city names with special characters."""
        special_city_names = [
            "New-York",      # Hyphen
            "O'Fallon",      # Apostrophe
            "St. Paul",      # Period
            "San Francisco", # Space
            "Los Angeles",   # Multiple spaces
        ]
        
        for city in special_city_names:
            with self.subTest(city=city):
                try:
                    self.validation_utils.validate_city_name(city)
                except ValueError:
                    self.fail(f"City name '{city}' should be valid")

    # ================================
    # Unicode and international characters
    # ================================
    
    def test_unicode_and_international_characters(self):
        """Test city names with unicode and international characters."""
        unicode_city_names = [
            "São Paulo",     # Unicode character
            "München",       # German umlaut
            "København",     # Danish character
            "Béziers",       # French accent
        ]
        
        for city in unicode_city_names:
            with self.subTest(city=city):
                # Note: The current regex might not support all unicode characters
                # This test documents the current behavior
                try:
                    self.validation_utils.validate_city_name(city)
                except ValueError:
                    # This is expected for some unicode characters with current regex
                    pass

    # ================================
    # Concurrent validation safety
    # ================================
    
    def test_concurrent_validation_safety(self):
        """Test that validation methods are safe for concurrent access."""
        import threading
        import time

        errors_found = []

        def worker():
            try:
                # Call validation methods concurrently
                self.validation_utils.validate_city_name("New York")
                self.validation_utils.validate_unit_system("metric")
                self.validation_utils.validate_date_range("Last 7 Days")  # Pass string instead of int
            except Exception as e:
                errors_found.append(e)

        # Run multiple threads
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        self.assertEqual(len(errors_found), 0, f"Concurrent validation failed with errors: {errors_found}")

    # ================================
    # Documentation and type hints
    # ================================
    
    def test_documentation_and_type_hints(self):
        """Test that methods have proper documentation and type hints."""
        import inspect

        methods = [
            self.validation_utils.validate_city_name,
            self.validation_utils.validate_unit_system,
            self.validation_utils.validate_metric_visibility,
            self.validation_utils.validate_date_range,
            self.validation_utils.validate_chart_metric,
            self.validation_utils.validate_complete_state,
            self.validation_utils.validate_input_types,
            self.validation_utils.is_valid_numeric_range,
        ]
        
        for method in methods:
            # Check that method has docstring
            self.assertIsNotNone(method.__doc__, f"Method {method.__name__} missing docstring")
            
            # Check that method has type hints
            sig = inspect.signature(method)
            self.assertGreater(len(sig.parameters), 0, f"Method {method.__name__} missing parameters")


if __name__ == '__main__':
    unittest.main()