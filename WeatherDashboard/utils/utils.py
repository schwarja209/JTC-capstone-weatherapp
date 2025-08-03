"""
Single function utilities for the Weather Dashboard application.

This module provides general utility functions for formatting, string manipulation,
and common operations used throughout the Weather Dashboard.
Includes functions for city name processing and status formatting.

Functions:
    is_fallback: Check if weather data is from fallback source
    format_fallback_status: Format status messages for fallback data
    city_key: Generate consistent city keys for data storage
"""

from typing import Dict, Any

from WeatherDashboard import config

from .validation_utils import ValidationUtils


class Utils:
    def __init__(self) -> None:
        # Direct imports for stable utilities
        self.config = config
        self.validation_utils = ValidationUtils()

    def is_fallback(self, data: Dict[str, Any]) -> bool:
        """Check if the data was generated as a fallback."""
        return data.get('source') == 'simulated'

    def format_fallback_status(self, fallback_used: bool, format_type: str = "display") -> str:
        """Return fallback status text based on boolean and format type.
        
        Args:
            fallback_used: Whether fallback data was used
            format_type: "display" for UI display, "log" for logging
            
        Returns:
            str: Formatted status text
            
        Raises:
            ValueError: If format_type is not 'display' or 'log'
        """
        if not fallback_used:
            return "Live" if format_type == "log" else ""
        
        if format_type == "log":
            return "Simulated"
        elif format_type == "display":
            return "(Simulated)"
        else:
            raise ValueError(self.config.ERROR_MESSAGES['validation'].format(field="Format type", reason=f"'{format_type}' is invalid. Must be 'display' or 'log'"))

    def city_key(self, name: str) -> str:
        """Generate a normalized key for city name for consistent storage/lookup.
        
        Args:
            name: City name
            
        Returns:
            str: Lowercase key with underscores (e.g., "New York" -> "new_york")
            
        Raises:
            ValueError: If name is invalid (propagated from normalize_city_name)
        """
        self.validation_utils.validate_city_name(name)
        
        normalized = name.strip().title()
        return normalized.lower().replace(" ", "_")
