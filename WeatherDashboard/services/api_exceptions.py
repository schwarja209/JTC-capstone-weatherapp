# In api_exceptions.py - Add missing error type definitions
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
            DataFetchError: Data retrieval failures
            TimeoutError: Operation timeout errors
            CancellationError: Operation cancellation errors
        ValidationError: Input validation failures
        UIError: User interface errors
            LoadingError: Async loading operation failures
            ChartRenderingError: Chart display errors
        LoggingError: Logging operation errors
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

class DataFetchError(WeatherAPIError):
    """Raised when weather data fetching fails.
    
    Indicates failures during data retrieval from weather APIs,
    including missing data, malformed responses, or service
    unavailability.
    """
    pass

class TimeoutError(WeatherAPIError):
    """Raised when operations exceed their time limits.
    
    Indicates that an operation (API call, data processing,
    etc.) has exceeded its configured timeout period.
    """
    pass

class CancellationError(WeatherAPIError):
    """Raised when operations are cancelled by user or system.
    
    Indicates that an operation was cancelled before completion,
    typically due to user action or system requirements.
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

class ChartRenderingError(UIError):
    """Raised when chart rendering operations fail.
    
    Indicates failures during chart data processing, visualization
    generation, or chart display operations.
    """
    pass

# System and Utility Errors
class LoggingError(WeatherDashboardError):
    """Raised when logging operations fail.
    
    Indicates failures during log writing, log configuration,
    or log management operations.
    """
    pass

# Theme System Errors (foundation for dual-theme)
class ThemeError(WeatherDashboardError):
    """Base exception for theme system errors.
    
    Foundation exception class for theme management, UI appearance
    control, and visual styling system errors.
    """
    pass