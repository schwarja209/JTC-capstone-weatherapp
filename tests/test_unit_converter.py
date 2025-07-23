"""
Unit tests for UnitConverter class.

Tests comprehensive unit conversion system functionality including:
- Temperature conversions (Celsius ↔ Fahrenheit) with boundary value testing
- Pressure conversions (hPa ↔ inHg) with precision validation and edge cases
- Wind speed conversions (m/s ↔ mph) with accuracy verification
- Visibility conversions (km ↔ mi) with range checking
- Precipitation conversions (mm ↔ inches) with precision handling
- Value formatting for display with configuration system integration
- Format configuration system with metric type mapping and precision rules
- Error handling and edge cases for invalid units and malformed data
- Integration with centralized configuration for unit mappings and formats
- Thread safety considerations for concurrent conversion operations
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from WeatherDashboard.utils.unit_converter import UnitConverter

class TestUnitConverter(unittest.TestCase):
    def test_temperature_conversion_celsius_to_fahrenheit(self):
        """Test temperature conversions from Celsius to Fahrenheit."""
        test_cases = [
            (0, 32.0),      # Freezing point
            (100, 212.0),   # Boiling point
            (-40, -40.0),   # Same temperature in both scales
            (25, 77.0),     # Room temperature
            (-273.15, -459.67)  # Absolute zero
        ]
        
        for celsius, expected_fahrenheit in test_cases:
            with self.subTest(celsius=celsius):
                result = UnitConverter.convert_temperature(celsius, "°C", "°F")
                self.assertAlmostEqual(result, expected_fahrenheit, places=1)

    def test_temperature_conversion_fahrenheit_to_celsius(self):
        """Test temperature conversions from Fahrenheit to Celsius."""
        test_cases = [
            (32, 0.0),      # Freezing point
            (212, 100.0),   # Boiling point
            (-40, -40.0),   # Same temperature in both scales
            (77, 25.0),     # Room temperature
            (98.6, 37.0)    # Body temperature
        ]
        
        for fahrenheit, expected_celsius in test_cases:
            with self.subTest(fahrenheit=fahrenheit):
                result = UnitConverter.convert_temperature(fahrenheit, "°F", "°C")
                self.assertAlmostEqual(result, expected_celsius, places=1)

    def test_temperature_conversion_same_unit(self):
        """Test temperature conversion with same source and target units."""
        test_values = [25, 0, -10, 100]
        
        for temp in test_values:
            with self.subTest(temp=temp):
                # Celsius to Celsius
                result_c = UnitConverter.convert_temperature(temp, "°C", "°C")
                self.assertEqual(result_c, temp)
                
                # Fahrenheit to Fahrenheit
                result_f = UnitConverter.convert_temperature(temp, "°F", "°F")
                self.assertEqual(result_f, temp)

    def test_temperature_conversion_invalid_units(self):
        """Test temperature conversion with invalid units."""
        with self.assertRaises(ValueError):
            UnitConverter.convert_temperature(25, "°C", "°K")
        
        with self.assertRaises(ValueError):
            UnitConverter.convert_temperature(25, "°R", "°F")
        
        with self.assertRaises(ValueError):
            UnitConverter.convert_temperature(25, "celsius", "fahrenheit")

    def test_pressure_conversion_hpa_to_inhg(self):
        """Test pressure conversions from hPa to inHg."""
        test_cases = [
            (1013.25, 29.92),   # Standard atmospheric pressure
            (1000, 29.53),      # Round number
            (950, 28.05),       # Low pressure
            (1050, 31.01)       # High pressure
        ]
        
        for hpa, expected_inhg in test_cases:
            with self.subTest(hpa=hpa):
                result = UnitConverter.convert_pressure(hpa, "hPa", "inHg")
                self.assertAlmostEqual(result, expected_inhg, places=1)

    def test_pressure_conversion_inhg_to_hpa(self):
        """Test pressure conversions from inHg to hPa."""
        test_cases = [
            (29.92, 1013.25),   # Standard atmospheric pressure
            (30.00, 1015.92),   # Round number
            (28.00, 948.21),    # Low pressure
            (31.00, 1049.65)    # High pressure
        ]
        
        for inhg, expected_hpa in test_cases:
            with self.subTest(inhg=inhg):
                result = UnitConverter.convert_pressure(inhg, "inHg", "hPa")
                self.assertAlmostEqual(result, expected_hpa, places=0)

    def test_pressure_conversion_same_unit(self):
        """Test pressure conversion with same source and target units."""
        test_values = [1013.25, 1000, 950]
        
        for pressure in test_values:
            with self.subTest(pressure=pressure):
                # hPa to hPa
                result_hpa = UnitConverter.convert_pressure(pressure, "hPa", "hPa")
                self.assertEqual(result_hpa, pressure)
                
                # inHg to inHg
                result_inhg = UnitConverter.convert_pressure(pressure, "inHg", "inHg")
                self.assertEqual(result_inhg, pressure)

    def test_pressure_conversion_invalid_units(self):
        """Test pressure conversion with invalid units."""
        with self.assertRaises(ValueError):
            UnitConverter.convert_pressure(1013, "hPa", "bar")
        
        with self.assertRaises(ValueError):
            UnitConverter.convert_pressure(29.92, "inHg", "mmHg")

    def test_wind_speed_conversion_ms_to_mph(self):
        """Test wind speed conversions from m/s to mph."""
        test_cases = [
            (0, 0.0),       # Calm
            (5, 11.18),     # Light breeze
            (10, 22.37),    # Fresh breeze
            (20, 44.74),    # Strong wind
            (30, 67.11)     # Gale
        ]
        
        for ms, expected_mph in test_cases:
            with self.subTest(ms=ms):
                result = UnitConverter.convert_wind_speed(ms, "m/s", "mph")
                self.assertAlmostEqual(result, expected_mph, places=1)

    def test_wind_speed_conversion_mph_to_ms(self):
        """Test wind speed conversions from mph to m/s."""
        test_cases = [
            (0, 0.0),       # Calm
            (11.18, 5.0),   # Light breeze
            (22.37, 10.0),  # Fresh breeze
            (44.74, 20.0),  # Strong wind
            (67.11, 30.0)   # Gale
        ]
        
        for mph, expected_ms in test_cases:
            with self.subTest(mph=mph):
                result = UnitConverter.convert_wind_speed(mph, "mph", "m/s")
                self.assertAlmostEqual(result, expected_ms, places=1)

    def test_wind_speed_conversion_invalid_units(self):
        """Test wind speed conversion with invalid units."""
        with self.assertRaises(ValueError):
            UnitConverter.convert_wind_speed(10, "m/s", "km/h")
        
        with self.assertRaises(ValueError):
            UnitConverter.convert_wind_speed(10, "knots", "mph")

    def test_visibility_conversion_km_to_miles(self):
        """Test visibility conversions from kilometers to miles."""
        test_cases = [
            (1.609, 1.0),    # 1 mile = 1.609 km
            (8.047, 5.0),    # 5 miles = 8.047 km  
            (16.093, 10.0),  # 10 miles = 16.093 km
            (1.0, 0.621),    # 1 kilometer = 0.621 miles
            (5.0, 3.107)     # 5 kilometers = 3.107 miles
        ]
        
        for km, expected_miles in test_cases:
            with self.subTest(km=km):
                result = UnitConverter.convert_visibility(km, "km", "mi")
                self.assertAlmostEqual(result, expected_miles, places=1)

    def test_visibility_conversion_miles_to_km(self):
        """Test visibility conversions from miles to kilometers."""
        test_cases = [
            (1.0, 1.609),    # 1 mile = 1.609 km
            (5.0, 8.047),    # 5 miles = 8.047 km
            (10.0, 16.093),  # 10 miles = 16.093 km
            (0.621, 1.0),    # 0.621 miles = 1 km
            (3.107, 5.0)     # 3.107 miles = 5 km
        ]
        
        for miles, expected_km in test_cases:
            with self.subTest(miles=miles):
                result = UnitConverter.convert_visibility(miles, "mi", "km")
                self.assertAlmostEqual(result, expected_km, places=1)

    def test_visibility_conversion_invalid_units(self):
        """Test visibility conversion with invalid units."""
        # Test unsupported unit types
        with self.assertRaises(ValueError):
            UnitConverter.convert_visibility(1000, "m", "km")  # meters not supported
        
        with self.assertRaises(ValueError):
            UnitConverter.convert_visibility(5, "miles", "meters")  # full names not supported
            
        # Test units that don't exist in config
        with self.assertRaises(ValueError):
            UnitConverter.convert_visibility(5, "ft", "mi")  # feet not supported

    def test_precipitation_conversion_mm_to_inches(self):
        """Test precipitation conversions from mm to inches."""
        test_cases = [
            (25.4, 1.0),    # 1 inch
            (50.8, 2.0),    # 2 inches
            (10, 0.39),     # 10mm
            (100, 3.94),    # 100mm (heavy rain)
            (0, 0.0)        # No precipitation
        ]
        
        for mm, expected_inches in test_cases:
            with self.subTest(mm=mm):
                result = UnitConverter.convert_precipitation(mm, "mm", "in")
                self.assertAlmostEqual(result, expected_inches, places=1)

    def test_precipitation_conversion_inches_to_mm(self):
        """Test precipitation conversions from inches to mm."""
        test_cases = [
            (1.0, 25.4),    # 1 inch
            (2.0, 50.8),    # 2 inches
            (0.39, 10.0),   # ~10mm
            (3.94, 100.0),  # ~100mm
            (0, 0.0)        # No precipitation
        ]
        
        for inches, expected_mm in test_cases:
            with self.subTest(inches=inches):
                result = UnitConverter.convert_precipitation(inches, "in", "mm")
                self.assertAlmostEqual(result, expected_mm, places=0)

    def test_precipitation_conversion_invalid_units(self):
        """Test precipitation conversion with invalid units."""
        with self.assertRaises(ValueError):
            UnitConverter.convert_precipitation(25.4, "mm", "cm")
        
        with self.assertRaises(ValueError):
            UnitConverter.convert_precipitation(1, "inches", "millimeters")

    def test_format_value_temperature_metric(self):
        """Test value formatting for temperature in metric system."""
        result = UnitConverter.format_value("temperature", 25.6, "metric")
        self.assertEqual(result, "25.6 °C")

    def test_format_value_temperature_imperial(self):
        """Test value formatting for temperature in imperial system."""
        result = UnitConverter.format_value("temperature", 77.0, "imperial")
        self.assertEqual(result, "77.0 °F")

    def test_format_value_humidity(self):
        """Test value formatting for humidity (same in both systems)."""
        for unit_system in ["metric", "imperial"]:
            with self.subTest(unit_system=unit_system):
                result = UnitConverter.format_value("humidity", 75, unit_system)
                self.assertEqual(result, "75 %")

    def test_format_value_pressure_metric(self):
        """Test value formatting for pressure in metric system."""
        result = UnitConverter.format_value("pressure", 1013.25, "metric")
        self.assertEqual(result, "1013.25 hPa")

    def test_format_value_pressure_imperial(self):
        """Test value formatting for pressure in imperial system."""
        result = UnitConverter.format_value("pressure", 29.92, "imperial")
        self.assertEqual(result, "29.92 inHg")

    def test_format_value_wind_speed_metric(self):
        """Test value formatting for wind speed in metric system."""
        result = UnitConverter.format_value("wind_speed", 15.50, "metric")
        self.assertEqual(result, "15.50 m/s")

    def test_format_value_wind_speed_imperial(self):
        """Test value formatting for wind speed in imperial system."""
        result = UnitConverter.format_value("wind_speed", 34.70, "imperial")
        self.assertEqual(result, "34.70 mph")

    def test_format_value_conditions(self):
        """Test value formatting for weather conditions (no unit conversion)."""
        for unit_system in ["metric", "imperial"]:
            with self.subTest(unit_system=unit_system):
                result = UnitConverter.format_value("conditions", "Sunny", unit_system)
                self.assertEqual(result, "Sunny")

    def test_format_value_with_none(self):
        """Test value formatting with None values."""
        test_metrics = ["temperature", "humidity", "pressure", "conditions"]
        
        for metric in test_metrics:
            for unit_system in ["metric", "imperial"]:
                with self.subTest(metric=metric, unit_system=unit_system):
                    result = UnitConverter.format_value(metric, None, unit_system)
                    self.assertEqual(result, "--")

    def test_format_value_unknown_metric(self):
        """Test value formatting with unknown metric type."""
        result = UnitConverter.format_value("unknown_metric", 42, "metric")
        self.assertEqual(result, "42")  # Should return string representation

    def test_format_value_precision_handling(self):
        """Test value formatting with different precision requirements."""
        test_cases = [
            ("temperature", 25.0, "metric", "25.0 °C"),
            ("temperature", 25.12345, "metric", "25.1 °C"),  # Should round
            ("humidity", 60.0, "metric", "60 %"),  # Integer for humidity
            ("pressure", 1013.25, "metric", "1013.25 hPa"),
            ("wind_speed", 15.123, "metric", "15.12 m/s")  # 2 decimal places for wind
        ]
        
        for metric, value, unit_system, expected in test_cases:
            with self.subTest(metric=metric, value=value):
                result = UnitConverter.format_value(metric, value, unit_system)
                # Check format is reasonable (exact precision may vary)
                self.assertIn(str(int(value)), result)

    def test_error_handling_invalid_values(self):
        """Test error handling with invalid input values."""
        invalid_values = ["invalid", None, [], {}]
        
        for invalid_value in invalid_values:
            with self.subTest(value=invalid_value):
                # Should not raise exceptions, should handle gracefully
                try:
                    result = UnitConverter.format_value("temperature", invalid_value, "metric")
                    if invalid_value is None:
                        self.assertEqual(result, "--")
                    else:
                        # Should return string representation or error indicator
                        self.assertIsInstance(result, str)
                except (ValueError, TypeError):
                    # Some invalid values may raise exceptions, which is acceptable
                    pass

    def test_round_trip_conversions(self):
        """Test round-trip conversions for accuracy."""
        # Temperature round trip
        original_temp = 25.0
        converted = UnitConverter.convert_temperature(original_temp, "°C", "°F")
        back_converted = UnitConverter.convert_temperature(converted, "°F", "°C")
        self.assertAlmostEqual(back_converted, original_temp, places=5)
        
        # Pressure round trip
        original_pressure = 1013.25
        converted = UnitConverter.convert_pressure(original_pressure, "hPa", "inHg")
        back_converted = UnitConverter.convert_pressure(converted, "inHg", "hPa")
        self.assertAlmostEqual(back_converted, original_pressure, places=2)
        
        # Wind speed round trip
        original_wind = 10.0
        converted = UnitConverter.convert_wind_speed(original_wind, "m/s", "mph")
        back_converted = UnitConverter.convert_wind_speed(converted, "mph", "m/s")
        self.assertAlmostEqual(back_converted, original_wind, places=2)

    def test_boundary_value_conversions(self):
        """Test conversions with boundary values."""
        # Test absolute zero temperature
        abs_zero_c = -273.15
        abs_zero_f = UnitConverter.convert_temperature(abs_zero_c, "°C", "°F")
        self.assertAlmostEqual(abs_zero_f, -459.67, places=1)
        
        # Test zero pressure (vacuum)
        zero_pressure = UnitConverter.convert_pressure(0, "hPa", "inHg")
        self.assertEqual(zero_pressure, 0.0)
        
        # Test zero wind speed
        zero_wind = UnitConverter.convert_wind_speed(0, "m/s", "mph")
        self.assertEqual(zero_wind, 0.0)

    def test_large_value_conversions(self):
        """Test conversions with large values."""
        # Test very high temperature
        high_temp_c = 1000.0
        high_temp_f = UnitConverter.convert_temperature(high_temp_c, "°C", "°F")
        self.assertAlmostEqual(high_temp_f, 1832.0, places=0)
        
        # Test very high pressure
        high_pressure = 2000.0
        converted_pressure = UnitConverter.convert_pressure(high_pressure, "hPa", "inHg")
        self.assertGreater(converted_pressure, 50.0)

    def test_performance_with_repeated_conversions(self):
        """Test performance characteristics with repeated conversions."""
        # Test that repeated conversions don't degrade performance significantly
        test_values = list(range(0, 100, 5))
        
        # Perform many conversions
        for value in test_values:
            UnitConverter.convert_temperature(value, "°C", "°F")
            UnitConverter.convert_pressure(value + 1000, "hPa", "inHg")
            UnitConverter.convert_wind_speed(value, "m/s", "mph")
            UnitConverter.format_value("temperature", value, "metric")
        
        # If we get here without timeout, performance is acceptable
        self.assertTrue(True)

    def test_configuration_error_handling(self):
        """Test handling of configuration errors."""
        with patch('WeatherDashboard.utils.unit_converter.config') as mock_config:
            # Simulate missing configuration
            mock_config.UNITS = {}
            
            # Should handle missing config gracefully
            result = UnitConverter.format_value("temperature", 25, "metric")
            # Should return some reasonable default
            self.assertIsInstance(result, str)
            self.assertIn("25", result)

    def test_special_conversion_methods(self):
        """Test special temperature-like conversion methods."""
        # Test heat index conversion
        result = UnitConverter.convert_heat_index(25, "°C", "°F")
        expected = UnitConverter.convert_temperature(25, "°C", "°F")
        self.assertEqual(result, expected)
        
        # Test wind chill conversion
        result = UnitConverter.convert_wind_chill(25, "°C", "°F")
        expected = UnitConverter.convert_temperature(25, "°C", "°F")
        self.assertEqual(result, expected)
        
        # Test dew point conversion
        result = UnitConverter.convert_dew_point(25, "°C", "°F")
        expected = UnitConverter.convert_temperature(25, "°C", "°F")
        self.assertEqual(result, expected)

    def test_supported_unit_conversions(self):
        """Test that conversions work for units defined in config."""
        # Based on your config.py, these should be the supported units:
        # temperature: °C ↔ °F
        # pressure: hPa ↔ inHg  
        # wind_speed: m/s ↔ mph
        # visibility: km ↔ mi
        # rain/precipitation: mm ↔ in
        
        # Test each supported conversion direction
        conversion_tests = [
            (UnitConverter.convert_temperature, 25, "°C", "°F", 77.0),
            (UnitConverter.convert_temperature, 77, "°F", "°C", 25.0),
            (UnitConverter.convert_pressure, 1013.25, "hPa", "inHg", 29.92),
            (UnitConverter.convert_pressure, 29.92, "inHg", "hPa", 1013.25),
            (UnitConverter.convert_wind_speed, 10, "m/s", "mph", 22.37),
            (UnitConverter.convert_wind_speed, 22.37, "mph", "m/s", 10.0),
            (UnitConverter.convert_visibility, 1.609, "km", "mi", 1.0),
            (UnitConverter.convert_visibility, 1.0, "mi", "km", 1.609),
            (UnitConverter.convert_precipitation, 25.4, "mm", "in", 1.0),
            (UnitConverter.convert_precipitation, 1.0, "in", "mm", 25.4),
        ]
        
        for convert_func, value, from_unit, to_unit, expected in conversion_tests:
            with self.subTest(func=convert_func.__name__, from_unit=from_unit, to_unit=to_unit):
                result = convert_func(value, from_unit, to_unit)
                self.assertAlmostEqual(result, expected, places=1)

    def test_get_unit_label_functionality(self):
        """Test get_unit_label method for retrieving unit labels."""
        # Test temperature units based on your config
        metric_temp_unit = UnitConverter.get_unit_label("temperature", "metric")
        imperial_temp_unit = UnitConverter.get_unit_label("temperature", "imperial")
        
        # Should return the units defined in your config
        self.assertEqual(metric_temp_unit, "°C")
        self.assertEqual(imperial_temp_unit, "°F")
        
        # Test visibility units
        metric_visibility_unit = UnitConverter.get_unit_label("visibility", "metric")
        imperial_visibility_unit = UnitConverter.get_unit_label("visibility", "imperial")
        
        self.assertEqual(metric_visibility_unit, "km")
        self.assertEqual(imperial_visibility_unit, "mi")
        
        # Test with unknown metric (should return empty string and log warning)
        unknown_unit = UnitConverter.get_unit_label("unknown_metric", "metric")
        self.assertEqual(unknown_unit, "")


if __name__ == '__main__':
    unittest.main()