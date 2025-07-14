"""
Data service layer that coordinates between controllers and data managers.

This module provides the service layer that abstracts data operations
for controllers. Handles weather data retrieval, historical data access,
logging operations, and coordinates between business logic and data storage.

Classes:
    WeatherDataService: Main service class coordinating data operations
"""

from typing import Tuple, Dict, Any, List, Optional

from WeatherDashboard.utils.utils import (
    normalize_city_name,
    validate_unit_system
)
from WeatherDashboard.services.api_exceptions import ValidationError


class WeatherDataService:
    """Service layer that abstracts data operations for controllers.
    
    Provides a clean interface between business logic controllers and data
    management systems. Handles weather data retrieval, historical data access,
    file logging, and coordinates data operations across the application.
    
    Attributes:
        data_manager: Weather data manager for storage and retrieval operations
    """
    def __init__(self, data_manager: Any) -> None:
        """Initialize the data service with a data manager.
        
        Args:
            data_manager: Weather data manager for handling data operations
        """
        self.data_manager = data_manager

    def get_city_data(self, city_name: str, unit_system: str) -> Tuple[str, Dict[str, Any], Optional[Exception]]:
        """Fetch weather data for a city with the specified unit system.
        
        Retrieves current weather data through the data manager with proper
        unit conversion and normalization of city names.
        
        Args:
            city_name: Name of the city to fetch weather for
            unit_system: Unit system for the weather data ('metric' or 'imperial')
            
        Returns:
            Tuple containing:
                - str: Normalized city name
                - Dict[str, Any]: Weather data with converted units
                - Optional[Exception]: Exception if fetch failed, None for success
        """
        # Normalize once at the entry point
        try:
            city = normalize_city_name(city_name)
            validate_unit_system(unit_system) 
        except ValueError as e:
            # Convert to our custom exception for consistent error handling
            raise ValidationError(str(e))
        
        data, use_fallback, error_exception = self.data_manager.fetch_current(city, unit_system)
        
        return city, data, error_exception

    def get_historical_data(self, city_name: str, num_days: int, unit_system: str) -> List[Dict[str, Any]]:
        """Get historical weather data for a city.
        
        Retrieves historical weather data through the data manager with
        proper unit conversion for the specified time period.
        
        Args:
            city: City name for historical data
            days: Number of days of historical data to retrieve
            unit_system: Unit system for the data ('metric' or 'imperial')
            
        Returns:
            List[Dict[str, Any]]: List of historical weather data entries
        """
        # Normalize once at the entry point
        try:
            city = normalize_city_name(city_name)
            validate_unit_system(unit_system) 
        except ValueError as e:
            raise ValidationError(str(e))
        
        raw = self.data_manager.get_historical(city, num_days)

        source_unit = "metric"  # Same as generator’s output
        if unit_system == source_unit:
            return raw
        return [self.data_manager.convert_units(d, unit_system) for d in raw]

    def write_to_log(self, city: str, data: Dict[str, Any], unit: str) -> None:
        """Write weather data to the log file.
        
        Args:
            city: City name for the log entry
            data: Weather data to log
            unit_system: Unit system for formatting ('metric' or 'imperial')
        """
        try:
            validate_unit_system(unit)
        except ValueError as e:
            raise ValidationError(str(e))
        
        self.data_manager.write_to_file(city, data, unit)