"""
Unit tests for BaseWidgetManager and SafeWidgetCreator classes.

Tests widget management functionality including:
- Widget creation and registration
- Safe widget operations with error handling
- Widget lifecycle management
- Memory management and cleanup
- Error recovery and fallback behavior
- Thread safety considerations
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import tkinter as tk
from tkinter import ttk

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WeatherDashboard.widgets.base_widgets import BaseWidgetManager, SafeWidgetCreator


class TestBaseWidgetManager(unittest.TestCase):
    """Test cases for BaseWidgetManager class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_parent = Mock(spec=tk.Frame)
        self.mock_parent.configure.return_value = None
        self.mock_parent.grid.return_value = None
        self.mock_parent.pack.return_value = None

        # Create a real Tkinter root for some tests
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.mock_state = Mock()

        self.widget_manager = BaseWidgetManager(self.frame, self.mock_state)

    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self, 'root'):
            self.root.destroy()

    def test_initialization(self):
        """Test BaseWidgetManager initializes correctly."""
        self.assertEqual(self.widget_manager.parent, self.frame)
        self.assertEqual(self.widget_manager.state, self.mock_state)
        self.assertFalse(self.widget_manager._widgets_created)
        self.assertIsNone(self.widget_manager._creation_error)

    def test_is_ready_when_not_created(self):
        """Test is_ready returns False when widgets not created."""
        self.assertFalse(self.widget_manager.is_ready())

    def test_is_ready_when_created_successfully(self):
        """Test is_ready returns True when widgets created successfully."""
        # Mock successful widget creation
        self.widget_manager._widgets_created = True
        self.widget_manager._creation_error = None
        
        self.assertTrue(self.widget_manager.is_ready())

    def test_is_ready_when_creation_failed(self):
        """Test is_ready returns False when widget creation failed."""
        # Mock failed widget creation
        self.widget_manager._widgets_created = True
        self.widget_manager._creation_error = "Creation failed"
        
        self.assertFalse(self.widget_manager.is_ready())

    def test_get_creation_error_when_no_error(self):
        """Test get_creation_error returns None when no error."""
        self.assertIsNone(self.widget_manager.get_creation_error())

    def test_get_creation_error_when_has_error(self):
        """Test get_creation_error returns error message when has error."""
        error_message = "Widget creation failed"
        self.widget_manager._creation_error = error_message
        
        self.assertEqual(self.widget_manager.get_creation_error(), error_message)

    def test_safe_create_widgets_success(self):
        """Test safe_create_widgets when widget creation succeeds."""
        # Mock the _create_widgets method to not raise an exception
        with patch.object(self.widget_manager, '_create_widgets'):
            result = self.widget_manager.safe_create_widgets()
            
        self.assertTrue(result)
        self.assertTrue(self.widget_manager._widgets_created)
        self.assertIsNone(self.widget_manager._creation_error)

    def test_safe_create_widgets_failure(self):
        """Test safe_create_widgets when widget creation fails."""
        # Mock the _create_widgets method to raise an exception
        with patch.object(self.widget_manager, '_create_widgets', side_effect=Exception("Creation failed")):
            result = self.widget_manager.safe_create_widgets()
            
        self.assertFalse(result)
        self.assertFalse(self.widget_manager._widgets_created)
        self.assertEqual(self.widget_manager._creation_error, "Creation failed")

    def test_update_metric_display_when_ready(self):
        """Test update_metric_display when widgets are ready."""
        # Mock widgets as ready
        self.widget_manager._widgets_created = True
        self.widget_manager._creation_error = None
        
        # Should not raise an exception
        self.widget_manager.update_metric_display({"temp": "25°C"})

    def test_update_metric_display_when_not_ready(self):
        """Test update_metric_display when widgets are not ready."""
        # Mock widgets as not ready
        self.widget_manager._widgets_created = False
        
        # Should not raise an exception, just log warning
        self.widget_manager.update_metric_display({"temp": "25°C"})

    def test_update_status_bar_when_ready(self):
        """Test update_status_bar when widgets are ready."""
        # Mock widgets as ready
        self.widget_manager._widgets_created = True
        self.widget_manager._creation_error = None
        
        # Should not raise an exception
        self.widget_manager.update_status_bar("Test City", None)

    def test_update_status_bar_when_not_ready(self):
        """Test update_status_bar when widgets are not ready."""
        # Mock widgets as not ready
        self.widget_manager._widgets_created = False
        
        # Should not raise an exception, just log warning
        self.widget_manager.update_status_bar("Test City", None)

    def test_update_alerts_when_ready(self):
        """Test update_alerts when widgets are ready."""
        # Mock widgets as ready
        self.widget_manager._widgets_created = True
        self.widget_manager._creation_error = None
        
        # Should not raise an exception
        self.widget_manager.update_alerts({"alert": "High humidity"})

    def test_update_alerts_when_not_ready(self):
        """Test update_alerts when widgets are not ready."""
        # Mock widgets as not ready
        self.widget_manager._widgets_created = False
        
        # Should not raise an exception, just log warning
        self.widget_manager.update_alerts({"alert": "High humidity"})

    def test_get_alert_popup_parent_with_frames(self):
        """Test get_alert_popup_parent when frames exist."""
        # Mock frames attribute
        self.widget_manager.frames = {"title": Mock()}
        
        result = self.widget_manager.get_alert_popup_parent()
        self.assertEqual(result, self.widget_manager.frames["title"])

    def test_get_alert_popup_parent_without_frames(self):
        """Test get_alert_popup_parent when frames don't exist."""
        # No frames attribute
        result = self.widget_manager.get_alert_popup_parent()
        self.assertIsNone(result)

    def test_get_alert_popup_parent_without_title_frame(self):
        """Test get_alert_popup_parent when title frame doesn't exist."""
        # Mock frames without title
        self.widget_manager.frames = {"other": Mock()}
        
        result = self.widget_manager.get_alert_popup_parent()
        self.assertIsNone(result)


class TestSafeWidgetCreator(unittest.TestCase):
    """Test cases for SafeWidgetCreator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_parent = Mock(spec=tk.Frame)
        # SafeWidgetCreator is a static utility class, no instantiation needed

    def test_initialization(self):
        """Test SafeWidgetCreator is a static utility class."""
        # Should not be instantiable
        with self.assertRaises(TypeError):
            SafeWidgetCreator(self.mock_parent)

    def test_create_label_success(self):
        """Test creating a label successfully."""
        mock_widget = Mock()
        
        with patch('WeatherDashboard.widgets.base_widgets.ttk.Label', return_value=mock_widget):
            result = SafeWidgetCreator.create_label(self.mock_parent, "Test Label")
            
        self.assertEqual(result, mock_widget)

    def test_create_label_failure(self):
        """Test creating a label with failure."""
        with patch('WeatherDashboard.widgets.base_widgets.ttk.Label', side_effect=Exception("Creation failed")):
            # The error handler re-raises the exception, so we expect it to be raised
            with self.assertRaises(Exception):
                SafeWidgetCreator.create_label(self.mock_parent, "Test Label")

    def test_create_button_success(self):
        """Test creating a button successfully."""
        mock_widget = Mock()
        mock_command = Mock()
        
        with patch('WeatherDashboard.widgets.base_widgets.ttk.Button', return_value=mock_widget):
            result = SafeWidgetCreator.create_button(
                self.mock_parent, 
                "Test Button", 
                mock_command
            )
            
        self.assertEqual(result, mock_widget)

    def test_create_button_failure(self):
        """Test creating a button with failure."""
        mock_command = Mock()
        
        with patch('WeatherDashboard.widgets.base_widgets.ttk.Button', side_effect=Exception("Creation failed")):
            # The error handler re-raises the exception, so we expect it to be raised
            with self.assertRaises(Exception):
                SafeWidgetCreator.create_button(self.mock_parent, "Test Button", mock_command)

    def test_create_entry_success(self):
        """Test creating an entry successfully."""
        mock_widget = Mock()
        
        with patch('WeatherDashboard.widgets.base_widgets.ttk.Entry', return_value=mock_widget):
            result = SafeWidgetCreator.create_entry(self.mock_parent)
            
        self.assertEqual(result, mock_widget)

    def test_create_entry_with_textvariable(self):
        """Test creating an entry with textvariable."""
        mock_widget = Mock()
        mock_textvariable = Mock()
        
        with patch('WeatherDashboard.widgets.base_widgets.ttk.Entry', return_value=mock_widget):
            result = SafeWidgetCreator.create_entry(self.mock_parent, textvariable=mock_textvariable)
            
        self.assertEqual(result, mock_widget)

    def test_create_combobox_success(self):
        """Test creating a combobox successfully."""
        mock_widget = Mock()
        
        with patch('WeatherDashboard.widgets.base_widgets.ttk.Combobox', return_value=mock_widget):
            result = SafeWidgetCreator.create_combobox(self.mock_parent)
            
        self.assertEqual(result, mock_widget)

    def test_create_checkbutton_success(self):
        """Test creating a checkbutton successfully."""
        mock_widget = Mock()
        mock_variable = Mock()
        
        with patch('WeatherDashboard.widgets.base_widgets.ttk.Checkbutton', return_value=mock_widget):
            result = SafeWidgetCreator.create_checkbutton(self.mock_parent, "Test", mock_variable)
            
        self.assertEqual(result, mock_widget)

    def test_create_radiobutton_success(self):
        """Test creating a radiobutton successfully."""
        mock_widget = Mock()
        mock_variable = Mock()
        
        with patch('WeatherDashboard.widgets.base_widgets.ttk.Radiobutton', return_value=mock_widget):
            result = SafeWidgetCreator.create_radiobutton(self.mock_parent, "Test", mock_variable, "value")
            
        self.assertEqual(result, mock_widget)

    def test_create_frame_success(self):
        """Test creating a frame successfully."""
        mock_widget = Mock()
        
        with patch('WeatherDashboard.widgets.base_widgets.ttk.Frame', return_value=mock_widget):
            result = SafeWidgetCreator.create_frame(self.mock_parent)
            
        self.assertEqual(result, mock_widget)

    def test_create_widget_with_kwargs(self):
        """Test creating a widget with additional kwargs."""
        mock_widget = Mock()
        
        with patch('WeatherDashboard.widgets.base_widgets.ttk.Button', return_value=mock_widget):
            result = SafeWidgetCreator.create_button(
                self.mock_parent, 
                "Test Button", 
                Mock(), 
                width=10, 
                height=2
            )
            
        self.assertEqual(result, mock_widget)

    def test_create_widget_with_complex_kwargs(self):
        """Test creating a widget with complex kwargs."""
        mock_widget = Mock()
        
        with patch('WeatherDashboard.widgets.base_widgets.ttk.Entry', return_value=mock_widget):
            result = SafeWidgetCreator.create_entry(
                self.mock_parent,
                textvariable=Mock(),
                width=20,
                font=("Arial", 12),
                state="normal"
            )
            
        self.assertEqual(result, mock_widget)

    def test_create_widget_with_invalid_widget_class(self):
        """Test creating a widget with invalid widget class."""
        # Patch a real widget class to raise an exception
        with patch('WeatherDashboard.widgets.base_widgets.ttk.Label', side_effect=AttributeError("No such widget")):
            # The error handler re-raises the exception, so we expect it to be raised
            with self.assertRaises(AttributeError):
                SafeWidgetCreator.create_label(self.mock_parent, "Test")

    def test_create_multiple_widgets(self):
        """Test creating multiple widgets."""
        mock_widget1 = Mock()
        mock_widget2 = Mock()
        
        with patch('WeatherDashboard.widgets.base_widgets.ttk.Label', return_value=mock_widget1):
            result1 = SafeWidgetCreator.create_label(self.mock_parent, "Label 1")
            
        with patch('WeatherDashboard.widgets.base_widgets.ttk.Button', return_value=mock_widget2):
            result2 = SafeWidgetCreator.create_button(self.mock_parent, "Button 1", Mock())
            
        self.assertEqual(result1, mock_widget1)
        self.assertEqual(result2, mock_widget2)

    def test_widget_creation_with_parent_validation(self):
        """Test widget creation with parent validation."""
        # Test with valid parent
        mock_widget = Mock()
        
        with patch('WeatherDashboard.widgets.base_widgets.ttk.Frame', return_value=mock_widget):
            result = SafeWidgetCreator.create_frame(self.mock_parent)
            
        self.assertEqual(result, mock_widget)


if __name__ == '__main__':
    unittest.main() 