"""
View models for preparing display-ready data from raw weather data.

This module provides view model classes that transform raw weather data
into formatted, display-ready information. Handles data sanitization,
formatting, status determination, and user-friendly presentation.

Classes:
    WeatherViewModel: Transforms raw weather data into display-ready format
"""

from typing import Dict, Any, Union
from WeatherDashboard import config
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
        """Format all weather metrics for display.
        
        Converts all weather metric values to properly formatted strings
        with appropriate units and precision for UI display.
        
        Returns:
            Dict[str, str]: Dictionary mapping metric keys to formatted display values
        """
        metrics = {}
        for key in config.KEY_TO_DISPLAY:
            raw_value = self.raw_data.get(key, "--")
            display_val = UnitConverter.format_value(key, raw_value, self.unit_system)
            metrics[key] = display_val
        return metrics

    def get_display_data(self) -> Dict[str, Union[str, Dict[str, str]]]:
        """Return all formatted data as a dictionary.
        
        Provides a convenient interface for accessing all formatted display
        data without exposing internal ViewModel structure.
        
        Returns:
            Dict containing all formatted display data including city, date, status, and metrics
        """
        return {
            'city_name': self.city_name,
            'date_str': self.date_str,
            'status': self.status,
            'metrics': self.metrics
        }

    def has_warnings(self) -> bool:
        """Check if there are any warnings to display."""
        return '_conversion_warnings' in self.raw_data

    def get_metric_value(self, metric_key: str) -> str:
        """Get a specific formatted metric value.
        
        Args:
            metric_key: Key of the metric to retrieve (e.g., 'temperature', 'humidity')
            
        Returns:
            str: Formatted metric value with units, or '--' if not available
        """
        return self.metrics.get(metric_key, "--")