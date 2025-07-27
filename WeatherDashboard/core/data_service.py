"""
Data service layer that coordinates between controllers and data managers.

This module provides the service layer that abstracts data operations
for controllers. Handles weather data retrieval, historical data access,
logging operations, and coordinates between business logic and data storage.

Classes:
    WeatherDataService: Main service class coordinating data operations
"""

from typing import Tuple, Dict, Any, List, Optional
import threading

from WeatherDashboard.utils.validation_utils import ValidationUtils

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
            data_manager: Weather data manager for handling data operations (injected for testability)
        """
        # Direct imports for stable utilities
        self.validation_utils = ValidationUtils()

        # Injected dependencies for testable components
        self.data_manager = data_manager

    def _validate_inputs(self, city_name: str, unit_system: str) -> Tuple[str, str]:
        """Validate and normalize inputs with consistent error handling.
        
        Returns:
            Tuple[str, str]: Validated city name and unit system
        """
        try:
            city_errors = self.validation_utils.validate_city_name(city_name)
            if city_errors:
                raise ValueError(city_errors[0])
            city = city_name.strip().title()
            
            unit_errors = self.validation_utils.validate_unit_system(unit_system)
            if unit_errors:
                raise ValueError(unit_errors[0])
            return city, unit_system
        except ValueError as e:
            raise ValidationError(str(e))

    def get_city_data(self, city_name: str, unit_system: str, cancel_event: Optional[threading.Event] = None) -> Tuple[str, Dict[str, Any], Optional[Exception]]:
        """Get weather data for a city with comprehensive error handling and normalization.
        
        Fetches current weather data through data manager, handles city name normalization,
        unit system validation, and provides consistent error handling. Converts service-level
        exceptions to appropriate application-level exceptions per ADR-004.
        
        Args:
            city: Raw city name input (will be normalized)
            unit_system: Target unit system ('metric' or 'imperial')
        
        Returns:
            Tuple containing:
                - str: Normalized city name
                - Dict[str, Any]: Weather data in requested units
                - Optional[Exception]: Error that occurred, None if successful
                
        Side Effects:
            Logs data operations via data manager
            May trigger data cleanup operations
        """
        validated_city, validated_unit = self._validate_inputs(city_name, unit_system)

        data, use_fallback, error_exception = self.data_manager.fetch_current(validated_city, validated_unit, cancel_event)
        
        return validated_city, data, error_exception

    def get_historical_data(self, city_name: str, num_days: int, unit_system: str) -> List[Dict[str, Any]]:
        """Get historical weather data for a city with unit conversion.
        
        Retrieves historical weather data through data manager and applies
        unit conversion to match the requested unit system. Handles validation
        of input parameters and provides consistent data formatting.
        
        Args:
            city: Target city name for historical data
            days: Number of days of historical data to retrieve
            unit_system: Target unit system for data formatting
            
        Returns:
            List[Dict[str, Any]]: Historical weather data entries with converted units
        """
        validated_city, validated_unit = self._validate_inputs(city_name, unit_system)
        
        raw = self.data_manager.get_historical(validated_city, num_days)

        source_unit = "metric"  # Same as generator’s output
        if validated_unit == source_unit:
            return raw
        return [self.data_manager.convert_units(d, validated_unit) for d in raw]

    def write_to_log(self, city: str, data: Dict[str, Any], unit: str) -> None:
        """Write weather data to the log file.
        
        Args:
            city: City name for the log entry
            data: Weather data to log
            unit_system: Unit system for formatting ('metric' or 'imperial')
        """       
        validated_city, validated_unit = self._validate_inputs(city, unit)
        
        self.data_manager.write_to_file(validated_city, data, validated_unit)