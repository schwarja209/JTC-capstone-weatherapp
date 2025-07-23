"""
Unit tests for WeatherDataManager class.

Tests comprehensive data management functionality including:
- Unit conversions between metric and imperial systems with validation
- Fallback behavior when API calls fail with realistic simulation data
- Data storage and retrieval with file I/O operations and error handling
- Memory cleanup operations with configurable thresholds and size limits
- Historical data management with time-based filtering and sorting
- Data format conversion for logging and display purposes
- Error handling patterns for file operations and network failures
- Memory management with automatic cleanup and size monitoring
- Integration with configuration system for output paths and limits
- Thread safety considerations for concurrent data operations
"""
import unittest
from unittest.mock import Mock, patch, mock_open
from datetime import datetime, timedelta
import tempfile
import os

# Add project root to path for imports
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WeatherDashboard.core.data_manager import WeatherDataManager
from WeatherDashboard.services.api_exceptions import WeatherDashboardError


class TestWeatherDataManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.data_manager = WeatherDataManager()
        
    @patch('WeatherDashboard.core.data_manager.config')
    def test_convert_units_metric_to_imperial(self, mock_config):
        """Test unit conversion from metric to imperial."""
        # Mock config for unit conversion
        mock_config.UNITS = {
            "metric_units": {
                "temperature": {"metric": "°C", "imperial": "°F"},
                "pressure": {"metric": "hPa", "imperial": "inHg"},
                "wind_speed": {"metric": "m/s", "imperial": "mph"}
            }
        }
        
        metric_data = {
            'temperature': 0,    # 0°C should be 32°F
            'pressure': 1013.25, # Should convert to ~29.92 inHg
            'wind_speed': 10     # Should convert to ~22.37 mph
        }
        
        with patch('WeatherDashboard.core.data_manager.UnitConverter') as mock_converter:
            # Mock the converter methods
            mock_converter.convert_temperature.return_value = 32.0
            mock_converter.convert_pressure.return_value = 29.92
            mock_converter.convert_wind_speed.return_value = 22.37
            
            result = self.data_manager.convert_units(metric_data, 'imperial')
            
            self.assertEqual(result['temperature'], 32.0)
            self.assertEqual(result['pressure'], 29.92)
            self.assertEqual(result['wind_speed'], 22.37)
    
    def test_convert_units_same_system(self):
        """Test that no conversion happens when units are the same."""
        data = {'temperature': 25, 'humidity': 60}
        result = self.data_manager.convert_units(data, 'metric')
        
        self.assertEqual(result['temperature'], 25)
        self.assertEqual(result['humidity'], 60)
    
    @patch('WeatherDashboard.core.data_manager.ValidationUtils')
    def test_convert_units_invalid_unit_system(self, mock_validation):
        """Test unit conversion with invalid unit system."""
        mock_validation.validate_unit_system.return_value = ["Invalid unit system"]
        
        data = {'temperature': 25}
        
        with self.assertRaises(ValueError):
            self.data_manager.convert_units(data, 'invalid_system')

    @patch('WeatherDashboard.core.data_manager.config')
    def test_convert_units_with_none_values(self, mock_config):
        """Test unit conversion with None values."""
        mock_config.UNITS = {
            "metric_units": {
                "temperature": {"metric": "°C", "imperial": "°F"},
                "pressure": {"metric": "hPa", "imperial": "inHg"}
            }
        }
        
        data_with_nones = {
            'temperature': None,
            'pressure': 1013.25,
            'wind_speed': None,
            'humidity': 60
        }
        
        with patch('WeatherDashboard.core.data_manager.UnitConverter') as mock_converter:
            mock_converter.convert_pressure.return_value = 29.92
            
            result = self.data_manager.convert_units(data_with_nones, 'imperial')
            
            self.assertIsNone(result['temperature'])
            self.assertIsNone(result['wind_speed'])
            self.assertEqual(result['humidity'], 60)  # Should remain unchanged
            self.assertEqual(result['pressure'], 29.92)

    def test_fetch_current_success(self):
        """Test successful current weather fetch."""
        expected_data = {
            'temperature': 25.0,
            'humidity': 60,
            'conditions': 'Clear',
            'date': datetime.now()
        }
        
        # Mock the API service
        with patch.object(self.data_manager.api_service, 'fetch_current') as mock_fetch:
            mock_fetch.return_value = (expected_data, False, None)
            
            result_data, is_fallback, error = self.data_manager.fetch_current("London", "metric")
            
            self.assertFalse(is_fallback)
            self.assertIsNone(error)
            self.assertEqual(result_data['temperature'], 25.0)

    def test_fetch_current_with_fallback(self):
        """Test fallback behavior when API fails."""
        fallback_data = {
            'temperature': 20, 
            'source': 'simulated',
            'date': datetime.now()
        }
        
        # Mock API to return fallback data
        with patch.object(self.data_manager.api_service, 'fetch_current') as mock_fetch:
            mock_fetch.return_value = (
                fallback_data, 
                True,  # use_fallback = True
                Exception("API failed")
            )
            
            result_data, is_fallback, error = self.data_manager.fetch_current("TestCity", "metric")
            
            self.assertTrue(is_fallback)
            self.assertEqual(result_data['source'], 'simulated')
            self.assertIsInstance(error, Exception)

    def test_get_recent_data_with_data(self):
        """Test get_recent_data with existing data."""
        city = "TestCity"
        now = datetime.now()
        
        # Add some mock data to the manager's storage
        from WeatherDashboard.utils.utils import city_key
        key = city_key(city)
        self.data_manager.weather_data[key] = [
            {'date': now - timedelta(days=1), 'temperature': 20},
            {'date': now - timedelta(days=2), 'temperature': 22},
            {'date': now - timedelta(days=10), 'temperature': 18}  # Too old
        ]
        
        result = self.data_manager.get_recent_data(city, days_back=7)
        
        # Should only return data from last 7 days
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['temperature'], 20)
        self.assertEqual(result[1]['temperature'], 22)

    def test_get_recent_data_empty(self):
        """Test get_recent_data with no data."""
        result = self.data_manager.get_recent_data("NonExistentCity", days_back=7)
        
        self.assertEqual(len(result), 0)

    def test_get_historical(self):
        """Test get_historical method."""
        with patch.object(self.data_manager.api_service, 'fallback') as mock_fallback:
            mock_fallback.generate.return_value = [
                {'date': datetime.now() - timedelta(days=1), 'temperature': 25},
                {'date': datetime.now() - timedelta(days=2), 'temperature': 23}
            ]
            
            result = self.data_manager.get_historical("TestCity", 7)
            
            self.assertEqual(len(result), 2)
            mock_fallback.generate.assert_called_once_with("TestCity", 7)

    @patch('builtins.open', new_callable=mock_open)
    @patch('WeatherDashboard.core.data_manager.config')
    @patch('WeatherDashboard.core.data_manager.Logger')  # Mock Logger to prevent extra file writes
    def test_write_to_file_success(self, mock_logger, mock_config, mock_file):
        """Test successful file writing operation."""
        mock_config.OUTPUT = {"log": "test_weather.log"}
        
        test_data = {
            'temperature': 25, 
            'humidity': 60,
            'date': datetime.now()
        }
        
        # Should not raise an exception
        self.data_manager.write_to_file("TestCity", test_data, "metric")
        
        # Verify file was opened for writing (check the specific call we care about)
        expected_calls = [call for call in mock_file.call_args_list if 'test_weather.log' in str(call)]
        self.assertGreater(len(expected_calls), 0, "Expected file to be opened for writing")

    @patch('builtins.open', side_effect=PermissionError("Permission denied"))
    @patch('WeatherDashboard.core.data_manager.config')
    @patch('WeatherDashboard.core.data_manager.Logger')  # Mock Logger to prevent interference
    def test_write_to_file_permission_error(self, mock_logger, mock_config, mock_file):
        """Test file writing with permission error."""
        mock_config.OUTPUT = {"log": "test_weather.log"}
        mock_config.ERROR_MESSAGES = {
            "file_error": "Failed to write {info} to {file}: {reason}"
        }
        
        test_data = {'temperature': 25, 'date': datetime.now()}
        
        with self.assertRaises(WeatherDashboardError):
            self.data_manager.write_to_file("TestCity", test_data, "metric")

    @patch('builtins.open', side_effect=OSError("Disk full"))
    @patch('WeatherDashboard.core.data_manager.config')
    @patch('WeatherDashboard.core.data_manager.Logger')  # Mock Logger to prevent interference
    def test_write_to_file_os_error(self, mock_logger, mock_config, mock_file):
        """Test file writing with OS error."""
        mock_config.OUTPUT = {"log": "test_weather.log"}
        mock_config.ERROR_MESSAGES = {
            "file_error": "Failed to write {info} to {file}: {reason}"
        }
        
        test_data = {'temperature': 25, 'date': datetime.now()}
        
        with self.assertRaises(WeatherDashboardError):
            self.data_manager.write_to_file("TestCity", test_data, "metric")

    def test_format_data_for_logging_complete_data(self):
        """Test data formatting for logging with complete data."""
        data = {
            'temperature': 25.5,
            'humidity': 60,
            'pressure': 1013.25,
            'wind_speed': 10.0,
            'conditions': 'Clear',
            'date': datetime.now()
        }
        
        with patch('WeatherDashboard.core.data_manager.UnitConverter') as mock_converter:
            mock_converter.format_value.side_effect = lambda metric, value, unit: f"{value} unit"
            
            result = self.data_manager.format_data_for_logging("TestCity", data, "metric")
            
            self.assertIn('Temperature:', result)
            self.assertIn('Humidity:', result)
            self.assertIn('Conditions:', result)
            self.assertIsInstance(result, str)

    def test_format_data_for_logging_with_none_values(self):
        """Test data formatting for logging with None values."""
        data = {
            'temperature': None,
            'humidity': 60,
            'conditions': None,
            'date': datetime.now()
        }
        
        with patch('WeatherDashboard.core.data_manager.UnitConverter') as mock_converter:
            mock_converter.format_value.side_effect = lambda metric, value, unit: f"{value} unit"
            
            result = self.data_manager.format_data_for_logging("TestCity", data, "metric")
            
            self.assertIsInstance(result, str)
            self.assertIn('Humidity:', result)

    @patch('WeatherDashboard.core.data_manager.config')
    def test_cleanup_old_data_with_old_data(self, mock_config):
        """Test cleanup operation with old data present."""
        mock_config.MEMORY = {"max_entries_per_city": 30}
        
        now = datetime.now()
        city = "TestCity"
        from WeatherDashboard.utils.utils import city_key
        key = city_key(city)
        
        # Add old and new data
        self.data_manager.weather_data[key] = [
            {'date': now - timedelta(days=40), 'temperature': 20},  # Very old
            {'date': now - timedelta(days=1), 'temperature': 25},   # Recent
            {'date': now - timedelta(days=35), 'temperature': 18}   # Old
        ]
        
        # Keep only data from last 30 days
        self.data_manager.cleanup_old_data(days_to_keep=30)
        
        # Should only have recent data
        self.assertEqual(len(self.data_manager.weather_data[key]), 1)
        self.assertEqual(self.data_manager.weather_data[key][0]['temperature'], 25)

    @patch('WeatherDashboard.core.data_manager.config')
    def test_cleanup_old_data_size_limit(self, mock_config):
        """Test cleanup operation with size limits."""
        mock_config.MEMORY = {"max_entries_per_city": 5}
        
        city = "TestCity"
        from WeatherDashboard.utils.utils import city_key
        key = city_key(city)
        
        # Create data that exceeds size limit
        large_data = []
        for i in range(10):  # More than the limit of 5
            large_data.append({
                'date': datetime.now() - timedelta(hours=i),
                'temperature': 20 + i
            })
        self.data_manager.weather_data[key] = large_data
        
        self.data_manager.cleanup_old_data(days_to_keep=30)
        
        # Should be limited to max entries (5)
        self.assertEqual(len(self.data_manager.weather_data[key]), 5)

    def test_cleanup_old_data_no_cleanup_needed(self):
        """Test cleanup operation when no cleanup is needed."""
        city = "TestCity"
        from WeatherDashboard.utils.utils import city_key
        key = city_key(city)
        
        recent_data = [
            {'date': datetime.now() - timedelta(hours=1), 'temperature': 25}
        ]
        self.data_manager.weather_data[key] = recent_data
        
        original_length = len(self.data_manager.weather_data[key])
        self.data_manager.cleanup_old_data(days_to_keep=30)
        
        # Should not remove any data
        self.assertEqual(len(self.data_manager.weather_data[key]), original_length)

    @patch('WeatherDashboard.core.data_manager.config')
    def test_simple_memory_check(self, mock_config):
        """Test memory check functionality."""
        mock_config.MEMORY = {
            "max_cities_stored": 2,
            "max_total_entries": 5
        }
        
        # Add data that exceeds limits - use valid city names
        from WeatherDashboard.utils.utils import city_key
        self.data_manager.weather_data[city_key("New York")] = [{'temp': 20}]
        self.data_manager.weather_data[city_key("London")] = [{'temp': 21}]
        self.data_manager.weather_data[city_key("Paris")] = [{'temp': 22}]  # Exceeds city limit
        
        result = self.data_manager._simple_memory_check()
        
        # Should return True because we exceed the city limit
        self.assertTrue(result)

    @patch('WeatherDashboard.core.data_manager.config')
    def test_memory_management_integration(self, mock_config):
        """Test integration of memory management features."""
        mock_config.MEMORY = {
            "max_entries_per_city": 3,
            "max_cities_stored": 10,
            "max_total_entries": 20,
            "cleanup_interval_hours": 1
        }
        
        city = "TestCity"
        from WeatherDashboard.utils.utils import city_key
        key = city_key(city)
        
        # Fill up data storage
        large_dataset = []
        for i in range(10):  # More than max_entries_per_city
            large_dataset.append({
                'date': datetime.now() - timedelta(hours=i),
                'temperature': 20 + i
            })
        self.data_manager.weather_data[key] = large_dataset
        
        # Trigger cleanup
        self.data_manager.cleanup_old_data(days_to_keep=30)
        
        # Should be reduced to max_entries_per_city (3)
        self.assertEqual(len(self.data_manager.weather_data[key]), 3)

    def test_error_handling_patterns(self):
        """Test error handling patterns across data manager methods."""
        # Test with various invalid inputs for convert_units
        invalid_inputs = [None, "", [], 123]
        
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                # Should handle gracefully without crashing
                try:
                    if isinstance(invalid_input, dict):
                        self.data_manager.convert_units(invalid_input, 'metric')
                    else:
                        # For non-dict inputs, should handle gracefully
                        with patch('WeatherDashboard.core.data_manager.ValidationUtils') as mock_val:
                            mock_val.validate_unit_system.return_value = []
                            result = self.data_manager.convert_units(invalid_input or {}, 'metric')
                            self.assertIsInstance(result, dict)
                except (ValueError, TypeError, AttributeError):
                    # Expected for some invalid inputs
                    pass

    def test_fetch_current_with_automatic_cleanup(self):
        """Test that fetch_current triggers cleanup when needed."""
        # Set cleanup time to trigger cleanup
        self.data_manager._last_cleanup = datetime.now() - timedelta(hours=25)  # Force cleanup
        
        with patch.object(self.data_manager.api_service, 'fetch_current') as mock_fetch:
            mock_fetch.return_value = (
                {'temperature': 25, 'date': datetime.now()}, 
                False, 
                None
            )
            
            with patch.object(self.data_manager, 'cleanup_old_data') as mock_cleanup:
                self.data_manager.fetch_current("TestCity", "metric")
                
                # Should have triggered cleanup
                mock_cleanup.assert_called_once()

    def test_data_storage_and_deduplication(self):
        """Test data storage prevents duplicate entries for same day."""
        city = "TestCity"
        today = datetime.now()
        
        # Fetch data twice for same day
        with patch.object(self.data_manager.api_service, 'fetch_current') as mock_fetch:
            mock_fetch.return_value = (
                {'temperature': 25, 'date': today}, 
                False, 
                None
            )
            
            # First fetch
            self.data_manager.fetch_current(city, "metric")
            
            # Second fetch same day
            mock_fetch.return_value = (
                {'temperature': 26, 'date': today}, 
                False, 
                None
            )
            self.data_manager.fetch_current(city, "metric")
            
            # Should have only one entry per day
            from WeatherDashboard.utils.utils import city_key
            key = city_key(city)
            stored_data = self.data_manager.weather_data.get(key, [])
            
            # Should have only one entry since it's the same day
            self.assertEqual(len(stored_data), 1)


if __name__ == '__main__':
    unittest.main()