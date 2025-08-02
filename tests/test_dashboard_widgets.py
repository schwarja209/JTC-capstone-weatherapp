"""
Unit tests for WeatherDashboardWidgets class.

Tests dashboard widget management functionality including:
- Widget creation and initialization
- Metric widget management
- Status bar widget management
- Control widget management
- Widget state management
- Error handling and recovery
- Integration with base widget manager
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import tkinter as tk
from tkinter import ttk

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WeatherDashboard.widgets.dashboard_widgets import WeatherDashboardWidgets


class TestWeatherDashboardWidgets(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.mock_parent = Mock(spec=tk.Frame)
        self.mock_parent.configure.return_value = None
        self.mock_parent.grid.return_value = None
        self.mock_parent.pack.return_value = None
        
        # Create a real Tkinter root for some tests
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        
        # Mock the widget creation methods
        with patch('WeatherDashboard.widgets.dashboard_widgets.MetricDisplayWidgets') as mock_metric_widgets, \
             patch('WeatherDashboard.widgets.dashboard_widgets.StatusBarWidgets') as mock_status_widgets, \
             patch('WeatherDashboard.widgets.dashboard_widgets.ControlWidgets') as mock_control_widgets:
            
            # Configure mock widget classes
            mock_metric_widgets_instance = Mock()
            mock_metric_widgets_instance.is_ready.return_value = True
            mock_metric_widgets_instance.get_creation_error.return_value = None
            mock_metric_widgets.return_value = mock_metric_widgets_instance
            
            mock_status_widgets_instance = Mock()
            mock_status_widgets_instance.is_ready.return_value = True
            mock_status_widgets_instance.get_creation_error.return_value = None
            mock_status_widgets.return_value = mock_status_widgets_instance
            
            mock_control_widgets_instance = Mock()
            mock_control_widgets_instance.is_ready.return_value = True
            mock_control_widgets_instance.get_creation_error.return_value = None
            mock_control_widgets.return_value = mock_control_widgets_instance
            
            self.dashboard_widgets = WeatherDashboardWidgets(self.frame)

    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self, 'root'):
            self.root.destroy()

    def test_initialization(self):
        """Test WeatherDashboardWidgets initializes correctly."""
        self.assertEqual(self.dashboard_widgets.parent, self.frame)
        self.assertIsNotNone(self.dashboard_widgets.metric_widgets)
        self.assertIsNotNone(self.dashboard_widgets.status_bar_widgets)
        self.assertIsNotNone(self.dashboard_widgets.control_widgets)

    def test_is_ready_all_widgets_ready(self):
        """Test is_ready when all widget components are ready."""
        # Mock all widgets to be ready
        self.dashboard_widgets.metric_widgets.is_ready.return_value = True
        self.dashboard_widgets.status_bar_widgets.is_ready.return_value = True
        self.dashboard_widgets.control_widgets.is_ready.return_value = True
        
        result = self.dashboard_widgets.is_ready()
        self.assertTrue(result)

    def test_is_ready_metric_widgets_not_ready(self):
        """Test is_ready when metric widgets are not ready."""
        self.dashboard_widgets.metric_widgets.is_ready.return_value = False
        self.dashboard_widgets.status_bar_widgets.is_ready.return_value = True
        self.dashboard_widgets.control_widgets.is_ready.return_value = True
        
        result = self.dashboard_widgets.is_ready()
        self.assertFalse(result)

    def test_is_ready_status_widgets_not_ready(self):
        """Test is_ready when status widgets are not ready."""
        self.dashboard_widgets.metric_widgets.is_ready.return_value = True
        self.dashboard_widgets.status_bar_widgets.is_ready.return_value = False
        self.dashboard_widgets.control_widgets.is_ready.return_value = True
        
        result = self.dashboard_widgets.is_ready()
        self.assertFalse(result)

    def test_is_ready_control_widgets_not_ready(self):
        """Test is_ready when control widgets are not ready."""
        self.dashboard_widgets.metric_widgets.is_ready.return_value = True
        self.dashboard_widgets.status_bar_widgets.is_ready.return_value = True
        self.dashboard_widgets.control_widgets.is_ready.return_value = False
        
        result = self.dashboard_widgets.is_ready()
        self.assertFalse(result)

    def test_get_creation_error_no_errors(self):
        """Test get_creation_error when no errors exist."""
        self.dashboard_widgets.metric_widgets.get_creation_error.return_value = None
        self.dashboard_widgets.status_bar_widgets.get_creation_error.return_value = None
        self.dashboard_widgets.control_widgets.get_creation_error.return_value = None
        
        result = self.dashboard_widgets.get_creation_error()
        self.assertIsNone(result)

    def test_get_creation_error_metric_widgets_error(self):
        """Test get_creation_error when metric widgets have error."""
        self.dashboard_widgets.metric_widgets.get_creation_error.return_value = "Metric widgets error"
        self.dashboard_widgets.status_bar_widgets.get_creation_error.return_value = None
        self.dashboard_widgets.control_widgets.get_creation_error.return_value = None
        
        result = self.dashboard_widgets.get_creation_error()
        self.assertEqual(result, "Metric widgets error")

    def test_get_creation_error_status_widgets_error(self):
        """Test get_creation_error when status widgets have error."""
        self.dashboard_widgets.metric_widgets.get_creation_error.return_value = None
        self.dashboard_widgets.status_bar_widgets.get_creation_error.return_value = "Status widgets error"
        self.dashboard_widgets.control_widgets.get_creation_error.return_value = None
        
        result = self.dashboard_widgets.get_creation_error()
        self.assertEqual(result, "Status widgets error")

    def test_get_creation_error_control_widgets_error(self):
        """Test get_creation_error when control widgets have error."""
        self.dashboard_widgets.metric_widgets.get_creation_error.return_value = None
        self.dashboard_widgets.status_bar_widgets.get_creation_error.return_value = None
        self.dashboard_widgets.control_widgets.get_creation_error.return_value = "Control widgets error"
        
        result = self.dashboard_widgets.get_creation_error()
        self.assertEqual(result, "Control widgets error")

    def test_get_creation_error_multiple_errors(self):
        """Test get_creation_error when multiple widgets have errors."""
        self.dashboard_widgets.metric_widgets.get_creation_error.return_value = "Metric widgets error"
        self.dashboard_widgets.status_bar_widgets.get_creation_error.return_value = "Status widgets error"
        self.dashboard_widgets.control_widgets.get_creation_error.return_value = "Control widgets error"
        
        result = self.dashboard_widgets.get_creation_error()
        # Should return the first error found (metric widgets)
        self.assertEqual(result, "Metric widgets error")

    def test_get_metric_widgets(self):
        """Test getting metric widgets."""
        result = self.dashboard_widgets.get_metric_widgets()
        self.assertEqual(result, self.dashboard_widgets.metric_widgets)

    def test_get_status_bar_widgets(self):
        """Test getting status bar widgets."""
        result = self.dashboard_widgets.get_status_bar_widgets()
        self.assertEqual(result, self.dashboard_widgets.status_bar_widgets)

    def test_get_control_widgets(self):
        """Test getting control widgets."""
        result = self.dashboard_widgets.get_control_widgets()
        self.assertEqual(result, self.dashboard_widgets.control_widgets)

    def test_update_metric_display(self):
        """Test updating metric display."""
        mock_weather_data = {"temperature": 25, "humidity": 60}
        
        self.dashboard_widgets.update_metric_display(mock_weather_data)
        
        # Verify that metric widgets update method was called
        self.dashboard_widgets.metric_widgets.update_display.assert_called_once_with(mock_weather_data)

    def test_update_status_bar(self):
        """Test updating status bar."""
        mock_status_message = "Weather data updated"
        
        self.dashboard_widgets.update_status_bar(mock_status_message)
        
        # Verify that status bar widgets update method was called
        self.dashboard_widgets.status_bar_widgets.update_status.assert_called_once_with(mock_status_message)

    def test_clear_all_displays(self):
        """Test clearing all displays."""
        self.dashboard_widgets.clear_all_displays()
        
        # Verify that all widget components clear methods were called
        self.dashboard_widgets.metric_widgets.clear_display.assert_called_once()
        self.dashboard_widgets.status_bar_widgets.clear_status.assert_called_once()
        self.dashboard_widgets.control_widgets.clear_controls.assert_called_once()

    def test_apply_theme_to_all_widgets(self):
        """Test applying theme to all widgets."""
        mock_theme = "optimistic"
        
        self.dashboard_widgets.apply_theme_to_all_widgets(mock_theme)
        
        # Verify that all widget components theme methods were called
        self.dashboard_widgets.metric_widgets.apply_theme.assert_called_once_with(mock_theme)
        self.dashboard_widgets.status_bar_widgets.apply_theme.assert_called_once_with(mock_theme)
        self.dashboard_widgets.control_widgets.apply_theme.assert_called_once_with(mock_theme)

    def test_get_widget_state(self):
        """Test getting widget state."""
        # Mock widget state methods
        self.dashboard_widgets.metric_widgets.get_state.return_value = {"metric": "ready"}
        self.dashboard_widgets.status_bar_widgets.get_state.return_value = {"status": "ready"}
        self.dashboard_widgets.control_widgets.get_state.return_value = {"control": "ready"}
        
        state = self.dashboard_widgets.get_widget_state()
        
        expected_state = {
            "metric_widgets": {"metric": "ready"},
            "status_bar_widgets": {"status": "ready"},
            "control_widgets": {"control": "ready"}
        }
        self.assertEqual(state, expected_state)

    def test_restore_widget_state(self):
        """Test restoring widget state."""
        mock_state = {
            "metric_widgets": {"metric": "restored"},
            "status_bar_widgets": {"status": "restored"},
            "control_widgets": {"control": "restored"}
        }
        
        self.dashboard_widgets.restore_widget_state(mock_state)
        
        # Verify that all widget components restore methods were called
        self.dashboard_widgets.metric_widgets.restore_state.assert_called_once_with({"metric": "restored"})
        self.dashboard_widgets.status_bar_widgets.restore_state.assert_called_once_with({"status": "restored"})
        self.dashboard_widgets.control_widgets.restore_state.assert_called_once_with({"control": "restored"})

    def test_validate_widget_integrity(self):
        """Test validating widget integrity."""
        # Mock all widgets to be valid
        self.dashboard_widgets.metric_widgets.validate_integrity.return_value = True
        self.dashboard_widgets.status_bar_widgets.validate_integrity.return_value = True
        self.dashboard_widgets.control_widgets.validate_integrity.return_value = True
        
        result = self.dashboard_widgets.validate_widget_integrity()
        self.assertTrue(result)

    def test_validate_widget_integrity_failure(self):
        """Test validating widget integrity when one component fails."""
        self.dashboard_widgets.metric_widgets.validate_integrity.return_value = True
        self.dashboard_widgets.status_bar_widgets.validate_integrity.return_value = False
        self.dashboard_widgets.control_widgets.validate_integrity.return_value = True
        
        result = self.dashboard_widgets.validate_widget_integrity()
        self.assertFalse(result)

    def test_get_widget_memory_usage(self):
        """Test getting widget memory usage."""
        # Mock memory usage methods
        self.dashboard_widgets.metric_widgets.get_memory_usage.return_value = 1024
        self.dashboard_widgets.status_bar_widgets.get_memory_usage.return_value = 512
        self.dashboard_widgets.control_widgets.get_memory_usage.return_value = 256
        
        memory_usage = self.dashboard_widgets.get_widget_memory_usage()
        
        expected_usage = {
            "metric_widgets": 1024,
            "status_bar_widgets": 512,
            "control_widgets": 256,
            "total": 1792
        }
        self.assertEqual(memory_usage, expected_usage)

    def test_cleanup_widgets(self):
        """Test cleaning up widgets."""
        self.dashboard_widgets.cleanup_widgets()
        
        # Verify that all widget components cleanup methods were called
        self.dashboard_widgets.metric_widgets.cleanup.assert_called_once()
        self.dashboard_widgets.status_bar_widgets.cleanup.assert_called_once()
        self.dashboard_widgets.control_widgets.cleanup.assert_called_once()


if __name__ == '__main__':
    unittest.main() 