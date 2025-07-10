"""
WeatherDashboard Error Handler Module
Handles errors related to weather data operations, including API errors,
input validation, and unexpected exceptions.
Provides user-friendly messages and logging for different error types.
"""

from typing import Optional
import tkinter.messagebox as messagebox
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.services.api_exceptions import (
    ValidationError,
    CityNotFoundError,
    RateLimitError,
    NetworkError
)

class WeatherErrorHandler:
    '''Handles error presentation and user messaging for weather data operations.'''
    
    @staticmethod
    def handle_weather_error(error_exception: Optional[Exception], city_name: str) -> bool:
        '''Handles weather-related errors and shows appropriate user messages.
        
        Returns:
            bool: True if the error was handled and operation should continue,
                  False if the operation should be aborted.
        '''
        if not error_exception:
            return True
            
        if isinstance(error_exception, ValidationError):
            # Critical errors - don't show fallback data
            messagebox.showerror("Input Error", str(error_exception))
            return False
        elif isinstance(error_exception, CityNotFoundError):
            # City not found - show error but continue with fallback
            messagebox.showerror("City Not Found", str(error_exception))
            return True
        elif isinstance(error_exception, RateLimitError):
            # Rate limit - show specific message
            messagebox.showerror("Rate Limit", f"API rate limit exceeded. Using simulated data for '{city_name}'.")
            return True
        elif isinstance(error_exception, NetworkError):
            # Network issues - show network-specific message
            messagebox.showwarning("Network Issue", f"Network problem detected. Using simulated data for '{city_name}'.")
            return True
        else:
            # Other API errors - show general fallback notice
            Logger.warn(f"Using fallback for {city_name}: {error_exception}")
            messagebox.showinfo("Notice", f"No live data available for '{city_name}'. Simulated data is shown.")
            return True

    @staticmethod
    def handle_input_validation_error(error: Exception) -> None:
        '''Handles input validation errors.'''
        Logger.error(f"Input validation error: {error}")
        messagebox.showerror("Input Error", str(error))

    @staticmethod
    def handle_unexpected_error(error: Exception) -> None:
        '''Handles unexpected errors.'''
        Logger.error(f"Unexpected error: {error}")
        messagebox.showerror("Error", f"Unexpected error: {error}")
    
    @staticmethod
    def handle_rate_limit_error(wait_time: float) -> None:
        """Handles rate limit errors with appropriate user messaging."""
        messagebox.showinfo("Rate Limit", f"Please wait {wait_time:.0f} more seconds before making another request.")