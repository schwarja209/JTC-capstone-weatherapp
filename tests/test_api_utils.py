"""
Test for WeatherDashboard.utils.api_utils

Covers: ApiUtils basic functionality
"""
import unittest
from unittest.mock import Mock, patch
from WeatherDashboard.utils.api_utils import ApiUtils

class TestApiUtils(unittest.TestCase):
    """Test cases for ApiUtils class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_utils = ApiUtils()
        self.sample_api_response = {
            "coord": {"lat": 40.7128, "lon": -74.0060},
            "weather": [
                {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}
            ],
            "main": {
                "temp": 25.0, "feels_like": 26.0, "temp_min": 20.0, "temp_max": 30.0,
                "pressure": 1013, "humidity": 60
            },
            "wind": {"speed": 5.0, "deg": 180},
            "rain": {"1h": 0.5},
            "snow": {"1h": 0.0},
            "clouds": {"all": 20},
            "visibility": 10000,
            "dt": 1640995200,
            "sys": {
                "type": 2, "id": 2004861, "country": "US", "sunrise": 1640952000, "sunset": 1640988000
            },
            "timezone": -18000,
            "id": 5128581,
            "name": "New York"
        }

    def test_get_aqi_description(self):
        """Test getting AQI description."""
        descriptions = {
            1: "Good",
            2: "Fair", 
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }
        for aqi, expected in descriptions.items():
            result = self.api_utils.get_aqi_description(aqi)
            self.assertEqual(result, expected)

    def test_get_aqi_description_invalid(self):
        """Test getting AQI description with invalid input."""
        result = self.api_utils.get_aqi_description(0)
        self.assertEqual(result, "Unknown")
        
        result = self.api_utils.get_aqi_description(6)
        self.assertEqual(result, "Unknown")

    def test_api_utils_initialization(self):
        """Test that ApiUtils can be instantiated."""
        self.assertIsInstance(self.api_utils, ApiUtils)