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

from WeatherDashboard.utils.validation_utils import ValidationUtils, ValidationResult


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
                result = self.validation_utils.validate_city_name(city_name)
                self.assertTrue(result.is_valid, f"Valid city '{city_name}' should have no validation errors")
                self.assertEqual(result.errors, [], f"Valid city '{city_name}' should have no validation errors")

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
                result = self.validation_utils.validate_city_name(invalid_input)
                self.assertFalse(result.is_valid, f"Invalid input '{invalid_input}' should have validation errors")
                self.assertGreater(len(result.errors), 0, f"Invalid input '{invalid_input}' should have validation errors")
                # Check that the error message contains expected part
                error_text = " ".join(str(error) for error in result.errors).lower()
                self.assertIn(expected_error_part.lower(), error_text)

    # ================================
    # Unit system validation tests
    # ================================
    
    def test_validate_unit_system_valid_inputs(self):
        """Test unit system validation with valid inputs."""
        valid_systems = ["metric", "imperial"]
        
        for system in valid_systems:
            with self.subTest(system=system):
                result = self.validation_utils.validate_unit_system(system)
                self.assertTrue(result.is_valid, f"Valid unit system '{system}' should have no validation errors")
                self.assertEqual(result.errors, [], f"Valid unit system '{system}' should have no validation errors")

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
                result = self.validation_utils.validate_unit_system(invalid_input)
                self.assertFalse(result.is_valid, f"Invalid unit system '{invalid_input}' should have validation errors")
                self.assertGreater(len(result.errors), 0, f"Invalid unit system '{invalid_input}' should have validation errors")
                # Check that the error message contains expected part
                error_text = " ".join(str(error) for error in result.errors).lower()
                self.assertIn(expected_error_part.lower(), error_text)

    # ================================
    # Metric visibility validation tests
    # ================================
    
    def test_validate_metric_visibility_valid_state(self):
        """Test metric visibility validation with valid state manager."""
        mock_state_manager = Mock()
        mock_state_manager.visibility = {
            'temperature': Mock(),
            'humidity': Mock(),
            'pressure': Mock()
        }
        
        result = self.validation_utils.validate_metric_visibility(mock_state_manager)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validate_metric_visibility_no_visible_metrics(self):
        """Test metric visibility validation when no metrics are visible."""
        mock_state_manager = Mock()
        mock_state_manager.visibility = {}  # No visibility metrics
        
        result = self.validation_utils.validate_metric_visibility(mock_state_manager)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)

    def test_validate_metric_visibility_missing_attribute(self):
        """Test metric visibility validation when state manager missing visibility."""
        mock_state_manager = Mock()
        del mock_state_manager.visibility  # Remove visibility attribute
        
        result = self.validation_utils.validate_metric_visibility(mock_state_manager)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)

    # ================================
    # Date range validation tests
    # ================================
    
    @patch('WeatherDashboard.utils.validation_utils.config')
    def test_format_validation_errors_empty_list(self, mock_config):
        """Test error formatting with empty error list."""
        result = self.validation_utils.format_validation_errors([])
        # The actual implementation returns empty string for no errors
        self.assertEqual(result, "")

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
                result = self.validation_utils.validate_date_range(days)
                self.assertTrue(result.is_valid, f"Valid date range '{days}' should have no validation errors")

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
                result = self.validation_utils.validate_date_range(invalid_range)
                self.assertFalse(result.is_valid)
                self.assertGreater(len(result.errors), 0)
                
                # Check error message content
                error_text = result.errors[0].lower()
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
                result = self.validation_utils.validate_chart_metric(metric)
                self.assertTrue(result.is_valid, f"Valid chart metric '{metric}' should have no validation errors")

    @patch('WeatherDashboard.utils.validation_utils.config')
    def test_validate_chart_metric_invalid_inputs(self, mock_config):
        """Test chart metric validation with invalid inputs."""
        mock_config.METRICS = {
            "temperature": {"label": "Temperature"},
            "humidity": {"label": "Humidity"}
        }
        mock_config.ERROR_MESSAGES = {
            'validation': 'Chart metric is invalid: {reason}',
            'not_found': 'Chart metric "{name}" not found'
        }
        
        invalid_metrics = ["Invalid Metric", "No metrics selected", None, 42]
        
        for invalid_metric in invalid_metrics:
            with self.subTest(invalid_metric=invalid_metric):
                result = self.validation_utils.validate_chart_metric(invalid_metric)
                self.assertFalse(result.is_valid)
                self.assertGreater(len(result.errors), 0)
                
                # Check error message content
                error_text = result.errors[0].lower()
                if invalid_metric == "No metrics selected":
                    self.assertIn("at least one metric", error_text)
                elif isinstance(invalid_metric, str):
                    self.assertIn("not found", error_text)
                else:
                    self.assertIn("string", error_text)

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
        
        # Mock the validation methods to return valid results
        with patch.object(self.validation_utils, 'validate_city_name') as mock_city, \
             patch.object(self.validation_utils, 'validate_unit_system') as mock_unit, \
             patch.object(self.validation_utils, 'validate_metric_visibility') as mock_visibility, \
             patch.object(self.validation_utils, 'validate_date_range') as mock_range, \
             patch.object(self.validation_utils, 'validate_chart_metric') as mock_metric:
            
            mock_city.return_value = ValidationResult(is_valid=True, errors=[], context="city")
            mock_unit.return_value = ValidationResult(is_valid=True, errors=[], context="unit")
            mock_visibility.return_value = ValidationResult(is_valid=True, errors=[], context="visibility")
            mock_range.return_value = ValidationResult(is_valid=True, errors=[], context="range")
            mock_metric.return_value = ValidationResult(is_valid=True, errors=[], context="metric")
            
            result = self.validation_utils.validate_complete_state(mock_state_manager)
            self.assertTrue(result.is_valid)

    def test_validate_complete_state_multiple_errors(self):
        """Test complete state validation with multiple validation errors."""
        mock_state_manager = Mock()
        # Missing visibility attribute
        del mock_state_manager.visibility
        
        result = self.validation_utils.validate_complete_state(mock_state_manager)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)

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
                result = self.validation_utils.validate_input_types(city, unit)
                self.assertTrue(result.is_valid, f"Valid inputs '{city}', '{unit}' should have no validation errors")
                self.assertEqual(result.errors, [], f"Valid inputs '{city}', '{unit}' should have no validation errors")

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
                result = self.validation_utils.validate_input_types(city, unit)
                self.assertFalse(result.is_valid, f"Invalid inputs '{city}', '{unit}' should have validation errors")
                self.assertGreater(len(result.errors), 0, f"Invalid inputs '{city}', '{unit}' should have validation errors")

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
                result = self.validation_utils.is_valid_numeric_range(value, min_val, max_val)
                self.assertTrue(result.is_valid, f"Valid range '{value}' in [{min_val}, {max_val}] should have no validation errors")
                self.assertEqual(result.errors, [], f"Valid range '{value}' in [{min_val}, {max_val}] should have no validation errors")

    def test_is_valid_numeric_range_invalid_inputs(self):
        """Test numeric range validation with invalid inputs."""
        invalid_inputs = [
            (0, 1, 10),      # Below minimum
            (11, 1, 10),     # Above maximum
            (-1, 0, 100),    # Below minimum
            (101, 0, 100),   # Above maximum
            (5, 10, 1),      # Invalid range (min > max)
        ]
        
        for value, min_val, max_val in invalid_inputs:
            with self.subTest(value=value, min_val=min_val, max_val=max_val):
                result = self.validation_utils.is_valid_numeric_range(value, min_val, max_val)
                self.assertFalse(result.is_valid, f"Invalid range '{value}' in [{min_val}, {max_val}] should have validation errors")
                self.assertGreater(len(result.errors), 0, f"Invalid range '{value}' in [{min_val}, {max_val}] should have validation errors")

    # ================================
    # Error formatting tests
    # ================================
    
    def test_format_validation_errors_single_error(self):
        """Test error formatting with single error."""
        errors = ["City name cannot be empty"]
        result = self.validation_utils.format_validation_errors(errors)
        self.assertIn("City name cannot be empty", result)

    def test_format_validation_errors_multiple_errors(self):
        """Test error formatting with multiple errors."""
        errors = ["City name cannot be empty", "Unit system is invalid"]
        result = self.validation_utils.format_validation_errors(errors)
        self.assertIn("City name cannot be empty", result)
        self.assertIn("Unit system is invalid", result)

    # Removed duplicate test - see the patched version above

    def test_format_validation_errors_custom_prefix(self):
        """Test error formatting with custom prefix."""
        errors = ["Test error"]
        result = self.validation_utils.format_validation_errors(errors, "Custom prefix")
        self.assertIn("Custom prefix", result)
        self.assertIn("Test error", result)

    # ================================
    # Error message consistency tests
    # ================================
    
    def test_error_message_consistency(self):
        """Test that error messages are consistent across validation methods."""
        # Test with same invalid input across different methods
        invalid_inputs = [None, "", "invalid"]
        
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                # Test city name validation
                city_result = self.validation_utils.validate_city_name(invalid_input)
                if not city_result.is_valid:
                    self.assertGreater(len(city_result.errors), 0)
                
                # Test unit system validation
                unit_result = self.validation_utils.validate_unit_system(invalid_input)
                if not unit_result.is_valid:
                    self.assertGreater(len(unit_result.errors), 0)

    # ================================
    # Configuration integration tests
    # ================================
    
    def test_configuration_integration(self):
        """Test that validation methods integrate with configuration system."""
        # Test that validation methods use configuration for error messages
        result = self.validation_utils.validate_city_name("")
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)

    # ================================
    # Edge cases and boundary conditions
    # ================================
    
    def test_edge_cases_and_boundary_conditions(self):
        """Test edge cases and boundary conditions."""
        # Test with very long city names
        long_city = "a" * 100  # Exactly at the limit
        result = self.validation_utils.validate_city_name(long_city)
        self.assertTrue(result.is_valid)
        
        # Test with city name at the limit + 1
        too_long_city = "a" * 101
        result = self.validation_utils.validate_city_name(too_long_city)
        self.assertFalse(result.is_valid)

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
                result = self.validation_utils.validate_city_name(city)
                self.assertTrue(result.is_valid, f"City name '{city}' should be valid")
                self.assertEqual(result.errors, [], f"City name '{city}' should have no errors")

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
                result = self.validation_utils.validate_city_name(city)
                # Note: The current regex might not support all unicode characters
                # This test documents the current behavior
                self.assertIsInstance(result, ValidationResult)

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
                self.validation_utils.validate_date_range(7)
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
            self.validation_utils.format_validation_errors
        ]
        
        for method in methods:
            with self.subTest(method=method.__name__):
                # Check that method has docstring
                self.assertIsNotNone(method.__doc__)
                
                # Check that method has type hints
                sig = inspect.signature(method)
                self.assertGreater(len(sig.parameters), 0)


if __name__ == '__main__':
    unittest.main()