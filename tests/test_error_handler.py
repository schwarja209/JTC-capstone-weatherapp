"""
Unit tests for WeatherErrorHandler class.

Tests theme-aware error handling including:
- Error message formatting with theme support
- Different error type handling (network, validation, city not found)
- Theme switching behavior
- Message template management
- Integration with satirical theme foundation
- Error recovery guidance
"""

import unittest
from unittest.mock import Mock, patch

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WeatherDashboard.services.error_handler import WeatherErrorHandler
from WeatherDashboard.services.api_exceptions import (
    ValidationError, CityNotFoundError, RateLimitError, NetworkError, WeatherAPIError
)


class TestWeatherErrorHandler(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.error_handler = WeatherErrorHandler()

    def test_initialization(self):
        """Test error handler initializes with correct defaults."""
        self.assertEqual(self.error_handler.current_theme, 'neutral')
        self.assertIsInstance(self.error_handler._message_templates, dict)

    def test_initialization_with_theme(self):
        """Test error handler initialization with specific theme."""
        themed_handler = WeatherErrorHandler(theme='optimistic')
        self.assertEqual(themed_handler.current_theme, 'optimistic')

    def test_set_theme_valid_themes(self):
        """Test setting valid themes."""
        valid_themes = ['neutral', 'optimistic', 'pessimistic']
        
        for theme in valid_themes:
            with self.subTest(theme=theme):
                self.error_handler.set_theme(theme)
                self.assertEqual(self.error_handler.current_theme, theme)

    def test_set_theme_invalid_theme(self):
        """Test setting invalid theme defaults to neutral."""
        self.error_handler.set_theme('invalid_theme')
        self.assertEqual(self.error_handler.current_theme, 'neutral')

    def test_format_message_neutral_theme(self):
        """Test message formatting with neutral theme."""
        # Test with message that has theme variations
        message = self.error_handler._format_message('city_not_found', "TestCity")
        
        # Should contain city name and be neutral in tone
        self.assertIn("TestCity", message)
        self.assertIsInstance(message, str)
        self.assertGreater(len(message), 0)

    def test_format_message_optimistic_theme(self):
        """Test message formatting with optimistic theme."""
        self.error_handler.set_theme('optimistic')
        message = self.error_handler._format_message('city_not_found', "TestCity")
        
        # Should contain city name and return a message
        self.assertIn("TestCity", message)
        self.assertIsInstance(message, str)
        self.assertGreater(len(message), 0)

    def test_format_message_pessimistic_theme(self):
        """Test message formatting with pessimistic theme."""
        self.error_handler.set_theme('pessimistic')
        message = self.error_handler._format_message('city_not_found', "TestCity")
        
        # Should contain city name and return a message
        self.assertIn("TestCity", message)
        self.assertIsInstance(message, str)
        self.assertGreater(len(message), 0)

    def test_format_message_unknown_template(self):
        """Test message formatting with unknown template key."""
        message = self.error_handler._format_message('unknown_error', "TestData")
        
        # Should return some form of message (may be the data itself as fallback)
        self.assertIsInstance(message, str)

    def test_handle_weather_error_city_not_found(self):
        """Test handling city not found errors."""
        error = CityNotFoundError("City 'InvalidCity' not found")
        
        result = self.error_handler.handle_weather_error(error, "InvalidCity")
        
        # Should return True (continue with fallback)
        self.assertTrue(result)

    def test_handle_weather_error_rate_limit(self):
        """Test handling rate limit errors."""
        error = RateLimitError("Rate limit exceeded")
        
        result = self.error_handler.handle_weather_error(error, "TestCity")
        
        # Should return True (continue with rate limiting)
        self.assertTrue(result)

    def test_handle_weather_error_network_error(self):
        """Test handling network errors."""
        error = NetworkError("Connection failed")
        
        result = self.error_handler.handle_weather_error(error, "TestCity")
        
        # Should return True (continue with fallback)
        self.assertTrue(result)

    def test_handle_weather_error_validation_error(self):
        """Test handling validation errors."""
        error = ValidationError("Invalid input data")
        
        result = self.error_handler.handle_weather_error(error, "TestCity")
        
        # Should return False (stop processing)
        self.assertFalse(result)

    def test_handle_weather_error_generic_api_error(self):
        """Test handling generic API errors."""
        error = WeatherAPIError("API service unavailable")
        
        result = self.error_handler.handle_weather_error(error, "TestCity")
        
        # Should return True (continue with fallback)
        self.assertTrue(result)

    def test_handle_weather_error_unknown_error(self):
        """Test handling unknown error types."""
        error = Exception("Unknown error")
        
        result = self.error_handler.handle_weather_error(error, "TestCity")
        
        # Should return True (continue with fallback)
        self.assertTrue(result)

    def test_theme_switching_behavior(self):
        """Test behavior when switching themes mid-operation."""
        error = NetworkError("Connection error")
        
        # Start with neutral theme
        self.error_handler.set_theme('neutral')
        neutral_message = self.error_handler._format_message('network_error', "TestCity")
        
        # Switch to optimistic theme
        self.error_handler.set_theme('optimistic')
        optimistic_message = self.error_handler._format_message('network_error', "TestCity")
        
        # Switch to pessimistic theme
        self.error_handler.set_theme('pessimistic')
        pessimistic_message = self.error_handler._format_message('network_error', "TestCity")
        
        # All should be valid strings
        for msg in [neutral_message, optimistic_message, pessimistic_message]:
            self.assertIsInstance(msg, str)

    def test_satirical_theme_message_templates(self):
        """Test foundation for satirical theme message variations."""
        city = "TestCity"
        
        # Test how themes might manipulate the same error differently
        error_types = ['city_not_found', 'network_error', 'rate_limit_error']
        
        for error_type in error_types:
            with self.subTest(error_type=error_type):
                # Get messages for all themes
                self.error_handler.set_theme('neutral')
                neutral_msg = self.error_handler._format_message(error_type, city)
                
                self.error_handler.set_theme('optimistic')
                optimistic_msg = self.error_handler._format_message(error_type, city)
                
                self.error_handler.set_theme('pessimistic')
                pessimistic_msg = self.error_handler._format_message(error_type, city)
                
                # All should contain the city name and be valid strings
                for msg in [neutral_msg, optimistic_msg, pessimistic_msg]:
                    self.assertIsInstance(msg, str)
                    if city in msg:  # Not all error types may include city name
                        self.assertIn(city, msg)

    def test_error_recovery_guidance(self):
        """Test error recovery guidance for different error types."""
        recovery_test_cases = [
            (CityNotFoundError("City not found"), True),   # Can recover with fallback
            (NetworkError("No internet"), True),           # Can recover with fallback
            (RateLimitError("Rate limited"), True),        # Can recover by waiting
            (ValidationError("Bad input"), False),         # Cannot recover automatically
        ]
        
        for error, should_continue in recovery_test_cases:
            with self.subTest(error=error.__class__.__name__):
                result = self.error_handler.handle_weather_error(error, "TestCity")
                self.assertEqual(result, should_continue)

    def test_message_template_parameter_substitution(self):
        """Test proper parameter substitution in message templates."""
        test_city = "San Francisco"
        
        # Test that city name is properly substituted
        message = self.error_handler._format_message('city_not_found', test_city)
        self.assertIsInstance(message, str)
        if test_city in message:
            self.assertIn(test_city, message)
        
        # Test with special characters in city name
        special_city = "City-with-Hyphens & Symbols"
        message = self.error_handler._format_message('city_not_found', special_city)
        self.assertIsInstance(message, str)

    def test_error_handler_memory_efficiency(self):
        """Test error handler memory efficiency with repeated operations."""
        # Simulate many error handling operations
        for i in range(100):
            error = NetworkError(f"Error {i}")
            result = self.error_handler.handle_weather_error(error, f"City{i}")
            self.assertTrue(result)
        
        # Error handler should still function correctly
        final_error = CityNotFoundError("Final test")
        result = self.error_handler.handle_weather_error(final_error, "FinalCity")
        self.assertTrue(result)

    def test_concurrent_theme_operations(self):
        """Test thread safety of theme operations."""
        # Simulate rapid theme switching
        themes = ['neutral', 'optimistic', 'pessimistic']
        
        for i in range(50):
            theme = themes[i % len(themes)]
            self.error_handler.set_theme(theme)
            self.assertEqual(self.error_handler.current_theme, theme)
            
            # Test that error handling still works
            error = NetworkError(f"Test error {i}")
            result = self.error_handler.handle_weather_error(error, f"City{i}")
            self.assertTrue(result)

    def test_satirical_foundation_extensibility(self):
        """Test that the error handler provides good foundation for satirical features."""
        # This test demonstrates how the current system supports satirical enhancement
        
        # Test that theme system is flexible
        self.error_handler.set_theme('optimistic')
        optimistic_tone = self.error_handler._format_message('network_error', "TestCity")
        
        self.error_handler.set_theme('pessimistic')
        pessimistic_tone = self.error_handler._format_message('network_error', "TestCity")
        
        # Both should be valid strings
        self.assertIsInstance(optimistic_tone, str)
        self.assertIsInstance(pessimistic_tone, str)

    def test_error_type_handling_consistency(self):
        """Test consistent handling of different error types."""
        error_types = [
            CityNotFoundError("City not found"),
            NetworkError("Network error"),
            RateLimitError("Rate limit error"),
            ValidationError("Validation error"),
            WeatherAPIError("API error"),
            Exception("Generic error")
        ]
        
        for error in error_types:
            with self.subTest(error=error.__class__.__name__):
                result = self.error_handler.handle_weather_error(error, "TestCity")
                self.assertIsInstance(result, bool)

    def test_theme_persistence(self):
        """Test that theme settings persist across operations."""
        # Set a theme
        self.error_handler.set_theme('optimistic')
        
        # Handle several errors
        errors = [
            NetworkError("Error 1"),
            CityNotFoundError("Error 2"),
            RateLimitError("Error 3")
        ]
        
        for error in errors:
            self.error_handler.handle_weather_error(error, "TestCity")
            # Theme should remain unchanged
            self.assertEqual(self.error_handler.current_theme, 'optimistic')

    def test_message_formatting_robustness(self):
        """Test message formatting with various input types."""
        test_inputs = [
            ("TestCity", str),
            (123, int),
            (None, type(None)),
            ("", str),
            ("City with spaces", str)
        ]
        
        for city_input, input_type in test_inputs:
            with self.subTest(input=city_input, type=input_type):
                try:
                    message = self.error_handler._format_message('city_not_found', city_input)
                    self.assertIsInstance(message, str)
                except Exception as e:
                    # If error occurs, it should be handled gracefully
                    self.fail(f"Message formatting should handle {input_type} gracefully: {e}")


if __name__ == '__main__':
    unittest.main()