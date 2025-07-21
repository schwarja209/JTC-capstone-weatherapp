"""
View models for preparing display-ready data from raw weather data.

This module provides view model classes that transform raw weather data
into formatted, display-ready information. Handles data sanitization,
formatting, status determination, and user-friendly presentation.

Classes:
    WeatherViewModel: Transforms raw weather data into display-ready format
"""

from typing import Dict, Any

from WeatherDashboard import config, styles
from WeatherDashboard.utils.utils import is_fallback, format_fallback_status
from WeatherDashboard.utils.unit_converter import UnitConverter


class WeatherViewModel:
    """Prepare sanitized, display-ready data from raw weather data.
    
    Transforms raw weather data into properly formatted strings and status
    information suitable for UI display. Encapsulates all formatting logic
    for easy testing, maintenance, and future extension.
    
    Attributes:
        city_name: Formatted city name for display
        unit_system: Unit system for value formatting
        raw_data: Original raw weather data
        date_str: Formatted date string
        status: Status text including fallback and warning information
        metrics: Dictionary of formatted metric values
    """
    def __init__(self, city: str, data: Dict[str, Any], unit_system: str) -> None:
        """Initialize the weather view model with formatted display data.
        
        Processes raw weather data into display-ready format on initialization
        for efficient access to formatted values throughout the UI.
        
        Args:
            city: City name for display
            data: Raw weather data dictionary
            unit_system: Unit system for value formatting ('metric' or 'imperial')
        """
        self.city_name: str = city
        self.unit_system: str = unit_system
        self.raw_data: Dict[str, Any] = data
        
        # Process all display data on initialization
        self.date_str: str = self._format_date()
        self.status: str = self._format_status()
        self.metrics: Dict[str, str] = self._format_metrics()

    def _format_date(self) -> str:
        """Format the date for display.
        
        Converts datetime object to display string format. Handles both explicit
        date values from weather data and current time fallback for real-time data.
        Provides consistent date formatting across different data sources.

        Returns:
            str: Formatted date string in YYYY-MM-DD format, or '--' if no date available
        """
        if 'date' in self.raw_data and self.raw_data['date']:
            return self.raw_data['date'].strftime("%Y-%m-%d")
        return "--"

    def _format_status(self) -> str:
        """Format the status text including fallback and warning information.
        
        Creates status text indicating data source (live vs simulated) and
        any conversion warnings that occurred during processing.
        
        Returns:
            str: Formatted status text with data source and warning information
        """
        status = f" {format_fallback_status(is_fallback(self.raw_data), 'display')}"
        
        # Check for conversion warnings
        if '_conversion_warnings' in self.raw_data:
            status += f" (Warning: {self.raw_data['_conversion_warnings']})"
        
        return status

    def _format_metrics(self) -> Dict[str, str]:
        """Format weather metrics with enhanced display combinations.
        
        Returns:
            Dict[str, str]: Dictionary mapping metric keys to formatted display values
        """
        metrics = {}

        # Process ALL individual metrics first
        for metric_key in config.METRICS:
            raw_value = self.raw_data.get(metric_key)
            display_val = UnitConverter.format_value(metric_key, raw_value, self.unit_system)
            metrics[metric_key] = display_val
        
        # Add enhanced combination displays
        metrics['enhanced_temperature'] = self._format_enhanced_display('temperature')
        metrics['temp_range'] = self._format_enhanced_display('temp_range')
        metrics['enhanced_conditions'] = self._format_enhanced_display('conditions')
        metrics['enhanced_wind'] = self._format_enhanced_display('wind')
        
        return metrics

    def _format_enhanced_display(self, display_type: str) -> str:
        """Format complex metric displays with enhanced user-friendly presentation.
    
        Handles special formatting for temperature (with feels-like), temperature ranges,
        weather conditions (with icons), and wind information (with direction/gusts).
        
        Args:
            display_type: Type of enhanced display ('temperature', 'temp_range', 
                        'conditions', 'wind')
            
        Returns:
            str: Formatted display string with enhanced information, or '--' if unavailable
        """
        if display_type == 'temperature':
            temp = self.raw_data.get('temperature')
            feels_like = self.raw_data.get('feels_like')
            if temp is None:
                return "--"
            
            temp_str = UnitConverter.format_value('temperature', temp, self.unit_system)
            
            if feels_like is not None:
                difference = abs(feels_like - temp)
                # Only show "feels like" if difference is significant (>2 degrees)
                TEMP_DIFF_THRESHOLD_METRIC = 2.0  # °C
                TEMP_DIFF_THRESHOLD_IMPERIAL = 3.6  # °F
                threshold = TEMP_DIFF_THRESHOLD_METRIC if self.unit_system == 'metric' else TEMP_DIFF_THRESHOLD_IMPERIAL
                
                if difference >= threshold:
                    feels_str = UnitConverter.format_value('feels_like', feels_like, self.unit_system)
                    
                    # Determine if feels warmer or cooler
                    if feels_like > temp:
                        return f"{temp_str} (feels {feels_str} ↑)"
                    else:
                        return f"{temp_str} (feels {feels_str} ↓)"
            
            return temp_str
        
        elif display_type == 'temp_range':
            temp_min = self.raw_data.get('temp_min')
            temp_max = self.raw_data.get('temp_max')
            if temp_min is None or temp_max is None:
                return "--"
            min_str = UnitConverter.format_value('temp_min', temp_min, self.unit_system)
            max_str = UnitConverter.format_value('temp_max', temp_max, self.unit_system)
            return f"{min_str} - {max_str}"
        
        elif display_type == 'conditions':
            conditions = self.raw_data.get('conditions', '--')
            icon = self._get_weather_icon()
            return f"{icon} {conditions}" if icon else str(conditions)
        
        elif display_type == 'wind':
            wind_speed = self.raw_data.get('wind_speed')
            wind_direction = self.raw_data.get('wind_direction')
            wind_gust = self.raw_data.get('wind_gust')
            
            if wind_speed is None:
                return "--"
            
            speed_str = UnitConverter.format_value('wind_speed', wind_speed, self.unit_system)
            
            # Add direction if available
            if wind_direction is not None:
                compass = self._degrees_to_compass(wind_direction)
                wind_info = f"{speed_str} from {compass}"
            else:
                wind_info = speed_str
            
            # Add gusts if available and significant
            if wind_gust is not None and wind_gust > wind_speed:
                gust_str = UnitConverter.format_value('wind_gust', wind_gust, self.unit_system)
                wind_info += f", gusts {gust_str}"
            
            return wind_info
        
        return "--"

    def _degrees_to_compass(self, degrees: float) -> str:
        """Convert wind direction degrees to compass direction."""
        if degrees is None:
            return ""
        
        directions = ["N","NNE","NE","ENE","E","ESE","SE","SSE",
                    "S","SSW","SW","WSW","W","WNW","NW","NNW"]
        return directions[int((degrees + 11.25) / 22.5) % 16]

    def _get_weather_icon(self) -> str:
        """Convert weather icon code to emoji."""
        icon_code = self.raw_data.get('weather_icon', '')
        return styles.WEATHER_ICONS.get(icon_code, '')

    def get_display_data(self) -> Dict[str, Any]:
        """Return all formatted data as a comprehensive dictionary.
        
        Provides a complete interface for accessing all formatted display data.
        Useful for future features like theme system processing, data export,
        and API endpoints.
        
        Returns:
            Dict containing complete formatted display data including city, date, 
            status, individual metrics, and enhanced display combinations
        """
        return {
            'city_name': self.city_name,
            'date_str': self.date_str,
            'status': self.status,
            'individual_metrics': self.metrics,
            'enhanced_displays': {
                'enhanced_temperature': self.metrics.get('enhanced_temperature', '--'),
                'temp_range': self.metrics.get('temp_range', '--'),
                'enhanced_conditions': self.metrics.get('enhanced_conditions', '--'),
                'enhanced_wind': self.metrics.get('enhanced_wind', '--')
            },
            'raw_data_available': bool(self.raw_data),
            'has_conversion_warnings': '_conversion_warnings' in self.raw_data,
            'unit_system': self.unit_system
        }

    def get_metric_value(self, metric_key: str) -> str:
        """Get a specific formatted metric value.
        
        Args:
            metric_key: Key of the metric to retrieve (e.g., 'temperature', 'humidity')
            
        Returns:
            str: Formatted metric value with units, or '--' if not available
        """
        return self.metrics.get(metric_key, "--")