"""
Main controller for coordinating weather data operations.

This module provides the central controller class that coordinates weather data
fetching, processing, display updates, and error handling. Supports theme-aware
operations and comprehensive error recovery.

Classes:
    WeatherDashboardController: Main controller coordinating all weather operations
"""

from typing import Tuple, List, Any
import tkinter.messagebox as messagebox

from WeatherDashboard import config
from WeatherDashboard.utils.utils import normalize_city_name, validate_unit_system
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.rate_limiter import RateLimiter
from WeatherDashboard.services.error_handler import WeatherErrorHandler
from WeatherDashboard.services.api_exceptions import ValidationError
from WeatherDashboard.core.view_models import WeatherViewModel
from WeatherDashboard.features.alerts.alert_manager import AlertManager


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
    def __init__(self, state: Any, data_service: Any, widgets: Any, theme: str = 'neutral') -> None:
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
        self.current_theme = theme
        
        # Initialize helper classes
        self.rate_limiter = RateLimiter()
        self.error_handler = WeatherErrorHandler(theme)

        # Initialize alert system
        self.alert_manager = AlertManager(state)
    
    def set_theme(self, theme: str) -> None:
        """Set theme for error handling and future theme system integration."""
        self.current_theme = theme
        self.error_handler.set_theme(theme)
        Logger.info(f"Controller theme set to: {theme}")
    
    def update_weather_display(self, city_name: str, unit_system: str) -> bool:
        """Coordinate fetching and displaying weather data with enhanced error handling.
        
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
            return False
        
        # Check rate limiting
        if not self._check_rate_limiting():
            return False
        
        # Fetch and process data
        return self._fetch_and_display_data(city_name, unit_system)

    def _validate_inputs_and_state(self, city_name: str, unit_system: str) -> bool:
        """Validate input parameters and application state with enhanced error reporting.
        
        Args:
            city_name: City name to validate
            unit_system: Unit system parameter (validated by service layer)
            
        Returns:
            bool: True if validation passed, False otherwise
        """
        # Input validation
        if not isinstance(city_name, str):
            self.error_handler.handle_input_validation_error("City name must be text")
            return False
        
        # State validation
        state_errors = self.state.validate_current_state()
        if state_errors:
            error_msg = "Invalid application state: " + "; ".join(state_errors)
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

    def _fetch_and_display_data(self, city_name: str, unit_system: str) -> bool:
        """Fetch weather data and update the display with comprehensive error handling.
        
        Args:
            city_name: Name of the city to fetch weather for
            unit_system: Unit system for the data
            
        Returns:
            bool: True if operation succeeded, False otherwise
        """
        try:
            # Fetch data
            city, raw_data, error_exception = self.service.get_city_data(city_name, unit_system)
            
            # Store data in centralized state instead of scattered variables
            self.state.set_weather_data(raw_data, is_fallback=bool(error_exception))

            # Create view model
            view_model = WeatherViewModel(city, raw_data, unit_system)
            
            # Handle any errors
            should_continue = self.error_handler.handle_weather_error(error_exception, city)
            if not should_continue:
                return False
            
            # Update display components
            self.state.update_city_display(
                city_name=view_model.city_name,
                date_str=view_model.date_str
            )

            # Update display
            self.state.update_metric_display(view_model.metrics)

            # Update status bar with data source info
            data_status = f"{view_model.city_name} ({'Simulated' if error_exception else 'Live'})"
            self.state.update_status_bar_data(data_status)

            if error_exception:
                # Simulated data - make it red/warning
                if hasattr(self.state, 'data_status_label') and self.state.data_status_label:
                    self.state.data_status_label.configure(foreground="red")
            else:
                # Live data - make it green/normal  
                if hasattr(self.state, 'data_status_label') and self.state.data_status_label:
                    self.state.data_status_label.configure(foreground="darkgreen")
                
            self.state.update_status_bar_system("Data updated", "info")

            # Check for weather alerts after successful data update
            if raw_data:
                # raw_data is already unit-converted by the data service
                alerts = self.alert_manager.check_weather_alerts(raw_data)
                # Update alert status widget if it exists. Access through tabbed widgets property
                if (hasattr(self.widgets, 'metric_widgets') and 
                    self.widgets.metric_widgets and
                    hasattr(self.widgets.metric_widgets, 'alert_status_widget')):
                    self.widgets.metric_widgets.update_alert_display(alerts)
            
            # Log the data
            self.service.write_to_log(city, raw_data, unit_system)
            return True

        except ValidationError as e:
            self.error_handler.handle_input_validation_error(str(e))
            return False
        except Exception as e:
            self.error_handler.handle_unexpected_error(str(e))
            return False

    def show_weather_alerts(self) -> None:
        """Display weather alerts popup with enhanced error handling."""
        from WeatherDashboard.features.alerts.alert_display import SimpleAlertPopup
        
        active_alerts = self.alert_manager.get_active_alerts()
        if active_alerts:
            # Get parent window for popup
            parent = None
            if (hasattr(self.widgets, 'frames') and 
                isinstance(self.widgets.frames, dict) and 
                'title' in self.widgets.frames):
                parent = self.widgets.frames['title']
            
            SimpleAlertPopup(parent, active_alerts)
        else:
            from tkinter import messagebox
            messagebox.showinfo("Weather Alerts", "No active weather alerts.")

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
            self._handle_chart_error("Chart configuration error", e)
        except ValueError as e:
            self._handle_chart_error("Chart data error", e)
        except Exception as e:
            self._handle_chart_error("Unexpected chart error", e)

    def _handle_chart_error(self, error_type: str, error: Exception) -> None:
        """Handle chart errors with proper recovery.
        
        Args:
            error_type: Type/category of the chart error
            error: The exception that occurred
        """
        Logger.error(f"{error_type}: {error}")
        messagebox.showwarning("Chart Error", f"{error_type}. Chart will be cleared.")
        
        # Clear the chart gracefully
        try:
            if self.state.is_chart_available():
                self.state.chart_ax.clear()
                self.state.chart_ax.text(0.5, 0.5, 'Chart unavailable\nPlease check settings', ha='center', va='center', transform=self.state.chart_ax.transAxes)
                self.state.chart_canvas.draw()
        except Exception as recovery_error:
            Logger.error(f"Failed to clear chart after error: {recovery_error}")

    def _get_chart_settings(self) -> Tuple[str, int, str, str]:
        """Retrieve the current settings for chart display.
        
        Returns:
            Tuple[str, int, str, str]: city, days, metric_key, unit_system
            
        Raises:
            ValueError: If city name is empty or date range is invalid
        """
        raw_city = self.state.get_current_city()
        if not raw_city or not raw_city.strip():
            raise ValueError("City name is required for chart display")
        
        city = normalize_city_name(raw_city)
        days = config.CHART["range_options"].get(self.state.get_current_range(), 7)
        
        if days <= 0:
            raise ValueError(f"Invalid date range: {days} days")
        
        metric_key = self._get_chart_metric_key()
        unit = self.state.get_current_unit_system()
        
        validate_unit_system(unit)  # Ensure unit system is valid
        
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
            raise ValueError(f"No historical data available for {city}.")

        if not all(metric_key in d for d in data):
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
        self.widgets.update_chart_display(x_vals, y_vals, metric_key, city, unit, fallback=True)

    def _get_chart_metric_key(self) -> str:
        """Determine the metric key for the chart based on user selection."""
        display_name = self.state.get_current_chart_metric()
        
        # Handle special case when no metrics are selected
        if display_name == "No metrics selected":
            raise ValueError("Please select at least one metric to display in the chart.")
        
        metric_key = config.DISPLAY_TO_KEY.get(display_name)
        if not metric_key:
            raise KeyError(f"Invalid chart metric: '{display_name}'. Please select a valid metric.")
        return metric_key