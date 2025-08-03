"""
Unit tests for WeatherDashboardWidgets class.

Tests widget coordination functionality including:
- Widget initialization and creation
- Error handling during widget creation
- Widget state management
- Update delegation to sub-widgets
- Widget registry operations
- Style application and widget movement
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
        # Create mock frames
        self.root = tk.Tk()
        self.frame = ttk.Frame(self.root)
        self.frames = {
            'title': ttk.Frame(self.frame),
            'control': ttk.Frame(self.frame),
            'tabbed': ttk.Frame(self.frame),
            'status': ttk.Frame(self.frame)
        }
        
        # Create mock state and callbacks
        self.mock_state = Mock()
        self.mock_update_cb = Mock()
        self.mock_clear_cb = Mock()
        self.mock_dropdown_cb = Mock()
        self.mock_cancel_cb = Mock()
        self.mock_scheduler_cb = Mock()
        self.mock_theme_cb = Mock()
        
        # Create dashboard widgets instance
        self.dashboard_widgets = WeatherDashboardWidgets(
            frames=self.frames,
            state=self.mock_state,
            update_cb=self.mock_update_cb,
            clear_cb=self.mock_clear_cb,
            dropdown_cb=self.mock_dropdown_cb,
            cancel_cb=self.mock_cancel_cb,
            scheduler_cb=self.mock_scheduler_cb,
            theme_cb=self.mock_theme_cb
        )

    def tearDown(self):
        """Clean up test fixtures."""
        self.root.destroy()

    def test_initialization(self):
        """Test WeatherDashboardWidgets initializes correctly."""
        self.assertEqual(self.dashboard_widgets.frames, self.frames)
        self.assertEqual(self.dashboard_widgets.state, self.mock_state)
        self.assertEqual(self.dashboard_widgets.callbacks['update'], self.mock_update_cb)
        self.assertEqual(self.dashboard_widgets.callbacks['reset'], self.mock_clear_cb)
        self.assertEqual(self.dashboard_widgets.callbacks['dropdown_update'], self.mock_dropdown_cb)
        self.assertEqual(self.dashboard_widgets.callbacks['cancel'], self.mock_cancel_cb)
        self.assertEqual(self.dashboard_widgets.scheduler_callback, self.mock_scheduler_cb)
        self.assertEqual(self.dashboard_widgets.theme_callback, self.mock_theme_cb)

    def test_is_ready_all_widgets_ready(self):
        """Test is_ready returns True when all widgets are ready."""
        # Mock the sub-widgets to be ready
        mock_metric_widgets = Mock()
        mock_metric_widgets.is_ready.return_value = True
        self.dashboard_widgets.tabbed_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets.get_metric_widgets.return_value = mock_metric_widgets
        
        self.dashboard_widgets.status_bar_widgets = Mock()
        self.dashboard_widgets.status_bar_widgets.is_ready.return_value = True
        
        mock_chart_widgets = Mock()
        mock_chart_widgets.is_ready.return_value = True
        self.dashboard_widgets.tabbed_widgets.get_chart_widgets.return_value = mock_chart_widgets
        
        self.dashboard_widgets.control_widgets = Mock()
        self.dashboard_widgets.control_widgets.is_ready.return_value = True
        
        result = self.dashboard_widgets.is_ready()
        self.assertTrue(result)

    def test_is_ready_metric_widgets_not_ready(self):
        """Test is_ready returns False when metric widgets are not ready."""
        mock_metric_widgets = Mock()
        mock_metric_widgets.is_ready.return_value = False
        self.dashboard_widgets.tabbed_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets.get_metric_widgets.return_value = mock_metric_widgets
        
        self.dashboard_widgets.status_bar_widgets = Mock()
        self.dashboard_widgets.status_bar_widgets.is_ready.return_value = True
        
        mock_chart_widgets = Mock()
        mock_chart_widgets.is_ready.return_value = True
        self.dashboard_widgets.tabbed_widgets.get_chart_widgets.return_value = mock_chart_widgets
        
        self.dashboard_widgets.control_widgets = Mock()
        self.dashboard_widgets.control_widgets.is_ready.return_value = True
        
        result = self.dashboard_widgets.is_ready()
        self.assertFalse(result)

    def test_is_ready_status_widgets_not_ready(self):
        """Test is_ready returns False when status widgets are not ready."""
        mock_metric_widgets = Mock()
        mock_metric_widgets.is_ready.return_value = True
        self.dashboard_widgets.tabbed_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets.get_metric_widgets.return_value = mock_metric_widgets
        
        self.dashboard_widgets.status_bar_widgets = Mock()
        self.dashboard_widgets.status_bar_widgets.is_ready.return_value = False
        
        mock_chart_widgets = Mock()
        mock_chart_widgets.is_ready.return_value = True
        self.dashboard_widgets.tabbed_widgets.get_chart_widgets.return_value = mock_chart_widgets
        
        self.dashboard_widgets.control_widgets = Mock()
        self.dashboard_widgets.control_widgets.is_ready.return_value = True
        
        result = self.dashboard_widgets.is_ready()
        self.assertFalse(result)

    def test_is_ready_control_widgets_not_ready(self):
        """Test is_ready returns False when control widgets are not ready."""
        mock_metric_widgets = Mock()
        mock_metric_widgets.is_ready.return_value = True
        self.dashboard_widgets.tabbed_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets.get_metric_widgets.return_value = mock_metric_widgets
        
        self.dashboard_widgets.status_bar_widgets = Mock()
        self.dashboard_widgets.status_bar_widgets.is_ready.return_value = True
        
        mock_chart_widgets = Mock()
        mock_chart_widgets.is_ready.return_value = True
        self.dashboard_widgets.tabbed_widgets.get_chart_widgets.return_value = mock_chart_widgets
        
        self.dashboard_widgets.control_widgets = Mock()
        self.dashboard_widgets.control_widgets.is_ready.return_value = False
        
        result = self.dashboard_widgets.is_ready()
        self.assertFalse(result)

    def test_get_creation_error_no_errors(self):
        """Test get_creation_error returns None when no errors."""
        mock_metric_widgets = Mock()
        mock_metric_widgets.get_creation_error.return_value = None
        self.dashboard_widgets.tabbed_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets.get_metric_widgets.return_value = mock_metric_widgets
        
        self.dashboard_widgets.status_bar_widgets = Mock()
        self.dashboard_widgets.status_bar_widgets.get_creation_error.return_value = None
        
        mock_chart_widgets = Mock()
        mock_chart_widgets.get_creation_error.return_value = None
        self.dashboard_widgets.tabbed_widgets.get_chart_widgets.return_value = mock_chart_widgets
        
        self.dashboard_widgets.control_widgets = Mock()
        self.dashboard_widgets.control_widgets.get_creation_error.return_value = None
        
        result = self.dashboard_widgets.get_creation_error()
        self.assertIsNone(result)

    def test_get_creation_error_metric_widgets_error(self):
        """Test get_creation_error returns error from metric widgets."""
        mock_metric_widgets = Mock()
        mock_metric_widgets.get_creation_error.return_value = "Metric widgets error"
        self.dashboard_widgets.tabbed_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets.get_metric_widgets.return_value = mock_metric_widgets
        
        self.dashboard_widgets.status_bar_widgets = Mock()
        self.dashboard_widgets.status_bar_widgets.get_creation_error.return_value = None
        
        mock_chart_widgets = Mock()
        mock_chart_widgets.get_creation_error.return_value = None
        self.dashboard_widgets.tabbed_widgets.get_chart_widgets.return_value = mock_chart_widgets
        
        self.dashboard_widgets.control_widgets = Mock()
        self.dashboard_widgets.control_widgets.get_creation_error.return_value = None
        
        result = self.dashboard_widgets.get_creation_error()
        self.assertEqual(result, "Metric widgets error")

    def test_get_creation_error_status_widgets_error(self):
        """Test get_creation_error returns error from status widgets."""
        mock_metric_widgets = Mock()
        mock_metric_widgets.get_creation_error.return_value = None
        self.dashboard_widgets.tabbed_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets.get_metric_widgets.return_value = mock_metric_widgets
        
        self.dashboard_widgets.status_bar_widgets = Mock()
        self.dashboard_widgets.status_bar_widgets.get_creation_error.return_value = "Status widgets error"
        
        mock_chart_widgets = Mock()
        mock_chart_widgets.get_creation_error.return_value = None
        self.dashboard_widgets.tabbed_widgets.get_chart_widgets.return_value = mock_chart_widgets
        
        self.dashboard_widgets.control_widgets = Mock()
        self.dashboard_widgets.control_widgets.get_creation_error.return_value = None
        
        result = self.dashboard_widgets.get_creation_error()
        self.assertEqual(result, "Status widgets error")

    def test_get_creation_error_control_widgets_error(self):
        """Test get_creation_error returns error from control widgets."""
        mock_metric_widgets = Mock()
        mock_metric_widgets.get_creation_error.return_value = None
        self.dashboard_widgets.tabbed_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets.get_metric_widgets.return_value = mock_metric_widgets
        
        self.dashboard_widgets.status_bar_widgets = Mock()
        self.dashboard_widgets.status_bar_widgets.get_creation_error.return_value = None
        
        mock_chart_widgets = Mock()
        mock_chart_widgets.get_creation_error.return_value = None
        self.dashboard_widgets.tabbed_widgets.get_chart_widgets.return_value = mock_chart_widgets
        
        self.dashboard_widgets.control_widgets = Mock()
        self.dashboard_widgets.control_widgets.get_creation_error.return_value = "Control widgets error"
        
        result = self.dashboard_widgets.get_creation_error()
        self.assertEqual(result, "Control widgets error")

    def test_get_creation_error_multiple_errors(self):
        """Test get_creation_error returns first error found."""
        mock_metric_widgets = Mock()
        mock_metric_widgets.get_creation_error.return_value = "Metric widgets error"
        self.dashboard_widgets.tabbed_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets.get_metric_widgets.return_value = mock_metric_widgets
        
        self.dashboard_widgets.status_bar_widgets = Mock()
        self.dashboard_widgets.status_bar_widgets.get_creation_error.return_value = "Status widgets error"
        
        mock_chart_widgets = Mock()
        mock_chart_widgets.get_creation_error.return_value = "Chart widgets error"
        self.dashboard_widgets.tabbed_widgets.get_chart_widgets.return_value = mock_chart_widgets
        
        self.dashboard_widgets.control_widgets = Mock()
        self.dashboard_widgets.control_widgets.get_creation_error.return_value = "Control widgets error"
        
        result = self.dashboard_widgets.get_creation_error()
        self.assertEqual(result, "Metric widgets error")  # First error found

    def test_update_metric_display(self):
        """Test update_metric_display delegates to metric_widgets."""
        mock_weather_data = {"temperature": "25°C", "humidity": "60%"}
        mock_metric_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets.get_metric_widgets.return_value = mock_metric_widgets
        
        self.dashboard_widgets.update_metric_display(mock_weather_data)
        
        mock_metric_widgets.update_metric_display.assert_called_once_with(mock_weather_data)

    def test_update_metric_display_no_metric_widgets(self):
        """Test update_metric_display handles None metric_widgets."""
        mock_weather_data = {"temperature": "25°C", "humidity": "60%"}
        self.dashboard_widgets.tabbed_widgets = None
        
        # Should not raise an exception
        self.dashboard_widgets.update_metric_display(mock_weather_data)

    def test_update_chart_display(self):
        """Test update_chart_display delegates to chart_widgets."""
        x_vals = ["Day 1", "Day 2", "Day 3"]
        y_vals = [25, 26, 24]
        mock_chart_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets.get_chart_widgets.return_value = mock_chart_widgets
        
        self.dashboard_widgets.update_chart_display(x_vals, y_vals, "temperature", "New York", "metric")
        
        mock_chart_widgets.update_chart_display.assert_called_once_with(
            x_vals, y_vals, "temperature", "New York", "metric", False
        )

    def test_clear_chart_with_error_message(self):
        """Test clear_chart_with_error_message delegates to chart_widgets."""
        mock_chart_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets.get_chart_widgets.return_value = mock_chart_widgets
        
        self.dashboard_widgets.clear_chart_with_error_message()
        
        mock_chart_widgets.clear_chart_with_error_message.assert_called_once()

    def test_update_status_bar(self):
        """Test update_status_bar delegates to status_bar_widgets."""
        self.dashboard_widgets.status_bar_widgets = Mock()
        
        self.dashboard_widgets.update_status_bar("New York", None, False)
        
        self.dashboard_widgets.status_bar_widgets.update_status_bar.assert_called_once_with("New York", None, False)

    def test_update_status_bar_with_error(self):
        """Test update_status_bar with error exception."""
        self.dashboard_widgets.status_bar_widgets = Mock()
        error = ValueError("Test error")
        
        self.dashboard_widgets.update_status_bar("New York", error, True)
        
        self.dashboard_widgets.status_bar_widgets.update_status_bar.assert_called_once_with("New York", error, True)

    def test_update_alerts(self):
        """Test update_alerts delegates to metric_widgets."""
        raw_data = {"alerts": [{"type": "warning", "message": "Test alert"}]}
        mock_metric_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets.get_metric_widgets.return_value = mock_metric_widgets
        
        self.dashboard_widgets.update_alerts(raw_data)
        
        mock_metric_widgets.update_alerts.assert_called_once_with(raw_data)

    def test_get_alert_popup_parent(self):
        """Test get_alert_popup_parent delegates to metric_widgets."""
        mock_parent = Mock()
        mock_metric_widgets = Mock()
        mock_metric_widgets.get_alert_popup_parent.return_value = mock_parent
        self.dashboard_widgets.tabbed_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets.get_metric_widgets.return_value = mock_metric_widgets
        
        result = self.dashboard_widgets.get_alert_popup_parent()
        
        self.assertEqual(result, mock_parent)
        mock_metric_widgets.get_alert_popup_parent.assert_called_once()

    def test_get_alert_popup_parent_no_metric_widgets(self):
        """Test get_alert_popup_parent returns None when metric_widgets is None."""
        self.dashboard_widgets.tabbed_widgets = None
        
        result = self.dashboard_widgets.get_alert_popup_parent()
        
        self.assertIsNone(result)

    def test_get_registry(self):
        """Test get_registry returns the widget registry."""
        registry = self.dashboard_widgets.get_registry()
        
        self.assertIsNotNone(registry)
        self.assertEqual(registry, self.dashboard_widgets.widget_registry)

    def test_apply_style_to_widget(self):
        """Test apply_style_to_widget delegates to registry."""
        with patch.object(self.dashboard_widgets.widget_registry, 'apply_style_to_widget') as mock_apply:
            mock_apply.return_value = True
            
            result = self.dashboard_widgets.apply_style_to_widget("test_widget", "test_style")
            
            self.assertTrue(result)
            mock_apply.assert_called_once_with("test_widget", "test_style")

    def test_apply_style_to_type(self):
        """Test apply_style_to_type delegates to registry."""
        with patch.object(self.dashboard_widgets.widget_registry, 'apply_style_to_type') as mock_apply:
            mock_apply.return_value = 5
            
            result = self.dashboard_widgets.apply_style_to_type("test_type", "test_style")
            
            self.assertEqual(result, 5)
            mock_apply.assert_called_once_with("test_type", "test_style")

    def test_move_widget(self):
        """Test move_widget delegates to registry."""
        with patch.object(self.dashboard_widgets.widget_registry, 'move_widget') as mock_move:
            mock_move.return_value = True
            new_position = {"x": 100, "y": 200}
            
            result = self.dashboard_widgets.move_widget("test_widget", "new_frame", new_position)
            
            self.assertTrue(result)
            mock_move.assert_called_once_with("test_widget", "new_frame", new_position)

    def test_show_widget(self):
        """Test show_widget delegates to registry."""
        with patch.object(self.dashboard_widgets.widget_registry, 'show_widget') as mock_show:
            mock_show.return_value = True
            
            result = self.dashboard_widgets.show_widget("test_widget")
            
            self.assertTrue(result)
            mock_show.assert_called_once_with("test_widget")

    def test_hide_widget(self):
        """Test hide_widget delegates to registry."""
        with patch.object(self.dashboard_widgets.widget_registry, 'hide_widget') as mock_hide:
            mock_hide.return_value = True
            
            result = self.dashboard_widgets.hide_widget("test_widget")
            
            self.assertTrue(result)
            mock_hide.assert_called_once_with("test_widget")

    def test_metric_widgets_property(self):
        """Test metric_widgets property returns from tabbed_widgets."""
        mock_metric_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets.get_metric_widgets.return_value = mock_metric_widgets
        
        result = self.dashboard_widgets.metric_widgets
        
        self.assertEqual(result, mock_metric_widgets)
        self.dashboard_widgets.tabbed_widgets.get_metric_widgets.assert_called_once()

    def test_metric_widgets_property_no_tabbed_widgets(self):
        """Test metric_widgets property returns None when tabbed_widgets is None."""
        self.dashboard_widgets.tabbed_widgets = None
        
        result = self.dashboard_widgets.metric_widgets
        
        self.assertIsNone(result)

    def test_chart_widgets_property(self):
        """Test chart_widgets property returns from tabbed_widgets."""
        mock_chart_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets = Mock()
        self.dashboard_widgets.tabbed_widgets.get_chart_widgets.return_value = mock_chart_widgets
        
        result = self.dashboard_widgets.chart_widgets
        
        self.assertEqual(result, mock_chart_widgets)
        self.dashboard_widgets.tabbed_widgets.get_chart_widgets.assert_called_once()

    def test_chart_widgets_property_no_tabbed_widgets(self):
        """Test chart_widgets property returns None when tabbed_widgets is None."""
        self.dashboard_widgets.tabbed_widgets = None
        
        result = self.dashboard_widgets.chart_widgets
        
        self.assertIsNone(result) 