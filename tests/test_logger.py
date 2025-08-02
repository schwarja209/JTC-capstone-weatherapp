"""
Comprehensive test suite for WeatherDashboard.utils.logger module.

Tests the Logger class functionality, file writing, error handling,
logging health checks, and various logging scenarios.
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import tempfile
import shutil
import json
from datetime import datetime
from pathlib import Path

# Import the module to test
from WeatherDashboard.utils.logger import Logger


class TestLoggerInitialization(unittest.TestCase):
    """Test Logger class initialization and basic properties."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_logger_initialization_default(self):
        """Test Logger initialization with default parameters."""
        logger = Logger()
        
        self.assertIsNotNone(logger.log_folder)
        self.assertIsNotNone(logger.plain_log)
        self.assertIsNotNone(logger.json_log)
        self.assertIsInstance(logger.config, type)
        self.assertIsInstance(logger.datetime, type)
        self.assertIsInstance(logger.os, type)
        self.assertIsInstance(logger.json, type)
    
    def test_logger_initialization_custom_folder(self):
        """Test Logger initialization with custom log folder."""
        custom_folder = os.path.join(self.temp_dir, "custom_logs")
        logger = Logger(log_folder=custom_folder)
        
        self.assertEqual(logger.log_folder, custom_folder)
        self.assertIn("custom_logs", logger.plain_log)
        self.assertIn("custom_logs", logger.json_log)
    
    def test_logger_attributes_exist(self):
        """Test that Logger has required attributes."""
        logger = Logger()
        
        self.assertTrue(hasattr(logger, 'log_folder'))
        self.assertTrue(hasattr(logger, 'plain_log'))
        self.assertTrue(hasattr(logger, 'json_log'))
        self.assertTrue(hasattr(logger, 'config'))
        self.assertTrue(hasattr(logger, 'datetime'))
        self.assertTrue(hasattr(logger, 'os'))
        self.assertTrue(hasattr(logger, 'json'))
    
    def test_logger_methods_exist(self):
        """Test that Logger has required methods."""
        logger = Logger()
        
        self.assertTrue(hasattr(logger, 'info'))
        self.assertTrue(hasattr(logger, 'warn'))
        self.assertTrue(hasattr(logger, 'error'))
        self.assertTrue(hasattr(logger, 'exception'))
        self.assertTrue(hasattr(logger, 'test_logging_health'))
        
        self.assertTrue(callable(logger.info))
        self.assertTrue(callable(logger.warn))
        self.assertTrue(callable(logger.error))
        self.assertTrue(callable(logger.exception))
        self.assertTrue(callable(logger.test_logging_health))


class TestLoggerTimestamp(unittest.TestCase):
    """Test the _timestamp method functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_timestamp_format(self):
        """Test that _timestamp returns correct format."""
        logger = Logger()
        timestamp = logger._timestamp()
        
        # Should be in YYYY-MM-DD HH:MM:SS format
        self.assertIsInstance(timestamp, str)
        self.assertEqual(len(timestamp), 19)  # 19 characters
        self.assertIn('-', timestamp)
        self.assertIn(':', timestamp)
        self.assertIn(' ', timestamp)
    
    def test_timestamp_is_recent(self):
        """Test that _timestamp returns recent time."""
        logger = Logger()
        timestamp = logger._timestamp()
        
        # Parse the timestamp
        parsed_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        
        # Should be within 1 second of current time
        time_diff = abs((current_time - parsed_time).total_seconds())
        self.assertLess(time_diff, 1.0)


class TestLoggerLoggingMethods(unittest.TestCase):
    """Test the main logging methods (info, warn, error)."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('WeatherDashboard.utils.logger.print')
    @patch('WeatherDashboard.utils.logger.Logger._write_to_files')
    def test_info_logging(self, mock_write_files, mock_print):
        """Test info logging functionality."""
        logger = Logger(log_folder=self.temp_dir)
        test_message = "Test info message"
        
        logger.info(test_message)
        
        # Should call print
        mock_print.assert_called()
        
        # Should call _write_to_files
        mock_write_files.assert_called_once()
        call_args = mock_write_files.call_args
        self.assertEqual(call_args[0][0], "INFO")  # level
        self.assertIn("Test info message", call_args[0][2])  # message
    
    @patch('WeatherDashboard.utils.logger.print')
    @patch('WeatherDashboard.utils.logger.Logger._write_to_files')
    def test_warn_logging(self, mock_write_files, mock_print):
        """Test warn logging functionality."""
        logger = Logger(log_folder=self.temp_dir)
        test_message = "Test warning message"
        
        logger.warn(test_message)
        
        # Should call print
        mock_print.assert_called()
        
        # Should call _write_to_files
        mock_write_files.assert_called_once()
        call_args = mock_write_files.call_args
        self.assertEqual(call_args[0][0], "WARN")  # level
        self.assertIn("Test warning message", call_args[0][2])  # message
    
    @patch('WeatherDashboard.utils.logger.print')
    @patch('WeatherDashboard.utils.logger.Logger._write_to_files')
    def test_error_logging(self, mock_write_files, mock_print):
        """Test error logging functionality."""
        logger = Logger(log_folder=self.temp_dir)
        test_message = "Test error message"
        
        logger.error(test_message)
        
        # Should call print
        mock_print.assert_called()
        
        # Should call _write_to_files
        mock_write_files.assert_called_once()
        call_args = mock_write_files.call_args
        self.assertEqual(call_args[0][0], "ERROR")  # level
        self.assertIn("Test error message", call_args[0][2])  # message
    
    @patch('WeatherDashboard.utils.logger.print')
    @patch('WeatherDashboard.utils.logger.Logger._write_to_files')
    def test_logging_with_unicode_characters(self, mock_write_files, mock_print):
        """Test logging with unicode characters."""
        logger = Logger(log_folder=self.temp_dir)
        test_message = "Test message with unicode: 🚀 🌤️"
        
        logger.info(test_message)
        
        # Should call print
        mock_print.assert_called()
        
        # Should call _write_to_files
        mock_write_files.assert_called_once()
        call_args = mock_write_files.call_args
        self.assertIn("🚀 🌤️", call_args[0][2])  # message should contain unicode


class TestLoggerExceptionHandling(unittest.TestCase):
    """Test exception logging functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('WeatherDashboard.utils.logger.print')
    @patch('WeatherDashboard.utils.logger.traceback.format_exception')
    def test_exception_logging_with_exception(self, mock_format_exception, mock_print):
        """Test exception logging with provided exception."""
        logger = Logger(log_folder=self.temp_dir)
        test_message = "Test exception message"
        test_exception = ValueError("Test error")
        
        mock_format_exception.return_value = ["Traceback line 1", "Traceback line 2"]
        
        logger.exception(test_message, test_exception)
        
        # Should call print twice (message + traceback)
        self.assertEqual(mock_print.call_count, 2)
        
        # Should call format_exception
        mock_format_exception.assert_called_once()
    
    @patch('WeatherDashboard.utils.logger.print')
    @patch('WeatherDashboard.utils.logger.traceback.format_exc')
    def test_exception_logging_without_exception(self, mock_format_exc, mock_print):
        """Test exception logging without provided exception."""
        logger = Logger(log_folder=self.temp_dir)
        test_message = "Test exception message"
        
        mock_format_exc.return_value = "Current traceback"
        
        logger.exception(test_message)
        
        # Should call print twice (message + traceback)
        self.assertEqual(mock_print.call_count, 2)
        
        # Should call format_exc
        mock_format_exc.assert_called_once()


class TestLoggerFileWriting(unittest.TestCase):
    """Test file writing functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_write_to_files_success(self, mock_makedirs, mock_file):
        """Test successful file writing."""
        logger = Logger(log_folder=self.temp_dir)
        
        logger._write_to_files("INFO", "2023-01-01 12:00:00", "Test message")
        
        # Should create directories
        mock_makedirs.assert_called_with(self.temp_dir, exist_ok=True)
        
        # Should open files for writing
        self.assertEqual(mock_file.call_count, 2)  # plain and json files
    
    @patch('builtins.open', side_effect=OSError("Permission denied"))
    @patch('os.makedirs')
    def test_write_to_files_permission_error(self, mock_makedirs, mock_file):
        """Test file writing with permission error."""
        logger = Logger(log_folder=self.temp_dir)
        
        # Should not raise exception
        try:
            logger._write_to_files("INFO", "2023-01-01 12:00:00", "Test message")
        except Exception as e:
            self.fail(f"_write_to_files() raised {type(e).__name__} unexpectedly: {e}")
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_write_to_files_creates_directories(self, mock_makedirs, mock_file):
        """Test that _write_to_files creates directories if needed."""
        logger = Logger(log_folder=self.temp_dir)
        
        logger._write_to_files("INFO", "2023-01-01 12:00:00", "Test message")
        
        # Should create directories
        mock_makedirs.assert_called_with(self.temp_dir, exist_ok=True)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_write_to_files_writes_both_formats(self, mock_makedirs, mock_file):
        """Test that _write_to_files writes both plain and JSON formats."""
        logger = Logger(log_folder=self.temp_dir)
        
        logger._write_to_files("INFO", "2023-01-01 12:00:00", "Test message")
        
        # Should open both files
        file_calls = mock_file.call_args_list
        self.assertEqual(len(file_calls), 2)
        
        # Check that both plain and JSON files are opened
        file_paths = [call[0][0] for call in file_calls]
        self.assertTrue(any('weather.log' in path for path in file_paths))
        self.assertTrue(any('weather.jsonl' in path for path in file_paths))


class TestLoggerHealthCheck(unittest.TestCase):
    """Test logging health check functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('WeatherDashboard.utils.logger.Logger._write_to_files')
    def test_test_logging_health_success(self, mock_write_files):
        """Test successful logging health check."""
        logger = Logger(log_folder=self.temp_dir)
        
        result = logger.test_logging_health()
        
        # Should return True on success
        self.assertTrue(result)
        
        # Should call _write_to_files
        mock_write_files.assert_called_once()
    
    @patch('WeatherDashboard.utils.logger.Logger._write_to_files', side_effect=Exception("Write error"))
    def test_test_logging_health_failure(self, mock_write_files):
        """Test logging health check with write error."""
        logger = Logger(log_folder=self.temp_dir)
        
        result = logger.test_logging_health()
        
        # Should return False on failure
        self.assertFalse(result)
        
        # Should call _write_to_files
        mock_write_files.assert_called_once()
    
    @patch('WeatherDashboard.utils.logger.Logger._write_to_files')
    def test_test_logging_health_creates_test_message(self, mock_write_files):
        """Test that health check creates appropriate test message."""
        logger = Logger(log_folder=self.temp_dir)
        
        logger.test_logging_health()
        
        # Should call _write_to_files with health check message
        mock_write_files.assert_called_once()
        call_args = mock_write_files.call_args
        self.assertEqual(call_args[0][0], "INFO")  # level
        self.assertIn("health check", call_args[0][2].lower())  # message


class TestLoggerErrorHandling(unittest.TestCase):
    """Test error handling in logging operations."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('WeatherDashboard.utils.logger.print')
    @patch('WeatherDashboard.utils.logger.Logger._write_to_files')
    def test_logging_with_encoding_error(self, mock_write_files, mock_print):
        """Test logging with encoding error in print."""
        logger = Logger(log_folder=self.temp_dir)
        test_message = "Test message with problematic characters: 🚀"
        
        # Mock print to raise UnicodeEncodeError
        mock_print.side_effect = UnicodeEncodeError('ascii', 'test', 0, 1, 'reason')
        
        # Should not raise exception
        try:
            logger.info(test_message)
        except Exception as e:
            self.fail(f"info() raised {type(e).__name__} unexpectedly: {e}")
        
        # Should still call _write_to_files
        mock_write_files.assert_called_once()
    
    @patch('WeatherDashboard.utils.logger.print')
    @patch('WeatherDashboard.utils.logger.Logger._write_to_files')
    def test_logging_with_safe_fallback(self, mock_write_files, mock_print):
        """Test logging with safe fallback for encoding errors."""
        logger = Logger(log_folder=self.temp_dir)
        test_message = "Test message with problematic characters: 🚀"
        
        # Mock print to raise UnicodeEncodeError on first call, succeed on second
        mock_print.side_effect = [UnicodeEncodeError('ascii', 'test', 0, 1, 'reason'), None]
        
        logger.info(test_message)
        
        # Should call print twice (original + fallback)
        self.assertEqual(mock_print.call_count, 2)
        
        # Should still call _write_to_files
        mock_write_files.assert_called_once()


class TestLoggerIntegration(unittest.TestCase):
    """Test integration between Logger components."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('WeatherDashboard.utils.logger.print')
    @patch('WeatherDashboard.utils.logger.Logger._write_to_files')
    def test_full_logging_cycle(self, mock_write_files, mock_print):
        """Test a complete logging cycle."""
        logger = Logger(log_folder=self.temp_dir)
        
        # Log different levels
        logger.info("Info message")
        logger.warn("Warning message")
        logger.error("Error message")
        
        # Should call print 3 times
        self.assertEqual(mock_print.call_count, 3)
        
        # Should call _write_to_files 3 times
        self.assertEqual(mock_write_files.call_count, 3)
        
        # Check different levels were used
        levels = [call[0][0] for call in mock_write_files.call_args_list]
        self.assertIn("INFO", levels)
        self.assertIn("WARN", levels)
        self.assertIn("ERROR", levels)
    
    @patch('WeatherDashboard.utils.logger.print')
    @patch('WeatherDashboard.utils.logger.Logger._write_to_files')
    def test_logger_with_multiple_messages(self, mock_write_files, mock_print):
        """Test logger with multiple messages."""
        logger = Logger(log_folder=self.temp_dir)
        
        messages = [
            "First message",
            "Second message",
            "Third message with special chars: 🎯",
            "Fourth message"
        ]
        
        for message in messages:
            logger.info(message)
        
        # Should call print and _write_to_files for each message
        self.assertEqual(mock_print.call_count, len(messages))
        self.assertEqual(mock_write_files.call_count, len(messages))
        
        # Check all messages were processed
        processed_messages = [call[0][2] for call in mock_write_files.call_args_list]
        for message in messages:
            self.assertTrue(any(message in msg for msg in processed_messages))


class TestLoggerEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_logger_with_empty_message(self):
        """Test logger with empty message."""
        logger = Logger(log_folder=self.temp_dir)
        
        # Should not raise exception
        try:
            logger.info("")
            logger.warn("")
            logger.error("")
        except Exception as e:
            self.fail(f"Logger methods raised {type(e).__name__} unexpectedly: {e}")
    
    def test_logger_with_very_long_message(self):
        """Test logger with very long message."""
        logger = Logger(log_folder=self.temp_dir)
        long_message = "A" * 10000  # 10k character message
        
        # Should not raise exception
        try:
            logger.info(long_message)
        except Exception as e:
            self.fail(f"info() raised {type(e).__name__} unexpectedly: {e}")
    
    def test_logger_with_none_message(self):
        """Test logger with None message."""
        logger = Logger(log_folder=self.temp_dir)
        
        # Should not raise exception
        try:
            logger.info(None)
            logger.warn(None)
            logger.error(None)
        except Exception as e:
            self.fail(f"Logger methods raised {type(e).__name__} unexpectedly: {e}")
    
    def test_logger_with_special_characters(self):
        """Test logger with special characters."""
        logger = Logger(log_folder=self.temp_dir)
        special_message = "Message with: \n\t\r\b\f special chars and unicode: 🚀🌤️⚡"
        
        # Should not raise exception
        try:
            logger.info(special_message)
        except Exception as e:
            self.fail(f"info() raised {type(e).__name__} unexpectedly: {e}")


if __name__ == '__main__':
    unittest.main() 