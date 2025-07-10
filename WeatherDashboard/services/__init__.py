"""
Service layer for the Weather Dashboard application.
Contains business logic for weather data fetching, parsing, and validation.
"""

__all__ = [
    "weather_service",
    "api_exceptions", 
    "fallback_generator",
    "error_handler"
]