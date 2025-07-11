"""
Unit tests for WeatherDataManager class.

Tests core data management functionality including:
- Unit conversions between metric and imperial systems
- Fallback behavior when API calls fail
- Data storage and retrieval
- Memory cleanup operations
"""
import unittest
from unittest.mock import Mock, patch
from datetime import datetime

from WeatherDashboard.core.data_manager import WeatherDataManager
from WeatherDashboard.services.weather_service import WeatherAPIService

class TestWeatherDataManager(unittest.TestCase):
    def setUp(self):
        self.data_manager = WeatherDataManager()
        
    def test_convert_units_metric_to_imperial(self):
        """Test unit conversion from metric to imperial."""
        metric_data = {
            'temperature': 0,    # 0°C should be 32°F
            'pressure': 1013.25, # Should convert to ~29.92 inHg
            'wind_speed': 10     # Should convert to ~22.37 mph
        }
        
        result = self.data_manager.convert_units(metric_data, 'imperial')
        
        self.assertAlmostEqual(result['temperature'], 32.0, places=1)
        self.assertAlmostEqual(result['pressure'], 29.92, places=1) 
        self.assertAlmostEqual(result['wind_speed'], 22.37, places=1)
    
    def test_convert_units_same_system(self):
        """Test that no conversion happens when units are the same."""
        data = {'temperature': 25, 'humidity': 60}
        result = self.data_manager.convert_units(data, 'metric')
        
        self.assertEqual(result['temperature'], 25)
        self.assertEqual(result['humidity'], 60)
    
    @patch('WeatherDashboard.core.data_manager.WeatherAPIService')
    def test_fetch_current_with_fallback(self, mock_api_service):
        """Test fallback behavior when API fails."""
        # Mock API to return fallback data
        mock_api_service.return_value.fetch_current.return_value = (
            {'temperature': 20, 'source': 'simulated'}, 
            True,  # use_fallback = True
            Exception("API failed")
        )
        
        result_data, is_fallback, error = self.data_manager.fetch_current("TestCity", "metric")
        
        self.assertTrue(is_fallback)
        self.assertEqual(result_data['source'], 'simulated')
        self.assertIsInstance(error, Exception)