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
                errors = ValidationUtils.validate_city_name(city_name)
                self.assertEqual(errors, [], f"Valid city '{city_name}' should have no validation errors")

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
                errors = ValidationUtils.validate_city_name(invalid_input)
                self.assertGreater(len(errors), 0, f"Invalid input '{invalid_input}' should have validation errors")
                # Check that the error message contains expected part
                error_text = " ".join(str(error) for error in errors).lower()
                self.assertIn(expected_error_part.lower(), error_text)

    # ================================
    # Unit system validation tests
    # ================================
    
    def test_validate_unit_system_valid_inputs(self):
        """Test unit system validation with valid inputs."""
        valid_systems = ["metric", "imperial"]
        
        for system in valid_systems:
            with self.subTest(system=system):
                errors = ValidationUtils.validate_unit_system(system)
                self.assertEqual(errors, [], f"Valid unit system '{system}' should have no validation errors")

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
            ([], "must be a string")
        ]
        
        for invalid_input, expected_error_part in invalid_inputs:
            with self.subTest(input=invalid_input):
                errors = ValidationUtils.validate_unit_system(invalid_input)
                self.assertGreater(len(errors), 0, f"Invalid input '{invalid_input}' should have validation errors")
                error_text = " ".join(str(error) for error in errors).lower()
                self.assertIn(expected_error_part.lower(), error_text)

    # ================================
    # Metric visibility validation tests
    # ================================
    
    def test_validate_metric_visibility_valid_state(self):
        """Test metric visibility validation with valid state manager."""
        # Create mock state manager with proper visibility
        mock_state = Mock()
        mock_var1 = Mock()
        mock_var1.get.return_value = True
        mock_var2 = Mock()
        mock_var2.get.return_value = False
        mock_var3 = Mock()
        mock_var3.get.return_value = True
        
        mock_state.visibility = {
            'temperature': mock_var1,
            'humidity': mock_var2,
            'pressure': mock_var3
        }
        
        errors = ValidationUtils.validate_metric_visibility(mock_state)
        self.assertEqual(errors, [], "Valid state with visible metrics should have no errors")

    def test_validate_metric_visibility_no_visible_metrics(self):
        """Test metric visibility validation when no metrics are visible."""
        # Create mock state manager with all metrics invisible
        mock_state = Mock()
        mock_var1 = Mock()
        mock_var1.get.return_value = False
        mock_var2 = Mock()
        mock_var2.get.return_value = False
        
        mock_state.visibility = {
            'temperature': mock_var1,
            'humidity': mock_var2
        }
        
        errors = ValidationUtils.validate_metric_visibility(mock_state)
        self.assertGreater(len(errors), 0, "State with no visible metrics should have validation errors")
        error_text = " ".join(str(error) for error in errors).lower()
        self.assertIn("at least one metric must be visible", error_text)

    def test_validate_metric_visibility_missing_attribute(self):
        """Test metric visibility validation when state manager missing visibility."""
        mock_state = Mock()
        del mock_state.visibility  # Remove visibility attribute
        
        errors = ValidationUtils.validate_metric_visibility(mock_state)
        self.assertGreater(len(errors), 0, "State without visibility should have validation errors")
        error_text = " ".join(str(error) for error in errors).lower()
        self.assertIn("missing visibility attribute", error_text)

    # ================================
    # Date range validation tests
    # ================================
    
    @patch('WeatherDashboard.utils.validation_utils.config')
    def test_validate_date_range_valid_inputs(self, mock_config):
        """Test date range validation with valid inputs."""
        mock_config.CHART = {
            "range_options": {
                "Last 7 Days": 7,
                "Last 30 Days": 30,
                "Last 90 Days": 90
            }
        }
        
        valid_ranges = ["Last 7 Days", "Last 30 Days", "Last 90 Days"]
        
        for date_range in valid_ranges:
            with self.subTest(range=date_range):
                errors = ValidationUtils.validate_date_range(date_range)
                self.assertEqual(errors, [], f"Valid date range '{date_range}' should have no validation errors")

    @patch('WeatherDashboard.utils.validation_utils.config')
    def test_validate_date_range_invalid_inputs(self, mock_config):
        """Test date range validation with invalid inputs."""
        mock_config.CHART = {
            "range_options": {
                "Last 7 Days": 7,
                "Last 30 Days": 30
            }
        }
        # Mock the ERROR_MESSAGES properly
        mock_config.ERROR_MESSAGES = {
            'validation': "{field} is invalid: {reason}",
            'not_found': "{resource} '{name}' not found"
        }
        
        invalid_inputs = [
            ("", "not a valid option"),
            ("Last 60 Days", "not a valid option"),
            ("Invalid Range", "not a valid option"),
            (None, "must be a string"),
            (123, "must be a string")
        ]
        
        for invalid_input, expected_error_part in invalid_inputs:
            with self.subTest(input=invalid_input):
                errors = ValidationUtils.validate_date_range(invalid_input)
                self.assertGreater(len(errors), 0, f"Invalid input '{invalid_input}' should have validation errors")
                error_text = " ".join(str(error) for error in errors).lower()
                self.assertIn(expected_error_part.lower(), error_text)

    # ================================
    # Chart metric validation tests
    # ================================
    
    @patch('WeatherDashboard.utils.validation_utils.config')
    def test_validate_chart_metric_valid_inputs(self, mock_config):
        """Test chart metric validation with valid inputs."""
        mock_config.METRICS = {
            "temperature": {"chartable": True, "label": "Temperature"},
            "humidity": {"chartable": True, "label": "Humidity"},
            "conditions": {"chartable": False, "label": "Conditions"}
        }
        
        valid_metrics = ["Temperature", "Humidity"]  # Using labels, not keys
        
        for metric in valid_metrics:
            with self.subTest(metric=metric):
                errors = ValidationUtils.validate_chart_metric(metric)
                self.assertEqual(errors, [], f"Valid chart metric '{metric}' should have no validation errors")

    @patch('WeatherDashboard.utils.validation_utils.config')
    def test_validate_chart_metric_invalid_inputs(self, mock_config):
        """Test chart metric validation with invalid inputs."""
        mock_config.METRICS = {
            "temperature": {"chartable": True, "label": "Temperature"},
            "conditions": {"chartable": False, "label": "Conditions"}
        }
        # Mock the ERROR_MESSAGES properly
        mock_config.ERROR_MESSAGES = {
            'validation': "{field} is invalid: {reason}",
            'not_found': "{resource} '{name}' not found"
        }
        
        invalid_inputs = [
            ("No metrics selected", "at least one metric must be selected"),
            ("Invalid Metric", "not found"),
            ("", "not found"),
            (None, "must be a string"),
            (123, "must be a string")
        ]
        
        for invalid_input, expected_error_part in invalid_inputs:
            with self.subTest(input=invalid_input):
                errors = ValidationUtils.validate_chart_metric(invalid_input)
                self.assertGreater(len(errors), 0, f"Invalid input '{invalid_input}' should have validation errors")
                error_text = " ".join(str(error) for error in errors).lower()
                self.assertIn(expected_error_part.lower(), error_text)

    # ================================
    # Complete state validation tests
    # ================================
    
    def test_validate_complete_state_valid_state(self):
        """Test complete state validation with valid state manager."""
        # Create comprehensive mock state manager
        mock_state = Mock()
        
        # Mock all the getter methods
        mock_state.get_current_city.return_value = "New York"
        mock_state.get_current_unit_system.return_value = "metric"
        mock_state.get_current_range.return_value = "Last 7 Days"
        mock_state.get_current_chart_metric.return_value = "Temperature"
        
        # Mock visibility with at least one visible metric
        mock_var = Mock()
        mock_var.get.return_value = True
        mock_state.visibility = {'temperature': mock_var}
        
        with patch('WeatherDashboard.utils.validation_utils.config') as mock_config:
            mock_config.CHART = {"range_options": {"Last 7 Days": 7}}
            mock_config.METRICS = {"temperature": {"label": "Temperature"}}
            
            errors = ValidationUtils.validate_complete_state(mock_state)
            self.assertEqual(errors, [], "Valid complete state should have no validation errors")

    def test_validate_complete_state_multiple_errors(self):
        """Test complete state validation with multiple validation errors."""
        # Create mock state manager with multiple invalid values
        mock_state = Mock()
        
        mock_state.get_current_city.return_value = ""  # Invalid city
        mock_state.get_current_unit_system.return_value = "invalid"  # Invalid unit
        mock_state.get_current_range.return_value = "Invalid Range"  # Invalid range
        mock_state.get_current_chart_metric.return_value = "No metrics selected"  # Invalid metric
        
        # Mock visibility with no visible metrics
        mock_var = Mock()
        mock_var.get.return_value = False
        mock_state.visibility = {'temperature': mock_var}
        
        with patch('WeatherDashboard.utils.validation_utils.config') as mock_config:
            mock_config.CHART = {"range_options": {"Last 7 Days": 7}}
            mock_config.METRICS = {"temperature": {"label": "Temperature"}}
            
            errors = ValidationUtils.validate_complete_state(mock_state)
            self.assertGreater(len(errors), 3, "State with multiple issues should have multiple validation errors")

    # ================================
    # Input type validation tests
    # ================================
    
    def test_validate_input_types_valid_inputs(self):
        """Test input type validation with valid inputs."""
        valid_combinations = [
            ("New York", "metric"),
            ("London", "imperial"),
            ("Paris", None)  # Unit system optional
        ]
        
        for city, unit in valid_combinations:
            with self.subTest(city=city, unit=unit):
                errors = ValidationUtils.validate_input_types(city, unit)
                self.assertEqual(errors, [], f"Valid inputs ('{city}', '{unit}') should have no validation errors")

    def test_validate_input_types_invalid_inputs(self):
        """Test input type validation with invalid inputs."""
        invalid_combinations = [
            ("", "metric", "cannot be empty"),  # Invalid city
            ("New York", "invalid", "invalid"),  # Invalid unit
            (None, "metric", "must be a string"),  # Invalid city type
        ]
        
        for city, unit, expected_error_part in invalid_combinations:
            with self.subTest(city=city, unit=unit):
                errors = ValidationUtils.validate_input_types(city, unit)
                self.assertGreater(len(errors), 0, f"Invalid inputs should have validation errors")
                error_text = " ".join(str(error) for error in errors).lower()
                self.assertIn(expected_error_part.lower(), error_text)

    # ================================
    # Numeric range validation tests
    # ================================
    
    def test_is_valid_numeric_range_valid_inputs(self):
        """Test numeric range validation with valid inputs."""
        valid_cases = [
            (25, 0, 50),      # Integer in range
            (25.5, 0.0, 50.0), # Float in range
            (0, 0, 50),       # At minimum
            (50, 0, 50),      # At maximum
            (25, None, 50),   # No minimum
            (25, 0, None),    # No maximum
            (25, None, None)  # No limits
        ]
        
        for value, min_val, max_val in valid_cases:
            with self.subTest(value=value, min_val=min_val, max_val=max_val):
                errors = ValidationUtils.is_valid_numeric_range(value, min_val, max_val)
                self.assertEqual(errors, [], f"Valid numeric value {value} should have no validation errors")

    def test_is_valid_numeric_range_invalid_inputs(self):
        """Test numeric range validation with invalid inputs."""
        invalid_cases = [
            ("25", 0, 50, "must be a number"),     # String
            (75, 0, 50, "must be <= 50"),          # Too high
            (-5, 0, 50, "must be >= 0"),           # Too low
            (None, 0, 50, "must be a number"),     # None
            ([], 0, 50, "must be a number"),       # List
        ]
        
        for value, min_val, max_val, expected_error_part in invalid_cases:
            with self.subTest(value=value, min_val=min_val, max_val=max_val):
                errors = ValidationUtils.is_valid_numeric_range(value, min_val, max_val)
                self.assertGreater(len(errors), 0, f"Invalid numeric value should have validation errors")
                error_text = " ".join(str(error) for error in errors).lower()
                self.assertIn(expected_error_part.lower(), error_text)

    # ================================
    # Error formatting tests
    # ================================
    
    def test_format_validation_errors_single_error(self):
        """Test formatting of single validation error."""
        errors = ["City name cannot be empty"]
        result = ValidationUtils.format_validation_errors(errors)
        expected = "Validation failed: City name cannot be empty"
        self.assertEqual(result, expected)

    def test_format_validation_errors_multiple_errors(self):
        """Test formatting of multiple validation errors."""
        errors = [
            "City name cannot be empty",
            "Unit system is invalid",
            "No metrics are visible"
        ]
        result = ValidationUtils.format_validation_errors(errors)
        expected = "Validation failed: City name cannot be empty; Unit system is invalid; No metrics are visible"
        self.assertEqual(result, expected)

    def test_format_validation_errors_empty_list(self):
        """Test formatting of empty error list."""
        errors = []
        result = ValidationUtils.format_validation_errors(errors)
        self.assertEqual(result, "")

    def test_format_validation_errors_custom_prefix(self):
        """Test formatting with custom prefix."""
        errors = ["Test error"]
        result = ValidationUtils.format_validation_errors(errors, "Custom prefix")
        expected = "Custom prefix: Test error"
        self.assertEqual(result, expected)

    # ================================
    # Integration and edge case tests
    # ================================
    
    def test_error_message_consistency(self):
        """Test that error messages are consistent and informative."""
        # Test various validation methods with invalid inputs
        test_cases = [
            (ValidationUtils.validate_city_name, [None]),
            (ValidationUtils.validate_unit_system, [None]),
            (ValidationUtils.validate_date_range, [None]),
            (ValidationUtils.validate_chart_metric, [None])
        ]
        
        for method, args in test_cases:
            with self.subTest(method=method.__name__):
                errors = method(*args)
                self.assertGreater(len(errors), 0, f"Method {method.__name__} should return validation errors")
                # All error messages should be informative
                for error in errors:
                    self.assertIsInstance(error, str)
                    self.assertGreater(len(error), 10, "Error messages should be descriptive")

    def test_configuration_integration(self):
        """Test integration with configuration system."""
        with patch('WeatherDashboard.utils.validation_utils.config') as mock_config:
            # Test that validation methods properly access configuration
            mock_config.CHART = {"range_options": {"Test Range": 7}}
            mock_config.METRICS = {"test_metric": {"label": "Test Metric"}}
            mock_config.ERROR_MESSAGES = {
                'validation': "{field} is invalid: {reason}",
                'not_found': "{resource} '{name}' not found"
            }
            
            # Should use config for validation
            errors = ValidationUtils.validate_date_range("Test Range")
            self.assertEqual(errors, [], "Valid config-based range should pass validation")
            
            errors = ValidationUtils.validate_chart_metric("Test Metric")
            self.assertEqual(errors, [], "Valid config-based metric should pass validation")

    def test_edge_cases_and_boundary_conditions(self):
        """Test edge cases and boundary conditions."""
        # Test boundary length for city names
        short_city = "ABC"  # Should be valid according to your regex
        errors = ValidationUtils.validate_city_name(short_city)
        self.assertEqual(errors, [], "3-character city should be valid")
        
        # Test single character (should be valid based on your regex)
        single_char = "A"
        errors = ValidationUtils.validate_city_name(single_char)
        self.assertEqual(errors, [], "Single character should be valid based on regex pattern")
        
        long_city = "A" * 100  # Maximum length
        errors = ValidationUtils.validate_city_name(long_city)
        self.assertEqual(errors, [], "100-character city should be valid")
        
        too_long_city = "A" * 101  # Over maximum
        errors = ValidationUtils.validate_city_name(too_long_city)
        self.assertGreater(len(errors), 0, "101-character city should be invalid")

    def test_special_characters_in_city_names(self):
        """Test handling of special characters in city names."""
        valid_special_cities = [
            "Saint-Jean-sur-Richelieu",  # Hyphens
            "O'Fallon",                  # Apostrophe
            "Washington, D.C.",          # Comma and periods
        ]
        
        for city in valid_special_cities:
            with self.subTest(city=city):
                errors = ValidationUtils.validate_city_name(city)
                self.assertEqual(errors, [], f"City with special characters '{city}' should be valid")
        
        invalid_special_cities = [
            "City@Domain",    # @ symbol
            "City123",        # Numbers
            "City#Tag",       # Hash symbol
            "City$Money"      # Dollar sign
        ]
        
        for city in invalid_special_cities:
            with self.subTest(city=city):
                errors = ValidationUtils.validate_city_name(city)
                self.assertGreater(len(errors), 0, f"City with invalid characters '{city}' should be invalid")

    def test_unicode_and_international_characters(self):
        """Test handling of Unicode and international characters."""
        # These should be invalid based on your regex pattern
        international_cities = [
            "München",        # German umlaut
            "São Paulo",      # Portuguese
            "Москва",         # Russian
            "北京"            # Chinese
        ]
        
        for city in international_cities:
            with self.subTest(city=city):
                errors = ValidationUtils.validate_city_name(city)
                # Based on your regex, these should fail (only ASCII letters allowed)
                self.assertGreater(len(errors), 0, f"Non-ASCII city '{city}' should be invalid with current regex")

    def test_concurrent_validation_safety(self):
        """Test that validation functions are safe for concurrent use."""
        import threading
        import time
        
        results = []
        errors_found = []
        
        def worker():
            try:
                for i in range(50):
                    # Test various validation functions
                    city_errors = ValidationUtils.validate_city_name(f"TestCity{i}")
                    unit_errors = ValidationUtils.validate_unit_system("metric")
                    
                    results.append((len(city_errors), len(unit_errors)))
                    time.sleep(0.001)  # Small delay to increase chance of race conditions
                    
            except Exception as e:
                errors_found.append(e)
        
        # Run multiple threads
        threads = []
        for _ in range(3):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        # Should complete without errors
        self.assertEqual(len(errors_found), 0, f"Concurrent validation failed with errors: {errors_found}")
        self.assertEqual(len(results), 150)  # 3 threads * 50 operations


if __name__ == '__main__':
    unittest.main()