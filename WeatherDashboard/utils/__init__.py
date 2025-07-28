"""
Utility modules for the Weather Dashboard application.

This package contains general-purpose utility functions and classes
for data validation, unit conversion, logging, rate limiting, and
common operations used throughout the Weather Dashboard.

Modules:
    logger: Centralized logging system with multiple output formats
    rate_limiter: API request rate limiting and throttling
    unit_converter: Weather unit conversion and formatting utilities
    derived_metrics: Calculations for derived metrics
    utils: General utility functions for validation and formatting
    api_utils: API data parsing utilities
    color_utils: Color utility functions for weather dashboard styling
    state_utils: Widget visibility utility functions
    validation_utils: Centralized validation utilities
    widget_utils: Centralized widget positioning and creation utilities
    preferences_utils: User Preferences Manager
"""

__all__ = [
    "logger",
    "rate_limiter",
    "unit_converter",
    "derived_metrics",
    "utils",
    "api_utils",
    "color_utils",
    "state_utils",
    "validation_utils",
    "widget_utils",
    "preferences_utils"
]