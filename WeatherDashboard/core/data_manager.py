"""
Data management for weather information including fetching, storage, and unit conversion.

This module provides comprehensive weather data management including API communication,
fallback data generation, unit conversion, data storage, and memory management.
Handles both live API data and simulated fallback data seamlessly.

Classes:
    WeatherDataManager: Main data management class with API integration and fallback handling
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
        """
        self.api_service = WeatherAPIService()
        self.weather_data = {}

        # Track when we last cleaned up data
        self._last_cleanup = datetime.now()
        self._cleanup_interval_hours = config.MEMORY["cleanup_interval_hours"]  # Cleanup every ___ hours

    def fetch_current(self, city: str, unit_system: str) -> Tuple[Dict[str, Any], bool, Optional[Exception]]:
        """Fetch current weather data for a city, using fallback if API call fails.
        
        Attempts to fetch live weather data from API, converts units as needed,
        and stores the data for future reference. Performs automatic cleanup
        periodically to manage memory usage.
        
        Args:
            city: Normalized city name (expected to already be processed)
            unit_system: Target unit system for the data ('metric' or 'imperial')
            
        Returns:
            Tuple containing:
                - Dict[str, Any]: Weather data with converted units
                - bool: True if fallback data was used
                - Optional[Exception]: Exception if API call failed, None otherwise
        """
        raw_data, use_fallback, error_exception = self.api_service.fetch_current(city)

        # All API and fallback data is assumed to be in metric units and converted downstream.
        # If this changes in future (e.g., new fallback with imperial), update convert_units().
        converted_data = self.convert_units(raw_data, unit_system)

        # Simple cleanup: time-based OR memory limits exceeded
        current_time = datetime.now()
        should_cleanup = (current_time - self._last_cleanup).total_seconds() > (self._cleanup_interval_hours * 3600)
        memory_over_limit = self._simple_memory_check()

        if should_cleanup or memory_over_limit:
            self.cleanup_old_data()
            self._last_cleanup = current_time

        key = city_key(city)
        existing_data = self.weather_data.setdefault(key, [])
        last_date = existing_data[-1].get("date") if existing_data else None
        current_date = converted_data.get("date")
        if not existing_data or (last_date and current_date and last_date.date() != current_date.date()):
            existing_data.append(converted_data)
            # Limit stored data to prevent memory issues (keep last 30 entries per city)
            max_entries = config.MEMORY["max_entries_per_city"]
            if len(existing_data) > max_entries:
                existing_data[:] = existing_data[-max_entries:]  # Keep only the most recent entries

        return converted_data, use_fallback, error_exception
    
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
            'wind_speed': UnitConverter.convert_wind_speed,
            'feels_like': UnitConverter.convert_temperature,
            'temp_min': UnitConverter.convert_temperature,
            'temp_max': UnitConverter.convert_temperature,
            'wind_gust': UnitConverter.convert_wind_speed,
            'visibility': UnitConverter.convert_visibility,
            'rain': UnitConverter.convert_precipitation,
            'snow': UnitConverter.convert_precipitation,
            'rain_1h': UnitConverter.convert_precipitation,
            'rain_3h': UnitConverter.convert_precipitation,
            'snow_1h': UnitConverter.convert_precipitation,
            'snow_3h': UnitConverter.convert_precipitation,
            'heat_index': UnitConverter.convert_heat_index,
            'wind_chill': UnitConverter.convert_wind_chill,
            'dew_point': UnitConverter.convert_dew_point
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
        """Generate historical weather data for a city."""
        return self.api_service.fallback.generate(city, num_days)

    def get_recent_data(self, city: str, days_back: int = 7) -> List[Dict[str, Any]]:
        """Return recent weather data for a city from the last N days."""
        city_data = self.weather_data.get(city_key(city), [])
        cutoff_date = datetime.now().date() - timedelta(days=days_back)
        
        return [
            entry for entry in city_data 
            if entry.get('date', datetime.now()).date() >= cutoff_date
        ]

    def write_to_file(self, city: str, data: Dict[str, Any], unit_system: str) -> None:
        """Write formatted weather data to a log file with timestamp and unit system information.
        
        Creates a formatted log entry with timestamp, city, and all weather metrics
        in the specified unit system. Handles file I/O errors gracefully.
        
        Args:
            city: City name for the log entry
            data: Weather data dictionary to log
            unit_system: Unit system for formatting ('metric' or 'imperial')
        """
        try:
            log_entry = self.format_data_for_logging(city, data, unit_system)
            with open(config.OUTPUT["log"], "a", encoding="utf-8") as f:
                f.write(log_entry)

            fallback_text = "Simulated" if is_fallback(data) else "Live"
            Logger.info(f"Weather data written for {city_key(city)} - {fallback_text}")
            
        except (OSError, IOError, PermissionError) as e:
            # Raise as custom exception for controller to handle via error_handler
            from WeatherDashboard.services.api_exceptions import WeatherDashboardError
            raise WeatherDashboardError(f"Failed to write weather data to file: {e}")
        except Exception as e:
            from WeatherDashboard.services.api_exceptions import WeatherDashboardError
            raise WeatherDashboardError(f"Unexpected error writing weather data: {e}")

    def format_data_for_logging(self, city: str, data: Dict[str, Any], unit_system: str) -> str:
        """Format weather data for file logging."""
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
        """Remove old weather data and manage memory usage.
        
        Args:
            days_to_keep: Number of days of data to retain (default 30)
        """
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        # Remove old entries and enforce per-city limits
        for city_key, data_list in self.weather_data.items():
            # Filter by date
            recent_data = [
                entry for entry in data_list 
                if entry.get('date', datetime.now()) >= cutoff_date
            ]
            # Enforce per-city entry limit
            max_entries = config.MEMORY["max_entries_per_city"]
            self.weather_data[city_key] = recent_data[-max_entries:]
        
        # Remove empty city entries
        empty_cities = [city for city, data in self.weather_data.items() if not data]
        for city in empty_cities:
            del self.weather_data[city]
    
    def _simple_memory_check(self) -> bool:
        """Check if memory limits are exceeded.
        
        Returns:
            bool: True if cleanup is needed due to memory limits
        """
        total_entries = sum(len(entries) for entries in self.weather_data.values())
        cities_count = len(self.weather_data)
        
        return (cities_count > config.MEMORY["max_cities_stored"] or 
                total_entries > config.MEMORY["max_total_entries"])