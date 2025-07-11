"""
Custom exceptions for Weather Dashboard API operations.

This module defines all custom exception classes used throughout the
Weather Dashboard application for proper error handling, categorization,
and user messaging. Provides hierarchical exception structure for
different error types and contexts.

Exception Hierarchy:
    WeatherDashboardError: Base exception for all application errors
        WeatherAPIError: API-related errors
            CityNotFoundError: City lookup failures
            RateLimitError: API rate limit exceeded
            NetworkError: Network/connection issues
        ValidationError: Input validation failures
        UIError: User interface errors
            LoadingError: Async loading operation failures
        ThemeError: Theme system errors
"""

class WeatherDashboardError(Exception):
    """Base exception for Weather Dashboard application.
    
    Root exception class for all application-specific errors.
    Provides a common base for exception handling throughout
    the Weather Dashboard.
    """
    pass

class WeatherAPIError(WeatherDashboardError):
    """Base exception for weather API related errors.
    
    Parent class for all errors related to external weather API
    communication, data retrieval, and processing.
    """
    pass

class CityNotFoundError(WeatherAPIError):
    """Raised when a city is not found in the weather API.
    
    Indicates that the requested city name could not be located
    in the weather service's database or geocoding system.
    """
    pass

class ValidationError(WeatherDashboardError):
    """Raised when input validation fails.
    
    Indicates that user input or data does not meet required
    validation criteria before processing can continue.
    """
    pass

class RateLimitError(WeatherAPIError):
    """Raised when API rate limit is exceeded.
    
    Indicates that the application has made too many requests
    to the weather API within the allowed time period.
    """
    pass

class NetworkError(WeatherAPIError):
    """Raised when network/connection issues occur.
    
    Indicates problems with network connectivity, timeouts,
    or other communication failures with external services.
    """
    pass

# UI and State Related Errors
class UIError(WeatherDashboardError):
    """Base exception for UI-related errors.
    
    Parent class for errors related to user interface components,
    widget management, and GUI operations.
    """
    pass

class LoadingError(UIError):
    """Raised when async loading operations fail.
    
    Indicates failures during background loading operations,
    async data fetching, or UI state management.
    """
    pass

# Theme System Errors (foundation for dual-theme)
class ThemeError(WeatherDashboardError):
    """Base exception for theme system errors.
    
    Foundation exception class for theme management, UI appearance
    control, and visual styling system errors.
    """
    pass