"""
Data service layer for weather operations without GUI interactions.
"""

from WeatherDashboard.utils.utils import (
    normalize_city_name,
    validate_unit_system
)
from WeatherDashboard.services.api_exceptions import ValidationError


class WeatherDataService:
    '''Handles fetching and returning weather data without interacting with GUI.'''
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def get_city_data(self, city_name, unit_system):
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

    def get_historical_data(self, city_name, num_days, unit_system):
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

    def write_to_log(self, city, data, unit):
        '''Writes weather data to log file with timestamp and unit system information.'''
        validate_unit_system(unit)
        self.data_manager.write_to_file(city, data, unit)