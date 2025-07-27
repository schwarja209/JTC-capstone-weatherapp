"""
Tests for the main window application class.

This module tests the WeatherDashboardMain class including dependency injection,
initialization, event handling, and async operation management.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from tkinter import Tk

from WeatherDashboard.gui.main_window import WeatherDashboardMain
from WeatherDashboard.core.data_manager import WeatherDataManager
from WeatherDashboard.core.data_service import WeatherDataService
from WeatherDashboard.gui.loading_states import LoadingStateManager, AsyncWeatherOperation


class TestWeatherDashboardMain(unittest.TestCase):
    """Test cases for the main window application."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_root = Mock(spec=Tk)
        
        # Create mock dependencies
        self.mock_data_manager = Mock(spec=WeatherDataManager)
        self.mock_data_service = Mock(spec=WeatherDataService)
        self.mock_loading_manager = Mock(spec=LoadingStateManager)
        self.mock_async_operations = Mock(spec=AsyncWeatherOperation)
        
        # Mock widget creation
        with patch('WeatherDashboard.gui.main_window.WeatherDashboardGUIFrames') as mock_frames, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardWidgets') as mock_widgets, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardController') as mock_controller:
            
            # Configure mock frames
            mock_frames_instance = Mock()
            mock_frames_instance.frames = {'main': Mock(), 'status': Mock()}
            mock_frames.return_value = mock_frames_instance
            
            # Configure mock widgets
            mock_widgets_instance = Mock()
            mock_widgets_instance.is_ready.return_value = True
            mock_widgets_instance.get_creation_error.return_value = None
            mock_widgets_instance.metric_widgets = Mock()
            mock_widgets_instance.status_bar_widgets = Mock()
            mock_widgets_instance.control_widgets = Mock()
            mock_widgets.return_value = mock_widgets_instance
            
            # Configure mock controller
            mock_controller_instance = Mock()
            mock_controller.return_value = mock_controller_instance
            
            # Create main window with injected dependencies
            self.main_window = WeatherDashboardMain(
                root=self.mock_root,
                data_manager=self.mock_data_manager,
                data_service=self.mock_data_service,
                loading_manager=self.mock_loading_manager,
                async_operations=self.mock_async_operations
            )
    
    def test_dependency_injection(self):
        """Test that dependencies are properly injected."""
        self.assertEqual(self.main_window.data_manager, self.mock_data_manager)
        self.assertEqual(self.main_window.service, self.mock_data_service)
        self.assertEqual(self.main_window.loading_manager, self.mock_loading_manager)
        self.assertEqual(self.main_window.async_operations, self.mock_async_operations)
    
    def test_default_dependency_creation(self):
        """Test that default dependencies are created when not injected."""
        with patch('WeatherDashboard.gui.main_window.WeatherDashboardGUIFrames') as mock_frames, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardWidgets') as mock_widgets, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardController') as mock_controller, \
             patch('WeatherDashboard.gui.main_window.WeatherDataManager') as mock_dm_class, \
             patch('WeatherDashboard.gui.main_window.WeatherDataService') as mock_ds_class, \
             patch('WeatherDashboard.gui.main_window.LoadingStateManager') as mock_lm_class, \
             patch('WeatherDashboard.gui.main_window.AsyncWeatherOperation') as mock_ao_class:
            
            # Configure mocks
            mock_frames_instance = Mock()
            mock_frames_instance.frames = {'main': Mock(), 'status': Mock()}
            mock_frames.return_value = mock_frames_instance
            
            mock_widgets_instance = Mock()
            mock_widgets_instance.is_ready.return_value = True
            mock_widgets_instance.metric_widgets = Mock()
            mock_widgets_instance.status_bar_widgets = Mock()
            mock_widgets_instance.control_widgets = Mock()
            mock_widgets.return_value = mock_widgets_instance
            
            mock_controller_instance = Mock()
            mock_controller.return_value = mock_controller_instance
            
            mock_dm_instance = Mock()
            mock_dm_class.return_value = mock_dm_instance
            
            mock_ds_instance = Mock()
            mock_ds_class.return_value = mock_ds_instance
            
            mock_lm_instance = Mock()
            mock_lm_class.return_value = mock_lm_instance
            
            mock_ao_instance = Mock()
            mock_ao_class.return_value = mock_ao_instance
            
            # Create main window without injected dependencies
            main_window = WeatherDashboardMain(root=self.mock_root)
            
            # Verify default instances were created
            mock_dm_class.assert_called_once()
            mock_ds_class.assert_called_once_with(mock_dm_instance)
            mock_lm_class.assert_called_once()
            mock_ao_class.assert_called_once()
    
    def test_ui_handler_methods(self):
        """Test UI handler methods work correctly."""
        # Test show_info
        with patch('WeatherDashboard.gui.main_window.messagebox') as mock_messagebox:
            self.main_window.show_info("Test Title", "Test Message")
            mock_messagebox.showinfo.assert_called_once_with("Test Title", "Test Message")
        
        # Test show_warning
        with patch('WeatherDashboard.gui.main_window.messagebox') as mock_messagebox:
            self.main_window.show_warning("Test Title", "Test Message")
            mock_messagebox.showwarning.assert_called_once_with("Test Title", "Test Message")
        
        # Test show_error
        with patch('WeatherDashboard.gui.main_window.messagebox') as mock_messagebox:
            self.main_window.show_error("Test Title", "Test Message")
            mock_messagebox.showerror.assert_called_once_with("Test Title", "Test Message")
    
    def test_update_chart_components(self):
        """Test chart components update method."""
        # Test chart update
        self.main_window.update_chart_components(
            x_vals=['2024-01-01', '2024-01-02'],
            y_vals=[25.0, 26.0],
            metric_key='temperature',
            city='New York',
            unit='metric'
        )
        
        # Verify chart display was updated
        self.main_window.widgets.update_chart_display.assert_called_once_with(
            ['2024-01-01', '2024-01-02'],
            [25.0, 26.0],
            'temperature',
            'New York',
            'metric',
            True
        )
        
        # Verify dropdown was updated
        self.main_window.widgets.control_widgets.update_chart_dropdown_options.assert_called_once()
        
        # Test chart clear
        self.main_window.update_chart_components(clear=True)
        self.main_window.widgets.clear_chart_with_error_message.assert_called_once()


if __name__ == '__main__':
    unittest.main()