"""
Unit tests for WeatherDashboard.gui.main_window module.

Tests main window functionality including:
- Window initialization and setup
- Widget management and integration
- Error handling and recovery
- Performance characteristics
"""

import unittest
from unittest.mock import Mock, patch
import tkinter as tk

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WeatherDashboard.gui.main_window import WeatherDashboardMain


class TestMainWindow(unittest.TestCase):
    """Test MainWindow functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock root window with proper screen size methods
        self.mock_root = Mock(spec=tk.Tk)
        self.mock_root.winfo_screenwidth.return_value = 1200
        self.mock_root.winfo_screenheight.return_value = 800
        
        # Create mock data manager
        self.mock_data_manager = Mock()
        self.mock_data_manager.history_service = Mock()
        
        # Create mock data service
        self.mock_data_service = Mock()
        
        # Create mock loading manager
        self.mock_loading_manager = Mock()
        
        # Create mock async operations
        self.mock_async_operations = Mock()
        
        # Create mock state manager to avoid Tkinter issues
        self.mock_state_manager = Mock()
        self.mock_state_manager.city = Mock()
        self.mock_state_manager.city.get.return_value = "New York"
        self.mock_state_manager.city.set = Mock()

    def test_initialization(self):
        """Test main window initialization."""
        # Test that main window can be created
        with patch('WeatherDashboard.gui.main_window.WeatherDashboardGUIFrames') as mock_frames, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardWidgets') as mock_widgets, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardController') as mock_controller:
            
            # Configure mocks
            mock_frames_instance = Mock()
            mock_frames_instance.frames = {'main': Mock(), 'status': Mock()}
            mock_frames.return_value = mock_frames_instance
            
            mock_widgets_instance = Mock()
            mock_widgets_instance.metric_widgets = Mock()
            mock_widgets_instance.status_bar_widgets = Mock()
            mock_widgets_instance.control_widgets = Mock()
            mock_widgets.return_value = mock_widgets_instance
            
            mock_controller_instance = Mock()
            mock_controller.return_value = mock_controller_instance
            
            # Create main window with mocked state manager
            main_window = WeatherDashboardMain(
                root=self.mock_root,
                data_manager=self.mock_data_manager,
                data_service=self.mock_data_service,
                loading_manager=self.mock_loading_manager,
                async_operations=self.mock_async_operations,
                state_manager=self.mock_state_manager
            )
            
            # Verify main window was created
            self.assertIsNotNone(main_window)

    def test_window_setup(self):
        """Test window setup and configuration."""
        with patch('WeatherDashboard.gui.main_window.WeatherDashboardGUIFrames') as mock_frames, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardWidgets') as mock_widgets, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardController') as mock_controller:
            
            # Configure mocks
            mock_frames_instance = Mock()
            mock_frames_instance.frames = {'main': Mock(), 'status': Mock()}
            mock_frames.return_value = mock_frames_instance
            
            mock_widgets_instance = Mock()
            mock_widgets_instance.metric_widgets = Mock()
            mock_widgets_instance.status_bar_widgets = Mock()
            mock_widgets_instance.control_widgets = Mock()
            mock_widgets.return_value = mock_widgets_instance
            
            mock_controller_instance = Mock()
            mock_controller.return_value = mock_controller_instance
            
            # Create main window with mocked state manager
            main_window = WeatherDashboardMain(
                root=self.mock_root,
                data_manager=self.mock_data_manager,
                data_service=self.mock_data_service,
                loading_manager=self.mock_loading_manager,
                async_operations=self.mock_async_operations,
                state_manager=self.mock_state_manager
            )
            
            # Verify window components were created
            self.assertIsNotNone(main_window.widgets)
            self.assertIsNotNone(main_window.data_manager)
            self.assertIsNotNone(main_window.service)

    def test_dependency_injection(self):
        """Test that dependencies are properly injected."""
        with patch('WeatherDashboard.gui.main_window.WeatherDashboardGUIFrames') as mock_frames, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardWidgets') as mock_widgets, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardController') as mock_controller:
            
            # Configure mocks
            mock_frames_instance = Mock()
            mock_frames_instance.frames = {'main': Mock(), 'status': Mock()}
            mock_frames.return_value = mock_frames_instance
            
            mock_widgets_instance = Mock()
            mock_widgets_instance.metric_widgets = Mock()
            mock_widgets_instance.status_bar_widgets = Mock()
            mock_widgets_instance.control_widgets = Mock()
            mock_widgets.return_value = mock_widgets_instance
            
            mock_controller_instance = Mock()
            mock_controller.return_value = mock_controller_instance
            
            # Create main window with mocked state manager
            main_window = WeatherDashboardMain(
                root=self.mock_root,
                data_manager=self.mock_data_manager,
                data_service=self.mock_data_service,
                loading_manager=self.mock_loading_manager,
                async_operations=self.mock_async_operations,
                state_manager=self.mock_state_manager
            )
            
            # Verify dependencies are accessible
            self.assertEqual(main_window.root, self.mock_root)
            self.assertEqual(main_window.data_manager, self.mock_data_manager)
            self.assertEqual(main_window.service, self.mock_data_service)
            self.assertEqual(main_window.loading_manager, self.mock_loading_manager)
            self.assertEqual(main_window.async_operations, self.mock_async_operations)

    def test_error_handling(self):
        """Test error handling in main window."""
        with patch('WeatherDashboard.gui.main_window.WeatherDashboardGUIFrames') as mock_frames, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardWidgets') as mock_widgets, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardController') as mock_controller:
            
            # Configure mocks to raise exceptions
            mock_frames.side_effect = Exception("Frames creation failed")
            
            # Should handle the exception gracefully
            with self.assertRaises(Exception):
                WeatherDashboardMain(
                    root=self.mock_root,
                    data_manager=self.mock_data_manager,
                    data_service=self.mock_data_service,
                    loading_manager=self.mock_loading_manager,
                    async_operations=self.mock_async_operations,
                    state_manager=self.mock_state_manager
                )

    def test_performance(self):
        """Test main window performance."""
        import time
        
        with patch('WeatherDashboard.gui.main_window.WeatherDashboardGUIFrames') as mock_frames, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardWidgets') as mock_widgets, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardController') as mock_controller:
            
            # Configure mocks
            mock_frames_instance = Mock()
            mock_frames_instance.frames = {'main': Mock(), 'status': Mock()}
            mock_frames.return_value = mock_frames_instance
            
            mock_widgets_instance = Mock()
            mock_widgets_instance.metric_widgets = Mock()
            mock_widgets_instance.status_bar_widgets = Mock()
            mock_widgets_instance.control_widgets = Mock()
            mock_widgets.return_value = mock_widgets_instance
            
            mock_controller_instance = Mock()
            mock_controller.return_value = mock_controller_instance
            
            start_time = time.time()
            
            # Create main window multiple times
            for _ in range(10):
                main_window = WeatherDashboardMain(
                    root=self.mock_root,
                    data_manager=self.mock_data_manager,
                    data_service=self.mock_data_service,
                    loading_manager=self.mock_loading_manager,
                    async_operations=self.mock_async_operations,
                    state_manager=self.mock_state_manager
                )
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Should complete 10 initializations in reasonable time
            self.assertLess(execution_time, 1.0)

    def test_memory_usage(self):
        """Test main window memory usage."""
        import gc
        
        with patch('WeatherDashboard.gui.main_window.WeatherDashboardGUIFrames') as mock_frames, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardWidgets') as mock_widgets, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardController') as mock_controller:
            
            # Configure mocks
            mock_frames_instance = Mock()
            mock_frames_instance.frames = {'main': Mock(), 'status': Mock()}
            mock_frames.return_value = mock_frames_instance
            
            mock_widgets_instance = Mock()
            mock_widgets_instance.metric_widgets = Mock()
            mock_widgets_instance.status_bar_widgets = Mock()
            mock_widgets_instance.control_widgets = Mock()
            mock_widgets.return_value = mock_widgets_instance
            
            mock_controller_instance = Mock()
            mock_controller.return_value = mock_controller_instance
            
            initial_objects = len(gc.get_objects())
            
            # Create many main windows
            windows = []
            for _ in range(50):
                window = WeatherDashboardMain(
                    root=self.mock_root,
                    data_manager=self.mock_data_manager,
                    data_service=self.mock_data_service,
                    loading_manager=self.mock_loading_manager,
                    async_operations=self.mock_async_operations,
                    state_manager=self.mock_state_manager
                )
                windows.append(window)
            
            # Force garbage collection
            gc.collect()
            
            final_objects = len(gc.get_objects())
            
            # Memory usage should not increase significantly
            # Increased threshold for Windows environment with many objects
            self.assertLess(abs(final_objects - initial_objects), 10000)

    def test_documentation(self):
        """Test that main window has proper documentation."""
        # Test that class exists and has docstring
        self.assertIsNotNone(WeatherDashboardMain.__doc__)
        
        # Test that class can be instantiated with proper mocks
        with patch('WeatherDashboard.gui.main_window.WeatherDashboardGUIFrames') as mock_frames, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardWidgets') as mock_widgets, \
             patch('WeatherDashboard.gui.main_window.WeatherDashboardController') as mock_controller:
            
            # Configure mocks
            mock_frames_instance = Mock()
            mock_frames_instance.frames = {'main': Mock(), 'status': Mock()}
            mock_frames.return_value = mock_frames_instance
            
            mock_widgets_instance = Mock()
            mock_widgets_instance.metric_widgets = Mock()
            mock_widgets_instance.status_bar_widgets = Mock()
            mock_widgets_instance.control_widgets = Mock()
            mock_widgets.return_value = mock_widgets_instance
            
            mock_controller_instance = Mock()
            mock_controller.return_value = mock_controller_instance
            
            # Create main window with mocked state manager
            main_window = WeatherDashboardMain(
                root=self.mock_root,
                data_manager=self.mock_data_manager,
                data_service=self.mock_data_service,
                loading_manager=self.mock_loading_manager,
                async_operations=self.mock_async_operations,
                state_manager=self.mock_state_manager
            )
            
            # Test that main window has expected attributes
            self.assertTrue(hasattr(main_window, 'root'))
            self.assertTrue(hasattr(main_window, 'data_manager'))
            self.assertTrue(hasattr(main_window, 'service'))
            self.assertTrue(hasattr(main_window, 'loading_manager'))
            self.assertTrue(hasattr(main_window, 'async_operations'))


if __name__ == '__main__':
    unittest.main()