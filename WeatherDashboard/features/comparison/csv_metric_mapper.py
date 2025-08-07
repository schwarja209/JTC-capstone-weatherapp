"""
CSV metric mapping utilities.

This module provides utilities for mapping CSV column names to standard
weather metrics using fuzzy matching. Handles various naming conventions
and provides efficient metric name normalization.

Classes:
    CSVMetricMapper: Main mapper for CSV metric name matching
"""

from difflib import SequenceMatcher
from typing import Dict, List, Optional

from WeatherDashboard.utils.logger import Logger


class CSVMetricMapper:
    """Maps CSV column names to standard weather metrics using fuzzy matching.
    
    Provides fuzzy matching between CSV column names and standard weather
    metrics, handling various naming conventions and abbreviations.
    Supports both exact and approximate matching with configurable thresholds.
    
    Attributes:
        logger: Application logger instance
        standard_metrics: Dictionary of standard metric names and their variations
        similarity_threshold: Minimum similarity score for fuzzy matching
    """
    
    def __init__(self, similarity_threshold: float = 0.6) -> None:
        """Initialize the CSV metric mapper.
        
        Sets up standard metric mappings and configures the similarity
        threshold for fuzzy matching operations.
        
        Args:
            similarity_threshold: Minimum similarity score for fuzzy matching (0.0-1.0)
        """
        self.logger = Logger()
        self.similarity_threshold = similarity_threshold
        
        # Standard weather metrics and their variations
        self.standard_metrics = {
            'temperature': [
                'temp', 'temperature', 'temp_f', 'temp_c', 'fahrenheit', 'celsius',
                't', 'temp_high', 'temp_low', 'max_temp', 'min_temp', 'avg_temp', 'avg_temp_F'
            ],
            'humidity': [
                'humidity', 'hum', 'relative_humidity', 'rh', 'humidity_percent',
                'moisture', 'dew_point'
            ],
            'pressure': [
                'pressure', 'barometric_pressure', 'atm', 'hpa', 'mb', 'millibars',
                'barometer', 'air_pressure'
            ],
            'wind_speed': [
                'wind_speed', 'wind', 'wind_velocity', 'wind_mph', 'wind_kmh',
                'wind_knots', 'wind_force', 'wind_velocity_mph'
            ],
            'wind_direction': [
                'wind_direction', 'wind_dir', 'wind_bearing', 'wind_degrees',
                'wind_angle', 'wind_heading'
            ],
            'wind_gust': [
                'wind_gust', 'gust', 'wind_gust_speed', 'gust_speed', 'wind_gust_mph'
            ],
            'visibility': [
                'visibility', 'vis', 'visibility_miles', 'visibility_km',
                'visibility_distance', 'fog_distance'
            ],
            'cloud_cover': [
                'cloud_cover', 'clouds', 'cloud_percentage', 'cloud_amount',
                'sky_cover', 'cloudiness'
            ],
            'feels_like': [
                'feels_like', 'apparent_temperature', 'real_feel', 'apparent_temp'
            ],
            'temp_min': [
                'temp_min', 'min_temp', 'minimum_temperature', 'low_temp', 'low_temperature', 'min_temp_F'
            ],
            'temp_max': [
                'temp_max', 'max_temp', 'maximum_temperature', 'high_temp', 'high_temperature', 'max_temp_F'
            ],
            'rain': [
                'rain', 'rainfall', 'rain_amount', 'rain_mm', 'rain_inches', 'precipitation', 'precip_mm'
            ],
            'snow': [
                'snow', 'snowfall', 'snow_amount', 'snow_mm', 'snow_inches'
            ],
            'weather_main': [
                'weather_main', 'weather_type', 'weather', 'condition', 'weather_condition',
                'conditions', 'weather_desc', 'weather_description'
            ],
            'weather_id': [
                'weather_id', 'weather_code', 'condition_id'
            ],
            'weather_icon': [
                'weather_icon', 'icon', 'weather_icon_code'
            ],
            'uv_index': [
                'uv_index', 'uv', 'ultraviolet', 'uv_radiation', 'sun_index'
            ],
            'air_quality_index': [
                'air_quality_index', 'aqi', 'air_quality', 'pollution_index', 'air_pollution'
            ],
            'air_quality_description': [
                'air_quality_description', 'aqi_description', 'air_quality_status', 'pollution_status'
            ],
            'heat_index': [
                'heat_index', 'heat_index_f', 'heat_index_c', 'apparent_heat'
            ],
            'wind_chill': [
                'wind_chill', 'wind_chill_f', 'wind_chill_c', 'apparent_cold'
            ],
            'dew_point': [
                'dew_point', 'dew_point_f', 'dew_point_c', 'dewpoint'
            ],
            'precipitation_probability': [
                'precipitation_probability', 'rain_probability', 'snow_probability', 'precip_chance',
                'rain_chance', 'snow_chance', 'precipitation_chance'
            ],
            'weather_comfort_score': [
                'weather_comfort_score', 'comfort_score', 'comfort_index', 'weather_comfort'
            ]
        }
        
        # Create reverse mapping for quick lookup
        self._create_reverse_mapping()
    
    def _create_reverse_mapping(self) -> None:
        """Create reverse mapping from variations to standard metrics.
        
        Builds a dictionary that maps each variation to its standard
        metric name for efficient lookup.
        """
        self.variation_to_standard = {}
        for standard_name, variations in self.standard_metrics.items():
            for variation in variations:
                self.variation_to_standard[variation.lower()] = standard_name
    
    def map_csv_columns(self, csv_headers: List[str]) -> Dict[str, str]:
        """Map CSV column headers to standard metric names.
        
        Processes a list of CSV column headers and maps each one to
        the appropriate standard metric name using fuzzy matching.
        
        Args:
            csv_headers: List of CSV column header names
            
        Returns:
            Dictionary mapping CSV column names to standard metric names
        """
        mapping = {}
        
        for header in csv_headers:
            # Skip date columns
            if self._is_date_column(header):
                continue
            
            # Skip location columns (these are metadata, not weather metrics)
            if self._is_location_column(header):
                self.logger.debug(f"Skipping location column: '{header}'")
                continue
            
            # Try exact match first
            standard_metric = self._exact_match(header)
            if standard_metric:
                mapping[header] = standard_metric
                continue
            
            # Try fuzzy match
            standard_metric = self._fuzzy_match(header)
            if standard_metric:
                mapping[header] = standard_metric
                self.logger.info(f"Mapped CSV column '{header}' to standard metric '{standard_metric}'")
            else:
                self.logger.warn(f"Could not map CSV column '{header}' to any standard metric")
        
        return mapping
    
    def _is_date_column(self, header: str) -> bool:
        """Check if a column header represents a date column.
        
        Args:
            header: Column header name to check
            
        Returns:
            True if the header represents a date column
        """
        date_keywords = ['date', 'time', 'datetime', 'timestamp']
        header_lower = header.lower()
        
        for keyword in date_keywords:
            if keyword in header_lower:
                return True
        
        return False

    def _is_location_column(self, header: str) -> bool:
        """Check if a column header represents a location column.
        
        Args:
            header: Column header name to check
            
        Returns:
            True if the header represents a location column
        """
        location_keywords = ['city', 'location', 'place', 'town', 'latitude', 'longitude', 'lat', 'lon', 'coord']
        header_lower = header.lower()
        
        for keyword in location_keywords:
            if keyword in header_lower:
                return True
        
        return False
    
    def _exact_match(self, header: str) -> Optional[str]:
        """Find exact match for a CSV column header.
        
        Checks if the header exactly matches any known variation
        of a standard metric name.
        
        Args:
            header: CSV column header name
            
        Returns:
            Standard metric name if exact match found, None otherwise
        """
        header_lower = header.lower()
        
        # Check direct mapping
        if header_lower in self.variation_to_standard:
            return self.variation_to_standard[header_lower]
        
        # Check for exact matches in variations
        for standard_name, variations in self.standard_metrics.items():
            if header_lower in [v.lower() for v in variations]:
                return standard_name
        
        return None
    
    def _fuzzy_match(self, header: str) -> Optional[str]:
        """Find fuzzy match for a CSV column header.
        
        Uses sequence matching to find the best match between the
        header and known metric variations.
        
        Args:
            header: CSV column header name
            
        Returns:
            Standard metric name if good match found, None otherwise
        """
        header_lower = header.lower()
        best_match = None
        best_score = 0.0
        
        # Try matching against all variations
        for standard_name, variations in self.standard_metrics.items():
            for variation in variations:
                variation_lower = variation.lower()
                
                # Calculate similarity score
                score = SequenceMatcher(None, header_lower, variation_lower).ratio()
                
                # Update best match if score is higher
                if score > best_score and score >= self.similarity_threshold:
                    best_score = score
                    best_match = standard_name
        
        return best_match
    
    def get_available_metrics(self, csv_headers: List[str]) -> List[str]:
        """Get list of available standard metrics from CSV headers.
        
        Maps CSV headers to standard metrics and returns the list
        of available standard metrics.
        
        Args:
            csv_headers: List of CSV column headers
            
        Returns:
            List of available standard metric names
        """
        mapping = self.map_csv_columns(csv_headers)
        return sorted(list(set(mapping.values())))