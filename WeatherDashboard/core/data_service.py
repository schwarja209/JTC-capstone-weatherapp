"""
Data service layer for weather operations without GUI interactions.
"""

from typing import Tuple, Dict, Any, List, Optional, Union
from WeatherDashboard.utils.utils import (
    normalize_city_name,
    validate_unit_system
)
from WeatherDashboard.services.api_exceptions import ValidationError


class WeatherDataService:
    '''Handles fetching and returning weather data without interacting with GUI.'''
    def __init__(self, data_manager: Any) -> None:
        self.data_manager = data_manager

    def get_city_data(self, city_name: str, unit_system: str) -> Tuple[str, Dict[str, Any], Optional[Exception]]:
        '''Fetches weather data for a city. Handles fallback. Returns (city, data, fallback_flag).'''
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
        '''Fetches historical data and applies unit conversion.'''
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
        '''Writes weather data to log file with timestamp and unit system information.'''
        validate_unit_system(unit)
        self.data_manager.write_to_file(city, data, unit)