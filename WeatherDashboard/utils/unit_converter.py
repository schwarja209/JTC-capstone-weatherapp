"""
Unit conversion utilities for weather data.

This module provides comprehensive unit conversion functions for weather
metrics including temperature, pressure, wind speed, and formatting utilities.
Supports conversion between metric and imperial units with proper error handling
and config-driven unit mappings.

Classes:
    UnitConverter: Static utility class for weather unit conversions and formatting
"""

from typing import Tuple, Any

from WeatherDashboard.utils.logger import Logger
from WeatherDashboard import config


class UnitConverter:
    """Utility class for converting between explicit weather units using config-driven mappings.
        
    Provides static methods for converting temperature, pressure, wind speed, and
    other weather metrics between different unit systems. Uses configuration-driven
    unit mappings for flexibility and includes formatting utilities for display.
    """

    def __init__(self):
        """Initialize unit converter with optional dependencies.
        
        Args:
            conversion_config: Conversion functions (defaults to built-in conversions)
            unit_cache: Cache for unit symbols (defaults to empty dict)
            config_provider: Function to get configuration (defaults to config module)
        """
        # Direct imports for stable utilities
        self.config = config
        self.logger = Logger()

        # Conversion factors and functions - centralized configuration
        self.conversion_config = {
            'temperature': {
                'metric_to_imperial': lambda x: (x * 9/5) + 32,
                'imperial_to_metric': lambda x: (x - 32) * 5/9,
            },
            'pressure': {
                'metric_to_imperial': lambda x: x * 0.02953,
                'imperial_to_metric': lambda x: x / 0.02953,
            },
            'wind_speed': {
                'metric_to_imperial': lambda x: x * 2.23694,
                'imperial_to_metric': lambda x: x / 2.23694,
            },
            'visibility': {
                'metric_to_imperial': lambda x: x * 0.621371,
                'imperial_to_metric': lambda x: x / 0.621371,
            },
            'rain': { # uses rain as a stand in for any precipitation, since same units
                'metric_to_imperial': lambda x: x * 0.0393701,
                'imperial_to_metric': lambda x: x / 0.0393701,
            }
        }

        # Instance class variable for cache
        self._unit_cache = {}

        # Data-driven format_value - replaces 15+ elif statements
        self.format_config = {
            'temperature': {'precision': 1, 'include_unit': True},
            'humidity': {'precision': 0, 'include_unit': True},
            'pressure': {'precision': 2, 'include_unit': True},
            'wind_speed': {'precision': 2, 'include_unit': True},
            'conditions': {'precision': None, 'include_unit': False},
            'feels_like': {'precision': 1, 'include_unit': True},
            'temp_min': {'precision': 1, 'include_unit': True},
            'temp_max': {'precision': 1, 'include_unit': True},
            'wind_gust': {'precision': 2, 'include_unit': True},
            'wind_direction': {'precision': 0, 'include_unit': True},
            'visibility': {'precision': 1, 'include_unit': True},
            'cloud_cover': {'precision': 0, 'include_unit': True},
            'rain': {'precision': 1, 'include_unit': True},
            'snow': {'precision': 1, 'include_unit': True},
            'rain_1h': {'precision': 1, 'include_unit': True},
            'rain_3h': {'precision': 1, 'include_unit': True},
            'snow_1h': {'precision': 1, 'include_unit': True},
            'snow_3h': {'precision': 1, 'include_unit': True},
            'heat_index': {'precision': 1, 'include_unit': True},
            'wind_chill': {'precision': 1, 'include_unit': True},
            'dew_point': {'precision': 1, 'include_unit': True},
            'precipitation_probability': {'precision': 0, 'include_unit': True},
            'weather_comfort_score': {'precision': 0, 'include_unit': True},
            'uv_index': {'precision': 0, 'include_unit': True},
            'air_quality_index': {'precision': 0, 'include_unit': True},
            'air_quality_description': {'precision': None, 'include_unit': False},
            'weather_main': {'precision': None, 'include_unit': False},
            'weather_id': {'precision': None, 'include_unit': False},
            'weather_icon': {'precision': None, 'include_unit': False},
        }

    def _generic_convert(self, value: float, from_unit: str, to_unit: str, conversion_type: str) -> float:
        """Generic conversion function for all unit types.
        
        Args:
            value: Value to convert
            from_unit: Source unit
            to_unit: Target unit  
            conversion_type: Type of conversion (temperature, pressure, etc.)
            
        Returns:
            float: Converted value
            
        Raises:
            ValueError: If conversion is not supported
        """
        if from_unit == to_unit:
            return value
            
        # Get conversion functions for this type
        conversions = self.conversion_config.get(conversion_type)
        if not conversions:
            raise ValueError(self.config.ERROR_MESSAGES['conversion'].format(
                field=conversion_type, from_unit=from_unit, to_unit=to_unit,
                reason="conversion type not supported"))
        
        # Get unit symbols for this metric type
        metric_unit, imperial_unit = self._get_unit_symbols(conversion_type)
        
        # Determine conversion direction and apply
        if from_unit == metric_unit and to_unit == imperial_unit:
            return conversions['metric_to_imperial'](value)
        elif from_unit == imperial_unit and to_unit == metric_unit:
            return conversions['imperial_to_metric'](value)
        else:
            raise ValueError(self.config_provider.ERROR_MESSAGES['conversion'].format(
                field=conversion_type, from_unit=from_unit, to_unit=to_unit,
                reason="unsupported conversion"))
    
    def convert_temperature(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert temperature using generic converter."""
        return self._generic_convert(value, from_unit, to_unit, 'temperature')
    
    def convert_pressure(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert pressure using generic converter.""" 
        return self._generic_convert(value, from_unit, to_unit, 'pressure')
    
    def convert_wind_speed(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert wind speed using generic converter."""
        return self._generic_convert(value, from_unit, to_unit, 'wind_speed')
    
    def convert_visibility(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert visibility using generic converter."""
        return self._generic_convert(value, from_unit, to_unit, 'visibility')
    
    def convert_precipitation(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert precipitation using generic converter."""
        return self._generic_convert(value, from_unit, to_unit, 'rain') # uses rain as a stand in for any precipitation, since same units
    
    # Temperature-like conversions reuse temperature logic
    def convert_heat_index(self, value: float, from_unit: str, to_unit: str) -> float:
        return self.convert_temperature(value, from_unit, to_unit)
    
    def convert_wind_chill(self, value: float, from_unit: str, to_unit: str) -> float:
        return self.convert_temperature(value, from_unit, to_unit)
    
    def convert_dew_point(self, value: float, from_unit: str, to_unit: str) -> float:
        return self.convert_temperature(value, from_unit, to_unit)

    def _get_unit_symbols(self, metric: str) -> Tuple[str, str]:
        """Get the metric and imperial unit symbols from config for a given metric.
        
        Results are cached for performance on repeated lookups.

        Args:
            metric: Metric name to look up unit symbols for
            
        Returns:
            Tuple[str, str]: Metric unit symbol, imperial unit symbol
            
        Raises:
            WeatherDashboardError: If unit configuration not found for metric
        """
        if metric not in self._unit_cache:
            try:
                units = self.config.UNITS["metric_units"][metric]
                self._unit_cache[metric] = (units["metric"], units["imperial"])
            except KeyError:
                # Import logger only when needed to avoid circular imports
                from WeatherDashboard.services.api_exceptions import WeatherDashboardError
                raise WeatherDashboardError(self.config.ERROR_MESSAGES['not_found'].format(resource="Unit configuration", name=metric))
        
        return self._unit_cache[metric]

    def get_unit_label(self, metric: str, unit_system: str) -> str:
        """Return the unit label for a given metric based on the unit system."""
        # Use cache if available, otherwise populate it
        if metric not in self._unit_cache:
            try:
                units = self.config.UNITS["metric_units"][metric]
                self._unit_cache[metric] = (units["metric"], units["imperial"])
            except KeyError:
                self.logger.warn(self.config.ERROR_MESSAGES['not_found'].format(resource="Unit label", name=f"metric '{metric}' in system '{unit_system}'"))
                return ""
        
        # Get from cache
        metric_unit, imperial_unit = self._unit_cache[metric]
        return metric_unit if unit_system == "metric" else imperial_unit
    
    def format_value(self, metric: str, val: Any, unit_system: str) -> str:
        """Format a value with appropriate units and precision based on metric type and unit system.
    
        Performs comprehensive value formatting using centralized configuration to determine
        appropriate units, precision, and display format for weather metrics. Handles None
        values, applies unit system-specific formatting, and provides consistent fallback
        behavior for unknown metric types.
        
        Args:
            metric_type (str): Type of metric to format (temperature, humidity, pressure, etc.)
            value: Numeric value to format, or None for missing data
            unit_system (str): Target unit system ('metric' or 'imperial')
        
        Returns:
            str: Formatted value with appropriate units (e.g., "25.0 °C", "77.0 °F", "60 %")
                or "--" for missing data
        """    
        if val is None:
            return "--"
        
        # Get format configuration for this metric
        format_spec = self.format_config.get(metric, {'precision': 1, 'include_unit': '{:.1f}'})
        
        try:
            # Format the value
            precision = format_spec.get('precision', 1)
            if precision is None:
                formatted_val = str(val)
            else:
                format_string = f"{{:.{precision}f}}"
                formatted_val = format_string.format(float(val))
            
            # Get unit label
            unit_label = self.get_unit_label(metric, unit_system)
            
            return f"{formatted_val} {unit_label}" if unit_label else formatted_val
            
        except (ValueError, TypeError):
            return str(val)