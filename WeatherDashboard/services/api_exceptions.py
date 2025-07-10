"""
Custom exceptions for Weather Dashboard API operations.
"""

class WeatherDashboardError(Exception):
    """Base exception for Weather Dashboard application."""
    pass

class WeatherAPIError(WeatherDashboardError):
    """Base exception for weather API related errors."""
    pass

class CityNotFoundError(WeatherAPIError):
    """Raised when a city is not found in the weather API."""
    pass

class ValidationError(WeatherDashboardError):
    """Raised when input validation fails."""
    pass

class RateLimitError(WeatherAPIError):
    """Raised when API rate limit is exceeded."""
    pass

class NetworkError(WeatherAPIError):
    """Raised when network/connection issues occur."""
    pass