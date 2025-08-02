"""
Comprehensive test suite for WeatherDashboard.main module.

Tests the main application entry point, system initialization, GUI creation,
error handling, and cleanup functionality.
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import tempfile
import shutil
import tkinter as tk
from pathlib import Path

# Import the module to test
from WeatherDashboard import main


class TestMainModuleImports(unittest.TestCase):
    """Test that main module can be imported and has required functions."""
    
    def test_main_module_imports_successfully(self):
        """Test that main module can be imported without errors."""
        try:
            from WeatherDashboard import main
        except ImportError as e:
            self.fail(f"Failed to import main module: {e}")
    
    def test_main_functions_exist(self):
        """Test that main module has required functions."""
        self.assertTrue(hasattr(main, 'initialize_system'))
        self.assertTrue(hasattr(main, 'create_and_run_gui'))
        self.assertTrue(hasattr(main, 'cleanup_gui_resources'))
        self.assertTrue(hasattr(main, 'main'))
    
    def test_main_functions_are_callable(self):
        """Test that main functions are callable."""
        self.assertTrue(callable(main.initialize_system))
        self.assertTrue(callable(main.create_and_run_gui))
        self.assertTrue(callable(main.cleanup_gui_resources))
        self.assertTrue(callable(main.main))


class TestInitializeSystem(unittest.TestCase):
    """Test system initialization functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('WeatherDashboard.main.sys.exit')
    @patch('WeatherDashboard.main.config')
    @patch('WeatherDashboard.main.Logger')
    @patch('WeatherDashboard.main.WeatherDashboardMain')
    @patch('WeatherDashboard.main.get_package_info')
    def test_initialize_system_success(self, mock_package_info, mock_main_window, mock_logger, mock_config, mock_exit):
        """Test successful system initialization."""
        # Mock successful imports and returns
        mock_package_info.return_value = {
            'name': 'WeatherDashboard',
            'version': '1.0.0',
            'description': 'Test Description',
            'author': 'Test Author'
        }
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        mock_logger_instance.test_logging_health.return_value = True
        
        # Mock config functions
        mock_config.ensure_directories.return_value = True
        mock_config.validate_config.return_value = None
        
        result = main.initialize_system()
        
        # Verify expected calls
        mock_config.ensure_directories.assert_called_once()
        mock_config.validate_config.assert_called_once()
        mock_logger_instance.info.assert_called()
        mock_logger_instance.test_logging_health.assert_called_once()
        
        # Verify return structure
        self.assertIsInstance(result, dict)
        self.assertIn('WeatherDashboardMain', result)
        self.assertIn('Logger', result)
        self.assertIn('package_info', result)
        self.assertEqual(result['package_info'], mock_package_info.return_value)
    
    @patch('WeatherDashboard.main.sys.exit')
    def test_initialize_system_import_error(self, mock_exit):
        """Test system initialization with import error."""
        with patch('WeatherDashboard.main.config', side_effect=ImportError("Module not found")):
            main.initialize_system()
            mock_exit.assert_called_once_with(1)
    
    @patch('WeatherDashboard.main.sys.exit')
    @patch('WeatherDashboard.main.config')
    @patch('WeatherDashboard.main.Logger')
    @patch('WeatherDashboard.main.WeatherDashboardMain')
    @patch('WeatherDashboard.main.get_package_info')
    def test_initialize_system_logging_health_failure(self, mock_package_info, mock_main_window, mock_logger, mock_config, mock_exit):
        """Test system initialization when logging health check fails."""
        mock_package_info.return_value = {
            'name': 'WeatherDashboard',
            'version': '1.0.0',
            'description': 'Test Description',
            'author': 'Test Author'
        }
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        mock_logger_instance.test_logging_health.return_value = False
        
        mock_config.ensure_directories.return_value = True
        mock_config.validate_config.return_value = None
        
        # Should not raise exception, just continue
        try:
            result = main.initialize_system()
            self.assertIsInstance(result, dict)
        except Exception as e:
            self.fail(f"initialize_system() raised {type(e).__name__} unexpectedly: {e}")
    
    @patch('WeatherDashboard.main.sys.exit')
    @patch('WeatherDashboard.main.config')
    @patch('WeatherDashboard.main.Logger')
    @patch('WeatherDashboard.main.WeatherDashboardMain')
    @patch('WeatherDashboard.main.get_package_info')
    def test_initialize_system_config_validation_error(self, mock_package_info, mock_main_window, mock_logger, mock_config, mock_exit):
        """Test system initialization when config validation fails."""
        mock_package_info.return_value = {
            'name': 'WeatherDashboard',
            'version': '1.0.0',
            'description': 'Test Description',
            'author': 'Test Author'
        }
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        mock_logger_instance.test_logging_health.return_value = True
        
        mock_config.ensure_directories.return_value = True
        mock_config.validate_config.side_effect = ValueError("Invalid config")
        
        with self.assertRaises(ValueError):
            main.initialize_system()


class TestCreateAndRunGUI(unittest.TestCase):
    """Test GUI creation and execution functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('WeatherDashboard.main.tk.Tk')
    @patch('WeatherDashboard.main.cleanup_gui_resources')
    def test_create_and_run_gui_success(self, mock_cleanup, mock_tk):
        """Test successful GUI creation and execution."""
        # Mock tkinter components
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        mock_app = MagicMock()
        mock_main_window_class = MagicMock(return_value=mock_app)
        
        components = {
            'WeatherDashboardMain': mock_main_window_class
        }
        
        # Mock mainloop to avoid blocking
        mock_root.mainloop = MagicMock()
        
        main.create_and_run_gui(components)
        
        # Verify expected calls
        mock_tk.assert_called_once()
        mock_root.title.assert_called_once_with("Weather Dashboard")
        mock_main_window_class.assert_called_once_with(mock_root)
        mock_app.load_initial_display.assert_called_once()
        mock_root.mainloop.assert_called_once()
        mock_cleanup.assert_called_once_with(mock_root)
    
    @patch('WeatherDashboard.main.tk.Tk')
    @patch('WeatherDashboard.main.cleanup_gui_resources')
    def test_create_and_run_gui_tk_error(self, mock_cleanup, mock_tk):
        """Test GUI creation with tkinter error."""
        mock_tk.side_effect = tk.TclError("Display error")
        
        components = {
            'WeatherDashboardMain': MagicMock()
        }
        
        with self.assertRaises(tk.TclError):
            main.create_and_run_gui(components)
        
        # Should still call cleanup even if root creation fails
        mock_cleanup.assert_called_once_with(None)
    
    @patch('WeatherDashboard.main.tk.Tk')
    @patch('WeatherDashboard.main.cleanup_gui_resources')
    def test_create_and_run_gui_app_creation_error(self, mock_cleanup, mock_tk):
        """Test GUI creation when app creation fails."""
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        mock_main_window_class = MagicMock(side_effect=Exception("App creation failed"))
        
        components = {
            'WeatherDashboardMain': mock_main_window_class
        }
        
        with self.assertRaises(Exception):
            main.create_and_run_gui(components)
        
        # Should still call cleanup
        mock_cleanup.assert_called_once_with(mock_root)
    
    @patch('WeatherDashboard.main.tk.Tk')
    @patch('WeatherDashboard.main.cleanup_gui_resources')
    def test_create_and_run_gui_mainloop_error(self, mock_cleanup, mock_tk):
        """Test GUI creation when mainloop fails."""
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        mock_app = MagicMock()
        mock_main_window_class = MagicMock(return_value=mock_app)
        
        # Mock mainloop to raise exception
        mock_root.mainloop.side_effect = Exception("Mainloop error")
        
        components = {
            'WeatherDashboardMain': mock_main_window_class
        }
        
        with self.assertRaises(Exception):
            main.create_and_run_gui(components)
        
        # Should still call cleanup
        mock_cleanup.assert_called_once_with(mock_root)


class TestCleanupGUIResources(unittest.TestCase):
    """Test GUI resource cleanup functionality."""
    
    def test_cleanup_gui_resources_with_valid_root(self):
        """Test cleanup with valid root window."""
        mock_root = MagicMock()
        mock_root.winfo_exists.return_value = True
        
        main.cleanup_gui_resources(mock_root)
        
        mock_root.winfo_exists.assert_called_once()
        mock_root.destroy.assert_called_once()
    
    def test_cleanup_gui_resources_with_none_root(self):
        """Test cleanup with None root window."""
        # Should not raise exception
        try:
            main.cleanup_gui_resources(None)
        except Exception as e:
            self.fail(f"cleanup_gui_resources() raised {type(e).__name__} unexpectedly: {e}")
    
    def test_cleanup_gui_resources_with_nonexistent_root(self):
        """Test cleanup with root that doesn't exist."""
        mock_root = MagicMock()
        mock_root.winfo_exists.return_value = False
        
        main.cleanup_gui_resources(mock_root)
        
        mock_root.winfo_exists.assert_called_once()
        mock_root.destroy.assert_not_called()
    
    def test_cleanup_gui_resources_with_destroy_error(self):
        """Test cleanup when destroy raises exception."""
        mock_root = MagicMock()
        mock_root.winfo_exists.return_value = True
        mock_root.destroy.side_effect = Exception("Destroy error")
        
        # Should not raise exception, should handle gracefully
        try:
            main.cleanup_gui_resources(mock_root)
        except Exception as e:
            self.fail(f"cleanup_gui_resources() raised {type(e).__name__} unexpectedly: {e}")


class TestMainFunction(unittest.TestCase):
    """Test the main function entry point."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('WeatherDashboard.main.sys.exit')
    @patch('WeatherDashboard.main.initialize_system')
    @patch('WeatherDashboard.main.create_and_run_gui')
    @patch('WeatherDashboard.main.Logger')
    def test_main_success(self, mock_logger, mock_create_gui, mock_init_system, mock_exit):
        """Test successful main execution."""
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        
        mock_components = {'test': 'components'}
        mock_init_system.return_value = mock_components
        
        main.main()
        
        # Verify expected calls
        mock_logger.assert_called_once()
        mock_init_system.assert_called_once()
        mock_create_gui.assert_called_once_with(mock_components)
        mock_exit.assert_called_once_with(0)
    
    @patch('WeatherDashboard.main.sys.exit')
    @patch('WeatherDashboard.main.initialize_system')
    @patch('WeatherDashboard.main.Logger')
    def test_main_logger_import_error(self, mock_logger, mock_init_system, mock_exit):
        """Test main execution when logger import fails."""
        mock_logger.side_effect = ImportError("Logger not found")
        
        main.main()
        
        mock_exit.assert_called_once_with(1)
    
    @patch('WeatherDashboard.main.sys.exit')
    @patch('WeatherDashboard.main.initialize_system')
    @patch('WeatherDashboard.main.create_and_run_gui')
    @patch('WeatherDashboard.main.Logger')
    def test_main_configuration_error(self, mock_logger, mock_create_gui, mock_init_system, mock_exit):
        """Test main execution with configuration error."""
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        
        mock_init_system.side_effect = ValueError("Config error")
        
        main.main()
        
        # Verify error handling
        mock_logger_instance.error.assert_called()
        mock_exit.assert_called_once_with(1)
    
    @patch('WeatherDashboard.main.sys.exit')
    @patch('WeatherDashboard.main.initialize_system')
    @patch('WeatherDashboard.main.create_and_run_gui')
    @patch('WeatherDashboard.main.Logger')
    def test_main_gui_error(self, mock_logger, mock_create_gui, mock_init_system, mock_exit):
        """Test main execution with GUI error."""
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        
        mock_components = {'test': 'components'}
        mock_init_system.return_value = mock_components
        mock_create_gui.side_effect = tk.TclError("GUI error")
        
        main.main()
        
        # Verify error handling
        mock_logger_instance.error.assert_called()
        mock_exit.assert_called_once_with(1)
    
    @patch('WeatherDashboard.main.sys.exit')
    @patch('WeatherDashboard.main.initialize_system')
    @patch('WeatherDashboard.main.create_and_run_gui')
    @patch('WeatherDashboard.main.Logger')
    def test_main_keyboard_interrupt(self, mock_logger, mock_create_gui, mock_init_system, mock_exit):
        """Test main execution with keyboard interrupt."""
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        
        mock_components = {'test': 'components'}
        mock_init_system.return_value = mock_components
        mock_create_gui.side_effect = KeyboardInterrupt()
        
        main.main()
        
        # Verify graceful shutdown
        mock_logger_instance.info.assert_called()
        mock_exit.assert_called_once_with(0)
    
    @patch('WeatherDashboard.main.sys.exit')
    @patch('WeatherDashboard.main.initialize_system')
    @patch('WeatherDashboard.main.create_and_run_gui')
    @patch('WeatherDashboard.main.Logger')
    def test_main_unexpected_error(self, mock_logger, mock_create_gui, mock_init_system, mock_exit):
        """Test main execution with unexpected error."""
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        
        mock_components = {'test': 'components'}
        mock_init_system.return_value = mock_components
        mock_create_gui.side_effect = Exception("Unexpected error")
        
        main.main()
        
        # Verify error handling
        mock_logger_instance.error.assert_called()
        mock_exit.assert_called_once_with(1)


class TestMainIntegration(unittest.TestCase):
    """Test integration between main module components."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('WeatherDashboard.main.sys.exit')
    @patch('WeatherDashboard.main.tk.Tk')
    @patch('WeatherDashboard.main.config')
    @patch('WeatherDashboard.main.Logger')
    @patch('WeatherDashboard.main.WeatherDashboardMain')
    @patch('WeatherDashboard.main.get_package_info')
    def test_full_initialization_flow(self, mock_package_info, mock_main_window, mock_logger, mock_config, mock_tk, mock_exit):
        """Test the complete initialization flow."""
        # Mock all dependencies
        mock_package_info.return_value = {
            'name': 'WeatherDashboard',
            'version': '1.0.0',
            'description': 'Test Description',
            'author': 'Test Author'
        }
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        mock_logger_instance.test_logging_health.return_value = True
        
        mock_config.ensure_directories.return_value = True
        mock_config.validate_config.return_value = None
        
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        mock_app = MagicMock()
        mock_main_window.return_value = mock_app
        
        # Mock mainloop to avoid blocking
        mock_root.mainloop = MagicMock()
        
        # Call main function
        main.main()
        
        # Verify the complete flow
        mock_config.ensure_directories.assert_called_once()
        mock_config.validate_config.assert_called_once()
        mock_logger_instance.info.assert_called()
        mock_tk.assert_called_once()
        mock_root.title.assert_called_once_with("Weather Dashboard")
        mock_main_window.assert_called_once_with(mock_root)
        mock_app.load_initial_display.assert_called_once()
        mock_root.mainloop.assert_called_once()
        mock_exit.assert_called_once_with(0)


if __name__ == '__main__':
    unittest.main() 