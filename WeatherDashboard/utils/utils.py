"""
Single function utilities for the Weather Dashboard application.

This module provides general utility functions for data validation, formatting,
string manipulation, and common operations used throughout the Weather Dashboard.
Includes functions for city name processing, unit validation, and status formatting.

Functions:
    is_fallback: Check if weather data is from fallback source
    format_fallback_status: Format status messages for fallback data
    normalize_city_name: Standardize city name formatting
    city_key: Generate consistent city keys for data storage
    validate_unit_system: Validate unit system parameters
"""

from typing import Dict, Any

def is_fallback(data: Dict[str, Any]) -> bool:
    """Check if the data was generated as a fallback."""
    return data.get('source') == 'simulated'

def format_fallback_status(fallback_used: bool, format_type: str = "display") -> str:
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
        raise ValueError(f"Invalid format_type: {format_type}. Use 'display' or 'log'")

def normalize_city_name(name: str) -> str:
    """Normalize city name for display: strips whitespace and title-cases each word.
    
    Args:
        name: Raw city name input
        
    Returns:
        str: Normalized city name for display (e.g., "new york" -> "New York")
        
    Raises:
        ValueError: If name is not a string or is empty after stripping
    """
    if not isinstance(name, str):
        raise ValueError(f"City name must be a string, got {type(name).__name__}")
    
    normalized = name.strip().title()
    if not normalized:
        raise ValueError("City name cannot be empty")
    
    return normalized

def city_key(name: str) -> str:
    """Generate a normalized key for city name for consistent storage/lookup.
    
    Args:
        name: City name
        
    Returns:
        str: Lowercase key with underscores (e.g., "New York" -> "new_york")
        
    Raises:
        ValueError: If name is invalid (propagated from normalize_city_name)
    """
    normalized = normalize_city_name(name)  # This also validates the input
    return normalized.lower().replace(" ", "_")

def validate_unit_system(unit_system: str) -> str:
    """Validate that the unit system is either 'metric' or 'imperial'.
    
    Args:
        unit_system: Unit system to validate
        
    Returns:
        str: The validated unit system (same as input if valid)
        
    Raises:
        ValueError: If unit system is not valid
    """
    if not isinstance(unit_system, str):
        raise ValueError(f"Unit system must be a string, got {type(unit_system).__name__}")
    
    valid_units = {"metric", "imperial"}
    if unit_system not in valid_units:
        raise ValueError(f"Invalid unit system: '{unit_system}'. Must be one of: {', '.join(valid_units)}")
    
    return unit_system