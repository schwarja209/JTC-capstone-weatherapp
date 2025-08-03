"""
Unit tests for API utility functions.

Tests comprehensive API response extraction functionality including:
- Safe nested data extraction with path traversal and default fallbacks
- List element extraction with bounds checking and type validation
- Weather data extraction with structured parsing methods
- Complete weather data integration with multiple API sources
- Error handling patterns and safe default return values
- Integration with malformed or incomplete API responses
"""

import unittest
from unittest.mock import Mock
from datetime import datetime

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WeatherDashboard.utils.api_utils import ApiUtils


class TestApiUtils(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.api_utils = ApiUtils()
        
        # Sample API response for testing
        self.sample_api_response = {
            "coord": {"lat": 40.7128, "lon": -74.006},
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01d"
                }
            ],
            "main": {
                "temp": 25.5,
                "feels_like": 27.0,
                "temp_min": 20.0,
                "temp_max": 30.0,
                "pressure": 1013.25,
                "humidity": 60
            },
            "wind": {
                "speed": 3.5,
                "deg": 90,
                "gust": 5.0
            },
            "rain": {"1h": 2.5, "3h": 6.0},
            "snow": {"1h": 0.0, "3h": 0.0},
            "clouds": {"all": 20},
            "visibility": 10000
        }

    def test_safe_get_nested_simple_keys(self):
        """Test safe_get_nested with simple key access."""
        data = {"temperature": 25.5, "humidity": 60}

        # Test existing keys
        self.assertEqual(self.api_utils.safe_get_nested(data, "temperature"), 25.5)
        self.assertEqual(self.api_utils.safe_get_nested(data, "humidity"), 60)

        # Test non-existing keys
        self.assertIsNone(self.api_utils.safe_get_nested(data, "missing"))
        
        # Test missing key with default
        self.assertIsNone(self.api_utils.safe_get_nested(data, "pressure"))
        self.assertEqual(self.api_utils.safe_get_nested(data, "pressure", default="default"), "default")

    def test_safe_get_nested_multiple_keys(self):
        """Test safe_get_nested with multiple key traversal."""
        # Test existing nested key
        result = self.api_utils.safe_get_nested(self.sample_api_response, "main", "temp")
        self.assertEqual(result, 25.5)

        # Test non-existing nested key
        result = self.api_utils.safe_get_nested(self.sample_api_response, "main", "missing")
        self.assertIsNone(result)

        # Test non-existing parent key
        result = self.api_utils.safe_get_nested(self.sample_api_response, "missing", "key")
        self.assertIsNone(result)

    def test_safe_get_nested_with_none_data(self):
        """Test safe_get_nested with None or invalid data."""
        test_cases = [
            (None, "key", None),
            ([], "key", None),
            ("string", "key", None),
            (123, "key", None)
        ]

        for data, key, expected in test_cases:
            with self.subTest(data=data, key=key):
                result = self.api_utils.safe_get_nested(data, key)
                self.assertEqual(result, expected)

    def test_safe_get_nested_with_defaults(self):
        """Test safe_get_nested with default values."""
        # Test with default for missing path
        result = self.api_utils.safe_get_nested(self.sample_api_response, "missing", "key", default="default")
        self.assertEqual(result, "default")

        # Test with default for valid path (should return actual value)
        result = self.api_utils.safe_get_nested(self.sample_api_response, "main", "temp", default="default")
        self.assertEqual(result, 25.5)

    def test_safe_get_list_item_valid_list(self):
        """Test safe_get_list_item with valid list data."""
        # Test with weather array
        result = self.api_utils.safe_get_list_item(self.sample_api_response, "weather", 0, "description")
        self.assertEqual(result, "clear sky")

        # Test with non-existing index
        result = self.api_utils.safe_get_list_item(self.sample_api_response, "weather", 1, "description")
        self.assertIsNone(result)

        # Test with non-existing list key
        result = self.api_utils.safe_get_list_item(self.sample_api_response, "missing", 0, "description")
        self.assertIsNone(result)

        # Test getting whole item
        result = self.api_utils.safe_get_list_item(self.sample_api_response, "weather", 0)
        expected = {
            "main": "Clear",
            "description": "clear sky", 
            "id": 800,
            "icon": "01d"
        }
        self.assertEqual(result, expected)

    def test_safe_get_list_item_invalid_data(self):
        """Test safe_get_list_item with invalid or missing data."""
        test_cases = [
            ({"weather": []}, "weather", 0, "description", None),  # Empty list
            ({"weather": None}, "weather", 0, "description", None),  # None value
            ({}, "weather", 0, "description", None),  # Missing key
            ({"weather": "string"}, "weather", 0, "description", None),  # Non-list value
            ({"weather": 123}, "weather", 0, "description", None)  # Non-list value
        ]
        
        for data, list_key, index, item_key, expected in test_cases:
            with self.subTest(data=data, list_key=list_key):
                result = self.api_utils.safe_get_list_item(data, list_key, index, item_key)
                self.assertEqual(result, expected)

    def test_safe_get_list_item_with_defaults(self):
        """Test safe_get_list_item with default values."""
        # Test missing key with default
        result = self.api_utils.safe_get_list_item({}, "weather", 0, "description", "default")
        self.assertEqual(result, "default")

        # Test missing index with default
        result = self.api_utils.safe_get_list_item(self.sample_api_response, "weather", 1, "description", "default")
        self.assertEqual(result, "default")

        # Test valid data with default (should return actual value)
        result = self.api_utils.safe_get_list_item(self.sample_api_response, "weather", 0, "description", "default")
        self.assertEqual(result, "clear sky")
        
        # Test empty list with default
        result = self.api_utils.safe_get_list_item({"weather": []}, "weather", 0, "description", "default")
        self.assertEqual(result, "default")

    def test_extract_weather_main_data(self):
        """Test extract_weather_main_data with complete main data."""
        result = self.api_utils.extract_weather_main_data(self.sample_api_response)
        
        self.assertEqual(result.temperature, 25.5)
        self.assertEqual(result.feels_like, 27.0)
        self.assertEqual(result.temp_min, 20.0)
        self.assertEqual(result.temp_max, 30.0)
        self.assertEqual(result.pressure, 1013.25)
        self.assertEqual(result.humidity, 60)

    def test_extract_weather_main_data_partial(self):
        """Test extract_weather_main_data with partial main data."""
        partial_data = {
            "main": {
                "temp": 22.0
                # Missing other temperature fields
            }
        }

        result = self.api_utils.extract_weather_main_data(partial_data)
        
        self.assertEqual(result.temperature, 22.0)
        self.assertIsNone(result.feels_like)
        self.assertIsNone(result.temp_min)
        self.assertIsNone(result.temp_max)
        self.assertIsNone(result.pressure)
        self.assertIsNone(result.humidity)

    def test_extract_weather_main_data_missing(self):
        """Test extract_weather_main_data with missing main section."""
        result = self.api_utils.extract_weather_main_data({})
        
        self.assertIsNone(result.temperature)
        self.assertIsNone(result.feels_like)
        self.assertIsNone(result.temp_min)
        self.assertIsNone(result.temp_max)
        self.assertIsNone(result.pressure)
        self.assertIsNone(result.humidity)

    def test_extract_weather_wind_data_complete(self):
        """Test extract_weather_wind_data with complete wind information."""
        result = self.api_utils.extract_weather_wind_data(self.sample_api_response)
        
        self.assertEqual(result.wind_speed, 3.5)
        self.assertEqual(result.wind_direction, 90)
        self.assertEqual(result.wind_gust, 5.0)

    def test_extract_weather_wind_data_partial(self):
        """Test extract_weather_wind_data with partial wind information."""
        partial_data = {
            "wind": {
                "speed": 3.5,
                "deg": 90
                # Missing gust
            }
        }

        result = self.api_utils.extract_weather_wind_data(partial_data)
        
        self.assertEqual(result.wind_speed, 3.5)
        self.assertEqual(result.wind_direction, 90)
        self.assertIsNone(result.wind_gust)

    def test_extract_weather_wind_data_missing(self):
        """Test extract_weather_wind_data with missing wind section."""
        result = self.api_utils.extract_weather_wind_data({})
        
        self.assertIsNone(result.wind_speed)
        self.assertIsNone(result.wind_direction)
        self.assertIsNone(result.wind_gust)

    def test_extract_weather_conditions_data(self):
        """Test extract_weather_conditions_data with valid weather data."""
        result = self.api_utils.extract_weather_conditions_data(self.sample_api_response)
        
        self.assertEqual(result.conditions, "Clear Sky")  # Title case from "clear sky"
        self.assertEqual(result.weather_main, "Clear")
        self.assertEqual(result.weather_id, 800)
        self.assertEqual(result.weather_icon, "01d")

    def test_extract_weather_conditions_data_missing(self):
        """Test extract_weather_conditions_data with missing weather data."""
        test_cases = [
            ({}),  # No weather key
            ({"weather": []}),  # Empty weather list
            ({"weather": [{}]}),  # Weather object without description
        ]

        for data in test_cases:
            with self.subTest(data=data):
                result = self.api_utils.extract_weather_conditions_data(data)
                
                self.assertEqual(result.conditions, "--")
                self.assertIsNone(result.weather_main)
                self.assertIsNone(result.weather_id)
                self.assertIsNone(result.weather_icon)

    def test_extract_precipitation_data_with_both_types(self):
        """Test extract_precipitation_data with both rain and snow data."""
        result = self.api_utils.extract_precipitation_data(self.sample_api_response)
        
        self.assertEqual(result.rain, 2.5)  # 1h rain
        self.assertEqual(result.snow, 0.0)  # 1h snow
        self.assertEqual(result.rain_1h, 2.5)
        self.assertEqual(result.rain_3h, 6.0)
        self.assertEqual(result.snow_1h, 0.0)
        self.assertEqual(result.snow_3h, 0.0)

    def test_extract_precipitation_data_partial_data(self):
        """Test extract_precipitation_data with partial precipitation data."""
        partial_data = {
            "rain": {"3h": 5.0},  # Only 3h data
            # No snow data
        }

        result = self.api_utils.extract_precipitation_data(partial_data)
        
        # The actual implementation calculates 3h/3 when 1h is not available
        expected_rain_1h = 5.0 / 3
        self.assertEqual(result.rain, expected_rain_1h)  # Uses 3h/3 when 1h not available
        self.assertIsNone(result.snow)  # No snow
        self.assertIsNone(result.rain_1h)  # No 1h data available
        self.assertEqual(result.rain_3h, 5.0)
        self.assertIsNone(result.snow_1h)
        self.assertIsNone(result.snow_3h)

    def test_extract_precipitation_data_missing_data(self):
        """Test extract_precipitation_data with no precipitation data."""
        result = self.api_utils.extract_precipitation_data({})
        
        self.assertIsNone(result.rain)
        self.assertIsNone(result.snow)
        self.assertIsNone(result.rain_1h)
        self.assertIsNone(result.rain_3h)
        self.assertIsNone(result.snow_1h)
        self.assertIsNone(result.snow_3h)

    def test_extract_atmospheric_data(self):
        """Test extract_atmospheric_data with valid atmospheric data."""
        result = self.api_utils.extract_atmospheric_data(self.sample_api_response)
        
        self.assertEqual(result.visibility, 10000)
        self.assertEqual(result.cloud_cover, 20)

    def test_extract_atmospheric_data_missing(self):
        """Test extract_atmospheric_data with missing atmospheric data."""
        result = self.api_utils.extract_atmospheric_data({})
        
        self.assertIsNone(result.visibility)
        self.assertIsNone(result.cloud_cover)

    def test_extract_coordinates(self):
        """Test extract_coordinates with valid coordinate data."""
        result = self.api_utils.extract_coordinates(self.sample_api_response)
        
        self.assertEqual(result.latitude, 40.7128)
        self.assertEqual(result.longitude, -74.006)

    def test_extract_coordinates_missing(self):
        """Test extract_coordinates with missing coordinate data."""
        result = self.api_utils.extract_coordinates({})
        
        self.assertIsNone(result.latitude)
        self.assertIsNone(result.longitude)

    def test_extract_complete_weather_data(self):
        """Test extract_complete_weather_data with all data sources."""
        uv_data = {"value": 7.5}
        air_quality_data = {
            "list": [
                {
                    "main": {"aqi": 3}
                }
            ]
        }

        result = self.api_utils.extract_complete_weather_data(
            self.sample_api_response,
            uv_data,
            air_quality_data
        )
        
        # Test main data
        self.assertEqual(result.main_data.temperature, 25.5)
        self.assertEqual(result.main_data.humidity, 60)
        
        # Test wind data
        self.assertEqual(result.wind_data.wind_speed, 3.5)
        self.assertEqual(result.wind_data.wind_direction, 90)
        
        # Test conditions data
        self.assertEqual(result.conditions_data.conditions, "Clear Sky")  # Title case
        self.assertEqual(result.conditions_data.weather_main, "Clear")
        self.assertEqual(result.conditions_data.weather_id, 800)
        self.assertEqual(result.conditions_data.weather_icon, "01d")
        
        # Test precipitation data
        self.assertEqual(result.precipitation_data.rain, 2.5)
        
        # Test atmospheric data
        self.assertEqual(result.atmospheric_data.visibility, 10000)
        
        # Test coordinates
        self.assertEqual(result.coordinates.latitude, 40.7128)
        self.assertEqual(result.coordinates.longitude, -74.006)
        
        # Test UV and air quality data
        self.assertEqual(result.uv_index, 7.5)
        self.assertEqual(result.air_quality_index, 3)
        self.assertEqual(result.air_quality_description, "Moderate")
        
        # Test metadata
        self.assertEqual(result.transformation_status, "success")
        self.assertGreater(result.extraction_success_rate, 0.9)
        self.assertEqual(len(result.missing_fields), 0)

    def test_extract_complete_weather_data_minimal(self):
        """Test extract_complete_weather_data with minimal data."""
        result = self.api_utils.extract_complete_weather_data({})
        
        # All fields should be None or default values
        self.assertIsNone(result.main_data.temperature)
        self.assertIsNone(result.wind_data.wind_speed)
        self.assertEqual(result.conditions_data.conditions, "--")
        self.assertIsNone(result.precipitation_data.rain)
        self.assertIsNone(result.atmospheric_data.visibility)
        self.assertIsNone(result.coordinates.latitude)
        
        # Test metadata
        self.assertEqual(result.transformation_status, "failed")
        self.assertLess(result.extraction_success_rate, 0.5)
        self.assertGreater(len(result.missing_fields), 0)

    def test_get_aqi_description(self):
        """Test get_aqi_description with various AQI values."""
        test_cases = [
            (1, "Good"),
            (2, "Fair"),
            (3, "Moderate"),
            (4, "Poor"),
            (5, "Very Poor"),
            (None, "Unknown"),
            (0, "Unknown"),  # Invalid AQI
            (6, "Unknown"),  # Invalid AQI
        ]

        for aqi, expected in test_cases:
            with self.subTest(aqi=aqi):
                result = self.api_utils.get_aqi_description(aqi)
                self.assertEqual(result, expected)

    def test_validate_api_response_structure_valid(self):
        """Test validate_api_response_structure with valid response."""
        required_sections = ["main", "weather", "wind"]
        result = self.api_utils.validate_api_response_structure(
            self.sample_api_response,
            required_sections
        )
        
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.missing_sections), 0)
        self.assertEqual(result.validation_status, "success")
        self.assertIsNone(result.error_message)

    def test_validate_api_response_structure_missing_sections(self):
        """Test validate_api_response_structure with missing sections."""
        required_sections = ["main", "weather", "missing_section"]
        result = self.api_utils.validate_api_response_structure(
            self.sample_api_response,
            required_sections
        )
        
        self.assertFalse(result.is_valid)
        self.assertIn("missing_section", result.missing_sections)
        self.assertEqual(result.validation_status, "partial")
        self.assertIsNotNone(result.error_message)

    def test_validate_api_response_structure_invalid_data(self):
        """Test validate_api_response_structure with invalid data types."""
        test_cases = [
            (None, ["main"]),
            ([], ["main"]),
            ("string", ["main"]),
            (123, ["main"]),
        ]

        for data, required_sections in test_cases:
            with self.subTest(data=type(data).__name__):
                result = self.api_utils.validate_api_response_structure(data, required_sections)
                
                self.assertFalse(result.is_valid)
                self.assertEqual(result.validation_status, "failed")
                self.assertIsNotNone(result.error_message)

    def test_error_handling_with_malformed_data(self):
        """Test all functions handle malformed API responses gracefully."""
        malformed_responses = [
            None,
            [],
            "string",
            123,
            {"weather": "not_a_list"},
            {"main": []},
            {"wind": "not_a_dict"},
            {"coord": [40.7, -74.0]},  # Should be dict, not list
        ]

        functions_to_test = [
            (self.api_utils.extract_weather_main_data, []),
            (self.api_utils.extract_weather_wind_data, []),
            (self.api_utils.extract_weather_conditions_data, []),
            (self.api_utils.extract_precipitation_data, []),
            (self.api_utils.extract_atmospheric_data, []),
            (self.api_utils.extract_coordinates, []),
            (self.api_utils.extract_complete_weather_data, []),
        ]

        for malformed_data in malformed_responses:
            for func, extra_args in functions_to_test:
                with self.subTest(data=type(malformed_data).__name__, func=func.__name__):
                    try:
                        result = func(malformed_data, *extra_args)
                        # Should return dataclass objects or appropriate type, not crash
                        self.assertIsNotNone(result)
                        # The extract methods return dataclass objects, not dicts
                        if func.__name__.startswith('extract_'):
                            # Check that it's a dataclass object (has attributes)
                            self.assertTrue(hasattr(result, '__dataclass_fields__'))
                    except Exception as e:
                        self.fail(f"{func.__name__} should handle malformed data gracefully, but raised {e}")

    def test_safe_get_nested_deep_nesting(self):
        """Test safe_get_nested with deeply nested data."""
        deep_data = {
            "level1": {
                "level2": {
                    "level3": {
                        "value": "found"
                    }
                }
            }
        }
        
        # Test valid deep path
        result = self.api_utils.safe_get_nested(deep_data, "level1", "level2", "level3", "value")
        self.assertEqual(result, "found")
        
        # Test path that goes too deep
        result = self.api_utils.safe_get_nested(deep_data, "level1", "level2", "level3", "value", "too_deep")
        self.assertIsNone(result)
        
        # Test path with non-dict intermediate value
        mixed_data = {
            "level1": {
                "level2": "string_value"  # Not a dict
            }
        }
        
        result = self.api_utils.safe_get_nested(mixed_data, "level1", "level2", "level3")
        self.assertIsNone(result)

    def test_safe_get_list_item_boundary_conditions(self):
        """Test safe_get_list_item with boundary conditions."""
        data_with_list = {
            "items": ["first", "second", "third"]
        }

        # Test valid indices
        self.assertEqual(self.api_utils.safe_get_list_item(data_with_list, "items", 0), "first")
        self.assertEqual(self.api_utils.safe_get_list_item(data_with_list, "items", 2), "third")

        # Test boundary conditions
        self.assertIsNone(self.api_utils.safe_get_list_item(data_with_list, "items", -1))  # Negative index
        self.assertIsNone(self.api_utils.safe_get_list_item(data_with_list, "items", 3))   # Out of bounds
        self.assertIsNone(self.api_utils.safe_get_list_item(data_with_list, "items", 10))  # Far out of bounds

    def test_type_safety_and_conversion(self):
        """Test type safety in all extraction functions."""
        # All functions should handle various data types gracefully
        test_data_types = [None, "", 0, [], {}, "string", 123.45]

        for test_data in test_data_types:
            with self.subTest(data_type=type(test_data).__name__):
                # These should all return safely without crashing
                self.api_utils.extract_weather_main_data(test_data)
                self.api_utils.extract_weather_wind_data(test_data)
                self.api_utils.extract_weather_conditions_data(test_data)
                self.api_utils.extract_precipitation_data(test_data)
                self.api_utils.extract_atmospheric_data(test_data)
                self.api_utils.extract_coordinates(test_data)
                self.api_utils.extract_complete_weather_data(test_data)


if __name__ == '__main__':
    unittest.main()