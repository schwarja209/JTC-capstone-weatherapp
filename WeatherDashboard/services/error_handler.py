"""
WeatherDashboard Error Handler Module

Handles errors related to weather data operations, including API errors,
input validation, and unexpected exceptions. Provides user-friendly 
messages and logging for different error types.

Provides theme-aware error messaging foundation for optimistic, pessimistic,
and neutral user experience modes in the dual-theme system.

Classes:
    WeatherErrorHandler: Main error handling class with theme support
"""

from typing import Optional
import tkinter.messagebox as messagebox

from WeatherDashboard import styles
from WeatherDashboard.utils.logger import Logger

from WeatherDashboard.services.api_exceptions import (
    ValidationError,
    CityNotFoundError,
    RateLimitError,
    NetworkError
)

class WeatherErrorHandler:
    """Handles error presentation and user messaging for weather data operations.
    
    Provides theme-aware error messaging and user notification handling for
    weather-related operations. Supports optimistic, pessimistic, and neutral
    themes with appropriate message formatting and UI interaction patterns.
    
    Attributes:
        current_theme: Current theme mode for message formatting
        _message_templates: Dictionary of theme-specific message templates
    """

    def __init__(self, theme: str = 'neutral'):
        """Initialize the error handler with specified theme.
        
        Sets up theme-aware message templates for different error types
        and user experience modes.
        
        Args:
            theme: Initial theme mode ('neutral', 'optimistic', 'pessimistic')
        """
        # Direct imports for stable utilities
        self.styles = styles
        self.logger = Logger()

        # Instance data
        self.current_theme = theme
        self._message_templates = {
            'city_not_found': {
                'neutral': "City '{}' not found",
                'optimistic': "Let's try a different city! '{}' isn't available right now",
                'pessimistic': "'{}' does not exist in our records"
            },
            'rate_limit': {
                'neutral': "API rate limit exceeded. Using simulated data for '{}'",
                'optimistic': "Taking a quick break! Showing sample data for '{}' instead", 
                'pessimistic': "Request quota exhausted. Degraded service active for '{}'"
            },
            'network_error': {
                'neutral': "Network problem detected. Using simulated data for '{}'",
                'optimistic': "Connection hiccup! No worries, showing backup data for '{}'",
                'pessimistic': "Network failure. System compromised. Fallback data for '{}'"
            }
        }
    
    def set_theme(self, theme: str) -> None:
        """Set the current theme for message formatting."""
        if theme in ['neutral', 'optimistic', 'pessimistic']:
            self.current_theme = theme
        else:
            self.logger.warn(f"Unknown theme: {theme}, keeping current theme")
    
    def _format_message(self, template_key: str, *args) -> str:
        """Format error message based on current theme and template.
        
        Retrieves the appropriate message template for the current theme and
        formats it with provided arguments. Falls back to neutral theme if
        current theme template is not available.
        
        Args:
            template_key: Key identifying the message template to use
            *args: Arguments to format into the message template
            
        Returns:
            str: Formatted message appropriate for current theme
        """
        template = self._message_templates.get(template_key, {})
        message_template = template.get(self.current_theme, template.get('neutral', '{}'))
        return message_template.format(*args)

    def handle_weather_error(self, error_exception: Optional[Exception], city_name: str) -> bool:
        """Handles weather-related errors and shows appropriate user messages.
        
        Args:
            error_exception: The exception that occurred, or None if no error
            city_name: Name of the city being processed
            
        Returns:
            bool: True if the error was handled and operation should continue,
                  False if the operation should be aborted.
        """
        if not error_exception:
            return True
            
        if isinstance(error_exception, ValidationError):
            # Critical errors - don't show fallback data
            messagebox.showerror("Input Error", str(error_exception))
            return False
        elif isinstance(error_exception, CityNotFoundError):
            # City not found - show error but continue with fallback
            message = self._format_message('city_not_found', city_name)
            getattr(messagebox, self.styles.DIALOG_CONFIG['dialog_types']['error'])(self.styles.DIALOG_CONFIG['error_titles']['city_not_found'], message)
            return True
        elif isinstance(error_exception, RateLimitError):
            # Rate limit - show specific message
            message = self._format_message('rate_limit', city_name)
            getattr(messagebox, self.styles.DIALOG_CONFIG['dialog_types']['error'])(self.styles.DIALOG_CONFIG['error_titles']['rate_limit'], message)
            return True
        elif isinstance(error_exception, NetworkError):
            # Network issues - show network-specific message
            message = self._format_message('network_error', city_name)
            getattr(messagebox, self.styles.DIALOG_CONFIG['dialog_types']['warning'])(self.styles.DIALOG_CONFIG['error_titles']['network_issue'], message)
            return True
        else:
            # Other API errors - show general fallback notice
            self.logger.warn(f"Using fallback for {city_name}: {error_exception}")
            getattr(messagebox, self.styles.DIALOG_CONFIG['dialog_types']['info'])(self.styles.DIALOG_CONFIG['error_titles']['notice'], f"No live data available for '{city_name}'. Simulated data is shown.")
            return True

    def handle_input_validation_error(self, error: Exception) -> None:
        """Handles input validation errors."""
        self.logger.error(f"Input validation error: {error}")
        getattr(messagebox, self.styles.DIALOG_CONFIG['dialog_types']['error'])(self.styles.DIALOG_CONFIG['error_titles']['input_error'], str(error))

    def handle_unexpected_error(self, error: Exception) -> None:
        """Handles unexpected errors."""
        self.logger.error(f"Unexpected error: {error}")
        getattr(messagebox, self.styles.DIALOG_CONFIG['dialog_types']['error'])(self.styles.DIALOG_CONFIG['error_titles']['general_error'], f"Unexpected error: {error}")
    
    def handle_rate_limit_error(self, wait_time: float) -> None:
        """Handle rate limit errors with appropriate user messaging."""
        getattr(messagebox, self.styles.DIALOG_CONFIG['dialog_types']['info'])(self.styles.DIALOG_CONFIG['error_titles']['rate_limit'], f"Please wait {wait_time:.0f} more seconds before making another request.")