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

import threading
from typing import Tuple, List, Any, Optional, Dict
from datetime import datetime

from WeatherDashboard import config, styles
from WeatherDashboard.utils.utils import Utils
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.rate_limiter import RateLimiter
from WeatherDashboard.utils.unit_converter import UnitConverter
from WeatherDashboard.utils.validation_utils import ValidationUtils

from WeatherDashboard.features.alerts.alert_manager import AlertManager, WeatherAlert
from WeatherDashboard.services.api_exceptions import (
    ValidationError, WeatherDashboardError, RateLimitError, 
    DataFetchError, TimeoutError, CancellationError, 
    LoggingError, ChartRenderingError, CityNotFoundError, NetworkError
)
from WeatherDashboard.services.error_handler import WeatherErrorHandler, RateLimitError
from WeatherDashboard.widgets.widget_interface import IWeatherDashboardWidgets

from .view_models import WeatherViewModel


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
     
    def __init__(self, state: Any, data_service: Any, widgets: IWeatherDashboardWidgets, ui_handler: Any, theme: str = 'neutral',
             error_handler: Optional[WeatherErrorHandler] = None, alert_manager: Optional[AlertManager] = None) -> None:
        """Initialize the weather dashboard controller with hybrid dependency injection.
        
        Args:
            state: Application state manager (injected for testability)
            data_service: Weather data service for API operations (injected for testability)
            widgets: UI widget manager for display updates (injected for testability)
            ui_handler: UI handler for user interactions (injected for testability)
            theme: Initial theme for error messaging ('neutral', 'optimistic', 'pessimistic')
            error_handler: Error handler with theme support (injected for testability)
            alert_manager: Weather alert processing manager (injected for testability)
        """
        # Direct imports for stable utilities
        self.logger = Logger()
        self.config = config
        self.styles = styles
        self.utils = Utils()
        self.rate_limiter = RateLimiter()
        self.unit_converter = UnitConverter()
        self.validation_utils = ValidationUtils()
        
        # Injected dependencies for testable components
        self.service = data_service
        self.widgets = widgets
        self.state = state
        self.ui_handler = ui_handler
        self.error_handler = error_handler or WeatherErrorHandler(theme)
        self.alert_manager = alert_manager or AlertManager(state, None)
        
        # Factory for complex objects
        self.view_model_factory = lambda city, data, unit: WeatherViewModel(
                city, data, unit
        )

        # Initialize internal service classes
        self._data_service = self._DataService(data_service)
        self._alert_service = self._AlertService(self.alert_manager)
        self._chart_service = self._ChartService(state, data_service, widgets, self.error_handler, ui_handler)
        self._validation_service = self._ValidationService(self.error_handler, state)
        self._rate_limit_service = self._RateLimitService(self.error_handler)
        self._theme_service = self._ThemeService(theme, self.error_handler)
        self._ui_service = self._UIService(widgets, ui_handler)
        
    def set_theme(self, theme: str) -> None:
        """Set theme for error handling and future theme system integration."""
        self._theme_service.set_theme(theme)

        # IMPORTANT: Actually reconfigure the styles for the new theme
        from WeatherDashboard import styles
        styles.configure_styles(theme)

# ================================
# 1. PUBLIC API METHODS
# ================================
    def update_weather_display(self, city_name: str, unit_system: str, cancel_event: Optional[threading.Event] = None) -> None:
        """Orchestrate the complete weather display update process.
        
        Coordinates validation, rate limiting, and data fetching in sequence.
        """
        self.logger.info(f"Starting weather update for {city_name}")

        try:
            # Step 1: Validate inputs
            self._validation_service.validate_inputs(city_name, unit_system)
            
            # Step 2: Check rate limiting
            rate_limit_result = self._rate_limit_service.can_proceed()
            if not rate_limit_result[0]:
                raise RateLimitError(rate_limit_result[1])
            
            # Step 3: Fetch and display data
            self._fetch_and_display_data(city_name, unit_system, cancel_event)
            self.logger.info(f"Weather update completed for {city_name}")
            
        except ValidationError as e:
            self.logger.error(f"Validation error for {city_name}: {e}")
            self.error_handler.handle_input_validation_error(e)
            return # Don't re-raise - validation errors should be handled gracefully
        except RateLimitError as e:
            self.logger.error(f"Rate limit error for {city_name}: {e}")
            self.error_handler.handle_rate_limit_error(e)
            raise
        except DataFetchError as e:
            self.logger.error(f"Data fetch error for {city_name}: {e}")
            self.error_handler.handle_data_fetch_error(e)
            raise
        except CancellationError as e:
            self.logger.error(f"Operation cancelled for {city_name}: {e}")
            return # Don't show error for user-initiated cancellations
        except Exception as e:
            self.logger.error(f"Unexpected error for {city_name}: {e}")
            self.error_handler.handle_unexpected_error(e)
            raise


    def update_chart(self) -> None:
        """Update the chart with historical weather data for the selected city and metric.
        
        Retrieves chart settings, builds data series, and renders the chart
        with comprehensive error handling and recovery.
        """
        self._chart_service.update_chart()

    def show_weather_alerts(self) -> None:
        """Display weather alerts popup with enhanced error handling."""        
        active_alerts = self._alert_service.get_active_alerts()
        self._ui_service.show_weather_alerts(active_alerts)

# ================================
# 2. PRIVATE HELPER METHODS
# ================================
    def _fetch_and_display_data(self, city_name: str, unit_system: str, cancel_event: Optional[threading.Event] = None) -> None:
        """Fetch weather data and update the display with standardized error handling.
        
        Args:
            city_name: Name of the city to fetch weather for
            unit_system: Unit system for the data
        """
        self.logger.info(f"Fetching data for {city_name}")

        try:
            # Step 1: Fetch data
            raw_data = self._data_service.fetch_data(city_name, unit_system, cancel_event)
            
            # Step 2: Check for API errors in the data
            api_error = None
            error_exception = None
            if isinstance(raw_data, dict) and 'api_error' in raw_data:
                api_error = raw_data['api_error']
                error_type = raw_data.get('error_type', 'APIError')
                # Create the appropriate exception for status bar display
                if error_type == 'CityNotFoundError':
                    error_exception = CityNotFoundError(api_error)
                else:
                    error_exception = DataFetchError(api_error)
                # Remove error info from data to avoid issues
                del raw_data['api_error']
                del raw_data['error_type']
            
            # Step 3: Generate alerts and inject into raw_data
            alerts = self._alert_service.generate_alerts(raw_data)
            raw_data["alerts"] = alerts

            # Step 4: Create view model
            view_model = self.view_model_factory(city_name, raw_data, unit_system)

            # Step 5: Find if data is simulated
            simulated = self._data_service.is_simulated_data(raw_data)

            # Step 6: Update all display components
            try:
                self._ui_service.update_display(view_model, error_exception, simulated)
            except Exception as e:
                self.logger.error(f"Error in update_display: {e}")
                self.logger.error(f"Error type: {type(e)}")
                raise
            
            # Step 7: Log the data
            self._data_service.log_data(city_name, raw_data, unit_system)
            
            # Step 8: Show error notification if there was an API error
            if api_error:
                self.error_handler.handle_data_fetch_error(DataFetchError(api_error))
            
            self.logger.info(f"Data fetch completed for {city_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to fetch and display data for {city_name}: {e}")
            raise

# ================================
# 3. INTERNAL CLASSES
# ================================
    class _DataService:
        """Internal service for data fetching and processing operations.
    
        Encapsulates weather data retrieval, simulated data detection, and logging
        functionality. Provides a clean interface for the controller to interact
        with the underlying data service layer.
        
        Attributes:
            logger: Logger instance for operation logging
            utils: Utils instance for utility operations
            data_service: Injected weather data service for API operations
        """
        
        def __init__(self, data_service: Any) -> None:
            """Initialize the data service with hybrid dependency injection.
    
            Args:
                data_service: Weather data service for API operations (injected for testability)
            """
            # Direct imports for stable utilities
            self.logger = Logger()
            self.utils = Utils()
            
            # Injected dependencies for testable components
            self.data_service = data_service
        
        def fetch_data(self, city_name: str, unit_system: str, cancel_event: Optional[threading.Event] = None) ->  Dict[str, Any]:
            """Fetch weather data for a specified city and unit system.
            
            Args:
                city_name: Name of the city to fetch weather data for
                unit_system: Unit system for the weather data ('metric' or 'imperial')
                cancel_event: Optional threading event for operation cancellation
            """
            try:
                self.logger.info(f"Fetching weather data for {city_name} with {unit_system} units")
                
                # Check for cancellation
                if cancel_event and cancel_event.is_set():
                    self.logger.info(f"Data fetch cancelled for {city_name}")
                    raise CancellationError(f"Data fetch cancelled for {city_name}")
                
                # Fetch data with timeout
                result = self.data_service.get_city_data(city_name, unit_system, cancel_event)
                
                if result is None:
                    raise DataFetchError(f"No data returned for {city_name}")
                
                if hasattr(result, 'error') and result.error:
                    raise DataFetchError(f"Data service error for {city_name}: {result.error}")
                
                self.logger.info(f"Successfully fetched data for {city_name}")
                return result
                
            except CancellationError:
                raise # Re-raise cancellation errors
            except CityNotFoundError as e:
                raise DataFetchError(f"City '{city_name}' not found") # Convert to DataFetchError so controller handles it properly
            except ValidationError as e:
                raise e # Re-raise validation errors
            except TimeoutError as e:
                self.logger.error(f"Timeout fetching data for {city_name}: {e}")
                raise TimeoutError(f"Data fetch timeout for {city_name}: {e}")
            except NetworkError as e:
                self.logger.error(f"Network error fetching data for {city_name}: {e}")
                raise NetworkError(f"Network error for {city_name}: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error fetching data for {city_name}: {e}")
                raise DataFetchError(f"Failed to fetch data for {city_name}: {e}")
        
        def is_simulated_data(self, raw_data: Dict[str, Any]) -> bool:
            """Determine if the provided weather data is simulated/fallback data."""
            return self.utils.is_fallback(raw_data)
        
        def log_data(self, city: str, raw_data: Dict[str, Any], unit_system: str) -> bool:
            """Log weather data for debugging and audit purposes.
            
            Args:
                city: City name for logging
                raw_data: Weather data to log
                unit_system: Unit system used
                
            Returns:
                bool: True if logging successful, False otherwise
            """
            try:
                result = self.data_service.write_to_log(city, raw_data, unit_system)
                if result.success:
                    self.logger.info(f"Data logged successfully for {city}")
                    return True
                else:
                    self.logger.warning(f"Data logging failed for {city}: {result.error}")
                    return False
            except Exception as e:
                self.logger.error(f"Exception during data logging for {city}: {e}")
                raise False

    class _RateLimitService:
        """Internal service for API rate limiting and request management.
    
        Manages API request frequency to prevent rate limit violations.
        Provides rate limit checking and request recording functionality
        with comprehensive error handling for rate limiting scenarios.
        
        Attributes:
            rate_limiter: Rate limiter instance for request tracking
            logger: Logger instance for rate limit logging
            error_handler: Error handler for rate limit error processing
        """
        
        def __init__(self, error_handler: WeatherErrorHandler) -> None:
            """Initialize the rate limit service with dependency injection.
            
            Args:
                error_handler: Error handler for rate limit error processing (injected for testability)
            """
            # Direct imports for stable utilities
            self.rate_limiter = RateLimiter()
            self.logger = Logger()
            
            # Injected dependencies for testable components
            self.error_handler = error_handler
        
        def can_proceed(self) -> Tuple[bool, Optional[str]]:
            """Check rate limiting and handle rate limit errors with theme-aware messaging.
        
            Returns:
                Tuple[bool, Optional[str]]: (can_proceed, error_message)
            """
            try:
                if not self.rate_limiter.can_make_request():
                    self.logger.warn("Fetch blocked due to rate limiting.")
                    return False, "Rate limit exceeded. Please wait before trying again."
                
                # Record the request if it can proceed
                self.rate_limiter.record_request()
                return True, None
                
            except Exception as e:
                return False, f"Rate limiting error: {str(e)}"

    class _ValidationService:
        """Internal service for input validation and state verification.
    
        Performs comprehensive validation of user inputs and application state
        before weather operations. Uses centralized validation utilities to
        ensure data integrity and proper application state.
        
        Attributes:
            validation_utils: Validation utilities for input checking
            error_handler: Error handler for validation error processing
            state: Application state manager for state validation
        """
        
        def __init__(self, error_handler: WeatherErrorHandler, state: Any) -> None:
            """Initialize the validation service with dependency injection.
            
            Args:
                error_handler: Error handler for validation error processing (injected for testability)
                state: Application state manager for state validation (injected for testability)
            """
            # Direct imports for stable utilities
            self.validation_utils = ValidationUtils()
            
            # Injected dependencies for testable components
            self.error_handler = error_handler
            self.state = state
        
        def validate_inputs(self, city_name: str, unit_system: str) -> None:
            """Validate input parameters and application state using centralized validation.
    
            Performs comprehensive validation of user inputs and current application state
            before proceeding with weather data operations. Uses centralized validation
            utilities to check input types, value ranges, and state consistency.
            
            Args:
                city_name: City name to validate (type and content checking)
                unit_system: Unit system to validate ('metric' or 'imperial')
                
            Raises:
                ValueError: If any validation fails
                
            Side Effects:
                Displays error messages to user via error handler for validation failures
            """
            try:
                # Use centralized validation of city and units
                self.validation_utils.validate_input_types(city_name, unit_system)
                
                # Only validate state if we have a valid city name
                # Skip metric visibility validation for edge cases
                if city_name and len(city_name.strip()) > 0:
                    self.validation_utils.validate_complete_state(self.state)
                
            except Exception as e:
                raise ValueError(f"Validation error: {str(e)}")

    class _UIService:
        """Internal service for UI component updates and user interface operations.
        
        Manages all UI-related operations including display updates, alert
        popups, and widget state management. Provides a centralized interface
        for controller-initiated UI changes.
        
        Attributes:
            widgets: UI widget manager for display operations
            ui_handler: UI handler for user interaction operations
        """
        
        def __init__(self, widgets: IWeatherDashboardWidgets, ui_handler: Any) -> None:
            """Initialize the UI service with dependency injection.
            
            Args:
                widgets: UI widget manager for display operations (injected for testability)
                ui_handler: UI handler for user interaction operations (injected for testability)
            """
            self.widgets = widgets
            self.ui_handler = ui_handler
            self.logger = Logger()
        
        def show_weather_alerts(self, active_alerts: List[WeatherAlert]) -> None:
            """Display weather alerts popup with enhanced error handling.
    
            Shows weather alerts in a popup window if alerts exist, otherwise
            displays an informational message indicating no active alerts.
            """ 
            if active_alerts:
                if not self.ui_handler.are_widgets_ready():
                    return
                
                self.ui_handler.show_alert_popup(active_alerts)
            else:
                self.ui_handler.show_info("Weather Alerts", "No active weather alerts.")
        
        def update_display(self, view_model: WeatherViewModel, error_exception: Optional[Exception] = None, simulated: bool = False) -> None:
            """Update all display components with weather data and alerts.
    
            Updates metric display, status bar, and alert components with
            current weather information and any error states.

            Args:
                view_model: Weather data view model containing metrics and metadata
                error_exception: Optional exception that occurred during data fetching
                simulated: Whether the displayed data is simulated/fallback data
            """
            # Update metrics (include city and date in the metrics dict)
            self.widgets.update_metric_display({
                **view_model.metrics,
                "city": view_model.city_name,
                "date": view_model.date_str
            })

            # Update status bar
            self.widgets.update_status_bar(view_model.city_name, error_exception, simulated)
            
            # Update alerts
            self.widgets.update_alerts(view_model.raw_data)

    class _AlertService:
        """Internal service for weather alert generation and management.
    
        Handles the creation and retrieval of weather alerts based on current
        weather conditions. Provides a simplified interface for alert operations
        within the controller.
        
        Attributes:
            alert_manager: Injected alert manager for alert processing
        """
        
        def __init__(self, alert_manager: AlertManager) -> None:
            """Initialize the alert service with dependency injection.
    
            Args:
                alert_manager: Alert manager for weather alert processing (injected for testability)
            """
            self.alert_manager = alert_manager
        
        def generate_alerts(self, weather_data: Dict[str, Any]) -> List[WeatherAlert]:
            """Generate weather alerts based on current weather conditions"""
            return self.alert_manager.check_weather_alerts(weather_data)
        
        def get_active_alerts(self) -> List[WeatherAlert]:
            """Retrieve currently active weather alerts."""
            return self.alert_manager.get_active_alerts()

    class _ChartService:
        """Internal service for chart rendering and historical data visualization.
    
        Manages chart configuration, data series building, and chart rendering
        operations. Handles chart-specific error scenarios and provides
        comprehensive error recovery for chart display issues.
        
        Attributes:
            logger: Logger instance for operation logging
            config: Configuration instance for chart settings
            validation_utils: Validation utilities for input validation
            state: Application state manager for current settings
            data_service: Weather data service for historical data retrieval
            widgets: UI widget manager for chart display updates
            error_handler: Error handler for chart-specific error processing
            ui_handler: UI handler for chart component updates
        """
        
        def __init__(self, state: Any, data_service: Any, widgets: IWeatherDashboardWidgets, error_handler: WeatherErrorHandler, ui_handler: Any) -> None:
            """Initialize the chart service with hybrid dependency injection.
            
            Args:
                state: Application state manager (injected for testability)
                data_service: Weather data service for historical data (injected for testability)
                widgets: UI widget manager for chart display (injected for testability)
                error_handler: Error handler for chart error processing (injected for testability)
                ui_handler: UI handler for chart component updates (injected for testability)
            """            
            # Direct imports for stable utilities
            self.logger = Logger()
            self.config = config
            self.validation_utils = ValidationUtils()
            
            # Injected dependencies for testable components
            self.state = state
            self.data_service = data_service
            self.widgets = widgets
            self.error_handler = error_handler
            self.ui_handler = ui_handler
        
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
                self._handle_chart_error("Chart configuration error", str(validation_error))
            except ValueError as e:
                validation_error = ValidationError(str(e))
                self._handle_chart_error("Chart data error", str(validation_error))
            except Exception as e:
                dashboard_error = WeatherDashboardError(str(e))
                self._handle_chart_error("Unexpected chart error", str(dashboard_error))

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
                raise ValueError(self.config.ERROR_MESSAGES['missing'].format(field="City name"))
            
            self.validation_utils.validate_city_name(raw_city)
            city = raw_city.strip().title()

            days = self.config.CHART["range_options"].get(self.state.get_current_range(), 7)
            
            if days <= 0:
                raise ValueError(self.config.ERROR_MESSAGES['validation'].format(field="Date range", reason=f"{days} days is invalid"))
            
            metric_key = self._get_chart_metric_key()
            unit = self.state.get_current_unit_system()
            
            self.validation_utils.validate_unit_system(unit) # Ensure unit system is valid

            return city, days, metric_key, unit
        
        def _build_chart_series(self, city: str, days: int, metric_key: str, unit: str) -> Tuple[List[str], List[Any]]:
            """Build the x and y axis values for the chart based on historical data."""
            # Get the dataclass result and extract the data entries
            result = self.data_service.get_historical_data(city, days, unit)
            data = result.data_entries  # Extract the list from the dataclass

            if not data:
                raise ValueError(self.config.ERROR_MESSAGES['not_found'].format(resource="Historical data", name=city))

            if not all(metric_key in d for d in data):
                self.logger.warn(f"Warning: Some data entries are missing '{metric_key}'")
                print(f"Warning: Some data entries are missing '{metric_key}'")

            x_vals = [d['date'].strftime("%Y-%m-%d") for d in data]  # Dynamic axis values
            y_vals = [d[metric_key] for d in data if metric_key in d]
            
            # ADD CURRENT WEATHER AS LAST POINT
            try:
                # Get current weather data for the city using the correct method
                current_weather = self.data_service.get_city_data(city, unit)  # Returns Dict[str, Any]
                if current_weather is None:
                    self.logger.warn(f"Failed to get city data for {city}")
                    return x_vals, y_vals
                
                # Since get_city_data returns the weather data directly as a dict
                if current_weather and metric_key in current_weather:
                    # Format the current weather value properly
                    current_value = current_weather[metric_key]
                    
                    # Format based on metric type (similar to how metrics are formatted in view models)
                    if isinstance(current_value, (int, float)):
                        if metric_key in ['temperature', 'feels_like', 'temp_min', 'temp_max', 'heat_index', 'wind_chill', 'dew_point']:
                            # Temperature values - round to 1 decimal
                            formatted_value = round(current_value, 1)
                        elif metric_key in ['humidity', 'pressure', 'cloud_cover', 'air_quality_index']:
                            # Integer values - round to whole number
                            formatted_value = round(current_value)
                        elif metric_key in ['wind_speed', 'wind_gust', 'visibility', 'rain', 'snow', 'uv_index']:
                            # Other numeric values - round to 1 decimal
                            formatted_value = round(current_value, 1)
                        else:
                            # Default formatting
                            formatted_value = round(current_value, 1)
                    else:
                        formatted_value = current_value
                    
                    # Add current weather as the last point
                    if isinstance(current_weather, dict):
                        current_date = current_weather.get('date', datetime.now())
                    else:
                        self.logger.warn(f"Current weather data is not a dictionary for {city}")
                        current_date = datetime.now()
                    x_vals.append(current_date.strftime("%Y-%m-%d"))
                    y_vals.append(formatted_value)
                    
                    self.logger.info(f"Added current weather data to chart: {metric_key} = {current_weather[metric_key]}")
                else:
                    self.logger.warn(f"Current weather data missing {metric_key} for {city}")
                    
            except Exception as e:
                self.logger.warn(f"Failed to add current weather to chart: {e}")
                # Continue with historical data only
            
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
            try:
                self.ui_handler.update_chart_components(x_vals, y_vals, metric_key, city, unit)
            except Exception as e:
                self.logger.error(f"Failed to render chart: {e}")
                raise ChartRenderingError(f"Failed to render chart for {city}: {e}")

        def _get_chart_metric_key(self) -> str:
            """Determine the metric key for the chart based on user selection."""
            display_name = self.state.get_current_chart_metric()
            
            # Handle special case when no metrics are selected
            if display_name == "No metrics selected":
                raise ValueError(self.config.ERROR_MESSAGES['validation'].format(field="Chart metric", reason="at least one metric must be selected"))
            
            # Find metric key by matching display label
            metric_key = None
            for key, metric_data in self.config.METRICS.items():
                if metric_data['label'] == display_name:
                    metric_key = key
                    break
            if not metric_key:
                raise KeyError(self.config.ERROR_MESSAGES['not_found'].format(resource="Chart metric", name=display_name))
            return metric_key
        
        def _handle_chart_error(self, error_type: str, error_message: str) -> None:
            """Handle chart-specific errors."""
            self.logger.error(f"{error_type}: {error_message}")
            self.ui_handler.show_warning("Chart Error", f"{error_type}. Chart will be cleared.")
            self.ui_handler.update_chart_components(clear=True)


    class _ThemeService:
        """Internal service for theme management and error message theming.
    
        Handles theme configuration and provides theme-aware error messaging.
        Manages theme transitions and ensures consistent theming across
        error handling operations.
        
        Attributes:
            logger: Logger instance for theme operation logging
            error_handler: Error handler for theme-aware error processing
            current_theme: Current active theme for the application
        """
        
        def __init__(self, theme: str, error_handler: WeatherErrorHandler) -> None:
            """Initialize the theme service with dependency injection.
    
            Args:
                theme: Initial theme for the application
                error_handler: Error handler for theme-aware error processing (injected for testability)
            """
            # Direct imports for stable utilities
            self.logger = Logger()
            
            # Injected dependencies for testable components
            self.error_handler = error_handler
            self.current_theme = theme
        
        def set_theme(self, theme: str) -> None:
            """Set the application theme and update error handler theming.
            
            Args:
                theme: New theme to apply ('neutral', 'optimistic', 'pessimistic')
            """
            self.current_theme = theme
            self.error_handler.set_theme(theme)
            self.logger.info(f"Controller theme set to: {theme}")