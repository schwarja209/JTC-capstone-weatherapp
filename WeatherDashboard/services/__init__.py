"""
Service layer for the Weather Dashboard application.

This package contains all service-layer components for external API
communication, data processing, error handling, and fallback data
generation with comprehensive validation and exception management.

Modules:
    weather_service: Weather API integration and data retrieval
    api_exceptions: Custom exception classes for API error handling
    fallback_generator: Simulated weather data generation
    error_handler: Centralized error processing and user messaging
"""

__all__ = [
    "weather_service",
    "api_exceptions",
    "fallback_generator", 
    "error_handler"
]