"""
View models for preparing display-ready data from raw weather data.

This module provides view model classes that transform raw weather data
into formatted, display-ready information. Handles data sanitization,
formatting, status determination, and user-friendly presentation.

Classes:
    WeatherViewModel: Transforms raw weather data into display-ready format
"""

from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime

from WeatherDashboard import config, styles
from WeatherDashboard.utils.utils import Utils
from WeatherDashboard.utils.unit_converter import UnitConverter


@dataclass
class WeatherDisplayData:
    """Type-safe container for weather display data.
    
    Provides a structured, immutable representation of all weather display
    information with type safety and clear field documentation.
    """
    city_name: str
    date_str: str
    status: str
    individual_metrics: Dict[str, str]
    enhanced_displays: Dict[str, str]
    raw_data_available: bool
    has_conversion_warnings: bool
    unit_system: str

    # Lightweight transformation metadata
    timestamp: datetime
    transformation_status: str = "success"  # "success", "partial", "failed"
    data_quality: str = "unknown"  # "live", "simulated", "cached", "unknown"

    def __post_init__(self):
        """Validate dataclass after initialization."""
        if not self.city_name:
            raise ValueError("city_name cannot be empty")
        if self.unit_system not in ['metric', 'imperial']:
            raise ValueError("unit_system must be 'metric' or 'imperial'")
        if self.transformation_status not in ['success', 'partial', 'failed']:
            raise ValueError("transformation_status must be 'success', 'partial', or 'failed'")
        if self.data_quality not in ['live', 'simulated', 'cached', 'unknown']:
            raise ValueError("data_quality must be 'live', 'simulated', 'cached', or 'unknown'")

@dataclass
class MetricValue:
    """Type-safe container for metric values.
    
    Provides structured access to metric data with availability status
    and type safety for metric operations.
    """
    value: str
    is_available: bool
    metric_key: str
    unit_system: str

    # Lightweight transformation metadata
    timestamp: datetime
    data_quality: str = "unknown"

    def __post_init__(self):
        """Validate dataclass after initialization."""
        if not self.metric_key:
            raise ValueError("metric_key cannot be empty")
        if self.unit_system not in ['metric', 'imperial']:
            raise ValueError("unit_system must be 'metric' or 'imperial'")
        if self.data_quality not in ['live', 'simulated', 'cached', 'unknown']:
            raise ValueError("data_quality must be 'live', 'simulated', 'cached', or 'unknown'")

@dataclass
class EnhancedDisplays:
    """Type-safe container for enhanced display combinations.
    
    Groups related enhanced display values for better organization
    and type safety.
    """
    enhanced_temperature: str
    temp_range: str
    enhanced_conditions: str
    enhanced_wind: str


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
        # Direct imports for stable utilities
        self.config = config
        self.styles = styles
        self.utils = Utils()
        self.unit_converter = UnitConverter()
        self.datetime = datetime

        # Instance data
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
        status = f" {self.utils.format_fallback_status(self.utils.is_fallback(self.raw_data), 'display')}"
        
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
        for metric_key in self.config.METRICS:
            raw_value = self.raw_data.get(metric_key)
            display_val = self.unit_converter.format_value(metric_key, raw_value, self.unit_system)
            metrics[metric_key] = display_val
        
        # Add enhanced combination displays
        metrics['enhanced_temperature'] = self._format_enhanced_display('temperature')
        metrics['temp_range'] = self._format_enhanced_display('temp_range')
        metrics['enhanced_conditions'] = self._format_enhanced_display('conditions')
        metrics['enhanced_wind'] = self._format_enhanced_display('wind')
        
        return metrics

    def _format_enhanced_display(self, display_type: str) -> str:
        """Format complex metric displays with enhanced user-friendly presentation.
    
        Delegates to specific formatting methods based on display type.
        
        Args:
            display_type: Type of enhanced display ('temperature', 'temp_range', 'conditions', 'wind')
            
        Returns:
            str: Formatted display string with enhanced information, or '--' if unavailable
        """
        if display_type == 'temperature':
            return self._format_temperature_display()
        elif display_type == 'temp_range':
            return self._format_temp_range_display()
        elif display_type == 'conditions':
            return self._format_conditions_display()
        elif display_type == 'wind':
            return self._format_wind_display()
        else:
            return "--"

    def _format_temperature_display(self) -> str:
        """Format temperature with feels-like information.
        
        Returns:
            str: Formatted temperature string with feels-like information if significant
        """
        temp = self.raw_data.get('temperature')
        feels_like = self.raw_data.get('feels_like')
        if temp is None:
            return "--"
        
        temp_str = self.unit_converter.format_value('temperature', temp, self.unit_system)
        
        if feels_like is not None:
            difference = abs(feels_like - temp)
            # Only show "feels like" if difference is significant (>2 degrees)
            threshold = self.config.TEMP_DIFF_THRESHOLD_METRIC if self.unit_system == 'metric' else self.config.TEMP_DIFF_THRESHOLD_IMPERIAL
            
            if difference >= threshold:
                feels_str = self.unit_converter.format_value('feels_like', feels_like, self.unit_system)
                
                # Determine if feels warmer or cooler
                if feels_like > temp:
                    return f"{temp_str} (feels {feels_str} ↑)"
                else:
                    return f"{temp_str} (feels {feels_str} ↓)"
        
        return temp_str

    def _format_temp_range_display(self) -> str:
        """Format temperature range display.
        
        Returns:
            str: Formatted temperature range string (min - max)
        """
        temp_min = self.raw_data.get('temp_min')
        temp_max = self.raw_data.get('temp_max')
        if temp_min is None or temp_max is None:
            return "--"
        min_str = self.unit_converter.format_value('temp_min', temp_min, self.unit_system)
        max_str = self.unit_converter.format_value('temp_max', temp_max, self.unit_system)
        return f"{min_str} - {max_str}"
        
    def _format_conditions_display(self) -> str:
        """Format weather conditions with icon.
        
        Returns:
            str: Formatted conditions string with weather icon
        """
        conditions = self.raw_data.get('conditions', '--')
        icon = self._get_weather_icon()
        return f"{icon} {conditions}" if icon else str(conditions)
        
    def _format_wind_display(self) -> str:
        """Format wind information with direction and gusts.
        
        Returns:
            str: Formatted wind string with speed, direction, and gusts
        """
        wind_speed = self.raw_data.get('wind_speed')
        wind_direction = self.raw_data.get('wind_direction')
        wind_gust = self.raw_data.get('wind_gust')
        
        if wind_speed is None:
            return "--"
        
        speed_str = self.unit_converter.format_value('wind_speed', wind_speed, self.unit_system)
        
        # Add direction if available
        if wind_direction is not None:
            compass = self._degrees_to_compass(wind_direction)
            wind_info = f"{speed_str} from {compass}"
        else:
            wind_info = speed_str
        
        # Add gusts if available and significant
        if wind_gust is not None and wind_gust > wind_speed:
            gust_str = self.unit_converter.format_value('wind_gust', wind_gust, self.unit_system)
            wind_info += f", gusts {gust_str}"
        
        return wind_info

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
        return self.styles.WEATHER_ICONS.get(icon_code, '')

    def get_display_data(self) -> WeatherDisplayData:
        """Return all formatted data as a type-safe dataclass.
        
        Provides a complete interface for accessing all formatted display data.
        Useful for future features like theme system processing, data export,
        and API endpoints.
        
        Returns:
            WeatherDisplayData: Type-safe container with all display information
        """
        enhanced_displays = EnhancedDisplays(
            enhanced_temperature=self.metrics.get('enhanced_temperature', '--'),
            temp_range=self.metrics.get('temp_range', '--'),
            enhanced_conditions=self.metrics.get('enhanced_conditions', '--'),
            enhanced_wind=self.metrics.get('enhanced_wind', '--')
        )

        # Determine data quality and transformation status
        data_quality = "unknown"
        transformation_status = "success"
        
        if self.utils.is_fallback(self.raw_data):
            data_quality = "simulated"
        elif self.raw_data:
            data_quality = "live"
        
        # Check for conversion warnings
        if '_conversion_warnings' in self.raw_data:
            transformation_status = "partial"
        
        return WeatherDisplayData(
            city_name=self.city_name,
            date_str=self.date_str,
            status=self.status,
            individual_metrics=self.metrics,
            enhanced_displays=enhanced_displays.__dict__, # Convert to dict for backward compatibility
            raw_data_available=bool(self.raw_data),
            has_conversion_warnings='_conversion_warnings' in self.raw_data,
            unit_system=self.unit_system,
            # LIGHT METADATA FIELDS:
            timestamp=self.datetime.now(),
            transformation_status=transformation_status,
            data_quality=data_quality
        )

    def get_metric_value(self, metric_key: str) -> MetricValue:
        """Get a specific formatted metric value with type safety.
        
        Args:
            metric_key: Key of the metric to retrieve (e.g., 'temperature', 'humidity')
            
        Returns:
            MetricValue: Type-safe container with metric value and availability status
        """
        value = self.metrics.get(metric_key, "--")

        # Determine data quality
        data_quality = "unknown"
        if self.utils.is_fallback(self.raw_data):
            data_quality = "simulated"
        elif self.raw_data:
            data_quality = "live"

        return MetricValue(
            value=value,
            is_available=value != "--",
            metric_key=metric_key,
            unit_system=self.unit_system,
            # LIGHT METADATA FIELDS:
            timestamp=self.datetime.now(),
            data_quality=data_quality
        )
    
    # BACKWARD COMPATIBILITY METHODS:
    def get_metric_value_str(self, metric_key: str) -> str:
        """Get a specific formatted metric value as a string (backward compatibility).
        
        Args:
            metric_key: Key of the metric to retrieve
            
        Returns:
            str: Formatted metric value with units, or '--' if not available
        """
        return self.metrics.get(metric_key, "--")

    def get_enhanced_display(self, display_type: str) -> str:
        """Get a specific enhanced display value (backward compatibility).
        
        Args:
            display_type: Type of enhanced display ('enhanced_temperature', 'temp_range', etc.)
            
        Returns:
            str: Enhanced display value, or '--' if not available
        """
        return self.metrics.get(display_type, "--")