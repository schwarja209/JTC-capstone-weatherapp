"""
Unit tests for utility functions in utils.py module.

Tests the three utility functions:
- is_fallback: Check if weather data is from fallback source
- format_fallback_status: Format status messages for fallback data  
- city_key: Generate consistent city keys for data storage

Focus is on testing the actual behavior of these utilities, not the
underlying validation logic which is tested separately.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, Mock
from WeatherDashboard.utils.utils import Utils

class TestUtils(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.utils = Utils()
    
    # ================================
    # is_fallback() function tests
    # ================================
    
    def test_is_fallback_with_simulated_data(self):
        """Test is_fallback returns True for simulated data."""
        fallback_data = {"source": "simulated", "temperature": 25, "humidity": 60}
        self.assertTrue(self.utils.is_fallback(fallback_data))
    
    def test_is_fallback_with_live_data(self):
        """Test is_fallback returns False for live data.""" 
        live_data = {"source": "api", "temperature": 25, "humidity": 60}
        self.assertFalse(self.utils.is_fallback(live_data))
        
        # Test other non-simulated sources
        other_sources = ["weather_service", "manual", "cached"]
        for source in other_sources:
            with self.subTest(source=source):
                data = {"source": source, "temperature": 25}
                self.assertFalse(self.utils.is_fallback(data))
    
    def test_is_fallback_with_missing_source(self):
        """Test is_fallback returns False when source key is missing."""
        no_source_data = {"temperature": 25, "humidity": 60}
        self.assertFalse(self.utils.is_fallback(no_source_data))
    
    def test_is_fallback_with_none_source(self):
        """Test is_fallback returns False when source is None."""
        none_source_data = {"source": None, "temperature": 25}
        self.assertFalse(self.utils.is_fallback(none_source_data))
    
    def test_is_fallback_with_empty_dict(self):
        """Test is_fallback returns False with empty dictionary."""
        self.assertFalse(self.utils.is_fallback({}))
    
    def test_is_fallback_case_sensitivity(self):
        """Test is_fallback is case sensitive for 'simulated'."""
        case_variations = [
            {"source": "Simulated"},
            {"source": "SIMULATED"}, 
            {"source": "Simulated_data"},
            {"source": "simulated_data"}
        ]
        
        for data in case_variations:
            with self.subTest(source=data["source"]):
                self.assertFalse(self.utils.is_fallback(data))
    
    # ================================
    # format_fallback_status() function tests
    # ================================
    
    def test_format_fallback_status_display_mode(self):
        """Test fallback status formatting in display mode."""
        test_cases = [
            (True, "display", "(Simulated)"),
            (False, "display", ""),
        ]
        
        for is_fallback_flag, mode, expected in test_cases:
            with self.subTest(fallback=is_fallback_flag, mode=mode):
                result = self.utils.format_fallback_status(is_fallback_flag, mode)
                self.assertEqual(result, expected)
    
    def test_format_fallback_status_log_mode(self):
        """Test fallback status formatting in log mode."""
        test_cases = [
            (True, "log", "Simulated"),
            (False, "log", "Live"),
        ]
        
        for is_fallback_flag, mode, expected in test_cases:
            with self.subTest(fallback=is_fallback_flag, mode=mode):
                result = self.utils.format_fallback_status(is_fallback_flag, mode)
                self.assertEqual(result, expected)
    
    def test_format_fallback_status_default_mode(self):
        """Test fallback status formatting with default mode."""
        # Default should be "display" mode
        result_true = self.utils.format_fallback_status(True)
        result_false = self.utils.format_fallback_status(False)
        
        self.assertEqual(result_true, "(Simulated)")
        self.assertEqual(result_false, "")
    
    def test_format_fallback_status_invalid_mode(self):
        """Test fallback status formatting with invalid mode."""
        invalid_modes = ["invalid", "DISPLAY", "LOG", "", None, 123, []]
        
        for invalid_mode in invalid_modes:
            with self.subTest(mode=invalid_mode):
                with self.assertRaises(ValueError) as context:
                    self.utils.format_fallback_status(True, invalid_mode)
                
                # Verify error message mentions the invalid format type
                error_msg = str(context.exception)
                self.assertIn("invalid", error_msg.lower())
    
    def test_format_fallback_status_boolean_coercion(self):
        """Test fallback status formatting with various truthy/falsy values."""
        # Test truthy values
        truthy_values = [1, "true", [1], {"a": 1}, "non-empty"]
        for truthy in truthy_values:
            with self.subTest(truthy=truthy):
                result = self.utils.format_fallback_status(truthy, "display")
                self.assertEqual(result, "(Simulated)")
        
        # Test falsy values
        falsy_values = [0, "", [], {}, None]
        for falsy in falsy_values:
            with self.subTest(falsy=falsy):
                result = self.utils.format_fallback_status(falsy, "display")
                self.assertEqual(result, "")
    
    # ================================
    # city_key() function tests
    # ================================
    
    @patch('WeatherDashboard.utils.utils.ValidationUtils.validate_city_name')
    def test_city_key_with_valid_cities(self, mock_validate):
        """Test city key generation with valid city names."""
        # Mock validation to return no errors (empty list)
        mock_validate.return_value = []
        
        test_cases = [
            ("New York", "new_york"),
            ("San Francisco", "san_francisco"),
            ("LONDON", "london"),
            ("Los-Angeles", "los-angeles"),
            ("Saint Paul", "saint_paul"),
            ("O'Fallon", "o'fallon"),
            ("Chicago", "chicago")
        ]
        
        for city_name, expected_key in test_cases:
            with self.subTest(city=city_name):
                result = self.utils.city_key(city_name)
                self.assertEqual(result, expected_key)
                mock_validate.assert_called_with(city_name)
    
    @patch('WeatherDashboard.utils.utils.ValidationUtils.validate_city_name')
    def test_city_key_validation_error_handling(self, mock_validate):
        """Test city key generation when validation fails."""
        # Mock validation to return an error
        mock_validate.return_value = ["City name is invalid: test error"]
        
        with self.assertRaises(ValueError) as context:
            self.utils.city_key("Invalid City")
        
        # Should raise the first validation error
        self.assertEqual(str(context.exception), "City name is invalid: test error")
        mock_validate.assert_called_once_with("Invalid City")
    
    @patch('WeatherDashboard.utils.utils.ValidationUtils.validate_city_name')
    def test_city_key_multiple_validation_errors(self, mock_validate):
        """Test city key generation with multiple validation errors."""
        # Mock validation to return multiple errors
        mock_validate.return_value = [
            "City name is invalid: too short",
            "City name is invalid: contains numbers"
        ]
        
        with self.assertRaises(ValueError) as context:
            self.utils.city_key("Bad123")
        
        # Should raise the first error only
        self.assertEqual(str(context.exception), "City name is invalid: too short")
    
    @patch('WeatherDashboard.utils.utils.ValidationUtils.validate_city_name')
    def test_city_key_normalization_behavior(self, mock_validate):
        """Test city key normalization behavior."""
        mock_validate.return_value = []
        
        # Test that the function handles the normalization correctly
        test_cases = [
            ("  New York  ", "new_york"),  # Should strip and normalize
            ("UPPER CASE", "upper_case"),  # Should lowercase
            ("Mixed-Case City", "mixed-case_city"),  # Should preserve hyphens, convert spaces
        ]
        
        for input_city, expected_key in test_cases:
            with self.subTest(input=input_city):
                result = self.utils.city_key(input_city)
                self.assertEqual(result, expected_key)
    
    @patch('WeatherDashboard.utils.utils.ValidationUtils.validate_city_name')
    def test_city_key_special_character_handling(self, mock_validate):
        """Test city key handling of special characters."""
        mock_validate.return_value = []
        
        test_cases = [
            ("City-with-Hyphens", "city-with-hyphens"),    # Preserve hyphens
            ("City with Spaces", "city_with_spaces"),       # Convert spaces to underscores
            ("City's Name", "city's_name"),                 # Preserve apostrophes
            ("Multi  Space  City", "multi__space__city"),   # Multiple spaces become multiple underscores
        ]
        
        for city_name, expected_key in test_cases:
            with self.subTest(city=city_name):
                result = self.utils.city_key(city_name)
                self.assertEqual(result, expected_key)
    
    # ================================
    # Integration and edge case tests
    # ================================
    
    def test_integration_is_fallback_and_format_status(self):
        """Test integration between is_fallback and format_fallback_status."""
        # Test with simulated data
        simulated_data = {"source": "simulated", "temperature": 25}
        is_fallback_result = is_fallback(simulated_data)
        
        display_status = format_fallback_status(is_fallback_result, "display")
        log_status = format_fallback_status(is_fallback_result, "log")
        
        self.assertTrue(is_fallback_result)
        self.assertEqual(display_status, "(Simulated)")
        self.assertEqual(log_status, "Simulated")
        
        # Test with live data
        live_data = {"source": "api", "temperature": 25}
        is_fallback_result = is_fallback(live_data)
        
        display_status = format_fallback_status(is_fallback_result, "display")
        log_status = format_fallback_status(is_fallback_result, "log")
        
        self.assertFalse(is_fallback_result)
        self.assertEqual(display_status, "")
        self.assertEqual(log_status, "Live")
    
    def test_function_argument_validation(self):
        """Test that functions properly validate their arguments."""
        # Test format_fallback_status with invalid format_type
        with self.assertRaises(ValueError):
            format_fallback_status(True, "invalid_format")
    
    def test_function_return_types(self):
        """Test that all functions return the expected types."""
        # Test is_fallback return type
        result = is_fallback({"source": "simulated"})
        self.assertIsInstance(result, bool)
        
        # Test format_fallback_status return type
        result = format_fallback_status(True, "display")
        self.assertIsInstance(result, str)
        
        # Test city_key return type (with mocked validation)
        with patch('WeatherDashboard.utils.utils.ValidationUtils.validate_city_name', return_value=[]):
            result = city_key("Test City")
            self.assertIsInstance(result, str)
    
    def test_edge_cases_empty_and_none_inputs(self):
        """Test edge cases with empty and None inputs."""
        # Test is_fallback with None
        with self.assertRaises(AttributeError):
            is_fallback(None)  # Should fail when trying to call .get() on None
        
        # Test format_fallback_status with None fallback_used
        result = format_fallback_status(None, "display")
        self.assertEqual(result, "")  # None is falsy
    
    def test_performance_characteristics(self):
        """Test performance characteristics of utility functions."""
        import time
        
        # Test that functions are reasonably fast
        start_time = time.time()
        
        # Perform many operations
        for i in range(1000):
            data = {"source": "simulated" if i % 2 == 0 else "api"}
            is_fallback(data)
            format_fallback_status(i % 2 == 0, "display")
        
        elapsed_time = time.time() - start_time
        self.assertLess(elapsed_time, 1.0, "Utility functions should be fast")
    
    @patch('WeatherDashboard.utils.utils.ValidationUtils.validate_city_name')
    def test_city_key_with_unicode_input(self, mock_validate):
        """Test city_key with unicode input (mocking validation)."""
        mock_validate.return_value = []
        
        # Test that city_key can handle unicode characters if validation passes
        unicode_city = "São Paulo"
        result = city_key(unicode_city)
        
        # Should convert to lowercase and replace spaces
        self.assertEqual(result, "são_paulo")
        mock_validate.assert_called_once_with(unicode_city)
    
    def test_comprehensive_workflow_simulation(self):
        """Test a comprehensive workflow using all utility functions."""
        # Simulate processing weather data
        weather_data = {"source": "simulated", "temperature": 25, "city": "New York"}
        
        # Check if data is fallback
        is_fallback_data = is_fallback(weather_data)
        self.assertTrue(is_fallback_data)
        
        # Format status for display
        display_status = format_fallback_status(is_fallback_data, "display")
        self.assertEqual(display_status, "(Simulated)")
        
        # Format status for logging
        log_status = format_fallback_status(is_fallback_data, "log")
        self.assertEqual(log_status, "Simulated")
        
        # Generate city key for storage (mock validation)
        with patch('WeatherDashboard.utils.utils.ValidationUtils.validate_city_name', return_value=[]):
            storage_key = city_key(weather_data["city"])
            self.assertEqual(storage_key, "new_york")
    
    def test_thread_safety_simulation(self):
        """Test thread safety of utility functions."""
        import threading
        import time
        
        results = []
        errors = []
        
        def worker():
            try:
                for i in range(100):
                    # Test is_fallback
                    data = {"source": "simulated" if i % 2 == 0 else "api"}
                    fallback_result = is_fallback(data)
                    
                    # Test format_fallback_status
                    status = format_fallback_status(fallback_result, "display")
                    
                    results.append((fallback_result, status))
                    
                    # Small delay to increase chance of race conditions
                    time.sleep(0.001)
                    
            except Exception as e:
                errors.append(e)
        
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
        self.assertEqual(len(errors), 0, f"Thread safety test failed with errors: {errors}")
        self.assertEqual(len(results), 300)  # 3 threads * 100 operations
    
    def test_memory_usage_patterns(self):
        """Test memory usage patterns of utility functions."""
        import gc
        
        # Force garbage collection
        gc.collect()
        initial_objects = len(gc.get_objects())
        
        # Perform many operations
        for i in range(1000):
            data = {"source": "simulated", "temp": i}
            is_fallback(data)
            format_fallback_status(i % 2 == 0, "display")
            format_fallback_status(i % 2 == 0, "log")
        
        # Force garbage collection again
        gc.collect()
        final_objects = len(gc.get_objects())
        
        # Memory usage should not grow excessively
        object_growth = final_objects - initial_objects
        self.assertLess(object_growth, 100, "Functions should not leak significant memory")


if __name__ == '__main__':
    unittest.main()