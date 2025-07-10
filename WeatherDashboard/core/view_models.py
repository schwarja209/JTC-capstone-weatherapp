"""
View models for preparing display-ready data from raw weather data.
"""

from typing import Dict, Any, Union
from WeatherDashboard import config
from WeatherDashboard.utils.utils import is_fallback, format_fallback_status
from WeatherDashboard.utils.unit_converter import UnitConverter


class WeatherViewModel:
    '''Prepares sanitized, display-ready data from raw weather data.
    
    This class encapsulates all display formatting logic, making it easy to:
    - Test formatting logic in isolation
    - Move to a separate views module later
    - Extend with additional display features
    '''

    def __init__(self, city: str, data: Dict[str, Any], unit_system: str) -> None:
        self.city_name: str = city
        self.unit_system: str = unit_system
        self.raw_data: Dict[str, Any] = data
        
        # Process all display data on initialization
        self.date_str: str = self._format_date()
        self.status: str = self._format_status()
        self.metrics: Dict[str, str] = self._format_metrics()

    def _format_date(self) -> str:
        '''Formats the date for display.'''
        if 'date' in self.raw_data and self.raw_data['date']:
            return self.raw_data['date'].strftime("%Y-%m-%d")
        return "--"

    def _format_status(self) -> str:
        '''Formats the status text including fallback and warning info.'''
        status = f" {format_fallback_status(is_fallback(self.raw_data), 'display')}"
        
        # Check for conversion warnings
        if '_conversion_warnings' in self.raw_data:
            status += f" (Warning: {self.raw_data['_conversion_warnings']})"
        
        return status

    def _format_metrics(self) -> Dict[str, str]:
        '''Formats all weather metrics for display.'''
        metrics = {}
        for key in config.KEY_TO_DISPLAY:
            raw_value = self.raw_data.get(key, "--")
            display_val = UnitConverter.format_value(key, raw_value, self.unit_system)
            metrics[key] = display_val
        return metrics

    def get_display_data(self) -> Dict[str, Union[str, Dict[str, str]]]:
        '''Returns all formatted data as a dictionary.
        
        This method makes it easy to pass data around without exposing
        internal ViewModel structure.
        '''
        return {
            'city_name': self.city_name,
            'date_str': self.date_str,
            'status': self.status,
            'metrics': self.metrics
        }

    def has_warnings(self) -> bool:
        '''Returns True if there are any warnings to display.'''
        return '_conversion_warnings' in self.raw_data

    def get_metric_value(self, metric_key: str) -> str:
        '''Gets a specific formatted metric value.'''
        return self.metrics.get(metric_key, "--")