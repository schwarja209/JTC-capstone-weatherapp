"""
Main controller for coordinating weather data operations.

This module provides the central controller class that orchestrates weather data
fetching, processing, display updates, chart rendering, alert management, and error
handling. Coordinates between services, state management, and UI components while
supporting theme-aware operations and comprehensive error recovery.

The controller handles both synchronous operations and coordinates with async
weather fetching, manages rate limiting, and integrates with the alert system
for comprehensive weather dashboard functionality.

Classes:
    WeatherDashboardController: Main controller coordinating all weather operations
"""

from typing import Tuple, List, Any, Optional
import threading

from WeatherDashboard import config
from WeatherDashboard.core.view_models import WeatherViewModel
from WeatherDashboard.features.alerts.alert_manager import AlertManager
from WeatherDashboard.services.api_exceptions import ValidationError, WeatherDashboardError
from WeatherDashboard.services.error_handler import WeatherErrorHandler
from WeatherDashboard.widgets.widget_interface import IWeatherDashboardWidgets
from WeatherDashboard.utils.utils import is_fallback
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.rate_limiter import RateLimiter
from WeatherDashboard.utils.validation_utils import ValidationUtils


class WeatherDashboardController:
    """Coordinate weather data operations with clean separation of concerns.
    
    Central controller that orchestrates weather data fetching, processing,
    display updates, chart rendering, and error handling. Provides theme-aware
    error messaging and comprehensive state management.
    
    Attributes:
        service: Weather data service for API operations
        widgets: UI widget manager for display updates
        state: Application state manager
        current_theme: Current theme for error messaging
        error_handler: Error handler with theme support
        recovery_manager: Error recovery and retry manager
        rate_limiter: API rate limiting manager
        alert_manager: Weather alert processing manager
    """    
    def __init__(self, state: Any, data_service: Any, widgets: IWeatherDashboardWidgets, ui_handler: Any, theme: str = 'neutral') -> None:
        """Initialize the weather dashboard controller.
        
        Args:
            state: Application state manager
            data_service: Weather data service for API operations
            widgets: UI widget manager for display updates
            theme: Initial theme for error messaging ('neutral', 'optimistic', 'pessimistic')
        """
        self.service = data_service
        self.widgets = widgets
        self.state = state
        self.ui_handler = ui_handler
        self.current_theme = theme
        
        # Initialize helper classes
        self.rate_limiter = RateLimiter()
        self.error_handler = WeatherErrorHandler(theme)
        self.alert_manager = AlertManager(state)
    
    def set_theme(self, theme: str) -> None:
        """Set theme for error handling and future theme system integration."""
        self.current_theme = theme
        self.error_handler.set_theme(theme)
        Logger.info(f"Controller theme set to: {theme}")
    
    def update_weather_display(self, city_name: str, unit_system: str, cancel_event: Optional[threading.Event] = None) -> Tuple[bool, Optional[str]]:
        """Coordinate fetching and displaying weather data with enhanced error handling and cancellation support.
        
        Validates inputs, checks rate limits, fetches weather data, and updates
        the display. Includes comprehensive error handling and retry logic.
        
        Args:
            city_name: Name of the city to fetch weather for
            unit_system: Unit system for display ('metric' or 'imperial')
            
        Returns:
            bool: True if operation succeeded, False if it failed
        """
        # Validate inputs and state
        if not self._validate_inputs_and_state(city_name, unit_system):
            return False, "Input validation failed"
        
        # Check rate limiting
        if not self._check_rate_limiting():
            return False, "Rate limiting failed"
        
        # Fetch and process data
        return self._fetch_and_display_data(city_name, unit_system, cancel_event)

    def update_chart(self) -> None:
        """Update the chart with historical weather data for the selected city and metric.
        
        Retrieves chart settings, builds data series, and renders the chart
        with comprehensive error handling and recovery.
        """
        try:
            city, days, metric_key, unit = self._get_chart_settings()
            x_vals, y_vals = self._build_chart_series(city, days, metric_key, unit)
            self._render_chart(x_vals, y_vals, metric_key, city, unit)

        except KeyError as e:
            validation_error = ValidationError(str(e))
            self._handle_error("Chart configuration error", str(validation_error), is_chart_error=True)
        except ValueError as e:
            validation_error = ValidationError(str(e))
            self._handle_error("Chart data error", str(validation_error), is_chart_error=True)
        except Exception as e:
            dashboard_error = WeatherDashboardError(str(e))
            self._handle_error("Unexpected chart error", str(dashboard_error), is_chart_error=True)

    def show_weather_alerts(self) -> None:
        """Display weather alerts popup with enhanced error handling."""        
        active_alerts = self.alert_manager.get_active_alerts()
        if active_alerts:
            # Get parent window for popup
            parent = self.ui_handler.get_alert_popup_parent()

            if not self.ui_handler.are_widgets_ready():
                return
            
            self.ui_handler.show_alert_popup(active_alerts)
        else:
            self.ui_handler.show_info("Weather Alerts", "No active weather alerts.")

    def _validate_inputs_and_state(self, city_name: str, unit_system: str) -> bool:
        """Validate input parameters and application state using centralized validation.
    
        Performs comprehensive validation of user inputs and current application state
        before proceeding with weather data operations. Uses centralized validation
        utilities to check input types, value ranges, and state consistency.
        
        Args:
            city_name: City name to validate (type and content checking)
            unit_system: Unit system to validate ('metric' or 'imperial')
            
        Returns:
            bool: True if all validation passes, False if any validation fails
            
        Side Effects:
            Displays error messages to user via error handler for validation failures
        """        
        # Validate inputs
        input_errors = ValidationUtils.validate_input_types(city_name, unit_system)
        if input_errors:
            error_msg = ValidationUtils.format_validation_errors(input_errors, "Input validation failed")
            self.error_handler.handle_input_validation_error(error_msg)
            return False
        
        # Validate state
        state_errors = ValidationUtils.validate_complete_state(self.state)
        if state_errors:
            error_msg = ValidationUtils.format_validation_errors(state_errors, "Invalid application state")
            self.error_handler.handle_input_validation_error(error_msg)
            return False
        
        return True

    def _check_rate_limiting(self) -> bool:
        """Check rate limiting and handle rate limit errors with theme-aware messaging.
        
        Returns:
            bool: True if request can proceed, False if rate limited
        """
        if not self.rate_limiter.can_make_request():
            wait_time = self.rate_limiter.get_wait_time()
            Logger.warn("Fetch blocked due to rate limiting.")
            # Delegate UI messaging to error handler
            self.error_handler.handle_rate_limit_error(wait_time)
            return False

        self.rate_limiter.record_request()
        return True

    def _fetch_and_display_data(self, city_name: str, unit_system: str, cancel_event: Optional[threading.Event] = None) -> Tuple[bool, Optional[str]]:
        """Fetch weather data and update the display with standardized error handling.
        
        Args:
            city_name: Name of the city to fetch weather for
            unit_system: Unit system for the data
            
        Returns:
            bool: True if operation succeeded, False otherwise
        """
        try:
            # Fetch data
            city, raw_data, error_exception = self.service.get_city_data(city_name, unit_system, cancel_event)

            # Generate alerts and inject into raw_data
            alerts = self.alert_manager.check_weather_alerts(raw_data)
            raw_data["alerts"] = alerts

            # Create view model
            view_model = WeatherViewModel(city, raw_data, unit_system)
            
            # Handle any errors using standardized error handler
            should_continue = self.error_handler.handle_weather_error(error_exception, city)
            if not should_continue:
                return False, str(error_exception) if error_exception else "Unknown error"

            # Find if data is simulated
            simulated = is_fallback(raw_data)
            if not should_continue or simulated:
                # Treat as error for the async layer
                return False, str(error_exception) if error_exception else "Simulated data used due to API failure"

            # Update all display components
            self.ui_handler.update_display(view_model, error_exception, simulated)
            
            # Log the data
            self.service.write_to_log(city, raw_data, unit_system)
            return True, None

        except ValidationError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)
    
    def _get_chart_settings(self) -> Tuple[str, int, str, str]:
        """Retrieve and validate current settings for chart display.
    
        Validates city name, retrieves date range from config, determines metric key
        from user selection, and validates unit system for chart rendering.
        
        Returns:
            Tuple containing:
                - str: Normalized city name
                - int: Number of days for chart data
                - str: Metric key for charting
                - str: Unit system ('metric' or 'imperial')
            
        Raises:
            ValueError: If city name is empty or date range is invalid
        """
        raw_city = self.state.get_current_city()
        if not raw_city or not raw_city.strip():
            raise ValueError(config.ERROR_MESSAGES['missing'].format(field="City name"))
        
        errors = ValidationUtils.validate_city_name(raw_city)
        if errors:
            raise ValueError(errors[0])
        city = raw_city.strip().title()

        days = config.CHART["range_options"].get(self.state.get_current_range(), 7)
        
        if days <= 0:
            raise ValueError(config.ERROR_MESSAGES['validation'].format(field="Date range", reason=f"{days} days is invalid"))
        
        metric_key = self._get_chart_metric_key()
        unit = self.state.get_current_unit_system()
        
        unit_errors = ValidationUtils.validate_unit_system(unit) # Ensure unit system is valid
        if unit_errors:
            raise ValueError(unit_errors[0])
        
        return city, days, metric_key, unit
    
    def _build_chart_series(self, city: str, days: int, metric_key: str, unit: str) -> Tuple[List[str], List[Any]]:
        """Build the x and y axis values for the chart based on historical data.
        
        Args:
            city: City name for data retrieval
            days: Number of days of historical data to retrieve
            metric_key: Weather metric to chart
            unit: Unit system for the data
            
        Returns:
            Tuple[List[str], List[Any]]: x_values (dates), y_values (metric data)
            
        Raises:
            ValueError: If no historical data is available
        """
        data = self.service.get_historical_data(city, days, unit)

        if not data:
            raise ValueError(config.ERROR_MESSAGES['not_found'].format(resource="Historical data", name=city))

        if not all(metric_key in d for d in data):
            Logger.warn(f"Warning: Some data entries are missing '{metric_key}'")
            print(f"Warning: Some data entries are missing '{metric_key}'")

        x_vals = [d['date'].strftime("%Y-%m-%d") for d in data]  # Dynamic axis values
        y_vals = [d[metric_key] for d in data if metric_key in d]
        return x_vals, y_vals
    
    def _render_chart(self, x_vals: List[str], y_vals: List[Any], metric_key: str, city: str, unit: str) -> None:
        """Render the chart with the provided x and y values.
        
        Args:
            x_vals: X-axis values (typically dates)
            y_vals: Y-axis values (metric data)
            metric_key: Weather metric being charted
            city: City name for chart title
            unit: Unit system for labeling
        """
        self.ui_handler.update_chart_components(x_vals, y_vals, metric_key, city, unit, fallback=True)

    def _get_chart_metric_key(self) -> str:
        """Determine the metric key for the chart based on user selection."""
        display_name = self.state.get_current_chart_metric()
        
        # Handle special case when no metrics are selected
        if display_name == "No metrics selected":
            raise ValueError(config.ERROR_MESSAGES['validation'].format(field="Chart metric", reason="at least one metric must be selected"))
        
        # Find metric key by matching display label
        metric_key = None
        for key, metric_data in config.METRICS.items():
            if metric_data['label'] == display_name:
                metric_key = key
                break
        if not metric_key:
            raise KeyError(config.ERROR_MESSAGES['not_found'].format(resource="Chart metric", name=display_name))
        return metric_key

    def _handle_error(self, error_type: str, error_message: str, is_chart_error: bool = False) -> bool:
        """Unified error handling for controller operations.
        
        Logs the error, displays user-friendly warning, and attempts to clear
        the chart display gracefully with fallback error message.

        Args:
            error_type: Type of error ('validation', 'unexpected', etc.)
            error_message: Error message to handle
            
        Returns:
            bool: Always False to indicate operation failure
        """
        if is_chart_error:
            Logger.exception(f"{error_type}: {error_message}", error_message)
            self.ui_handler.show_warning("Chart Error", f"{error_type}. Chart will be cleared.")
            self.ui_handler.update_chart_components(clear=True)
        else:
            if error_type == "validation":
                self.error_handler.handle_input_validation_error(error_message)
            else:
                self.error_handler.handle_unexpected_error(error_message)
        return False