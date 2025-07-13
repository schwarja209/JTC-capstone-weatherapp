"""
Utility modules for the Weather Dashboard application.

This package contains general-purpose utility functions and classes
for data validation, unit conversion, logging, rate limiting, and
common operations used throughout the Weather Dashboard.

Modules:
    utils: General utility functions for validation and formatting
    unit_converter: Weather unit conversion and formatting utilities
    logger: Centralized logging system with multiple output formats
    rate_limiter: API request rate limiting and throttling
"""

__all__ = [
    "utils",
    "unit_converter", 
    "logger",
    "rate_limiter",
    "derived_metrics"
]