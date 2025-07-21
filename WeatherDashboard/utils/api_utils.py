"""
API data parsing utilities for the Weather Dashboard application.

This module provides centralized utilities for safe API response parsing and data extraction.
Eliminates repetitive nested dictionary access patterns throughout the weather service layer
with safe accessor methods and structured data extraction functions.

Classes:
    ApiUtils: Static utility class for API response parsing and data extraction
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from WeatherDashboard.utils.logger import Logger


class ApiUtils:
    """Utilities for safe API response parsing and data extraction."""
    
    @staticmethod
    def safe_get_nested(data: Dict[str, Any], *keys: str, default: Any = None) -> Any:
        """Safely extract nested dictionary values.
        
        Replaces repeated data.get("section", {}).get("field") patterns.
        
        Args:
            data: Source dictionary
            *keys: Sequence of keys to traverse (e.g., "main", "temp")
            default: Default value if path not found
            
        Returns:
            Extracted value or default
            
        Example:
            # Instead of: weather_data.get("main", {}).get("temp")
            # Use: ApiUtils.safe_get_nested(weather_data, "main", "temp")
        """
        try:
            current = data
            for key in keys:
                if not isinstance(current, dict) or key not in current:
                    return default
                current = current[key]
            return current
        except (TypeError, KeyError, AttributeError):
            return default
    
    @staticmethod
    def safe_get_list_item(data: Dict[str, Any], list_key: str, 
                          index: int = 0, item_key: Optional[str] = None, 
                          default: Any = None) -> Any:
        """Safely extract item from list in dictionary.
        
        Replaces patterns like data.get("weather", [{}])[0].get("description")
        
        Args:
            data: Source dictionary
            list_key: Key for the list in data
            index: Index in list (default 0)
            item_key: Key in list item (if None, returns whole item)
            default: Default value if not found
            
        Returns:
            Extracted value or default
            
        Example:
            # Instead of: weather_data.get("weather", [{}])[0].get("description", "--")
            # Use: ApiUtils.safe_get_list_item(weather_data, "weather", 0, "description", "--")
        """
        try:
            list_data = data.get(list_key, [])
            if not isinstance(list_data, list) or len(list_data) <= index:
                return default
            
            item = list_data[index]
            if item_key is None:
                return item
            
            if isinstance(item, dict):
                return item.get(item_key, default)
            else:
                return default
                
        except (TypeError, IndexError, KeyError):
            return default
    
    @staticmethod
    def extract_weather_main_data(weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract main weather data section with safe defaults.
        
        Consolidates repeated main section extractions.
        
        Args:
            weather_data: OpenWeatherMap API response
            
        Returns:
            Dict with main weather metrics
        """
        return {
            'temperature': ApiUtils.safe_get_nested(weather_data, "main", "temp"),
            'humidity': ApiUtils.safe_get_nested(weather_data, "main", "humidity"),
            'pressure': ApiUtils.safe_get_nested(weather_data, "main", "pressure"),
            'feels_like': ApiUtils.safe_get_nested(weather_data, "main", "feels_like"),
            'temp_min': ApiUtils.safe_get_nested(weather_data, "main", "temp_min"),
            'temp_max': ApiUtils.safe_get_nested(weather_data, "main", "temp_max"),
        }
    
    @staticmethod
    def extract_weather_wind_data(weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract wind data section with safe defaults.
        
        Args:
            weather_data: OpenWeatherMap API response
            
        Returns:
            Dict with wind metrics
        """
        return {
            'wind_speed': ApiUtils.safe_get_nested(weather_data, "wind", "speed"),
            'wind_direction': ApiUtils.safe_get_nested(weather_data, "wind", "deg"),
            'wind_gust': ApiUtils.safe_get_nested(weather_data, "wind", "gust"),
        }
    
    @staticmethod
    def extract_weather_conditions_data(weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract weather conditions with safe defaults.
        
        Args:
            weather_data: OpenWeatherMap API response
            
        Returns:
            Dict with weather condition data
        """
        return {
            'conditions': ApiUtils.safe_get_list_item(
                weather_data, "weather", 0, "description", "--").title(),
            'weather_main': ApiUtils.safe_get_list_item(
                weather_data, "weather", 0, "main"),
            'weather_id': ApiUtils.safe_get_list_item(
                weather_data, "weather", 0, "id"),
            'weather_icon': ApiUtils.safe_get_list_item(
                weather_data, "weather", 0, "icon"),
        }
    
    @staticmethod
    def extract_precipitation_data(weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract precipitation data with smart fallback logic.
        
        Args:
            weather_data: OpenWeatherMap API response
            
        Returns:
            Dict with precipitation metrics
        """
        def get_precipitation_1h(precip_type: str) -> Optional[float]:
            """Helper to get 1h precipitation with 3h fallback."""
            primary = ApiUtils.safe_get_nested(weather_data, precip_type, '1h')
            fallback = ApiUtils.safe_get_nested(weather_data, precip_type, '3h')
            
            if primary is not None:
                return primary
            elif fallback is not None:
                return fallback / 3  # Convert 3h to 1h estimate
            else:
                return None
        
        return {
            # Simplified precipitation
            'rain': get_precipitation_1h('rain'),
            'snow': get_precipitation_1h('snow'),
            
            # Detailed precipitation
            'rain_1h': ApiUtils.safe_get_nested(weather_data, "rain", "1h"),
            'rain_3h': ApiUtils.safe_get_nested(weather_data, "rain", "3h"),
            'snow_1h': ApiUtils.safe_get_nested(weather_data, "snow", "1h"),
            'snow_3h': ApiUtils.safe_get_nested(weather_data, "snow", "3h"),
        }
    
    @staticmethod
    def extract_atmospheric_data(weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract atmospheric conditions data.
        
        Args:
            weather_data: OpenWeatherMap API response
            
        Returns:
            Dict with atmospheric metrics
        """
        return {
            'visibility': ApiUtils.safe_get_nested(weather_data, "visibility"),
            'cloud_cover': ApiUtils.safe_get_nested(weather_data, "clouds", "all"),
        }
    
    @staticmethod
    def extract_coordinates(weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract coordinate data for additional API calls.
        
        Args:
            weather_data: OpenWeatherMap API response
            
        Returns:
            Dict with latitude and longitude
        """
        return {
            'latitude': ApiUtils.safe_get_nested(weather_data, "coord", "lat"),
            'longitude': ApiUtils.safe_get_nested(weather_data, "coord", "lon"),
        }
    
    @staticmethod
    def extract_complete_weather_data(weather_data: Dict[str, Any], 
                                    uv_data: Optional[Dict[str, Any]] = None,
                                    air_quality_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Extract complete weather data using all safe extraction methods.
        
        Replaces the large manual parsing in WeatherDataParser.parse_weather_data.
        
        Args:
            weather_data: Main weather API response
            uv_data: UV index API response (optional)
            air_quality_data: Air quality API response (optional)
            
        Returns:
            Complete parsed weather data dictionary
        """
        parsed_data = {
            'date': datetime.now(),
        }
        
        # Extract all sections using safe methods
        parsed_data.update(ApiUtils.extract_weather_main_data(weather_data))
        parsed_data.update(ApiUtils.extract_weather_wind_data(weather_data))
        parsed_data.update(ApiUtils.extract_weather_conditions_data(weather_data))
        parsed_data.update(ApiUtils.extract_precipitation_data(weather_data))
        parsed_data.update(ApiUtils.extract_atmospheric_data(weather_data))
        parsed_data.update(ApiUtils.extract_coordinates(weather_data))
        
        # Add UV index data if provided
        if uv_data:
            parsed_data['uv_index'] = uv_data.get('value')
        
        # Add air quality data if provided
        if air_quality_data:
            aqi_data = ApiUtils.safe_get_list_item(air_quality_data, 'list', 0, default={})
            parsed_data['air_quality_index'] = ApiUtils.safe_get_nested(aqi_data, 'main', 'aqi')
            parsed_data['air_quality_description'] = ApiUtils.get_aqi_description(
                parsed_data.get('air_quality_index'))
        
        return parsed_data
    
    @staticmethod
    def get_aqi_description(aqi: Optional[int]) -> str:
        """Convert AQI number to description.
        
        Args:
            aqi: Air Quality Index number
            
        Returns:
            Human-readable AQI description
        """
        if aqi is None:
            return "Unknown"
        
        aqi_descriptions = {
            1: "Good",
            2: "Fair", 
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }
        return aqi_descriptions.get(aqi, "Unknown")
    
    @staticmethod
    def validate_api_response_structure(data: Dict[str, Any], 
                                      required_sections: List[str]) -> bool:
        """Validate that API response has required structure.
        
        Args:
            data: API response to validate
            required_sections: List of required top-level keys
            
        Returns:
            bool: True if structure is valid
        """
        try:
            if not isinstance(data, dict):
                Logger.warn(f"API response is not a dictionary: {type(data)}")
                return False
            
            missing_sections = [section for section in required_sections 
                              if section not in data]
            
            if missing_sections:
                Logger.warn(f"API response missing required sections: {missing_sections}")
                return False
            
            return True
            
        except Exception as e:
            Logger.error(f"Error validating API response structure: {e}")
            return False