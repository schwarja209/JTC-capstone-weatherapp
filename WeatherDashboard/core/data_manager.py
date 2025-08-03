"""
Data management for weather information including fetching, storage, and unit conversion.

This module provides comprehensive weather data management including API communication,
fallback data generation, unit conversion, data storage, and memory management.
Handles both live API data and simulated fallback data seamlessly with automatic
cleanup algorithms and data validation.

Features include automatic memory management with time-based and limit-based cleanup,
comprehensive unit conversion between metric and imperial systems, and intelligent
fallback to simulated data when APIs are unavailable.

Classes:
    WeatherDataManager: Main data management class with API integration and fallback handling
"""

from typing import Dict, List, Any, Optional
import threading

from WeatherDashboard import config
from WeatherDashboard.utils.utils import Utils
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.unit_converter import UnitConverter
from WeatherDashboard.utils.validation_utils import ValidationUtils
from WeatherDashboard.services.weather_service import WeatherAPIService
from WeatherDashboard.features.history.history_service import WeatherHistoryService


# ================================
# 1. INITIALIZATION & SETUP
# ================================
class WeatherDataManager:
    """Manage weather data fetching and storage, including fallback handling.
    
    Coordinates weather API calls, fallback data generation, unit conversion,
    and data storage. Provides automatic cleanup and memory management for
    stored weather data.
    
    Attributes:
        api_service: Weather API service for external data fetching
        weather_data: Dictionary storing weather data by city key
        _last_cleanup: Timestamp of last data cleanup operation
        _cleanup_interval_hours: Hours between automatic cleanup operations (from config)
    """
    
    def __init__(self) -> None:
        """Initialize the weather data manager.
        
        Sets up the API service, data storage, and automatic cleanup tracking.

        Args:
            api_service: Weather API service for external data fetching (injected for testability)
        """
        # Direct imports for stable utilities
        self.logger = Logger()
        self.config = config
        self.utils = Utils()
        self.unit_converter = UnitConverter()
        self.validation_utils = ValidationUtils()

        # Injected dependencies for testable components
        self.api_service = WeatherAPIService()

        # Internal state
        self.history_service = WeatherHistoryService()

# ================================  
# 2. DATA FETCHING & HISTORY
# ================================
    def fetch_current(self, city: str, unit_system: str, cancel_event: Optional[threading.Event] = None) -> Dict[str, Any]:
        """Fetch current weather data with comprehensive error handling, fallback and cancellation support.
        
        Attempts to retrieve live weather data from API service with automatic fallback
        to simulated data on failure. Handles unit conversion, data validation, and
        error recovery. Provides detailed error information for troubleshooting.
        
        Args:
            city: Target city name for weather data retrieval
            unit_system: Unit system for data formatting ('metric' or 'imperial')
            
        Returns:
            Dict[str, Any]: Weather data (live or fallback)
                
        Side Effects:
            May log error messages and warnings via Logger
            Updates internal error tracking for monitoring
        """
        self.logger.info(f"Fetching current weather for {city}")
        
        try:
            weather_data = self.api_service.fetch_current(city, cancel_event)

            # All API and fallback data is assumed to be in metric units and converted downstream.
            # If this changes in future (e.g., new fallback with imperial), update convert_units().
            converted_data = self.convert_units(weather_data, unit_system)

            # Store latest call
            self.store_current_weather(city, converted_data, unit_system)
            self.logger.info(f"Current weather fetched for {city}")
            
            return converted_data
            
        except Exception as e:
            self.logger.error(f"Failed to fetch weather for {city}: {e}")
            raise

    def get_historical(self, city: str, num_days: int) -> List[Dict[str, Any]]:
        """Generate historical weather data for a city."""
        return self.history_service.get_historical(city, num_days)

    def get_recent_data(self, city: str, days_back: int = 7) -> List[Dict[str, Any]]:
        """Return recent weather data for a city from the last N days."""
        return self.history_service.get_recent_data(city, days_back)

    def store_current_weather(self, city: str, weather_data: Dict[str, Any], unit_system: str = "metric") -> None:
        """Store current weather data for historical tracking."""
        self.history_service.store_current_weather(city, weather_data, unit_system)

# ================================
# 3. DATA PROCESSING
# ================================
    def convert_units(self, data: Dict[str, Any], unit_system: str) -> Dict[str, Any]:
        """Convert weather data units based on the selected UI unit system.
        
        Converts temperature, pressure, and wind speed from metric (API default)
        to imperial units when requested. Logs conversion errors and continues
        with original values if conversion fails.
        
        Args:
            data: Weather data dictionary with metric units
            unit_system: Target unit system ('metric' or 'imperial')
            
        Returns:
            Dict[str, Any]: Weather data with converted units
        """
        self.validation_utils.validate_unit_system(unit_system)

        # Skip conversion if already in target system
        if unit_system == "metric":
            return data.copy()
        self.logger.info(f"Converting units to {unit_system}")
        
        converted = data.copy()
        
        # Get unit mappings from config
        unit_config = self.config.UNITS.get("metric_units", {})
        
        # Define converter functions mapping
        converters = {
            'temperature': self.unit_converter.convert_temperature,
            'pressure': self.unit_converter.convert_pressure,
            'wind_speed': self.unit_converter.convert_wind_speed,
            'feels_like': self.unit_converter.convert_temperature,
            'temp_min': self.unit_converter.convert_temperature,
            'temp_max': self.unit_converter.convert_temperature,
            'wind_gust': self.unit_converter.convert_wind_speed,
            'visibility': self.unit_converter.convert_visibility,
            'rain': self.unit_converter.convert_precipitation,
            'snow': self.unit_converter.convert_precipitation,
            'rain_1h': self.unit_converter.convert_precipitation,
            'rain_3h': self.unit_converter.convert_precipitation,
            'snow_1h': self.unit_converter.convert_precipitation,
            'snow_3h': self.unit_converter.convert_precipitation,
            'heat_index': self.unit_converter.convert_heat_index,
            'wind_chill': self.unit_converter.convert_wind_chill,
            'dew_point': self.unit_converter.convert_dew_point
        }
        
        conversion_errors: List[str] = []  # Track conversion failures

        # Apply conversions using config-defined units
        for field, converter_func in converters.items():
            if field in data and data[field] is not None and field in unit_config:
                try:
                    from_unit = unit_config[field]["metric"]  # Always convert from metric
                    to_unit = unit_config[field]["imperial"]  # To imperial
                    converted[field] = converter_func(data[field], from_unit, to_unit)
                except (ValueError, TypeError, KeyError) as e:
                    self.logger.warn(self.config.ERROR_MESSAGES['conversion'].format(field=field, from_unit="metric", to_unit="imperial", reason=str(e))) # For debugging
                    conversion_errors.append(field)
                    # Keep original value if conversion fails
        
        
        if conversion_errors: # Track which fields failed conversion
            converted['_conversion_warnings'] = f"Some units could not be converted: {', '.join(conversion_errors)}"
            self.logger.error(self.config.ERROR_MESSAGES['conversion'].format(field=f"fields: {', '.join(conversion_errors)}", from_unit="metric", to_unit="imperial", reason="conversion failed"))

        return converted

# ================================
# 4. FILE I/O & LOGGING --> now in history feature
# ================================
    def write_to_file(self, city: str, data: Dict[str, Any], unit_system: str) -> None:
        """Write formatted weather data to log file (delegates to history service)."""
        # This method now just delegates to the history service
        # The actual file writing is handled by the history service
        pass  # Remove the implementation since history service handles it