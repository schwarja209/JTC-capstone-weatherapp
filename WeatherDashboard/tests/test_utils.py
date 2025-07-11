"""
Unit tests for utility functions.

Tests utility functions including:
- City name normalization and key generation
- Unit system validation  
- Fallback status formatting
- Data validation helpers
"""
import unittest
from WeatherDashboard.utils.utils import (
    normalize_city_name, 
    city_key, 
    validate_unit_system,
    format_fallback_status
)

class TestUtils(unittest.TestCase):
    def test_normalize_city_name(self):
        """Test city name normalization."""
        self.assertEqual(normalize_city_name("new york"), "New York")
        self.assertEqual(normalize_city_name("  PARIS  "), "Paris")
        self.assertEqual(normalize_city_name("san francisco"), "San Francisco")
        
        # Test error cases
        with self.assertRaises(ValueError):
            normalize_city_name("")
        with self.assertRaises(ValueError):
            normalize_city_name("   ")
        with self.assertRaises(ValueError):
            normalize_city_name(123)
    
    def test_city_key(self):
        """Test city key generation."""
        self.assertEqual(city_key("New York"), "new_york")
        self.assertEqual(city_key("San Francisco"), "san_francisco")
        self.assertEqual(city_key("LONDON"), "london")
    
    def test_validate_unit_system(self):
        """Test unit system validation."""
        self.assertEqual(validate_unit_system("metric"), "metric")
        self.assertEqual(validate_unit_system("imperial"), "imperial")
        
        with self.assertRaises(ValueError):
            validate_unit_system("invalid")
        with self.assertRaises(ValueError):
            validate_unit_system("")
        with self.assertRaises(ValueError):
            validate_unit_system(None)
    
    def test_format_fallback_status(self):
        """Test fallback status formatting."""
        self.assertEqual(format_fallback_status(True, "display"), "(Simulated)")
        self.assertEqual(format_fallback_status(False, "display"), "")
        self.assertEqual(format_fallback_status(True, "log"), "Simulated")
        self.assertEqual(format_fallback_status(False, "log"), "Live")
        
        with self.assertRaises(ValueError):
            format_fallback_status(True, "invalid")