"""
Unit tests for WeatherDashboardController class.

Tests core business logic orchestration including:
- Weather data fetching and display coordination
- Chart update management
- Alert system integration
- Error handling and recovery
- Theme management
- Rate limiting coordination
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WeatherDashboard.core.controller import WeatherDashboardController
from WeatherDashboard.services.api_exceptions import (
    ValidationError, CityNotFoundError, RateLimitError, NetworkError
)


class TestWeatherDashboardController(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures with mocked dependencies."""
        # Create mock dependencies
        self.mock_state = Mock()
        self.mock_data_service = Mock()
        self.mock_widgets = Mock()
        self.mock_ui_handler = Mock()
        
        # Configure mock state methods
        self.mock_state.get_current_city.return_value = "New York"
        self.mock_state.get_current_unit_system.return_value = "metric"
        self.mock_state.get_current_range.return_value = "Last 7 Days"
        self.mock_state.get_current_chart_metric.return_value = "Temperature"
        
        # Configure mock visibility state properly
        self.mock_visibility = {}
        for metric in ['temperature', 'humidity', 'wind_speed', 'pressure']:
            mock_var = Mock()
            mock_var.get.return_value = True
            self.mock_visibility[metric] = mock_var
        self.mock_state.visibility = self.mock_visibility
        
        # Configure mock widgets
        self.mock_widgets.metric_widgets = Mock()
        self.mock_widgets.status_bar_widgets = Mock()
        
        # Create mock dependencies for injection
        self.mock_rate_limiter = Mock()
        self.mock_error_handler = Mock()
        self.mock_alert_manager = Mock()
        
        # Create controller instance with injected dependencies
        self.controller = WeatherDashboardController(
            state=self.mock_state,
            data_service=self.mock_data_service,
            widgets=self.mock_widgets,
            ui_handler=self.mock_ui_handler,
            theme='neutral',
            rate_limiter=self.mock_rate_limiter,
            error_handler=self.mock_error_handler,
            alert_manager=self.mock_alert_manager
        )

    def test_dependency_injection(self):
        """Test that dependencies are properly injected."""
        # Verify injected dependencies are used
        self.assertEqual(self.controller.rate_limiter, self.mock_rate_limiter)
        self.assertEqual(self.controller.error_handler, self.mock_error_handler)
        self.assertEqual(self.controller.alert_manager, self.mock_alert_manager)
        
        # Verify these are mock objects, not real instances
        self.assertIsInstance(self.controller.rate_limiter, Mock)
        self.assertIsInstance(self.controller.error_handler, Mock)
        self.assertIsInstance(self.controller.alert_manager, Mock)

    def test_initialization(self):
        """Test controller initializes with correct dependencies."""
        self.assertEqual(self.controller.state, self.mock_state)
        self.assertEqual(self.controller.service, self.mock_data_service)
        self.assertEqual(self.controller.widgets, self.mock_widgets)
        self.assertEqual(self.controller.current_theme, 'neutral')
        self.assertIsNotNone(self.controller.rate_limiter)
        self.assertIsNotNone(self.controller.error_handler)
        self.assertIsNotNone(self.controller.alert_manager)

    def test_set_theme(self):
        """Test theme setting updates controller and error handler."""
        self.controller.set_theme('optimistic')
        self.assertEqual(self.controller.current_theme, 'optimistic')
        # Verify error handler theme was updated
        self.assertEqual(self.controller.error_handler.current_theme, 'optimistic')

    @patch('WeatherDashboard.core.controller.Logger')
    @patch('WeatherDashboard.core.controller.ValidationUtils')
    def test_update_weather_display_success(self, mock_validation_utils, mock_logger):
        """Test successful weather data update flow."""
        # Configure validation to pass
        mock_validation_utils.validate_input_types.return_value = []
        mock_validation_utils.validate_complete_state.return_value = []
        
        # Configure mocks for successful flow
        self.mock_rate_limiter.can_make_request.return_value = True
        
        # Mock successful data service response
        mock_city = "New York"
        mock_data = {
            'temperature': 25.0,
            'humidity': 60,
            'conditions': 'Clear'
        }
        self.mock_data_service.get_city_data.return_value = (mock_city, mock_data, None)
        
        # Mock view model creation
        with patch('WeatherDashboard.core.controller.WeatherViewModel') as mock_view_model:
            mock_vm_instance = Mock()
            mock_vm_instance.city_name = mock_city
            mock_vm_instance.date_str = "2024-12-01"
            mock_vm_instance.metrics = {'temperature': '25.0 °C'}
            mock_view_model.return_value = mock_vm_instance
            
            # Execute update
            result = self.controller.update_weather_display("New York", "metric")
            
            # Verify success
            self.assertTrue(result)
            # Fix: Check for the correct call signature with cancel_event=None
            self.mock_data_service.get_city_data.assert_called_once_with("New York", "metric", None)
            self.mock_data_service.write_to_log.assert_called_once()

    @patch('WeatherDashboard.core.controller.ValidationUtils')
    def test_update_weather_display_validation_failure(self, mock_validation_utils):
        """Test weather update with validation errors."""
        # Configure input validation to return errors
        mock_validation_utils.validate_input_types.return_value = ["City name cannot be empty"]
        
        # Execute update
        result = self.controller.update_weather_display("", "metric")
        
        # Verify failure
        self.assertFalse(result)
        # Verify data service was not called
        self.mock_data_service.get_city_data.assert_not_called()

    def test_update_weather_display_rate_limit(self):
        """Test weather update blocked by rate limiting."""
        # Configure rate limiter to block request
        self.mock_rate_limiter.can_make_request.return_value = False
        self.mock_rate_limiter.get_wait_time.return_value = 5.0
        
        # Mock validation to pass so we get to rate limiting check
        with patch('WeatherDashboard.core.controller.ValidationUtils') as mock_validation_utils:
            mock_validation_utils.validate_input_types.return_value = []
            mock_validation_utils.validate_complete_state.return_value = []
            
            # Execute update
            result = self.controller.update_weather_display("New York", "metric")
            
            # Verify failure due to rate limiting
            self.assertFalse(result)
            self.mock_data_service.get_city_data.assert_not_called()

    @patch('WeatherDashboard.core.controller.ValidationUtils')
    def test_update_weather_display_city_not_found(self, mock_validation_utils):
        """Test weather update with city not found error."""
        # Configure validation to pass
        mock_validation_utils.validate_input_types.return_value = []
        mock_validation_utils.validate_complete_state.return_value = []
        
        # Configure mocks for city not found
        self.mock_rate_limiter.can_make_request.return_value = True
        city_error = CityNotFoundError("City 'InvalidCity' not found")
        self.mock_data_service.get_city_data.return_value = ("InvalidCity", {}, city_error)
        
        # Mock view model creation
        with patch('WeatherDashboard.core.controller.WeatherViewModel') as mock_view_model:
            mock_vm_instance = Mock()
            mock_view_model.return_value = mock_vm_instance
            
            # Execute update
            result = self.controller.update_weather_display("InvalidCity", "metric")
            
            # Should still return True (fallback data used)
            self.assertTrue(result)

    def test_update_chart_success(self):
        """Test successful chart update."""
        # Configure mocks for chart data
        mock_x_vals = ['2024-12-01', '2024-12-02', '2024-12-03']
        mock_y_vals = [20.0, 22.0, 25.0]
        
        # Mock config access
        with patch('WeatherDashboard.core.controller.config') as mock_config:
            mock_config.CHART = {"range_options": {"Last 7 Days": 7}}
            mock_config.METRICS = {"temperature": {"label": "Temperature"}}
            
            # Mock service response
            self.mock_data_service.get_historical_data.return_value = [
                {'date': datetime(2024, 12, 1), 'temperature': 20.0},
                {'date': datetime(2024, 12, 2), 'temperature': 22.0},
                {'date': datetime(2024, 12, 3), 'temperature': 25.0}
            ]
            
            # Execute chart update
            self.controller.update_chart()
            
            # Verify chart was updated
            self.mock_widgets.update_chart_display.assert_called_once()

    def test_update_chart_no_data(self):
        """Test chart update with no historical data."""
        # Configure mocks for no data
        with patch('WeatherDashboard.core.controller.config') as mock_config:
            mock_config.CHART = {"range_options": {"Last 7 Days": 7}}
            mock_config.METRICS = {"temperature": {"label": "Temperature"}}
            
            # Mock service response with no data
            self.mock_data_service.get_historical_data.return_value = []
            
            # Execute chart update - should handle gracefully
            self.controller.update_chart()

    def test_update_chart_invalid_metric(self):
        """Test chart update with invalid metric selection."""
        # Configure state to return invalid metric
        self.mock_state.get_current_chart_metric.return_value = "Invalid Metric"
        
        with patch('WeatherDashboard.core.controller.config') as mock_config:
            mock_config.CHART = {"range_options": {"Last 7 Days": 7}}
            mock_config.METRICS = {"temperature": {"label": "Temperature"}}
            
            # Execute chart update - should handle error gracefully
            self.controller.update_chart()

    def test_show_weather_alerts_with_alerts(self):
        """Test showing weather alerts when alerts exist."""
        # Mock alert manager to return alerts
        mock_alerts = [Mock(), Mock()]
        self.mock_alert_manager.get_active_alerts.return_value = mock_alerts
        
        # Mock widgets to have frames
        self.mock_widgets.frames = {'title': Mock()}
        
        # Mock the alert popup to prevent actual Tkinter window creation
        with patch('WeatherDashboard.core.controller.SimpleAlertPopup') as mock_popup:
            self.controller.show_weather_alerts()
            
            # Verify popup was created with correct parameters
            mock_popup.assert_called_once_with(self.mock_widgets.frames['title'], mock_alerts)

    def test_show_weather_alerts_no_alerts(self):
        """Test showing weather alerts when no alerts exist."""
        # Mock alert manager to return no alerts
        self.mock_alert_manager.get_active_alerts.return_value = []
        
        # Mock the local import of messagebox in the method
        with patch('tkinter.messagebox') as mock_messagebox:
            self.controller.show_weather_alerts()
            
            # Verify info message was shown
            mock_messagebox.showinfo.assert_called_once_with("Weather Alerts", "No active weather alerts.")

    @patch('WeatherDashboard.core.controller.Logger')
    @patch('WeatherDashboard.core.controller.ValidationUtils')
    def test_fetch_and_display_data_network_error(self, mock_validation_utils, mock_logger):
        """Test handling of network errors during data fetching."""
        # Configure validation to pass
        mock_validation_utils.validate_input_types.return_value = []
        mock_validation_utils.validate_complete_state.return_value = []
        
        # Configure rate limiter to allow request
        self.mock_rate_limiter.can_make_request.return_value = True
        
        # Configure service to raise network error
        network_error = NetworkError("Connection failed")
        self.mock_data_service.get_city_data.return_value = ("New York", {}, network_error)
        
        # Mock view model creation
        with patch('WeatherDashboard.core.controller.WeatherViewModel') as mock_view_model:
            mock_vm_instance = Mock()
            mock_view_model.return_value = mock_vm_instance
            
            # Execute update
            result = self.controller.update_weather_display("New York", "metric")
            
            # Should handle error gracefully and return True (fallback used)
            self.assertTrue(result)

    @patch('WeatherDashboard.core.controller.ValidationUtils')
    def test_validate_inputs_and_state_invalid_city(self, mock_validation_utils):
        """Test input validation with invalid city name."""
        # Configure validation to return error for invalid input type
        mock_validation_utils.validate_input_types.return_value = ["City name must be a string, got int"]
        
        # Test with non-string city name
        result = self.controller._validate_inputs_and_state(123, "metric")
        self.assertFalse(result)

    @patch('WeatherDashboard.core.controller.ValidationUtils')
    def test_validate_inputs_and_state_invalid_state(self, mock_validation_utils):
        """Test input validation with invalid application state."""
        # Configure input validation to pass
        mock_validation_utils.validate_input_types.return_value = []
        # Configure state validation to return errors
        mock_validation_utils.validate_complete_state.return_value = ["Invalid unit system"]
        
        result = self.controller._validate_inputs_and_state("New York", "metric")
        self.assertFalse(result)

    def test_check_rate_limiting_blocked(self):
        """Test rate limiting check when request is blocked."""
        # Configure rate limiter to block request
        self.mock_rate_limiter.can_make_request.return_value = False
        self.mock_rate_limiter.get_wait_time.return_value = 10.0
        
        result = self.controller._check_rate_limiting()
        
        self.assertFalse(result)
        # Verify request was not recorded
        self.mock_rate_limiter.record_request.assert_not_called()

    def test_check_rate_limiting_allowed(self):
        """Test rate limiting check when request is allowed."""
        # Configure rate limiter to allow request
        self.mock_rate_limiter.can_make_request.return_value = True
        
        result = self.controller._check_rate_limiting()
        
        self.assertTrue(result)
        # Verify request was recorded
        self.mock_rate_limiter.record_request.assert_called_once()

    @patch('WeatherDashboard.core.controller.config')
    def test_get_chart_settings_empty_city(self, mock_config):
        """Test chart settings retrieval with empty city name."""
        # Configure state to return empty city
        self.mock_state.get_current_city.return_value = ""
        
        # Mock config
        mock_config.ERROR_MESSAGES = {"missing": "{field} is required for chart display"}
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.controller._get_chart_settings()
        
        self.assertIn("City name is required", str(context.exception))

    def test_get_chart_settings_invalid_range(self):
        """Test chart settings retrieval with invalid date range."""
        # Configure mocks
        self.mock_state.get_current_city.return_value = "New York"
        self.mock_state.get_current_range.return_value = "Invalid Range"
        self.mock_state.get_current_chart_metric.return_value = "Temperature"
        
        with patch('WeatherDashboard.core.controller.config') as mock_config:
            mock_config.CHART = {"range_options": {"Last 7 Days": 7}}
            mock_config.METRICS = {"temperature": {"label": "Temperature"}}
            
            # Mock ValidationUtils
            with patch('WeatherDashboard.core.controller.ValidationUtils') as mock_validation_utils:
                mock_validation_utils.validate_city_name.return_value = []
                mock_validation_utils.validate_unit_system.return_value = []
                
                # Should handle gracefully (get() returns None, defaults to 7)
                city, days, metric_key, unit = self.controller._get_chart_settings()
                self.assertEqual(days, 7)  # Default fallback

    def test_error_handler_integration(self):
        """Test integration with error handler for different error types."""
        # Test different error scenarios
        test_cases = [
            (ValidationError("Invalid input"), False),
            (CityNotFoundError("City not found"), True),
            (RateLimitError("Rate limited"), True),
            (NetworkError("Network error"), True),
        ]
        
        for error, expected_continue in test_cases:
            with self.subTest(error=error.__class__.__name__):
                result = self.controller.error_handler.handle_weather_error(error, "TestCity")
                self.assertEqual(result, expected_continue)


if __name__ == '__main__':
    unittest.main()