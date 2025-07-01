'''
Utility package for shared helper functions and reusable modules.
This module provides a UnitConverter class for converting between different weather units
and formatting values for display in the Weather Dashboard application.
It includes methods for temperature, pressure, and wind speed conversions,
as well as unit label retrieval and value formatting based on the selected unit system.
'''

import config

class UnitConverter:
    '''Utility class for converting between explicit weather units.'''

    TEMP_UNITS = ("C", "F")
    PRESSURE_UNITS = ("hPa", "inHg")
    WIND_UNITS = ("m/s", "mph")

    @staticmethod
    def convert_temperature(value, from_unit, to_unit):
        '''Converts temperature between Celsius and Fahrenheit.'''
        C, F = UnitConverter.TEMP_UNITS
        if from_unit == to_unit:
            return value
        if from_unit == F and to_unit == C:
            return (value - 32) * 5 / 9
        if from_unit == C and to_unit == F:
            return (value * 9 / 5) + 32
        raise ValueError(f"Unsupported temperature conversion: {from_unit} to {to_unit}")

    @staticmethod
    def convert_pressure(value, from_unit, to_unit):
        '''Converts pressure between hPa and inHg.'''
        HPA, INHG = UnitConverter.PRESSURE_UNITS
        if from_unit == to_unit:
            return value
        if from_unit == HPA and to_unit == INHG:
            return value * 0.02953
        if from_unit == INHG and to_unit == HPA:
            return value / 0.02953
        raise ValueError(f"Unsupported pressure conversion: {from_unit} to {to_unit}")

    @staticmethod
    def convert_wind_speed(value, from_unit, to_unit):
        '''Converts wind speed between m/s and mph.'''
        if from_unit == to_unit:
            return value
        if from_unit == "m/s" and to_unit == "mph":
            return value * 2.23694
        if from_unit == "mph" and to_unit == "m/s":
            return value / 2.23694
        raise ValueError(f"Unsupported wind speed conversion: {from_unit} to {to_unit}")
    
    @staticmethod
    def get_unit_label(metric, unit_system):
        '''Returns the unit label for a given metric based on the unit system (imperial or metric).'''
        return config.UNITS["metric_units"].get(metric, {}).get(unit_system, "")

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
        return f"{val} {unit}" if unit else str(val)