"""
Data management for weather information including fetching, storage, and unit conversion.
"""

from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, timedelta

from WeatherDashboard import config
from WeatherDashboard.utils.utils import (
    city_key,
    is_fallback,
    validate_unit_system
)
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.unit_converter import UnitConverter
from WeatherDashboard.services.weather_service import WeatherAPIService


class WeatherDataManager:
    '''Manages weather data fetching and storage, including fallback handling.'''
    def __init__(self) -> None:
        self.api_service = WeatherAPIService()
        self.weather_data = {}

        # Track when we last cleaned up data
        self._last_cleanup = datetime.now()
        self._cleanup_interval_hours = 24  # Cleanup every 24 hours

    def fetch_current(self, city: str, unit_system: str) -> Tuple[Dict[str, Any], bool, Optional[Exception]]:
        '''Fetches current weather data for a city, using fallback if API call fails.
        
        Args:
            city (str): Normalized city name (expected to already be processed)
            unit_system (str): Target unit system for the data
        '''
        raw_data, use_fallback, error_exception = self.api_service.fetch_current(city)

        # All API and fallback data is assumed to be in metric units and converted downstream.
        # If this changes in future (e.g., new fallback with imperial), update convert_units().
        converted_data = self.convert_units(raw_data, unit_system)

        # Periodic cleanup check
        current_time = datetime.now()
        if (current_time - self._last_cleanup).total_seconds() > (self._cleanup_interval_hours * 3600):
            self.cleanup_old_data()
            self._last_cleanup = current_time

        key = city_key(city)
        existing_data = self.weather_data.setdefault(key, [])
        last_date = existing_data[-1].get("date") if existing_data else None
        current_date = converted_data.get("date")
        if not existing_data or (last_date and current_date and last_date.date() != current_date.date()):
            existing_data.append(converted_data)
            # Limit stored data to prevent memory issues (keep last 30 entries per city)
            max_entries = 30
            if len(existing_data) > max_entries:
                existing_data[:] = existing_data[-max_entries:]  # Keep only the most recent entries

        return converted_data, use_fallback, error_exception
    
    def convert_units(self, data: Dict[str, Any], unit_system: str) -> Dict[str, Any]:
        '''Converts weather data units based on the selected UI unit system (metric or imperial).'''
        validate_unit_system(unit_system)

        # Skip conversion if already in target system
        if unit_system == "metric":
            return data.copy()
        
        converted = data.copy()
        
        # Get unit mappings from config
        unit_config = config.UNITS.get("metric_units", {})
        
        # Define converter functions mapping
        converters = {
            'temperature': UnitConverter.convert_temperature,
            'pressure': UnitConverter.convert_pressure,
            'wind_speed': UnitConverter.convert_wind_speed
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
                    Logger.warn(f"Failed to convert {field}: {e}")
                    conversion_errors.append(field)
                    # Keep original value if conversion fails
        
        
        if conversion_errors: # Track which fields failed conversion
            converted['_conversion_warnings'] = f"Some units could not be converted: {', '.join(conversion_errors)}"

        return converted

    def get_historical(self, city: str, num_days: int) -> List[Dict[str, Any]]:
        '''Fetches historical weather data for a city. Currently always defaults to fallback.'''
        return self.api_service.fallback.generate(city, num_days)

    def get_recent_data(self, city: str, days_back: int = 7) -> List[Dict[str, Any]]:
        '''Returns recent weather data for a city from the last N days.
        
        Args:
            city: City name
            days_back: Number of days to look back (default 7)
        
        Returns:
            List of weather data entries from the specified time period
        
        Note: Reserved for future features like trend analysis or prediction.
        '''
        city_data = self.weather_data.get(city_key(city), [])
        cutoff_date = datetime.now().date() - timedelta(days=days_back)
        
        return [
            entry for entry in city_data 
            if entry.get('date', datetime.now()).date() >= cutoff_date
        ]

    def write_to_file(self, city: str, data: Dict[str, Any], unit_system: str) -> None:
        '''Writes formatted weather data to a log file with timestamp and unit system information.'''
        try:
            log_entry = self.format_data_for_logging(city, data, unit_system)
            with open(config.OUTPUT["log"], "a", encoding="utf-8") as f:
                f.write(log_entry)

            fallback_text = "Simulated" if is_fallback(data) else "Live"
            Logger.info(f"Weather data written for {city_key(city)} - {fallback_text}")
            
        except (OSError, IOError, PermissionError) as e:
            Logger.error(f"Failed to write weather data to file: {e}")
        except Exception as e:
            Logger.error(f"Unexpected error writing weather data: {e}")

    def format_data_for_logging(self, city: str, data: Dict[str, Any], unit_system: str) -> str:
        '''Formats weather data for logging to a file with timestamp and unit system information.'''
        timestamp = data.get('date', datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            f"\n\nTime: {timestamp}",
            f"City: {city_key(city)}",
            f"Temperature: {UnitConverter.format_value('temperature', data.get('temperature'), unit_system)}",
            f"Humidity: {UnitConverter.format_value('humidity', data.get('humidity'), unit_system)}",
            f"Pressure: {UnitConverter.format_value('pressure', data.get('pressure'), unit_system)}",
            f"Wind Speed: {UnitConverter.format_value('wind_speed', data.get('wind_speed'), unit_system)}",
            f"Conditions: {data.get('conditions', '--')}"
        ]
        return "\n".join(lines)
    
    def cleanup_old_data(self, days_to_keep: int = 30) -> None:
        '''Removes weather data older than specified days to free memory.'''
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        for city_key, data_list in self.weather_data.items():
            # Filter out entries older than cutoff date
            self.weather_data[city_key] = [
                entry for entry in data_list 
                if entry.get('date', datetime.now()) >= cutoff_date
            ]