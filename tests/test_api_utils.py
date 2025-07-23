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
        """Set up test fixtures with comprehensive API response data."""
        self.sample_api_response = {
            "main": {
                "temp": 25.5,
                "humidity": 60,
                "pressure": 1013.25,
                "feels_like": 27.0,
                "temp_min": 20.0,
                "temp_max": 30.0
            },
            "weather": [
                {
                    "main": "Clear",
                    "description": "clear sky",
                    "id": 800,
                    "icon": "01d"
                }
            ],
            "wind": {
                "speed": 5.2,
                "deg": 180,
                "gust": 8.1
            },
            "coord": {
                "lat": 40.7128,
                "lon": -74.0060
            },
            "visibility": 10000,
            "clouds": {
                "all": 20
            },
            "rain": {
                "1h": 2.5,
                "3h": 6.0
            },
            "snow": {
                "1h": 1.0,
                "3h": 2.5
            }
        }

    def test_safe_get_nested_simple_keys(self):
        """Test safe_get_nested with simple key access."""
        data = {"temperature": 25.5, "humidity": 60}
        
        # Test existing keys
        self.assertEqual(ApiUtils.safe_get_nested(data, "temperature"), 25.5)
        self.assertEqual(ApiUtils.safe_get_nested(data, "humidity"), 60)
        
        # Test missing key with default
        self.assertIsNone(ApiUtils.safe_get_nested(data, "pressure"))
        self.assertEqual(ApiUtils.safe_get_nested(data, "pressure", default="default"), "default")

    def test_safe_get_nested_multiple_keys(self):
        """Test safe_get_nested with multiple key traversal."""
        # Test existing nested key
        result = ApiUtils.safe_get_nested(self.sample_api_response, "main", "temp")
        self.assertEqual(result, 25.5)
        
        # Test missing nested key
        result = ApiUtils.safe_get_nested(self.sample_api_response, "main", "missing")
        self.assertIsNone(result)
        
        # Test missing parent key
        result = ApiUtils.safe_get_nested(self.sample_api_response, "missing", "temp")
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
                result = ApiUtils.safe_get_nested(data, key)
                self.assertEqual(result, expected)

    def test_safe_get_nested_with_defaults(self):
        """Test safe_get_nested with default values."""
        # Test with default for missing path
        result = ApiUtils.safe_get_nested(self.sample_api_response, "missing", "key", default="default")
        self.assertEqual(result, "default")
        
        # Test with default for valid path (should return actual value)
        result = ApiUtils.safe_get_nested(self.sample_api_response, "main", "temp", default="default")
        self.assertEqual(result, 25.5)

    def test_safe_get_list_item_valid_list(self):
        """Test safe_get_list_item with valid list data."""
        # Test with weather array
        result = ApiUtils.safe_get_list_item(self.sample_api_response, "weather", 0, "description")
        self.assertEqual(result, "clear sky")
        
        # Test getting whole item
        result = ApiUtils.safe_get_list_item(self.sample_api_response, "weather", 0)
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
                result = ApiUtils.safe_get_list_item(data, list_key, index, item_key)
                self.assertEqual(result, expected)

    def test_safe_get_list_item_with_defaults(self):
        """Test safe_get_list_item with default values."""
        # Test missing key with default
        result = ApiUtils.safe_get_list_item({}, "weather", 0, "description", "default")
        self.assertEqual(result, "default")
        
        # Test empty list with default
        result = ApiUtils.safe_get_list_item({"weather": []}, "weather", 0, "description", "default")
        self.assertEqual(result, "default")

    def test_extract_weather_main_data(self):
        """Test extract_weather_main_data with complete main data."""
        result = ApiUtils.extract_weather_main_data(self.sample_api_response)
        expected = {
            'temperature': 25.5,
            'humidity': 60,
            'pressure': 1013.25,
            'feels_like': 27.0,
            'temp_min': 20.0,
            'temp_max': 30.0,
        }
        self.assertEqual(result, expected)

    def test_extract_weather_main_data_partial(self):
        """Test extract_weather_main_data with partial main data."""
        partial_data = {
            "main": {
                "temp": 22.0
                # Missing other temperature fields
            }
        }
        
        result = ApiUtils.extract_weather_main_data(partial_data)
        expected = {
            'temperature': 22.0,
            'humidity': None,
            'pressure': None,
            'feels_like': None,
            'temp_min': None,
            'temp_max': None,
        }
        self.assertEqual(result, expected)

    def test_extract_weather_main_data_missing(self):
        """Test extract_weather_main_data with missing main section."""
        result = ApiUtils.extract_weather_main_data({})
        expected = {
            'temperature': None,
            'humidity': None,
            'pressure': None,
            'feels_like': None,
            'temp_min': None,
            'temp_max': None,
        }
        self.assertEqual(result, expected)

    def test_extract_weather_wind_data_complete(self):
        """Test extract_weather_wind_data with complete wind information."""
        result = ApiUtils.extract_weather_wind_data(self.sample_api_response)
        expected = {
            "wind_speed": 5.2,
            "wind_direction": 180,
            "wind_gust": 8.1
        }
        self.assertEqual(result, expected)

    def test_extract_weather_wind_data_partial(self):
        """Test extract_weather_wind_data with partial wind information."""
        partial_data = {
            "wind": {
                "speed": 3.5,
                "deg": 90
                # Missing gust
            }
        }
        
        result = ApiUtils.extract_weather_wind_data(partial_data)
        expected = {
            "wind_speed": 3.5,
            "wind_direction": 90,
            "wind_gust": None
        }
        self.assertEqual(result, expected)

    def test_extract_weather_wind_data_missing(self):
        """Test extract_weather_wind_data with missing wind section."""
        result = ApiUtils.extract_weather_wind_data({})
        expected = {
            "wind_speed": None,
            "wind_direction": None,
            "wind_gust": None
        }
        self.assertEqual(result, expected)

    def test_extract_weather_conditions_data(self):
        """Test extract_weather_conditions_data with valid weather data."""
        result = ApiUtils.extract_weather_conditions_data(self.sample_api_response)
        expected = {
            'conditions': "Clear Sky",  # Title case from "clear sky"
            'weather_main': "Clear",
            'weather_id': 800,
            'weather_icon': "01d",
        }
        self.assertEqual(result, expected)

    def test_extract_weather_conditions_data_missing(self):
        """Test extract_weather_conditions_data with missing weather data."""
        test_cases = [
            ({}),  # No weather key
            ({"weather": []}),  # Empty weather list
            ({"weather": [{}]}),  # Weather object without description
        ]
        
        for data in test_cases:
            with self.subTest(data=data):
                result = ApiUtils.extract_weather_conditions_data(data)
                expected = {
                    'conditions': "--",  # Default value
                    'weather_main': None,
                    'weather_id': None,
                    'weather_icon': None,
                }
                self.assertEqual(result, expected)

    def test_extract_precipitation_data_with_both_types(self):
        """Test extract_precipitation_data with both rain and snow data."""
        result = ApiUtils.extract_precipitation_data(self.sample_api_response)
        expected = {
            "rain": 2.5,  # Prefers 1h over 3h
            "snow": 1.0,  # Prefers 1h over 3h
            "rain_1h": 2.5,
            "rain_3h": 6.0,
            "snow_1h": 1.0,
            "snow_3h": 2.5
        }
        self.assertEqual(result, expected)

    def test_extract_precipitation_data_partial_data(self):
        """Test extract_precipitation_data with partial precipitation data."""
        partial_data = {
            "rain": {"3h": 5.0},  # Only 3h data
            # No snow data
        }
        
        result = ApiUtils.extract_precipitation_data(partial_data)
        # The helper function should return 3h data divided by 3 for 1h estimate
        expected_rain_1h = 5.0 / 3
        expected = {
            "rain": expected_rain_1h,  # Uses 3h/3 when 1h not available
            "snow": None,  # No snow data
            "rain_1h": None,
            "rain_3h": 5.0,
            "snow_1h": None,
            "snow_3h": None
        }
        self.assertEqual(result, expected)

    def test_extract_precipitation_data_missing_data(self):
        """Test extract_precipitation_data with no precipitation data."""
        result = ApiUtils.extract_precipitation_data({})
        expected = {
            "rain": None,
            "snow": None,
            "rain_1h": None,
            "rain_3h": None,
            "snow_1h": None,
            "snow_3h": None
        }
        self.assertEqual(result, expected)

    def test_extract_atmospheric_data(self):
        """Test extract_atmospheric_data with valid atmospheric data."""
        result = ApiUtils.extract_atmospheric_data(self.sample_api_response)
        expected = {
            'visibility': 10000,
            'cloud_cover': 20,
        }
        self.assertEqual(result, expected)

    def test_extract_atmospheric_data_missing(self):
        """Test extract_atmospheric_data with missing atmospheric data."""
        result = ApiUtils.extract_atmospheric_data({})
        expected = {
            'visibility': None,
            'cloud_cover': None,
        }
        self.assertEqual(result, expected)

    def test_extract_coordinates(self):
        """Test extract_coordinates with valid coordinate data."""
        result = ApiUtils.extract_coordinates(self.sample_api_response)
        expected = {
            'latitude': 40.7128,
            'longitude': -74.0060,
        }
        self.assertEqual(result, expected)

    def test_extract_coordinates_missing(self):
        """Test extract_coordinates with missing coordinate data."""
        result = ApiUtils.extract_coordinates({})
        expected = {
            'latitude': None,
            'longitude': None,
        }
        self.assertEqual(result, expected)

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
        
        result = ApiUtils.extract_complete_weather_data(
            self.sample_api_response, 
            uv_data, 
            air_quality_data
        )
        
        # Check that all sections are included
        self.assertIn('temperature', result)
        self.assertIn('wind_speed', result)
        self.assertIn('conditions', result)
        self.assertIn('rain', result)
        self.assertIn('visibility', result)
        self.assertIn('latitude', result)
        self.assertIn('uv_index', result)
        self.assertIn('air_quality_index', result)
        self.assertIn('air_quality_description', result)
        self.assertIn('date', result)
        
        # Check specific values
        self.assertEqual(result['temperature'], 25.5)
        self.assertEqual(result['uv_index'], 7.5)
        self.assertEqual(result['air_quality_index'], 3)
        self.assertEqual(result['air_quality_description'], "Moderate")
        self.assertIsInstance(result['date'], datetime)

    def test_extract_complete_weather_data_minimal(self):
        """Test extract_complete_weather_data with minimal data."""
        result = ApiUtils.extract_complete_weather_data({})
        
        # Should still have all expected keys with None/default values
        expected_keys = [
            'date', 'temperature', 'humidity', 'pressure', 'feels_like', 
            'temp_min', 'temp_max', 'wind_speed', 'wind_direction', 'wind_gust',
            'conditions', 'weather_main', 'weather_id', 'weather_icon',
            'rain', 'snow', 'rain_1h', 'rain_3h', 'snow_1h', 'snow_3h',
            'visibility', 'cloud_cover', 'latitude', 'longitude'
        ]
        
        for key in expected_keys:
            self.assertIn(key, result)

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
                result = ApiUtils.get_aqi_description(aqi)
                self.assertEqual(result, expected)

    def test_validate_api_response_structure_valid(self):
        """Test validate_api_response_structure with valid response."""
        required_sections = ["main", "weather", "wind"]
        result = ApiUtils.validate_api_response_structure(
            self.sample_api_response, 
            required_sections
        )
        self.assertTrue(result)

    def test_validate_api_response_structure_missing_sections(self):
        """Test validate_api_response_structure with missing sections."""
        required_sections = ["main", "weather", "missing_section"]
        result = ApiUtils.validate_api_response_structure(
            self.sample_api_response, 
            required_sections
        )
        self.assertFalse(result)

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
                result = ApiUtils.validate_api_response_structure(data, required_sections)
                self.assertFalse(result)

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
            (ApiUtils.extract_weather_main_data, []),
            (ApiUtils.extract_weather_wind_data, []),
            (ApiUtils.extract_weather_conditions_data, []),
            (ApiUtils.extract_precipitation_data, []),
            (ApiUtils.extract_atmospheric_data, []),
            (ApiUtils.extract_coordinates, []),
            (ApiUtils.extract_complete_weather_data, []),
        ]
        
        for malformed_data in malformed_responses:
            for func, extra_args in functions_to_test:
                with self.subTest(data=type(malformed_data).__name__, func=func.__name__):
                    try:
                        result = func(malformed_data, *extra_args)
                        # Should return dict or appropriate type, not crash
                        self.assertIsNotNone(result)
                        if func.__name__.startswith('extract_'):
                            self.assertIsInstance(result, dict)
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
        result = ApiUtils.safe_get_nested(deep_data, "level1", "level2", "level3", "value")
        self.assertEqual(result, "found")
        
        # Test path that goes too deep
        result = ApiUtils.safe_get_nested(deep_data, "level1", "level2", "level3", "value", "too_deep")
        self.assertIsNone(result)
        
        # Test path with non-dict intermediate value
        mixed_data = {
            "level1": {
                "level2": "string_value"  # Not a dict
            }
        }
        
        result = ApiUtils.safe_get_nested(mixed_data, "level1", "level2", "level3")
        self.assertIsNone(result)

    def test_safe_get_list_item_boundary_conditions(self):
        """Test safe_get_list_item with boundary conditions."""
        data_with_list = {
            "items": ["first", "second", "third"]
        }
        
        # Test valid indices
        self.assertEqual(ApiUtils.safe_get_list_item(data_with_list, "items", 0), "first")
        self.assertEqual(ApiUtils.safe_get_list_item(data_with_list, "items", 2), "third")
        
        # Test out of bounds
        self.assertIsNone(ApiUtils.safe_get_list_item(data_with_list, "items", 5))
        self.assertIsNone(ApiUtils.safe_get_list_item(data_with_list, "items", -1))

    def test_type_safety_and_conversion(self):
        """Test type safety in all extraction functions."""
        # All functions should handle various data types gracefully
        test_data_types = [None, "", 0, [], {}, "string", 123.45]
        
        for test_data in test_data_types:
            with self.subTest(data_type=type(test_data).__name__):
                # These should all return safely without crashing
                ApiUtils.extract_weather_main_data(test_data)
                ApiUtils.extract_weather_wind_data(test_data)
                ApiUtils.extract_weather_conditions_data(test_data)
                ApiUtils.extract_precipitation_data(test_data)
                ApiUtils.extract_atmospheric_data(test_data)
                ApiUtils.extract_coordinates(test_data)


if __name__ == '__main__':
    unittest.main()