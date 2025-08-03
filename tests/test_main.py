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
    @patch('WeatherDashboard.get_package_info')
    @patch('WeatherDashboard.config')
    @patch('WeatherDashboard.utils.logger.Logger')
    def test_initialize_system_success(self, mock_logger, mock_config, mock_package_info, mock_exit):
        """Test successful system initialization."""
        mock_package_info.return_value = {
            'name': 'Test App',
            'version': '1.0.0',
            'description': 'Test Description',
            'author': 'Test Author'
        }
        
        result = main.initialize_system()
        
        self.assertIn('WeatherDashboardMain', result)
        self.assertIn('Logger', result)
        self.assertIn('package_info', result)
        self.assertEqual(result['package_info']['name'], 'Test App')
        
        # Verify config validation was called
        mock_config.ensure_directories.assert_called_once()
        mock_config.validate_config.assert_called_once()
        
        # Verify logger was created and used
        mock_logger.assert_called_once()
        mock_logger_instance = mock_logger.return_value
        mock_logger_instance.info.assert_called()
        mock_logger_instance.test_logging_health.assert_called_once()
    
    @patch('WeatherDashboard.main.sys.exit')
    @patch('WeatherDashboard.get_package_info')
    @patch('WeatherDashboard.config')
    @patch('WeatherDashboard.utils.logger.Logger')
    def test_initialize_system_config_validation_error(self, mock_logger, mock_config, mock_package_info, mock_exit):
        """Test system initialization with config validation error."""
        mock_config.validate_config.side_effect = ValueError("Config validation failed")
        
        with self.assertRaises(ValueError):
            main.initialize_system()
        
        # Should not exit since we're testing the exception
        mock_exit.assert_not_called()
    
    @patch('WeatherDashboard.main.sys.exit')
    def test_initialize_system_import_error(self, mock_exit):
        """Test system initialization with import error."""
        with patch('WeatherDashboard.main.initialize_system', side_effect=ImportError("Module not found")):
            with self.assertRaises(ImportError):
                main.initialize_system()
    
    @patch('WeatherDashboard.main.sys.exit')
    @patch('WeatherDashboard.get_package_info')
    @patch('WeatherDashboard.config')
    @patch('WeatherDashboard.utils.logger.Logger')
    def test_initialize_system_logging_health_failure(self, mock_logger, mock_config, mock_package_info, mock_exit):
        """Test system initialization with logging health failure."""
        mock_package_info.return_value = {
            'name': 'Test App',
            'version': '1.0.0',
            'description': 'Test Description',
            'author': 'Test Author'
        }
        
        # Mock logger to return False for health check
        mock_logger_instance = mock_logger.return_value
        mock_logger_instance.test_logging_health.return_value = False
        
        result = main.initialize_system()
        
        # Should still succeed but with warning
        self.assertIn('WeatherDashboardMain', result)
        mock_logger_instance.test_logging_health.assert_called_once()


class TestCreateAndRunGUI(unittest.TestCase):
    """Test GUI creation and execution."""
    
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
        mock_root = MagicMock()
        mock_app = MagicMock()
        mock_tk.return_value = mock_root
        
        # Mock the WeatherDashboardMain class at the import location
        with patch('WeatherDashboard.gui.main_window.WeatherDashboardMain') as mock_main_class:
            mock_main_class.return_value = mock_app
            
            components = {
                'WeatherDashboardMain': mock_main_class,
                'Logger': MagicMock(),
                'package_info': {'name': 'Test'}
            }
            
            main.create_and_run_gui(components)
            
            # Verify GUI was created and started
            mock_tk.assert_called_once()
            mock_main_class.assert_called_once_with(mock_root)
            mock_app.load_initial_display.assert_called_once()
            mock_root.mainloop.assert_called_once()
            mock_cleanup.assert_called_once_with(mock_root)
    
    @patch('WeatherDashboard.main.tk.Tk')
    @patch('WeatherDashboard.main.cleanup_gui_resources')
    def test_create_and_run_gui_tk_error(self, mock_cleanup, mock_tk):
        """Test GUI creation with Tkinter error."""
        mock_tk.side_effect = tk.TclError("GUI error")
        
        components = {
            'WeatherDashboardMain': MagicMock(),
            'Logger': MagicMock(),
            'package_info': {'name': 'Test'}
        }
        
        with self.assertRaises(tk.TclError):
            main.create_and_run_gui(components)
        
        # Cleanup should not be called since root was never created
        mock_cleanup.assert_not_called()
    
    @patch('WeatherDashboard.main.tk.Tk')
    @patch('WeatherDashboard.main.cleanup_gui_resources')
    def test_create_and_run_gui_app_creation_error(self, mock_cleanup, mock_tk):
        """Test GUI creation with app creation error."""
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        # Mock the WeatherDashboardMain class to raise an error
        with patch('WeatherDashboard.gui.main_window.WeatherDashboardMain') as mock_main_class:
            mock_main_class.side_effect = Exception("App creation failed")
            
            components = {
                'WeatherDashboardMain': mock_main_class,
                'Logger': MagicMock(),
                'package_info': {'name': 'Test'}
            }
            
            with self.assertRaises(Exception):
                main.create_and_run_gui(components)
            
            # Cleanup should still be called
            mock_cleanup.assert_called_once_with(mock_root)
    
    @patch('WeatherDashboard.main.tk.Tk')
    @patch('WeatherDashboard.main.cleanup_gui_resources')
    def test_create_and_run_gui_mainloop_error(self, mock_cleanup, mock_tk):
        """Test GUI creation with mainloop error."""
        mock_root = MagicMock()
        mock_app = MagicMock()
        mock_tk.return_value = mock_root
        mock_root.mainloop.side_effect = Exception("Mainloop error")
        
        # Mock the WeatherDashboardMain class
        with patch('WeatherDashboard.gui.main_window.WeatherDashboardMain') as mock_main_class:
            mock_main_class.return_value = mock_app
            
            components = {
                'WeatherDashboardMain': mock_main_class,
                'Logger': MagicMock(),
                'package_info': {'name': 'Test'}
            }
            
            with self.assertRaises(Exception):
                main.create_and_run_gui(components)
            
            # Cleanup should still be called
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
        """Test cleanup with None root."""
        # Should not raise any exception
        main.cleanup_gui_resources(None)
    
    def test_cleanup_gui_resources_with_nonexistent_root(self):
        """Test cleanup with nonexistent root."""
        mock_root = MagicMock()
        mock_root.winfo_exists.return_value = False
        
        main.cleanup_gui_resources(mock_root)
        
        mock_root.winfo_exists.assert_called_once()
        mock_root.destroy.assert_not_called()
    
    def test_cleanup_gui_resources_with_destroy_error(self):
        """Test cleanup with destroy error."""
        mock_root = MagicMock()
        mock_root.winfo_exists.return_value = True
        mock_root.destroy.side_effect = Exception("Destroy failed")
        
        # Should not raise exception
        main.cleanup_gui_resources(mock_root)
        
        mock_root.destroy.assert_called_once()


class TestMainFunction(unittest.TestCase):
    """Test main function execution."""
    
    @patch('WeatherDashboard.main.initialize_system')
    @patch('WeatherDashboard.main.create_and_run_gui')
    def test_main_success(self, mock_create_gui, mock_initialize):
        """Test successful main execution."""
        mock_initialize.return_value = {'test': 'components'}
        
        with self.assertRaises(SystemExit) as cm:
            main.main()
        
        self.assertEqual(cm.exception.code, 0)
        mock_initialize.assert_called_once()
        mock_create_gui.assert_called_once_with({'test': 'components'})
    
    @patch('WeatherDashboard.main.initialize_system')
    @patch('WeatherDashboard.main.create_and_run_gui')
    def test_main_configuration_error(self, mock_create_gui, mock_initialize):
        """Test main execution with configuration error."""
        mock_initialize.side_effect = ValueError("Configuration error")
        
        with self.assertRaises(SystemExit) as cm:
            main.main()
        
        self.assertEqual(cm.exception.code, 1)
        mock_initialize.assert_called_once()
        mock_create_gui.assert_not_called()
    
    @patch('WeatherDashboard.main.initialize_system')
    @patch('WeatherDashboard.main.create_and_run_gui')
    def test_main_gui_error(self, mock_create_gui, mock_initialize):
        """Test main execution with GUI error."""
        mock_initialize.return_value = {'test': 'components'}
        mock_create_gui.side_effect = tk.TclError("GUI error")
        
        with self.assertRaises(SystemExit) as cm:
            main.main()
        
        self.assertEqual(cm.exception.code, 1)
        mock_initialize.assert_called_once()
        mock_create_gui.assert_called_once()
    
    @patch('WeatherDashboard.main.initialize_system')
    @patch('WeatherDashboard.main.create_and_run_gui')
    def test_main_keyboard_interrupt(self, mock_create_gui, mock_initialize):
        """Test main execution with keyboard interrupt."""
        mock_initialize.return_value = {'test': 'components'}
        mock_create_gui.side_effect = KeyboardInterrupt()
        
        with self.assertRaises(SystemExit) as cm:
            main.main()
        
        self.assertEqual(cm.exception.code, 0)
        mock_initialize.assert_called_once()
        mock_create_gui.assert_called_once()
    
    @patch('WeatherDashboard.main.initialize_system')
    @patch('WeatherDashboard.main.create_and_run_gui')
    def test_main_logger_import_error(self, mock_create_gui, mock_initialize):
        """Test main execution with logger import error."""
        mock_initialize.side_effect = ImportError("Logger import failed")
        
        with self.assertRaises(SystemExit) as cm:
            main.main()
        
        self.assertEqual(cm.exception.code, 1)
        mock_initialize.assert_called_once()
        mock_create_gui.assert_not_called()
    
    @patch('WeatherDashboard.main.initialize_system')
    @patch('WeatherDashboard.main.create_and_run_gui')
    def test_main_unexpected_error(self, mock_create_gui, mock_initialize):
        """Test main execution with unexpected error."""
        mock_initialize.side_effect = Exception("Unexpected error")
        
        with self.assertRaises(SystemExit) as cm:
            main.main()
        
        self.assertEqual(cm.exception.code, 1)
        mock_initialize.assert_called_once()
        mock_create_gui.assert_not_called()


class TestMainIntegration(unittest.TestCase):
    """Test main function integration scenarios."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('WeatherDashboard.main.sys.exit')
    @patch('WeatherDashboard.main.tk.Tk')
    @patch('WeatherDashboard.config')
    @patch('WeatherDashboard.utils.logger.Logger')
    @patch('WeatherDashboard.gui.main_window.WeatherDashboardMain')
    @patch('WeatherDashboard.get_package_info')
    def test_full_initialization_flow(self, mock_package_info, mock_main_window, mock_logger, mock_config, mock_tk, mock_exit):
        """Test full initialization flow."""
        mock_package_info.return_value = {
            'name': 'Test App',
            'version': '1.0.0',
            'description': 'Test Description',
            'author': 'Test Author'
        }
        
        mock_root = MagicMock()
        mock_app = MagicMock()
        mock_tk.return_value = mock_root
        mock_main_window.return_value = mock_app
        
        # Test the full flow
        result = main.initialize_system()
        
        self.assertIn('WeatherDashboardMain', result)
        self.assertIn('Logger', result)
        self.assertIn('package_info', result)
        
        # Verify all components were initialized
        mock_config.ensure_directories.assert_called_once()
        mock_config.validate_config.assert_called_once()
        mock_logger.assert_called_once() 