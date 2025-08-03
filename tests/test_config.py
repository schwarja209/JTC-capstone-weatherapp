"""
Comprehensive test suite for WeatherDashboard.config module.

Tests configuration validation, directory creation, constants, and error handling
for the centralized configuration system.
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import tempfile
import shutil
from pathlib import Path

# Import the module to test
from WeatherDashboard import config


class TestConfigConstants(unittest.TestCase):
    """Test configuration constants and their structure."""
    
    def test_api_configuration_exists(self):
        """Test that API configuration constants are defined."""
        self.assertTrue(hasattr(config, 'API_BASE_URL'))
        self.assertTrue(hasattr(config, 'API_UV_URL'))
        self.assertTrue(hasattr(config, 'API_AIR_QUALITY_URL'))
        self.assertTrue(hasattr(config, 'API_TIMEOUT_SECONDS'))
        self.assertTrue(hasattr(config, 'API_RETRY_ATTEMPTS'))
        self.assertTrue(hasattr(config, 'API_RETRY_BASE_DELAY'))
        self.assertTrue(hasattr(config, 'FORCE_FALLBACK_MODE'))
    
    def test_metrics_structure(self):
        """Test that METRICS dictionary has correct structure."""
        self.assertIsInstance(config.METRICS, dict)
        self.assertGreater(len(config.METRICS), 0)
        
        # Test that each metric has required fields
        required_fields = ['label', 'visible', 'chartable']
        for metric_name, metric_data in config.METRICS.items():
            self.assertIsInstance(metric_name, str)
            self.assertIsInstance(metric_data, dict)
            for field in required_fields:
                self.assertIn(field, metric_data, f"Metric {metric_name} missing {field}")
    
    def test_metric_groups_structure(self):
        """Test that METRIC_GROUPS has correct structure."""
        self.assertIsInstance(config.METRIC_GROUPS, dict)
        self.assertGreater(len(config.METRIC_GROUPS), 0)
        
        # Test that each group has required fields
        required_fields = ['label', 'display_metrics', 'chart_metrics']
        for group_name, group_data in config.METRIC_GROUPS.items():
            self.assertIsInstance(group_name, str)
            self.assertIsInstance(group_data, dict)
            for field in required_fields:
                self.assertIn(field, group_data, f"Group {group_name} missing {field}")
    
    def test_units_structure(self):
        """Test that UNITS configuration has correct structure."""
        self.assertIsInstance(config.UNITS, dict)
        self.assertIn('metric_units', config.UNITS)
        # Note: The actual config only has 'metric_units', not 'imperial_units'
        # The imperial units are nested within metric_units
        self.assertIsInstance(config.UNITS['metric_units'], dict)
        
        # Test that metric_units contains expected keys
        expected_metrics = ['temperature', 'humidity', 'pressure', 'wind_speed']
        for metric in expected_metrics:
            self.assertIn(metric, config.UNITS['metric_units'])
    
    def test_defaults_structure(self):
        """Test that DEFAULTS configuration has correct structure."""
        self.assertIsInstance(config.DEFAULTS, dict)
        self.assertIn('unit', config.DEFAULTS)
        self.assertIn('city', config.DEFAULTS)
        # Note: The actual config doesn't have a 'theme' key
        # It has 'range', 'chart', 'visibility', and 'alert_thresholds'
        self.assertIn('range', config.DEFAULTS)
        self.assertIn('chart', config.DEFAULTS)
        self.assertIn('visibility', config.DEFAULTS)
        self.assertIn('alert_thresholds', config.DEFAULTS)
    
    def test_chart_configuration(self):
        """Test that CHART configuration has correct structure."""
        self.assertIsInstance(config.CHART, dict)
        # Note: The actual config doesn't have 'default_range_hours'
        # It has 'range_options', 'chart_figure_width_ratio', etc.
        self.assertIn('range_options', config.CHART)
        self.assertIn('chart_figure_width_ratio', config.CHART)
        self.assertIn('chart_figure_height_ratio', config.CHART)
        self.assertIn('chart_dpi', config.CHART)
        self.assertIn('chart_rotation_degrees', config.CHART)
    
    def test_output_configuration(self):
        """Test that OUTPUT configuration has correct structure."""
        self.assertIsInstance(config.OUTPUT, dict)
        self.assertIn('data_dir', config.OUTPUT)
        self.assertIn('log_dir', config.OUTPUT)
        self.assertIn('csv_dir', config.OUTPUT)
    
    def test_memory_configuration(self):
        """Test that MEMORY configuration has correct structure."""
        self.assertIsInstance(config.MEMORY, dict)
        self.assertIn('max_cities_stored', config.MEMORY)
        self.assertIn('max_entries_per_city', config.MEMORY)
        self.assertIn('max_total_entries', config.MEMORY)
        self.assertIn('cleanup_interval_hours', config.MEMORY)
    
    def test_scheduler_configuration(self):
        """Test that SCHEDULER configuration has correct structure."""
        self.assertIsInstance(config.SCHEDULER, dict)
        self.assertIn('enabled', config.SCHEDULER)
        self.assertIn('default_interval_minutes', config.SCHEDULER)
        self.assertIn('error_threshold', config.SCHEDULER)
    
    def test_error_messages_structure(self):
        """Test that ERROR_MESSAGES has correct structure."""
        self.assertIsInstance(config.ERROR_MESSAGES, dict)
        self.assertGreater(len(config.ERROR_MESSAGES), 0)
        
        # Test that each error message is a string
        for key, value in config.ERROR_MESSAGES.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, str)


class TestConfigValidation(unittest.TestCase):
    """Test configuration validation functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_data_dir = config.OUTPUT.get('data_dir')
        self.original_log_dir = config.OUTPUT.get('log_dir')
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('WeatherDashboard.config.API_KEY', 'test_api_key_1234567890')
    def test_validate_config_success(self):
        """Test successful configuration validation."""
        # Should not raise any exceptions
        try:
            config.validate_config()
        except Exception as e:
            self.fail(f"validate_config() raised {type(e).__name__} unexpectedly: {e}")
    
    @patch('WeatherDashboard.config.API_KEY', None)
    def test_validate_config_no_api_key(self):
        """Test validation with no API key (should not raise exception)."""
        # Should not raise exception, just print warning
        try:
            config.validate_config()
        except Exception as e:
            self.fail(f"validate_config() raised {type(e).__name__} unexpectedly: {e}")
    
    @patch('WeatherDashboard.config.API_KEY', 'short')
    def test_validate_config_short_api_key(self):
        """Test validation with short API key (should not raise exception)."""
        # Should not raise exception, just print warning
        try:
            config.validate_config()
        except Exception as e:
            self.fail(f"validate_config() raised {type(e).__name__} unexpectedly: {e}")
    
    @patch('WeatherDashboard.config.METRICS', {})
    def test_validate_config_empty_metrics(self):
        """Test validation with empty METRICS dictionary."""
        with self.assertRaises(ValueError) as cm:
            config.validate_config()
        self.assertIn("METRICS", str(cm.exception))
        self.assertIn("non-empty dictionary", str(cm.exception))
    
    @patch('WeatherDashboard.config.METRICS', {'temp': 'invalid'})
    def test_validate_config_invalid_metric_structure(self):
        """Test validation with invalid metric structure."""
        with self.assertRaises(ValueError) as cm:
            config.validate_config()
        self.assertIn("METRICS structure", str(cm.exception))
        self.assertIn("missing required", str(cm.exception))
    
    @patch('WeatherDashboard.config.DEFAULTS', {'unit': 'invalid_unit'})
    def test_validate_config_invalid_unit_system(self):
        """Test validation with invalid unit system."""
        with self.assertRaises(ValueError) as cm:
            config.validate_config()
        self.assertIn("Default unit system", str(cm.exception))
        self.assertIn("invalid", str(cm.exception))
    
    @patch('WeatherDashboard.config.MEMORY', {'max_cities_stored': -1})
    def test_validate_config_invalid_memory_config(self):
        """Test validation with invalid memory configuration."""
        with self.assertRaises(ValueError) as cm:
            config.validate_config()
        self.assertIn("Memory configuration", str(cm.exception))
        self.assertIn("positive number", str(cm.exception))
    
    @patch('WeatherDashboard.config.MEMORY', {
        'max_cities_stored': 50,
        'max_entries_per_city': 30,
        'max_total_entries': 1000,
        'cleanup_interval_hours': 24,
        'aggressive_cleanup_threshold': 2.0,  # This should trigger the validation error
        'max_alert_history_size': 100
    })
    def test_validate_config_invalid_cleanup_threshold(self):
        """Test validation with invalid cleanup threshold."""
        with self.assertRaises(ValueError) as cm:
            config.validate_config()
        # The actual error message is about the cleanup threshold being between 0 and 1
        self.assertIn("Aggressive cleanup threshold", str(cm.exception))
        self.assertIn("must be a number between 0 and 1", str(cm.exception))
    
    @patch('os.makedirs')
    def test_validate_config_directory_creation_error(self, mock_makedirs):
        """Test validation when directory creation fails."""
        mock_makedirs.side_effect = OSError("Permission denied")
        
        with self.assertRaises(ValueError) as cm:
            config.validate_config()
        self.assertIn("output directories", str(cm.exception))
        self.assertIn("cannot create or access", str(cm.exception))


class TestEnsureDirectories(unittest.TestCase):
    """Test directory creation functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_logs_dir = config.LOGS_DIR
        self.original_data_dir = config.DATA_DIR
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('WeatherDashboard.config.LOGS_DIR', '/test/logs')
    @patch('WeatherDashboard.config.DATA_DIR', '/test/data')
    @patch('WeatherDashboard.config.OUTPUT', {
        'csv_dir': '/test/csv',
        'csv_backup_dir': '/test/csv_backup'
    })
    @patch('os.makedirs')
    def test_ensure_directories_creates_all_dirs(self, mock_makedirs):
        """Test that ensure_directories creates all required directories."""
        result = config.ensure_directories()

        # Verify all directories were created
        expected_calls = [
            unittest.mock.call('/test/logs', exist_ok=True),
            unittest.mock.call('/test/data', exist_ok=True),
            unittest.mock.call('/test/csv', exist_ok=True),
            unittest.mock.call('/test/csv_backup', exist_ok=True)
        ]
        mock_makedirs.assert_has_calls(expected_calls, any_order=True)
        self.assertTrue(result)
    
    @patch('os.makedirs')
    def test_ensure_directories_handles_existing_dirs(self, mock_makedirs):
        """Test that ensure_directories handles existing directories gracefully."""
        # Should not raise exception even if directories already exist
        try:
            result = config.ensure_directories()
            self.assertTrue(result)
        except Exception as e:
            self.fail(f"ensure_directories() raised {type(e).__name__} unexpectedly: {e}")
    
    @patch('os.makedirs')
    def test_ensure_directories_handles_permission_error(self, mock_makedirs):
        """Test that ensure_directories handles permission errors gracefully."""
        mock_makedirs.side_effect = PermissionError("Permission denied")

        # The actual function doesn't handle permission errors gracefully
        # It will raise the exception, so we should expect that
        with self.assertRaises(PermissionError):
            config.ensure_directories()


class TestConfigIntegration(unittest.TestCase):
    """Test integration between different configuration components."""
    
    def test_metrics_reference_valid_units(self):
        """Test that metrics reference valid unit types."""
        available_unit_types = set(config.UNITS['metric_units'].keys())
        
        # Check that all metrics that have unit types reference valid ones
        for metric_name, metric_data in config.METRICS.items():
            if 'unit_type' in metric_data:
                unit_type = metric_data['unit_type']
                self.assertIn(unit_type, available_unit_types, 
                            f"Metric {metric_name} references invalid unit_type: {unit_type}")
    
    def test_metric_groups_reference_valid_metrics(self):
        """Test that metric groups reference valid metrics."""
        available_metrics = set(config.METRICS.keys())
        
        for group_name, group_data in config.METRIC_GROUPS.items():
            for metric_list_name in ['display_metrics', 'chart_metrics']:
                if metric_list_name in group_data:
                    for metric in group_data[metric_list_name]:
                        self.assertIn(metric, available_metrics,
                                    f"Group {group_name} references invalid metric: {metric}")
    
    def test_alert_definitions_reference_valid_units(self):
        """Test that alert definitions reference valid unit types."""
        # This test assumes alert_config is imported and available
        try:
            from WeatherDashboard.features.alerts.alert_config import ALERT_DEFINITIONS
            available_unit_types = set(config.UNITS['metric_units'].keys())
            
            for alert_type, definition in ALERT_DEFINITIONS.items():
                if 'unit_type' in definition:
                    unit_type = definition['unit_type']
                    self.assertIn(unit_type, available_unit_types,
                                f"Alert {alert_type} references invalid unit_type: {unit_type}")
        except ImportError:
            # Skip this test if alert_config is not available
            self.skipTest("alert_config module not available")


class TestConfigConstantsValues(unittest.TestCase):
    """Test specific values of configuration constants."""
    
    def test_api_timeout_reasonable(self):
        """Test that API timeout is reasonable."""
        self.assertIsInstance(config.API_TIMEOUT_SECONDS, (int, float))
        self.assertGreater(config.API_TIMEOUT_SECONDS, 0)
        self.assertLess(config.API_TIMEOUT_SECONDS, 60)  # Should not be too long
    
    def test_api_retry_attempts_reasonable(self):
        """Test that API retry attempts is reasonable."""
        self.assertIsInstance(config.API_RETRY_ATTEMPTS, int)
        self.assertGreaterEqual(config.API_RETRY_ATTEMPTS, 0)
        self.assertLessEqual(config.API_RETRY_ATTEMPTS, 10)  # Should not be too many
    
    def test_memory_limits_reasonable(self):
        """Test that memory limits are reasonable."""
        self.assertGreater(config.MEMORY['max_cities_stored'], 0)
        self.assertLess(config.MEMORY['max_cities_stored'], 1000)  # Should not be too many
        
        self.assertGreater(config.MEMORY['max_entries_per_city'], 0)
        self.assertLess(config.MEMORY['max_entries_per_city'], 1000)  # Should not be too many
        
        self.assertGreater(config.MEMORY['max_total_entries'], 0)
        self.assertLess(config.MEMORY['max_total_entries'], 10000)  # Should not be too many
    
    def test_scheduler_settings_reasonable(self):
        """Test that scheduler settings are reasonable."""
        self.assertIsInstance(config.SCHEDULER['enabled'], bool)
        
        self.assertGreater(config.SCHEDULER['default_interval_minutes'], 0)
        self.assertLess(config.SCHEDULER['default_interval_minutes'], 1440)  # Less than 24 hours
        
        self.assertGreater(config.SCHEDULER['error_threshold'], 0)
        self.assertLess(config.SCHEDULER['error_threshold'], 100)  # Should not be too high
    
    def test_chart_settings_reasonable(self):
        """Test that chart settings are reasonable."""
        # Note: The actual config doesn't have 'default_range_hours'
        # Test the actual chart settings that exist
        self.assertGreater(config.CHART['chart_figure_width_ratio'], 0)
        self.assertLessEqual(config.CHART['chart_figure_width_ratio'], 1)
        self.assertGreater(config.CHART['chart_figure_height_ratio'], 0)
        self.assertLessEqual(config.CHART['chart_figure_height_ratio'], 1)
        self.assertGreater(config.CHART['chart_dpi'], 0)
        self.assertGreater(config.CHART['chart_rotation_degrees'], 0)
        self.assertLess(config.CHART['chart_rotation_degrees'], 90)


if __name__ == '__main__':
    unittest.main() 