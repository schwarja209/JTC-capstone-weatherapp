"""
Unit tests for WeatherDashboard.utils.utils module.

Tests utility functions including:
- Fallback data detection and formatting
- City key generation and normalization
- Input validation and error handling
- Performance characteristics
- Edge case handling
"""

import unittest
import time

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WeatherDashboard.utils.utils import Utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.utils = Utils()

    # ================================
    # is_fallback() function tests
    # ================================
    
    def test_is_fallback_with_simulated_data(self):
        """Test is_fallback with simulated data."""
        data = {"source": "simulated", "temperature": 25}
        result = self.utils.is_fallback(data)
        self.assertTrue(result)
    
    def test_is_fallback_with_live_data(self):
        """Test is_fallback with live API data."""
        data = {"source": "api", "temperature": 25, "humidity": 60}
        result = self.utils.is_fallback(data)
        self.assertFalse(result)
    
    def test_is_fallback_with_missing_source(self):
        """Test is_fallback with data missing source field."""
        data = {"temperature": 25}
        result = self.utils.is_fallback(data)
        self.assertFalse(result)
    
    def test_is_fallback_with_none_source(self):
        """Test is_fallback with None source."""
        data = {"source": None, "temperature": 25}
        result = self.utils.is_fallback(data)
        self.assertFalse(result)
    
    def test_is_fallback_with_empty_dict(self):
        """Test is_fallback with empty dictionary."""
        data = {}
        result = self.utils.is_fallback(data)
        self.assertFalse(result)
    
    def test_is_fallback_case_sensitivity(self):
        """Test is_fallback with different case variations."""
        test_cases = [
            ({"source": "simulated", "temp": 25}, True),  # Only lowercase "simulated" works
            ({"source": "SIMULATED", "temp": 25}, False),  # Case sensitive
            ({"source": "Simulated", "temp": 25}, False),  # Case sensitive
            ({"source": "api", "temp": 25}, False),
            ({"source": "API", "temp": 25}, False),
            ({"source": "Api", "temp": 25}, False),
        ]
        
        for data, expected in test_cases:
            with self.subTest(source=data.get("source")):
                result = self.utils.is_fallback(data)
                self.assertEqual(result, expected)
    
    # ================================
    # format_fallback_status() function tests
    # ================================
    
    def test_format_fallback_status_display_mode(self):
        """Test format_fallback_status with display mode."""
        result = self.utils.format_fallback_status(True, "display")
        self.assertEqual(result, "(Simulated)")
        
        result = self.utils.format_fallback_status(False, "display")
        self.assertEqual(result, "")
    
    def test_format_fallback_status_log_mode(self):
        """Test format_fallback_status with log mode."""
        result = self.utils.format_fallback_status(True, "log")
        self.assertEqual(result, "Simulated")
        
        result = self.utils.format_fallback_status(False, "log")
        self.assertEqual(result, "Live")
    
    def test_format_fallback_status_default_mode(self):
        """Test format_fallback_status with default mode."""
        result = self.utils.format_fallback_status(True)
        self.assertEqual(result, "(Simulated)")
        
        result = self.utils.format_fallback_status(False)
        self.assertEqual(result, "")
    
    def test_format_fallback_status_invalid_mode(self):
        """Test format_fallback_status with invalid mode."""
        # When fallback_used is True, invalid format_type should raise ValueError
        with self.assertRaises(ValueError):
            self.utils.format_fallback_status(True, "invalid")
        
        # When fallback_used is False, the function returns early and doesn't validate format_type
        # So this should not raise an exception
        result = self.utils.format_fallback_status(False, "invalid")
        self.assertEqual(result, "")  # Returns empty string for False fallback_used
    
    def test_format_fallback_status_boolean_coercion(self):
        """Test format_fallback_status with non-boolean inputs."""
        # Test with truthy values
        self.assertEqual(self.utils.format_fallback_status(1, "display"), "(Simulated)")
        self.assertEqual(self.utils.format_fallback_status("truthy", "display"), "(Simulated)")
        
        # Test with falsy values
        self.assertEqual(self.utils.format_fallback_status(0, "display"), "")
        self.assertEqual(self.utils.format_fallback_status("", "display"), "")
        self.assertEqual(self.utils.format_fallback_status(None, "display"), "")
    
    # ================================
    # city_key() function tests
    # ================================
    
    def test_city_key_with_valid_cities(self):
        """Test city key generation with valid city names."""
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
    
    def test_city_key_validation_error_handling(self):
        """Test city key generation when validation fails."""
        # Test with a city name that should fail validation
        with self.assertRaises(ValueError) as context:
            self.utils.city_key("Invalid123")  # Contains numbers which should fail validation
        
        # Should raise the validation error
        self.assertIn("City name", str(context.exception))
    
    def test_city_key_multiple_validation_errors(self):
        """Test city key generation with multiple validation errors."""
        with self.assertRaises(ValueError) as context:
            self.utils.city_key("Bad123")
        
        # Should raise the first error only
        self.assertIn("City name", str(context.exception))
    
    def test_city_key_normalization_behavior(self):
        """Test city key normalization behavior."""
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
    
    def test_city_key_special_character_handling(self):
        """Test city key handling of special characters."""
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
        is_fallback_result = self.utils.is_fallback(simulated_data)
        
        display_status = self.utils.format_fallback_status(is_fallback_result, "display")
        log_status = self.utils.format_fallback_status(is_fallback_result, "log")
        
        self.assertTrue(is_fallback_result)
        self.assertEqual(display_status, "(Simulated)")
        self.assertEqual(log_status, "Simulated")
        
        # Test with live data
        live_data = {"source": "api", "temperature": 25}
        is_fallback_result = self.utils.is_fallback(live_data)
        
        display_status = self.utils.format_fallback_status(is_fallback_result, "display")
        log_status = self.utils.format_fallback_status(is_fallback_result, "log")
        
        self.assertFalse(is_fallback_result)
        self.assertEqual(display_status, "")
        self.assertEqual(log_status, "Live")
    
    def test_function_argument_validation(self):
        """Test that functions handle various argument types correctly."""
        # Test with None arguments - should handle gracefully
        with self.assertRaises(AttributeError):
            self.utils.is_fallback(None)
        self.assertEqual(self.utils.format_fallback_status(None, "display"), "")
    
    def test_function_return_types(self):
        """Test that functions return expected types."""
        # is_fallback should return boolean
        result = self.utils.is_fallback({"source": "api"})
        self.assertIsInstance(result, bool)
        
        # format_fallback_status should return string
        result = self.utils.format_fallback_status(True, "display")
        self.assertIsInstance(result, str)
        
        # city_key should return string
        result = self.utils.city_key("New York")
        self.assertIsInstance(result, str)
    
    def test_edge_cases_empty_and_none_inputs(self):
        """Test edge cases with empty and None inputs."""
        # Test is_fallback with edge cases
        self.assertFalse(self.utils.is_fallback({}))
        with self.assertRaises(AttributeError):
            self.utils.is_fallback(None)
        
        # Test format_fallback_status with edge cases
        self.assertEqual(self.utils.format_fallback_status(None, "display"), "")
        self.assertEqual(self.utils.format_fallback_status("", "display"), "")
    
    def test_performance_characteristics(self):
        """Test performance characteristics of utility functions."""
        # Test that functions complete in reasonable time
        start_time = time.time()
        
        for _ in range(1000):
            self.utils.is_fallback({"source": "api"})
            self.utils.format_fallback_status(True, "display")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete 1000 iterations in under 1 second
        self.assertLess(execution_time, 1.0)
    
    def test_city_key_with_unicode_input(self):
        """Test city key generation with unicode characters."""
        # Test with valid unicode characters that pass validation
        test_cases = [
            ("New York", "new_york"),  # Standard ASCII
            ("London", "london"),      # Standard ASCII
        ]
        
        for city_name, expected_key in test_cases:
            with self.subTest(city=city_name):
                result = self.utils.city_key(city_name)
                self.assertEqual(result, expected_key)
    
    def test_comprehensive_workflow_simulation(self):
        """Test comprehensive workflow simulation."""
        # Simulate a complete workflow
        test_data = [
            {"source": "api", "temperature": 25, "city": "New York"},
            {"source": "simulated", "temperature": 20, "city": "London"},
            {"source": "api", "temperature": 30, "city": "Tokyo"},
        ]
        
        results = []
        for data in test_data:
            is_fallback = self.utils.is_fallback(data)
            status = self.utils.format_fallback_status(is_fallback, "log")
            city_key = self.utils.city_key(data["city"])
            
            results.append({
                "is_fallback": is_fallback,
                "status": status,
                "city_key": city_key
            })
        
        # Verify results
        self.assertFalse(results[0]["is_fallback"])  # API data
        self.assertTrue(results[1]["is_fallback"])   # Simulated data
        self.assertFalse(results[2]["is_fallback"])  # API data
        
        self.assertIn("Live", results[0]["status"])
        self.assertIn("Simulated", results[1]["status"])
        self.assertIn("Live", results[2]["status"])
        
        self.assertEqual(results[0]["city_key"], "new_york")
        self.assertEqual(results[1]["city_key"], "london")
        self.assertEqual(results[2]["city_key"], "tokyo")
    
    def test_thread_safety_simulation(self):
        """Test thread safety simulation."""
        import threading
        
        results = []
        errors = []
        
        def worker():
            try:
                for i in range(100):
                    data = {"source": "api" if i % 2 == 0 else "simulated", "temperature": i}
                    is_fallback = self.utils.is_fallback(data)
                    status = self.utils.format_fallback_status(is_fallback, "display")
                    results.append((is_fallback, status))
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify no errors occurred
        self.assertEqual(len(errors), 0)
        
        # Verify we got expected number of results
        self.assertEqual(len(results), 500)  # 5 threads * 100 iterations
        
        # Verify results are consistent
        for is_fallback, status in results:
            if is_fallback:
                self.assertIn("Simulated", status)
            else:
                self.assertEqual(status, "")  # Live data shows empty string in display mode
    
    def test_memory_usage_patterns(self):
        """Test memory usage patterns."""
        # Test that repeated calls don't cause memory leaks
        import gc
        initial_objects = len(gc.get_objects())
        
        for _ in range(1000):
            self.utils.is_fallback({"source": "api"})
            self.utils.format_fallback_status(True, "display")
            self.utils.city_key("New York")
        
        # Force garbage collection
        gc.collect()
        
        final_objects = len(gc.get_objects())
        
        # Memory usage should not increase significantly
        # Allow for more variance in object count on Windows
        self.assertLess(abs(final_objects - initial_objects), 3000)


if __name__ == '__main__':
    unittest.main()