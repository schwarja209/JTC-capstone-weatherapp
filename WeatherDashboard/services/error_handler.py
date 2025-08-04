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

import tkinter.messagebox as messagebox
from typing import Optional

from WeatherDashboard import styles, dialog
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.services.api_exceptions import (
    ValidationError, WeatherDashboardError, RateLimitError, 
    DataFetchError, TimeoutError, CancellationError, 
    LoggingError, ChartRenderingError, CityNotFoundError, NetworkError
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
        """Initialize the error handler with specified theme."""
        # Direct imports for stable utilities
        self.styles = styles
        self.dialog = dialog
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
            },
            'data_fetch_error': {
                'neutral': "Failed to fetch weather data: {}",
                'optimistic': "Data retrieval hiccup! {}",
                'pessimistic': "Data acquisition failure: {}"
            },
            'cancellation': {
                'neutral': "Operation cancelled: {}",
                'optimistic': "No problem! Operation cancelled: {}",
                'pessimistic': "Operation terminated: {}"
            },
            'logging_error': {
                'neutral': "Logging issue detected: {}",
                'optimistic': "Minor logging hiccup: {}",
                'pessimistic': "Logging system failure: {}"
            },
            'chart_error': {
                'neutral': "Chart rendering failed: {}",
                'optimistic': "Chart display issue: {}",
                'pessimistic': "Chart system failure: {}"
            },
            'timeout_error': {
                'neutral': "Operation timed out: {}",
                'optimistic': "Taking too long! {}",
                'pessimistic': "System timeout: {}"
            }
        }
    
    def set_theme(self, theme: str) -> None:
        """Set the current theme for message formatting."""
        if theme in ['neutral', 'optimistic', 'pessimistic']:
            self.current_theme = theme
        else:
            self.logger.warn(f"Unknown theme: {theme}, keeping current theme")
    
    def _format_message(self, template_key: str, *args) -> str:
        """Format error message based on current theme and template."""
        template = self._message_templates.get(template_key, {})
        message_template = template.get(self.current_theme, template.get('neutral', '{}'))
        return message_template.format(*args)

    def _get_theme_aware_message(self, template_key: str, error_message: str) -> str:
        """Get theme-aware error message.
        
        Args:
            template_key: Key for message template
            error_message: Error message to format
            
        Returns:
            str: Theme-aware formatted message
        """
        try:
            dialog_config = self.styles.DIALOG_CONFIG()
            template = dialog_config.get('error_templates', {}).get(template_key, error_message)
            return template.format(reason=error_message)
        except (KeyError, AttributeError):
            return error_message

    def _show_error_dialog(self, title: str, message: str) -> None:
        """Show error dialog with theme-aware styling."""
        self.dialog.dialog_manager.show_error(title, message)

    def _show_warning_dialog(self, title: str, message: str) -> None:
        """Show warning dialog with theme-aware styling."""
        self.dialog.dialog_manager.show_warning(title, message)

    def _show_info_dialog(self, title: str, message: str) -> None:
        """Show info dialog with theme-aware styling."""
        self.dialog.dialog_manager.show_info(title, message)

    def handle_weather_error(self, error_exception: Optional[Exception], city_name: str) -> bool:
        """Handles weather-related errors and shows appropriate user messages."""
        if not error_exception:
            return True
            
        if isinstance(error_exception, ValidationError):
            # Critical errors - don't show fallback data
            self.dialog.dialog_manager.show_error("Input Error", str(error_exception))
            return False
        elif isinstance(error_exception, CityNotFoundError):
            # City not found - show error but continue with fallback
            # Note: This error is already shown by the API layer, so we only log it
            self.logger.warn(f"City '{city_name}' not found - using fallback data")
            return True
        elif isinstance(error_exception, RateLimitError):
            # Rate limit - show specific message
            message = self._format_message('rate_limit', city_name)
            self.dialog.dialog_manager.show_theme_aware_dialog('error', 'rate_limit', message)
            return True
        elif isinstance(error_exception, NetworkError):
            # Network issues - show network-specific message
            message = self._format_message('network_error', city_name)
            self.dialog.dialog_manager.show_theme_aware_dialog('warning', 'network_issue', message)
            return True
        elif isinstance(error_exception, DataFetchError):
            # Data fetch errors - show error but continue with fallback
            message = self._format_message('data_fetch_error', str(error_exception))
            self.dialog.dialog_manager.show_theme_aware_dialog('error', 'data_fetch_error', message)
            return True
        else:
            # Other API errors - show general fallback notice
            self.logger.warn(f"Using fallback for {city_name}: {error_exception}")
            self.dialog.dialog_manager.show_theme_aware_dialog('info', 'notice', f"No live data available for '{city_name}'. Simulated data is shown.")
            return True

    def handle_input_validation_error(self, error: Exception) -> None:
        """Handles input validation errors."""
        self.logger.error(f"Input validation error: {error}")
        self.dialog.dialog_manager.show_theme_aware_dialog('error', 'input_error', str(error))

    def handle_unexpected_error(self, error: Exception) -> None:
        """Handles unexpected errors."""
        if isinstance(error, str):
            self.logger.error(f"Unexpected error: {error}")
            self.dialog.dialog_manager.show_theme_aware_dialog('error', 'general_error', str(error))
        else:
            self.logger.error(f"Unexpected error: {error}")
            self.dialog.dialog_manager.show_theme_aware_dialog('error', 'general_error', str(error))
    
    def handle_rate_limit_error(self, error: RateLimitError) -> None:  # Fixed signature
        """Handle rate limit errors with theme-aware messaging."""
        message = self._get_theme_aware_message("rate_limit", str(error))
        self._show_error_dialog("Rate Limit Error", message)

    def handle_data_fetch_error(self, error: DataFetchError) -> None:
        """Handle data fetch errors with theme-aware messaging."""
        message = self._get_theme_aware_message("data_fetch_error", str(error))
        self._show_error_dialog("Data Fetch Error", message)

    def handle_cancellation_error(self, error: CancellationError) -> None:
        """Handle operation cancellation with theme-aware messaging."""
        message = self._get_theme_aware_message("cancellation", str(error))
        self._show_info_dialog("Operation Cancelled", message)

    def handle_logging_error(self, error: LoggingError) -> None:
        """Handle logging errors with theme-aware messaging."""
        message = self._get_theme_aware_message("logging_error", str(error))
        self._show_warning_dialog("Logging Error", message)

    def handle_chart_rendering_error(self, error: ChartRenderingError) -> None:
        """Handle chart rendering errors with theme-aware messaging."""
        message = self._get_theme_aware_message("chart_error", str(error))
        self._show_error_dialog("Chart Error", message)

    def handle_timeout_error(self, error: TimeoutError) -> None:
        """Handle timeout errors with theme-aware messaging."""
        message = self._get_theme_aware_message("timeout_error", str(error))
        self._show_error_dialog("Timeout Error", message)