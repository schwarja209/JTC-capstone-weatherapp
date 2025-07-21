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

from WeatherDashboard import config


class UnitConverter:
    """Utility class for converting between explicit weather units using config-driven mappings.
        
        Provides static methods for converting temperature, pressure, wind speed, and
        other weather metrics between different unit systems. Uses configuration-driven
        unit mappings for flexibility and includes formatting utilities for display.
        """
    # Class variable for cache
    _unit_cache = {}

    # Conversion factors and functions - centralized configuration
    CONVERSION_CONFIG = {
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

    @staticmethod
    def _generic_convert(value: float, from_unit: str, to_unit: str, 
                        conversion_type: str) -> float:
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
        conversions = UnitConverter.CONVERSION_CONFIG.get(conversion_type)
        if not conversions:
            raise ValueError(config.ERROR_MESSAGES['conversion'].format(
                field=conversion_type, from_unit=from_unit, to_unit=to_unit,
                reason="conversion type not supported"))
        
        # Get unit symbols for this metric type
        metric_unit, imperial_unit = UnitConverter._get_unit_symbols(conversion_type)
        
        # Determine conversion direction and apply
        if from_unit == metric_unit and to_unit == imperial_unit:
            return conversions['metric_to_imperial'](value)
        elif from_unit == imperial_unit and to_unit == metric_unit:
            return conversions['imperial_to_metric'](value)
        else:
            raise ValueError(config.ERROR_MESSAGES['conversion'].format(
                field=conversion_type, from_unit=from_unit, to_unit=to_unit,
                reason="unsupported conversion"))
    
    @staticmethod
    def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
        """Convert temperature using generic converter."""
        return UnitConverter._generic_convert(value, from_unit, to_unit, 'temperature')
    
    @staticmethod
    def convert_pressure(value: float, from_unit: str, to_unit: str) -> float:
        """Convert pressure using generic converter.""" 
        return UnitConverter._generic_convert(value, from_unit, to_unit, 'pressure')
    
    @staticmethod
    def convert_wind_speed(value: float, from_unit: str, to_unit: str) -> float:
        """Convert wind speed using generic converter."""
        return UnitConverter._generic_convert(value, from_unit, to_unit, 'wind_speed')
    
    @staticmethod
    def convert_visibility(value: float, from_unit: str, to_unit: str) -> float:
        """Convert visibility using generic converter."""
        return UnitConverter._generic_convert(value, from_unit, to_unit, 'visibility')
    
    @staticmethod
    def convert_precipitation(value: float, from_unit: str, to_unit: str) -> float:
        """Convert precipitation using generic converter."""
        return UnitConverter._generic_convert(value, from_unit, to_unit, 'rain') # uses rain as a stand in for any precipitation, since same units
    
    # Temperature-like conversions reuse temperature logic
    @staticmethod
    def convert_heat_index(value: float, from_unit: str, to_unit: str) -> float:
        return UnitConverter.convert_temperature(value, from_unit, to_unit)
    
    @staticmethod
    def convert_wind_chill(value: float, from_unit: str, to_unit: str) -> float:
        return UnitConverter.convert_temperature(value, from_unit, to_unit)
    
    @staticmethod
    def convert_dew_point(value: float, from_unit: str, to_unit: str) -> float:
        return UnitConverter.convert_temperature(value, from_unit, to_unit)

    @staticmethod
    def _get_unit_symbols(metric: str) -> Tuple[str, str]:
        """Get the metric and imperial unit symbols from config for a given metric.
        
        Results are cached for performance on repeated lookups.

        Args:
            metric: Metric name to look up unit symbols for
            
        Returns:
            Tuple[str, str]: Metric unit symbol, imperial unit symbol
            
        Raises:
            WeatherDashboardError: If unit configuration not found for metric
        """
        if metric not in UnitConverter._unit_cache:
            try:
                units = config.UNITS["metric_units"][metric]
                UnitConverter._unit_cache[metric] = (units["metric"], units["imperial"])
            except KeyError:
                # Import logger only when needed to avoid circular imports
                from WeatherDashboard.services.api_exceptions import WeatherDashboardError
                raise WeatherDashboardError(config.ERROR_MESSAGES['not_found'].format(resource="Unit configuration", name=metric))
        
        return UnitConverter._unit_cache[metric]

    @staticmethod
    def get_unit_label(metric: str, unit_system: str) -> str:
        """Return the unit label for a given metric based on the unit system."""
        # Use cache if available, otherwise populate it
        if metric not in UnitConverter._unit_cache:
            try:
                units = config.UNITS["metric_units"][metric]
                UnitConverter._unit_cache[metric] = (units["metric"], units["imperial"])
            except KeyError:
                # Import logger only when needed to avoid circular imports
                from WeatherDashboard.utils.logger import Logger
                Logger.warn(config.ERROR_MESSAGES['not_found'].format(resource="Unit label", name=f"metric '{metric}' in system '{unit_system}'"))
                return ""
        
        # Get from cache
        metric_unit, imperial_unit = UnitConverter._unit_cache[metric]
        return metric_unit if unit_system == "metric" else imperial_unit

    # Data-driven format_value - replaces 15+ elif statements
    FORMAT_CONFIG = {
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
    
    @staticmethod
    def format_value(metric: str, val: Any, unit_system: str) -> str:
        """Data-driven value formatting - replaces 15+ elif statements."""
        if val is None:
            return "--"
        
        # Get formatting configuration
        format_config = UnitConverter.FORMAT_CONFIG.get(metric)
        if not format_config:
            # Fallback for unknown metrics
            from WeatherDashboard.utils.logger import Logger
            Logger.warn(f"Unrecognized metric key: {metric}")
            unit = UnitConverter.get_unit_label(metric, unit_system)
            return f"{val} {unit}" if unit else str(val)
        
        # Format based on configuration
        precision = format_config['precision']
        include_unit = format_config['include_unit']
        
        if precision is None:
            # String metrics (conditions, weather_main, etc.)
            return str(val)
        
        # Numeric metrics
        if include_unit:
            unit = UnitConverter.get_unit_label(metric, unit_system)
            if precision == 0:
                return f"{val:.0f} {unit}"
            elif precision == 1:
                return f"{val:.1f} {unit}"
            elif precision == 2:
                return f"{val:.2f} {unit}"
            else:
                return f"{val:.{precision}f} {unit}"
        else:
            # Numeric without unit
            if precision == 0:
                return f"{val:.0f}"
            else:
                return f"{val:.{precision}f}"