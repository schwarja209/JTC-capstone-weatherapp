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
    @staticmethod
    def _get_unit_symbols(metric: str) -> Tuple[str, str]:
        """Get the metric and imperial unit symbols from config for a given metric.
        
        Args:
            metric: Metric name to look up unit symbols for
            
        Returns:
            Tuple[str, str]: Metric unit symbol, imperial unit symbol
            
        Raises:
            WeatherDashboardError: If unit configuration not found for metric
        """
        try:
            units = config.UNITS["metric_units"][metric]
            return units["metric"], units["imperial"]
        except KeyError:
            from WeatherDashboard.services.api_exceptions import WeatherDashboardError
            raise WeatherDashboardError(f"Unit configuration not found for metric: {metric}")

    @staticmethod
    def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
        """Convert temperature between Celsius and Fahrenheit using config units.
        
        Args:
            value: Temperature value to convert
            from_unit: Source unit (°C or °F)
            to_unit: Target unit (°C or °F)
            
        Returns:
            float: Converted temperature value
            
        Raises:
            ValueError: If conversion between specified units is not supported
        """
        metric_unit, imperial_unit = UnitConverter._get_unit_symbols("temperature")
        
        if from_unit == to_unit:
            return value
        if from_unit == imperial_unit and to_unit == metric_unit:  # F to C
            return (value - 32) * 5 / 9
        if from_unit == metric_unit and to_unit == imperial_unit:  # C to F
            return (value * 9 / 5) + 32
        raise ValueError(f"Unsupported temperature conversion: {from_unit} to {to_unit}")

    @staticmethod
    def convert_pressure(value: float, from_unit: str, to_unit: str) -> float:
        """Convert pressure between hPa and inHg using config units.
        
        Args:
            value: Pressure value to convert
            from_unit: Source unit (hPa or inHg)
            to_unit: Target unit (hPa or inHg)
            
        Returns:
            float: Converted pressure value
            
        Raises:
            ValueError: If conversion between specified units is not supported
        """
        metric_unit, imperial_unit = UnitConverter._get_unit_symbols("pressure")
        
        if from_unit == to_unit:
            return value
        if from_unit == metric_unit and to_unit == imperial_unit:  # hPa to inHg
            return value * 0.02953
        if from_unit == imperial_unit and to_unit == metric_unit:  # inHg to hPa
            return value / 0.02953
        raise ValueError(f"Unsupported pressure conversion: {from_unit} to {to_unit}")

    @staticmethod
    def convert_wind_speed(value: float, from_unit: str, to_unit: str) -> float:
        """Convert wind speed between m/s and mph using config units.
        
        Args:
            value: Wind speed value to convert
            from_unit: Source unit (m/s or mph)
            to_unit: Target unit (m/s or mph)
            
        Returns:
            float: Converted wind speed value
            
        Raises:
            ValueError: If conversion between specified units is not supported
        """
        metric_unit, imperial_unit = UnitConverter._get_unit_symbols("wind_speed")
        
        if from_unit == to_unit:
            return value
        if from_unit == metric_unit and to_unit == imperial_unit:  # m/s to mph
            return value * 2.23694
        if from_unit == imperial_unit and to_unit == metric_unit:  # mph to m/s
            return value / 2.23694
        raise ValueError(f"Unsupported wind speed conversion: {from_unit} to {to_unit}")
    
    @staticmethod
    def get_unit_label(metric: str, unit_system: str) -> str:
        """Return the unit label for a given metric based on the unit system."""
        try:
            return config.UNITS["metric_units"][metric][unit_system]
        except KeyError:
            # Import logger only when needed to avoid circular imports
            from WeatherDashboard.utils.logger import Logger
            Logger.warn(f"Unit label not found for metric '{metric}' in system '{unit_system}'")
            return ""

    @staticmethod
    def format_value(metric: str, val: Any, unit_system: str) -> str:
        """Format the metric value for display based on the unit system and metric type.
        
        Formats weather values with appropriate precision and units for display.
        Handles None values gracefully and applies metric-specific formatting rules.
        
        Args:
            metric: Metric name for formatting rules
            val: Value to format (can be None)
            unit_system: Unit system for unit labels ('metric' or 'imperial')
            
        Returns:
            str: Formatted value string with units, or '--' if value is None
        """
        if val is None:
            return "--"
        
        unit = UnitConverter.get_unit_label(metric, unit_system)
            
        if metric == "temperature":
            return f"{val:.1f} {unit}"
        elif metric == "humidity":
            return f"{val} {unit}"
        elif metric in ["pressure", "wind_speed"]:
            return f"{val:.2f} {unit}"
        elif metric == "conditions":
            return str(val)  # No unit needed
        
        # Import logger only when needed to avoid circular imports
        from WeatherDashboard.utils.logger import Logger
        Logger.warn(f"Unrecognized metric key: {metric}")
        return f"{val} {unit}" if unit else str(val)