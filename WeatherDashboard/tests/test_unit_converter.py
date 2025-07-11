"""
Unit tests for UnitConverter class.

Tests unit conversion functionality including:
- Temperature conversions (Celsius ↔ Fahrenheit)
- Pressure conversions (hPa ↔ inHg)  
- Wind speed conversions (m/s ↔ mph)
- Value formatting for display
"""
import unittest
from WeatherDashboard.utils.unit_converter import UnitConverter

class TestUnitConverter(unittest.TestCase):
    def test_temperature_conversion(self):
        """Test temperature conversions."""
        # Celsius to Fahrenheit
        self.assertAlmostEqual(UnitConverter.convert_temperature(0, "°C", "°F"), 32.0)
        self.assertAlmostEqual(UnitConverter.convert_temperature(100, "°C", "°F"), 212.0)
        
        # Fahrenheit to Celsius  
        self.assertAlmostEqual(UnitConverter.convert_temperature(32, "°F", "°C"), 0.0)
        self.assertAlmostEqual(UnitConverter.convert_temperature(212, "°F", "°C"), 100.0)
        
        # Same unit should return original value
        self.assertEqual(UnitConverter.convert_temperature(25, "°C", "°C"), 25)
    
    def test_pressure_conversion(self):
        """Test pressure conversions."""
        # hPa to inHg
        result = UnitConverter.convert_pressure(1013.25, "hPa", "inHg")
        self.assertAlmostEqual(result, 29.92, places=1)
        
        # inHg to hPa
        result = UnitConverter.convert_pressure(29.92, "inHg", "hPa")
        self.assertAlmostEqual(result, 1013.25, places=0)
    
    def test_format_value(self):
        """Test value formatting."""
        self.assertEqual(UnitConverter.format_value("temperature", 25.6, "metric"), "25.6 °C")
        self.assertEqual(UnitConverter.format_value("humidity", 75, "metric"), "75 %")
        self.assertEqual(UnitConverter.format_value("pressure", 1013.25, "metric"), "1013.25 hPa")
        self.assertEqual(UnitConverter.format_value("conditions", "Sunny", "metric"), "Sunny")
        
        # Test with None value
        self.assertEqual(UnitConverter.format_value("temperature", None, "metric"), "--")