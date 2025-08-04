"""
Weather History Service - Historical weather data management.

This module provides comprehensive weather history tracking functionality
for storing, retrieving, and analyzing historical weather data. Designed
to support 24/7 weather monitoring and future prediction capabilities.

Classes:
    WeatherHistoryService: Main service for historical weather data operations
"""

from typing import Dict, List, Any, Optional
import csv
from pathlib import Path
from datetime import datetime, timedelta

from WeatherDashboard import config, dialog
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.utils import Utils
from WeatherDashboard.utils.unit_converter import UnitConverter

from WeatherDashboard.services.weather_service import WeatherAPIService
from WeatherDashboard.services.api_exceptions import WeatherDashboardError


class WeatherHistoryService:
    """Manage historical weather data storage and retrieval.
    
    Provides methods for storing current weather data and retrieving
    historical data for analysis and charting. Designed to support
    future expansion into 24/7 monitoring and prediction systems.
    
    Attributes:
        api_service: Weather API service for data generation
        utils: Utility functions for data processing
        logger: Logger for operation tracking
        weather_data: Dictionary storing weather data by city key
    """
    
    def __init__(self) -> None:
        """Initialize the weather history service.
        
        Args:
            api_service: Weather API service for data generation (injected for testability)
        """
        # Direct imports for stable utilities
        self.logger = Logger()
        self.config = config
        self.dialog = dialog
        self.utils = Utils()
        self.unit_converter = UnitConverter()

        # Injected dependencies for testable components
        self.api_service = WeatherAPIService()

        # Internal state
        self.weather_data = {}
        self._last_cleanup = datetime.now()  # Track when we last cleaned up data

# ================================
# 1. DATA STORAGE
# ================================    
    def store_current_weather(self, city: str, weather_data: Dict[str, Any], unit_system: str = "metric") -> None:
        """Store current weather data with timestamp for historical tracking.
        
        Stores data in both memory (for fast access) and CSV (for persistence).
        Also writes to text log for debugging purposes.
        
        Args:
            city: City name for the weather data
            weather_data: Weather data dictionary to store
        """
        # Validate inputs
        if not city or not city.strip():
            raise ValueError("City name cannot be empty")
        if not isinstance(weather_data, dict):
            raise ValueError("Weather data must be a dictionary")
        if unit_system not in ['metric', 'imperial']:
            raise ValueError("Unit system must be 'metric' or 'imperial'")

        # Check if cleanup is needed
        if self._should_perform_cleanup() or self._simple_memory_check():
            self.cleanup_old_data()
            self._last_cleanup = datetime.now()

        key = self.utils.city_key(city)
        existing_data = self.weather_data.setdefault(key, [])
        
        # Add timestamp if not present
        if 'date' not in weather_data:
            weather_data['date'] = datetime.now()

        # Always store data from scheduler, but limit memory usage
        existing_data.append(weather_data)
        
        # Limit stored data to prevent memory issues (keep last 30 entries per city)
        max_entries = self.config.MEMORY["max_entries_per_city"]
        if len(existing_data) > max_entries:
            existing_data[:] = existing_data[-max_entries:]  # Keep only the most recent entries
        
        # Store in CSV for persistence
        self._store_to_csv(city, weather_data)
        
        # Write to text log
        self._write_to_text_log(city, weather_data, unit_system)
        
        self.logger.info(f"Stored weather data for {city} - {len(existing_data)} entries")
    
    def _store_to_csv(self, city: str, weather_data: Dict[str, Any]) -> None:
        """Store weather data to CSV file for robust data handling.
        
        Args:
            city: City name for the weather data
            weather_data: Weather data dictionary to store
        """
        # Use the CSV directory configuration
        csv_file = Path(self.config.OUTPUT["csv_dir"]) / "weather_data.csv"

        # Ensure directory exists
        csv_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Define CSV headers based on weather data structure
        headers = [
            'timestamp', 'city', 'temperature', 'humidity', 'pressure', 'wind_speed',
            'wind_direction', 'conditions', 'feels_like', 'temp_min', 'temp_max',
            'wind_gust', 'visibility', 'cloud_cover', 'rain', 'snow', 'uv_index',
            'air_quality_index', 'source'
        ]
        
        # Prepare row data
        row_data = {
            'timestamp': weather_data.get('date', datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
            'city': city,
            'temperature': weather_data.get('temperature'),
            'humidity': weather_data.get('humidity'),
            'pressure': weather_data.get('pressure'),
            'wind_speed': weather_data.get('wind_speed'),
            'wind_direction': weather_data.get('wind_direction'),
            'conditions': weather_data.get('conditions'),
            'feels_like': weather_data.get('feels_like'),
            'temp_min': weather_data.get('temp_min'),
            'temp_max': weather_data.get('temp_max'),
            'wind_gust': weather_data.get('wind_gust'),
            'visibility': weather_data.get('visibility'),
            'cloud_cover': weather_data.get('cloud_cover'),
            'rain': weather_data.get('rain'),
            'snow': weather_data.get('snow'),
            'uv_index': weather_data.get('uv_index'),
            'air_quality_index': weather_data.get('air_quality_index'),
            'source': 'simulated' if self.utils.is_fallback(weather_data) else 'api'
        }
        
        try:
            # Create file with headers if it doesn't exist
            file_exists = csv_file.exists()
            
            with open(csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(row_data)
                
        except (OSError, IOError, PermissionError) as e:
            self.logger.error(f"Failed to write CSV data for {city}: {e}")

# ================================
# 2. DATA ACCESS
# ================================    
    def get_historical(self, city: str, num_days: int) -> List[Dict[str, Any]]:
        """Generate historical weather data for a city.
        
        Args:
            city: Target city name for data generation
            num_days: Number of days of historical data to generate
            
        Returns:
            List[Dict[str, Any]]: Generated historical weather data
        """
        return self.api_service.fallback.generate(city, num_days)

    def get_recent_data(self, city: str, days_back: int = 7) -> List[Dict[str, Any]]:
        """Return recent weather data for a city from the last N days.
        
        Stored in local memory, fast, limited to 30 entries.

        Args:
            city: Target city name for data retrieval
            days_back: Number of days to look back (default 7)

        Returns:
            List[Dict[str, Any]]: Recent weather data entries for the specified time period
        """
        city_data = self.weather_data.get(self.utils.city_key(city), [])
        cutoff_date = datetime.now().date() - timedelta(days=days_back)
        
        return [
            entry for entry in city_data 
            if entry.get('date', datetime.now()).date() >= cutoff_date
        ]

    def get_recent_data_from_csv(self, city: str, days_back: int = 7) -> List[Dict[str, Any]]:
        """Get recent weather data from CSV file.
        
        Args:
            city: Target city name for data retrieval
            days_back: Number of days to look back (default 7)
            
        Returns:
            List[Dict[str, Any]]: Recent weather data entries from CSV
        """
        # Use the config CSV directory configuration
        csv_file = Path(self.config.OUTPUT["csv_dir"]) / "weather_data.csv"
        
        if not csv_file.exists():
            return []
        
        cutoff_date = datetime.now().date() - timedelta(days=days_back)
        recent_data = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                # Validate CSV structure
                expected_fields = ['timestamp', 'city', 'temperature', 'humidity', 'pressure', 'wind_speed']
                actual_fields = reader.fieldnames or []
                missing_fields = [field for field in expected_fields if field not in actual_fields]

                if missing_fields:
                    self.logger.error(f"CSV file missing required fields: {missing_fields}")
                    return []

                for row in reader:
                    # Validate required fields
                    required_fields = ['timestamp', 'city']
                    for field in required_fields:
                        if field not in row:
                            self.logger.warn(f"Missing required field '{field}' in CSV row for {city}")
                            continue

                    # Filter by city
                    if row['city'] != city:
                        continue

                    # Parse timestamp
                    try:
                        row_date = datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S").date()
                        if row_date >= cutoff_date:
                            # Convert back to dictionary format
                            data_entry = {
                                'date': datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S"),
                                'temperature': float(row['temperature']) if row['temperature'] != '' else None,
                                'humidity': int(row['humidity']) if row['humidity'] != '' else None,
                                'pressure': int(row['pressure']) if row['pressure'] != '' else None,
                                'wind_speed': float(row['wind_speed']) if row['wind_speed'] != '' else None,
                                'wind_direction': float(row['wind_direction']) if row['wind_direction'] != '' else None,
                                'conditions': row['conditions'] if row['conditions'] != '' else None,
                                'feels_like': float(row['feels_like']) if row['feels_like'] != '' else None,
                                'temp_min': float(row['temp_min']) if row['temp_min'] != '' else None,
                                'temp_max': float(row['temp_max']) if row['temp_max'] != '' else None,
                                'wind_gust': float(row['wind_gust']) if row['wind_gust'] != '' else None,
                                'visibility': float(row['visibility']) if row['visibility'] != '' else None,
                                'cloud_cover': int(row['cloud_cover']) if row['cloud_cover'] != '' else None,
                                'rain': float(row['rain']) if row['rain'] != '' else None,
                                'snow': float(row['snow']) if row['snow'] != '' else None,
                                'uv_index': float(row['uv_index']) if row['uv_index'] != '' else None,
                                'air_quality_index': int(row['air_quality_index']) if row['air_quality_index'] != '' else None,
                            }
                            recent_data.append(data_entry)

                    except (ValueError, KeyError) as e:
                        self.logger.warn(f"Error parsing CSV row for {city}: {e}")
                        continue
                        
        except (OSError, IOError, PermissionError) as e:
            self.logger.error(f"Failed to read CSV data for {city}: {e}")
            return []
        
        return recent_data
    
    def get_all_cities_from_csv(self) -> List[str]:
        """Get list of all cities that have data in the CSV file.
        
        Returns:
            List[str]: List of unique city names
        """
        csv_file = Path(self.config.OUTPUT["csv_dir"]) / "weather_data.csv"
        
        if not csv_file.exists():
            return []
        
        cities = set()
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'city' in row and row['city']:
                        cities.add(row['city'])
        except (OSError, IOError, PermissionError) as e:
            self.logger.error(f"Failed to read CSV file: {e}")
            return []
        
        return list(cities)
    
    def _safe_float_parse(self, value: str) -> Optional[float]:
        """Safely parse float value from CSV."""
        if not value or value.strip() == '':
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def _safe_int_parse(self, value: str) -> Optional[int]:
        """Safely parse int value from CSV."""
        if not value or value.strip() == '':
            return None
        try:
            return int(float(value))  # Handle float strings like "1.0"
        except (ValueError, TypeError):
            return None

# ================================
# 3. DATA TEXT FILE FOR BACKUP
# ================================    
    def _write_to_text_log(self, city: str, data: Dict[str, Any], unit_system: str) -> None:
        """Write formatted weather data to text log for debugging.
        
        Creates a formatted text log entry with timestamp, city, and all weather metrics
        in the specified unit system. Handles file I/O errors gracefully
        
        Args:
            city: City name for the weather data
            weather_data: Weather data dictionary to text log
            unit_system: Unit system for formatting ('metric' or 'imperial')
        """
        try:
            text_entry = self._format_data_for_logging(city, data, unit_system)
            with open(self.config.OUTPUT["text_file"], "a", encoding="utf-8") as f:
                f.write(text_entry)

            fallback_text = "Simulated" if self.utils.is_fallback(data) else "Live"
            self.logger.info(f"Weather data written for {self.utils.city_key(city)} - {fallback_text}")
            
        except (OSError, IOError, PermissionError) as e:
            # Raise as custom exception for controller to handle via error_handler
            self.dialog.dialog_manager.show_theme_aware_dialog('error', 'file_error', 
                "Failed to write {info} to {file}: {reason}", 
                info="weather data", file=self.config.OUTPUT["text_file"], reason=str(e))
            raise WeatherDashboardError(f"Failed to write weather data to {self.config.OUTPUT['text_file']}: {e}")
        except Exception as e:
            raise WeatherDashboardError(f"Unexpected error writing weather data: {e}")

    def _format_data_for_logging(self, city: str, weather_data: Dict[str, Any], unit_system: str) -> str:
        """Format weather data for text file logging."""
        timestamp = weather_data.get('date', datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            f"\n\nTime: {timestamp}",
            f"City: {self.utils.city_key(city)}",
            f"Unit System: {unit_system}",
            f"Temperature: {self.unit_converter.format_value('temperature', weather_data.get('temperature'), unit_system)}",
            f"Humidity: {self.unit_converter.format_value('humidity', weather_data.get('humidity'), unit_system)}",
            f"Pressure: {self.unit_converter.format_value('pressure', weather_data.get('pressure'), unit_system)}",
            f"Wind Speed: {self.unit_converter.format_value('wind_speed', weather_data.get('wind_speed'), unit_system)}",
            f"Conditions: {weather_data.get('conditions', '--')}"
        ]
        return "\n".join(lines)
    
# ================================
# 4. MEMORY MANAGEMENT
# ================================  
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
            max_entries = self.config.MEMORY["max_entries_per_city"]
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
        
        return (cities_count > self.config.MEMORY["max_cities_stored"] or 
                total_entries > self.config.MEMORY["max_total_entries"])

    def _should_perform_cleanup(self) -> bool:
        """Check if cleanup should be performed based on time interval.
        
        Returns:
            bool: True if cleanup is needed
        """
        if not hasattr(self, '_last_cleanup'):
            self._last_cleanup = datetime.now()
            return False
        
        current_time = datetime.now()
        cleanup_interval = self.config.MEMORY.get("cleanup_interval_hours", 24)
        time_since_cleanup = (current_time - self._last_cleanup).total_seconds()
        
        # Add minimum cleanup interval to prevent excessive cleanup
        min_cleanup_interval = self.config.MEMORY.get("minimum_cleanup_interval", 3600)
        return time_since_cleanup > max(cleanup_interval * 3600, min_cleanup_interval)