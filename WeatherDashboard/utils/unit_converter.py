'''
Utility package for shared helper functions and reusable modules.
This module provides a UnitConverter class for converting between different weather units
and formatting values for display in the Weather Dashboard application.
It includes methods for temperature, pressure, and wind speed conversions,
as well as unit label retrieval and value formatting based on the selected unit system.
'''

from WeatherDashboard import config

class UnitConverter:
    '''Utility class for converting between explicit weather units using config-driven mappings.'''

    @staticmethod
    def _get_unit_symbols(metric):
        '''Gets the metric and imperial unit symbols from config for a given metric.'''
        try:
            units = config.UNITS["metric_units"][metric]
            return units["metric"], units["imperial"]
        except KeyError:
            from WeatherDashboard.services.api_exceptions import WeatherDashboardError
            raise WeatherDashboardError(f"Unit configuration not found for metric: {metric}")

    @staticmethod
    def convert_temperature(value, from_unit, to_unit):
        '''Converts temperature between Celsius and Fahrenheit using config units.'''
        metric_unit, imperial_unit = UnitConverter._get_unit_symbols("temperature")
        
        if from_unit == to_unit:
            return value
        if from_unit == imperial_unit and to_unit == metric_unit:  # F to C
            return (value - 32) * 5 / 9
        if from_unit == metric_unit and to_unit == imperial_unit:  # C to F
            return (value * 9 / 5) + 32
        raise ValueError(f"Unsupported temperature conversion: {from_unit} to {to_unit}")

    @staticmethod
    def convert_pressure(value, from_unit, to_unit):
        '''Converts pressure between hPa and inHg using config units.'''
        metric_unit, imperial_unit = UnitConverter._get_unit_symbols("pressure")
        
        if from_unit == to_unit:
            return value
        if from_unit == metric_unit and to_unit == imperial_unit:  # hPa to inHg
            return value * 0.02953
        if from_unit == imperial_unit and to_unit == metric_unit:  # inHg to hPa
            return value / 0.02953
        raise ValueError(f"Unsupported pressure conversion: {from_unit} to {to_unit}")

    @staticmethod
    def convert_wind_speed(value, from_unit, to_unit):
        '''Converts wind speed between m/s and mph using config units.'''
        metric_unit, imperial_unit = UnitConverter._get_unit_symbols("wind_speed")
        
        if from_unit == to_unit:
            return value
        if from_unit == metric_unit and to_unit == imperial_unit:  # m/s to mph
            return value * 2.23694
        if from_unit == imperial_unit and to_unit == metric_unit:  # mph to m/s
            return value / 2.23694
        raise ValueError(f"Unsupported wind speed conversion: {from_unit} to {to_unit}")
    
    @staticmethod
    def get_unit_label(metric, unit_system):
        '''Returns the unit label for a given metric based on the unit system (imperial or metric).'''
        try:
            return config.UNITS["metric_units"][metric][unit_system]
        except KeyError:
            # Import logger only when needed to avoid circular imports
            from WeatherDashboard.utils.logger import Logger
            Logger.warn(f"Unit label not found for metric '{metric}' in system '{unit_system}'")
            return ""

    @staticmethod
    def format_value(metric, val, unit_system):
        '''Formats the metric value for display based on the unit system and metric type.'''
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