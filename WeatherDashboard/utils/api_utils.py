"""
API data parsing utilities for the Weather Dashboard application.

This module provides centralized utilities for safe API response parsing and data extraction.
Eliminates repetitive nested dictionary access patterns throughout the weather service layer
with safe accessor methods and structured data extraction functions.

Classes:
    ApiUtils: Static utility class for API response parsing and data extraction
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime

from WeatherDashboard.utils.logger import Logger


@dataclass
class WeatherMainData:
    """Type-safe container for main weather data.
    
    Contains temperature, humidity, pressure, and related metrics
    with proper type safety and validation.
    """
    temperature: Optional[float]
    humidity: Optional[int]
    pressure: Optional[int]
    feels_like: Optional[float]
    temp_min: Optional[float]
    temp_max: Optional[float]
    
    def __post_init__(self):
        """Validate dataclass after initialization."""
        if self.humidity is not None and not (0 <= self.humidity <= 100):
            raise ValueError("humidity must be between 0 and 100")
        if self.pressure is not None and self.pressure < 0:
            raise ValueError("pressure cannot be negative")

@dataclass
class WeatherWindData:
    """Type-safe container for wind data.
    
    Contains wind speed, direction, and gust information
    with proper type safety and validation.
    """
    wind_speed: Optional[float]
    wind_direction: Optional[float]
    wind_gust: Optional[float]
    
    def __post_init__(self):
        """Validate dataclass after initialization."""
        if self.wind_speed is not None and self.wind_speed < 0:
            raise ValueError("wind_speed cannot be negative")
        if self.wind_direction is not None and not (0 <= self.wind_direction <= 360):
            raise ValueError("wind_direction must be between 0 and 360 degrees")
        if self.wind_gust is not None and self.wind_gust < 0:
            raise ValueError("wind_gust cannot be negative")

@dataclass
class WeatherConditionsData:
    """Type-safe container for weather conditions.
    
    Contains weather description, main condition, ID, and icon
    with proper type safety and validation.
    """
    conditions: str
    weather_main: Optional[str]
    weather_id: Optional[int]
    weather_icon: Optional[str]
    
    def __post_init__(self):
        """Validate dataclass after initialization."""
        if not self.conditions:
            raise ValueError("conditions cannot be empty")
        if self.weather_id is not None and self.weather_id < 0:
            raise ValueError("weather_id cannot be negative")

@dataclass
class PrecipitationData:
    """Type-safe container for precipitation data.
    
    Contains rain and snow data with both simplified and detailed metrics
    with proper type safety and validation.
    """
    rain: Optional[float]
    snow: Optional[float]
    rain_1h: Optional[float]
    rain_3h: Optional[float]
    snow_1h: Optional[float]
    snow_3h: Optional[float]
    
    def __post_init__(self):
        """Validate dataclass after initialization."""
        for field_name in ['rain', 'snow', 'rain_1h', 'rain_3h', 'snow_1h', 'snow_3h']:
            value = getattr(self, field_name)
            if value is not None and value < 0:
                raise ValueError(f"{field_name} cannot be negative")

@dataclass
class AtmosphericData:
    """Type-safe container for atmospheric conditions.
    
    Contains visibility and cloud cover information
    with proper type safety and validation.
    """
    visibility: Optional[int]
    cloud_cover: Optional[int]
    
    def __post_init__(self):
        """Validate dataclass after initialization."""
        if self.visibility is not None and self.visibility < 0:
            raise ValueError("visibility cannot be negative")
        if self.cloud_cover is not None and not (0 <= self.cloud_cover <= 100):
            raise ValueError("cloud_cover must be between 0 and 100")

@dataclass
class Coordinates:
    """Type-safe container for geographic coordinates.
    
    Contains latitude and longitude with proper validation
    for geographic coordinate ranges.
    """
    latitude: Optional[float]
    longitude: Optional[float]
    
    def __post_init__(self):
        """Validate dataclass after initialization."""
        if self.latitude is not None and not (-90 <= self.latitude <= 90):
            raise ValueError("latitude must be between -90 and 90 degrees")
        if self.longitude is not None and not (-180 <= self.longitude <= 180):
            raise ValueError("longitude must be between -180 and 180 degrees")

@dataclass
class CompleteWeatherData:
    """Type-safe container for complete weather data.
    
    Combines all weather data sections into a single structured
    container with comprehensive validation.
    """
    date: datetime
    main_data: WeatherMainData
    wind_data: WeatherWindData
    conditions_data: WeatherConditionsData
    precipitation_data: PrecipitationData
    atmospheric_data: AtmosphericData
    coordinates: Coordinates
    uv_index: Optional[float] = None
    air_quality_index: Optional[int] = None
    air_quality_description: Optional[str] = None

    # Lightweight transformation metadata
    transformation_status: str = "success"
    extraction_success_rate: float = 1.0  # Percentage of fields successfully extracted
    missing_fields: List[str] = None  # Fields that couldn't be extracted
    
    def __post_init__(self):
        """Validate dataclass after initialization."""
        if self.uv_index is not None and self.uv_index < 0:
            raise ValueError("uv_index cannot be negative")
        if self.air_quality_index is not None and not (1 <= self.air_quality_index <= 5):
            raise ValueError("air_quality_index must be between 1 and 5")
        if self.transformation_status not in ['success', 'partial', 'failed']:
            raise ValueError("transformation_status must be 'success', 'partial', or 'failed'")
        if not (0.0 <= self.extraction_success_rate <= 1.0):
            raise ValueError("extraction_success_rate must be between 0.0 and 1.0")
        if self.missing_fields is None:
            self.missing_fields = []

@dataclass
class APIValidationResult:
    """Type-safe container for API response validation results.
    
    Contains validation status and any missing sections
    for comprehensive error reporting.
    """
    is_valid: bool
    missing_sections: List[str]
    timestamp: datetime
    error_message: Optional[str] = None

    # Lightweight transformation metadata
    validation_status: str = "success"  # "success", "partial", "failed"

    def __post_init__(self):
        """Validate dataclass after initialization."""
        if self.validation_status not in ['success', 'partial', 'failed']:
            raise ValueError("validation_status must be 'success', 'partial', or 'failed'")


class ApiUtils:
    """Utilities for safe API response parsing and data extraction."""
    
    def __init__(self) -> None:
        """Initialize API utils with hybrid dependency injection."""
        # Direct imports for stable utilities
        self.logger = Logger()
        self.datetime = datetime

    def safe_get_nested(self, data: Dict[str, Any], *keys: str, default: Any = None) -> Any:
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
    
    def safe_get_list_item(self, data: Dict[str, Any], list_key: str, index: int = 0, item_key: Optional[str] = None, default: Any = None) -> Any:
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
            # Check if data is a dictionary first
            if not isinstance(data, dict):
                return default
                
            list_data = data.get(list_key, [])
            if not isinstance(list_data, list) or len(list_data) <= index or index < 0:
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
    
    def extract_weather_main_data(self, weather_data: Dict[str, Any]) -> WeatherMainData:
        """Extract main weather data section with safe defaults.
        
        Consolidates repeated main section extractions.
        
        Args:
            weather_data: OpenWeatherMap API response
            
        Returns:
            WeatherMainData: Type-safe container with main weather metrics
        """
        try:
            if not isinstance(weather_data, dict):
                return WeatherMainData(
                    temperature=None,
                    humidity=None,
                    pressure=None,
                    feels_like=None,
                    temp_min=None,
                    temp_max=None
                )

            return WeatherMainData(
                temperature=self.safe_get_nested(weather_data, "main", "temp"),
                humidity=self.safe_get_nested(weather_data, "main", "humidity"),
                pressure=self.safe_get_nested(weather_data, "main", "pressure"),
                feels_like=self.safe_get_nested(weather_data, "main", "feels_like"),
                temp_min=self.safe_get_nested(weather_data, "main", "temp_min"),
                temp_max=self.safe_get_nested(weather_data, "main", "temp_max")
            )
        except Exception as e:
            self.logger.error(f"Error extracting main weather data: {e}")
            return WeatherMainData(
                temperature=None,
                humidity=None,
                pressure=None,
                feels_like=None,
                temp_min=None,
                temp_max=None
            )
    
    def extract_weather_wind_data(self, weather_data: Dict[str, Any]) -> WeatherWindData:
        """Extract wind data section with safe defaults.
        
        Args:
            weather_data: OpenWeatherMap API response
            
        Returns:
            WeatherWindData: Type-safe container with wind metrics
        """
        try:
            if not isinstance(weather_data, dict):
                return WeatherWindData(
                    wind_speed=None,
                    wind_direction=None,
                    wind_gust=None
                )
            
            return WeatherWindData(
                wind_speed=self.safe_get_nested(weather_data, "wind", "speed"),
                wind_direction=self.safe_get_nested(weather_data, "wind", "deg"),
                wind_gust=self.safe_get_nested(weather_data, "wind", "gust")
            )
        except Exception as e:
            self.logger.error(f"Error extracting wind data: {e}")
            return WeatherWindData(
                wind_speed=None,
                wind_direction=None,
                wind_gust=None
            )
    
    def extract_weather_conditions_data(self, weather_data: Dict[str, Any]) -> WeatherConditionsData:
        """Extract weather conditions with safe defaults.
        
        Args:
            weather_data: OpenWeatherMap API response
            
        Returns:
            WeatherConditionsData: Type-safe container with weather condition data
        """
        try:
            if not isinstance(weather_data, dict):
                return WeatherConditionsData(
                    conditions="--",
                    weather_main=None,
                    weather_id=None,
                    weather_icon=None
                )
            
            # Get the description safely
            description = self.safe_get_list_item(weather_data, "weather", 0, "description", "--")
            
            # Handle the case where description might not be a string
            if isinstance(description, str):
                conditions = description.title()
            else:
                conditions = "--"
            
            return WeatherConditionsData(
                conditions=conditions,
                weather_main=self.safe_get_list_item(weather_data, "weather", 0, "main"),
                weather_id=self.safe_get_list_item(weather_data, "weather", 0, "id"),
                weather_icon=self.safe_get_list_item(weather_data, "weather", 0, "icon")
            )
        except Exception as e:
            self.logger.error(f"Error extracting conditions data: {e}")
            return WeatherConditionsData(
                conditions="--",
                weather_main=None,
                weather_id=None,
                weather_icon=None
            )
    
    def extract_precipitation_data(self, weather_data: Dict[str, Any]) -> PrecipitationData:
        """Extract precipitation data with smart fallback logic.
        
        Args:
            weather_data: OpenWeatherMap API response
            
        Returns:
            PrecipitationData: Type-safe container with precipitation metrics
        """
        try:
            if not isinstance(weather_data, dict):
                return PrecipitationData(
                    rain=None,
                    snow=None,
                    rain_1h=None,
                    rain_3h=None,
                    snow_1h=None,
                    snow_3h=None
                )
            
            def get_precipitation_1h(precip_type: str) -> Optional[float]:
                """Helper to get 1h precipitation with 3h fallback."""
                primary = self.safe_get_nested(weather_data, precip_type, '1h')
                fallback = self.safe_get_nested(weather_data, precip_type, '3h')
                
                if primary is not None:
                    return primary
                elif fallback is not None:
                    return fallback / 3  # Convert 3h to 1h estimate
                else:
                    return None
            
            return PrecipitationData(
                # Simplified precipitation
                rain=get_precipitation_1h('rain'),
                snow=get_precipitation_1h('snow'),
                
                # Detailed precipitation
                rain_1h=self.safe_get_nested(weather_data, "rain", "1h"),
                rain_3h=self.safe_get_nested(weather_data, "rain", "3h"),
                snow_1h=self.safe_get_nested(weather_data, "snow", "1h"),
                snow_3h=self.safe_get_nested(weather_data, "snow", "3h")
            )
        except Exception as e:
            self.logger.error(f"Error extracting precipitation data: {e}")
            return PrecipitationData(
                rain=None,
                snow=None,
                rain_1h=None,
                rain_3h=None,
                snow_1h=None,
                snow_3h=None
            )
            
    def extract_atmospheric_data(self, weather_data: Dict[str, Any]) -> AtmosphericData:
        """Extract atmospheric conditions data.
        
        Args:
            weather_data: OpenWeatherMap API response
            
        Returns:
            AtmosphericData: Type-safe container with atmospheric metrics
        """
        try:
            if not isinstance(weather_data, dict):
                return AtmosphericData(
                    visibility=None,
                    cloud_cover=None
                )
            
            return AtmosphericData(
                visibility=self.safe_get_nested(weather_data, "visibility"),
                cloud_cover=self.safe_get_nested(weather_data, "clouds", "all")
            )
        except Exception as e:
            self.logger.error(f"Error extracting atmospheric data: {e}")
            return AtmosphericData(
                visibility=None,
                cloud_cover=None
            )
        
    def extract_coordinates(self, weather_data: Dict[str, Any]) -> Coordinates:
        """Extract coordinate data for additional API calls.
        
        Args:
            weather_data: OpenWeatherMap API response
            
        Returns:
            Coordinates: Type-safe container with latitude and longitude
        """
        try:
            if not isinstance(weather_data, dict):
                return Coordinates(
                    latitude=None,
                    longitude=None
                )
            
            return Coordinates(
                latitude=self.safe_get_nested(weather_data, "coord", "lat"),
                longitude=self.safe_get_nested(weather_data, "coord", "lon")
            )
        except Exception as e:
            self.logger.error(f"Error extracting coordinates: {e}")
            return Coordinates(
                latitude=None,
                longitude=None
            )
    
    def extract_complete_weather_data(self, weather_data: Dict[str, Any], uv_data: Optional[Dict[str, Any]] = None, air_quality_data: Optional[Dict[str, Any]] = None) -> CompleteWeatherData:
        """Extract complete weather data using all safe extraction methods.
        
        Replaces the large manual parsing in WeatherDataParser.parse_weather_data.
        
        Args:
            weather_data: Main weather API response
            uv_data: UV index API response (optional)
            air_quality_data: Air quality API response (optional)
            
        Returns:
            CompleteWeatherData: Type-safe container with all weather data
        """
        try:
            # Extract all sections using safe methods
            main_data = self.extract_weather_main_data(weather_data)
            wind_data = self.extract_weather_wind_data(weather_data)
            conditions_data = self.extract_weather_conditions_data(weather_data)
            precipitation_data = self.extract_precipitation_data(weather_data)
            atmospheric_data = self.extract_atmospheric_data(weather_data)
            coordinates = self.extract_coordinates(weather_data)

            # Calculate extraction success rate
            total_fields = 6  # main, wind, conditions, precipitation, atmospheric, coordinates
            successful_extractions = sum([
                1 if main_data.temperature is not None else 0,
                1 if wind_data.wind_speed is not None else 0,
                1 if conditions_data.conditions != "--" else 0,
                1 if precipitation_data.rain is not None else 0,
                1 if atmospheric_data.visibility is not None else 0,
                1 if coordinates.latitude is not None else 0
            ])
            extraction_success_rate = successful_extractions / total_fields
            
            # Determine transformation status
            transformation_status = "success"
            if extraction_success_rate < 1.0:
                transformation_status = "partial" if extraction_success_rate > 0.5 else "failed"
            
            # Track missing fields
            missing_fields = []
            if main_data.temperature is None:
                missing_fields.append("temperature")
            if wind_data.wind_speed is None:
                missing_fields.append("wind_speed")
            if conditions_data.conditions == "--":
                missing_fields.append("conditions")
            if precipitation_data.rain is None:
                missing_fields.append("precipitation")
            if atmospheric_data.visibility is None:
                missing_fields.append("visibility")
            if coordinates.latitude is None:
                missing_fields.append("coordinates")
            
            # Extract UV and air quality data
            uv_index = None
            air_quality_index = None
            air_quality_description = None
            
            if uv_data and isinstance(uv_data, dict):
                uv_index = uv_data.get('value')
            
            if air_quality_data and isinstance(air_quality_data, dict):
                aqi_data = self.safe_get_list_item(air_quality_data, 'list', 0, default={})
                air_quality_index = self.safe_get_nested(aqi_data, 'main', 'aqi')
                air_quality_description = self.get_aqi_description(air_quality_index)
            
            return CompleteWeatherData(
                date=self.datetime.now(),
                main_data=main_data,
                wind_data=wind_data,
                conditions_data=conditions_data,
                precipitation_data=precipitation_data,
                atmospheric_data=atmospheric_data,
                coordinates=coordinates,
                uv_index=uv_index,
                air_quality_index=air_quality_index,
                air_quality_description=air_quality_description,
                # LIGHT METADATA FIELDS:
                transformation_status=transformation_status,
                extraction_success_rate=extraction_success_rate,
                missing_fields=missing_fields
            )
        
        except Exception as e:
            self.logger.error(f"Error extracting complete weather data: {e}")
            # Return minimal valid structure even if everything fails
            return CompleteWeatherData(
                date=self.datetime.now(),
                main_data=WeatherMainData(None, None, None, None, None, None),
                wind_data=WeatherWindData(None, None, None),
                conditions_data=WeatherConditionsData("--", None, None, None),
                precipitation_data=PrecipitationData(None, None, None, None, None, None),
                atmospheric_data=AtmosphericData(None, None),
                coordinates=Coordinates(None, None),
                # LIGHT METADATA FIELDS:
                transformation_status="failed",
                extraction_success_rate=0.0,
                missing_fields=["all_fields"]
            )
    
    def get_aqi_description(self, aqi: Optional[int]) -> str:
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
    
    def validate_api_response_structure(self, data: Dict[str, Any], required_sections: List[str]) -> APIValidationResult:
        """Validate that API response has required structure.
        
        Args:
            data: API response to validate
            required_sections: List of required top-level keys
            
        Returns:
            APIValidationResult: Type-safe container with validation results
        """
        try:
            if not isinstance(data, dict):
                return APIValidationResult(
                    is_valid=False,
                    missing_sections=required_sections,
                    timestamp=self.datetime.now(),
                    error_message=f"API response is not a dictionary: {type(data)}",
                    # LIGHT METADATA FIELDS:
                    validation_status="failed"
                )
            
            missing_sections = [section for section in required_sections if section not in data]
            
            if missing_sections:
                return APIValidationResult(
                    is_valid=False,
                    missing_sections=missing_sections,
                    timestamp=self.datetime.now(),
                    error_message=f"API response missing required sections: {missing_sections}",
                    # LIGHT METADATA FIELDS:
                    validation_status="partial" if len(missing_sections) < len(required_sections) else "failed"
                )
            
            return APIValidationResult(
                is_valid=True,
                missing_sections=[],
                timestamp=self.datetime.now(),
                # LIGHT METADATA FIELDS:
                validation_status="success"
            )
            
        except Exception as e:
            return APIValidationResult(
                is_valid=False,
                missing_sections=required_sections,
                timestamp=self.datetime.now(),
                error_message=f"Error validating API response structure: {e}",
                # LIGHT METADATA FIELDS:
                validation_status="failed"
            )
        
    # BACKWARD COMPATILIBITY METHODS:
    def extract_weather_main_data_dict(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract main weather data as dictionary (backward compatibility).
        
        Args:
            weather_data: OpenWeatherMap API response
            
        Returns:
            Dict[str, Any]: Dictionary with main weather metrics
        """
        main_data = self.extract_weather_main_data(weather_data)
        return {
            'temperature': main_data.temperature,
            'humidity': main_data.humidity,
            'pressure': main_data.pressure,
            'feels_like': main_data.feels_like,
            'temp_min': main_data.temp_min,
            'temp_max': main_data.temp_max,
        }

    def extract_complete_weather_data_dict(self, weather_data: Dict[str, Any], uv_data: Optional[Dict[str, Any]] = None, air_quality_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Extract complete weather data as dictionary (backward compatibility).
        
        Args:
            weather_data: Main weather API response
            uv_data: UV index API response (optional)
            air_quality_data: Air quality API response (optional)
            
        Returns:
            Dict[str, Any]: Complete parsed weather data dictionary
        """
        complete_data = self.extract_complete_weather_data(weather_data, uv_data, air_quality_data)
        
        # Convert to dictionary format for backward compatibility
        result = {
            'date': complete_data.date,
            'uv_index': complete_data.uv_index,
            'air_quality_index': complete_data.air_quality_index,
            'air_quality_description': complete_data.air_quality_description,
        }
        
        # Add main data
        result.update({
            'temperature': complete_data.main_data.temperature,
            'humidity': complete_data.main_data.humidity,
            'pressure': complete_data.main_data.pressure,
            'feels_like': complete_data.main_data.feels_like,
            'temp_min': complete_data.main_data.temp_min,
            'temp_max': complete_data.main_data.temp_max,
        })
        
        # Add wind data
        result.update({
            'wind_speed': complete_data.wind_data.wind_speed,
            'wind_direction': complete_data.wind_data.wind_direction,
            'wind_gust': complete_data.wind_data.wind_gust,
        })
        
        # Add conditions data
        result.update({
            'conditions': complete_data.conditions_data.conditions,
            'weather_main': complete_data.conditions_data.weather_main,
            'weather_id': complete_data.conditions_data.weather_id,
            'weather_icon': complete_data.conditions_data.weather_icon,
        })
        
        # Add precipitation data
        result.update({
            'rain': complete_data.precipitation_data.rain,
            'snow': complete_data.precipitation_data.snow,
            'rain_1h': complete_data.precipitation_data.rain_1h,
            'rain_3h': complete_data.precipitation_data.rain_3h,
            'snow_1h': complete_data.precipitation_data.snow_1h,
            'snow_3h': complete_data.precipitation_data.snow_3h,
        })
        
        # Add atmospheric data
        result.update({
            'visibility': complete_data.atmospheric_data.visibility,
            'cloud_cover': complete_data.atmospheric_data.cloud_cover,
        })
        
        # Add coordinates
        result.update({
            'latitude': complete_data.coordinates.latitude,
            'longitude': complete_data.coordinates.longitude,
        })
        
        return result