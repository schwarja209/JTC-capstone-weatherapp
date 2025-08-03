"""
Standardized logging interface for the Weather Dashboard application.

This module provides a centralized logging system with both plain text and
structured JSON logging capabilities. Handles different log levels, timestamps,
and writes to multiple output formats for easy parsing and analysis.

Classes:
    Logger: Static logging utility with multiple output formats and severity levels
"""

import os
import json
import traceback
from datetime import datetime
from typing import Optional

from WeatherDashboard import config


class Logger:
    """Standardized logging interface for the Weather Dashboard application."""
    
    def __init__(self, log_folder: Optional[str] = None):
        """Initialize logger with optional dependencies.
        
        Args:
            log_folder: Directory for log files (defaults to config.OUTPUT.get("log_dir", "data_dir"))
        """
        # Direct imports for stable utilities
        self.config = config
        self.os = os
        self.json = json
        self.trackback = traceback

        # Instance data
        self.log_folder = log_folder or self.config.OUTPUT.get("log_dir", "data_dir")
        self.plain_log = self.os.path.join(self.log_folder, "weather.log")
        self.json_log = self.os.path.join(self.log_folder, "weather.jsonl")

    def _default_file_writer(self, filepath: str, content: str, mode: str = "a", encoding: str = "utf-8"):
        """Default file writing implementation."""
        with open(filepath, mode, encoding=encoding) as f:
            f.write(content)

    def _timestamp(self) -> str:
        """Return current timestamp in YYYY-MM-DD HH:MM:SS format."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def info(self, msg: str) -> None: 
        """Log an informational message."""
        self._log("INFO", msg)

    def warn(self, msg: str) -> None: 
        """Log a warning message."""
        self._log("WARN", msg)

    def error(self, msg: str) -> None: 
        """Log an error message."""
        self._log("ERROR", msg)

    def debug(self, msg: str) -> None: 
        """Log a debug message."""
        self._log("DEBUG", msg)

    def exception(self, msg: str, exc: Exception = None):
        print(f"[ERROR] {msg}")
        if exc:
            print("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
        else:
            print(traceback.format_exc())

    def _log(self, level: str, msg: str) -> None:
        """Log a message with the specified level, timestamp, and write to files.
        
        Args:
            level: Log level (INFO, WARN, ERROR)
            msg: Message to log
        """
        ts = self._timestamp()
        formatted = f"[{level}] {ts} {msg}"

        # Try to print with original message, fallback to safe encoding
        try:
            print(formatted)
        except UnicodeEncodeError as e:
            # Create safe fallback message
            safe_msg = msg.encode('ascii', errors='replace').decode('ascii')
            safe_formatted = f"[{level}] {ts} {safe_msg}"
            print(safe_formatted)
            print(f"[WARN] {ts} Original message had encoding issues: {e}")

        self._write_to_files(level, ts, msg)

    def _write_to_files(self, level: str, ts: str, msg: str) -> None:
        """Write log entry to both plain text and JSON files.
        
        Creates log directory if needed and handles file writing errors gracefully.
        
        Args:
            level: Log level string
            ts: Timestamp string
            msg: Message to write
        """
        # Ensure log directory exists before writing
        try:
            self.os.makedirs(self.log_folder, exist_ok=True)
        except OSError as e:
            print(f"Warning: Could not create log directory {self.log_folder}: {e}")
            return  # Exit early if we can't create the directory
        
        # Write to plain text log with fallback
        log_written = False
        try:
            self._default_file_writer(self.plain_log, f"[{level}] {ts} {msg}\n")
            log_written = True
        except (OSError, IOError, PermissionError) as e:
            print(f"Warning: Could not write to plain log file {self.plain_log}: {e}")
        except UnicodeEncodeError as e:
            # Try with safe encoding
            try:
                safe_msg = msg.encode('utf-8', errors='replace').decode('utf-8')
                self._default_file_writer(self.plain_log, f"[{level}] {ts} {safe_msg}\n")
                self._default_file_writer(self.plain_log, f"[WARN] {ts} Original message had encoding issues\n")
                log_written = True
            except Exception as fallback_error:
                print(f"Warning: Fallback plain log write also failed: {fallback_error}")

        # If primary log failed, try emergency backup
        if not log_written:
            self._emergency_log_fallback(level, ts, msg)

        # Write to JSON log with encoding safety
        try:
            # Ensure message is JSON-safe
            safe_msg = msg
            if not isinstance(msg, str):
                safe_msg = str(msg)
            
            log_entry = {
                "timestamp": ts,
                "level": level,
                "message": safe_msg
            }
            
            self._default_file_writer(self.json_log, self.json.dumps(log_entry, ensure_ascii=False) + "\n")
                
        except (OSError, IOError, PermissionError) as e:
            print(f"Warning: {self.config.ERROR_MESSAGES['file_error'].format(info='log data', file=self.plain_log, reason=str(e))}")
        except json.JSONEncodeError as e:
            # Fallback: try with ASCII-safe encoding
            try:
                safe_msg = msg.encode('ascii', errors='replace').decode('ascii')
                log_entry = {
                    "timestamp": ts,
                    "level": level,
                    "message": safe_msg,
                    "encoding_warning": "Original message contained non-JSON characters"
                }
                self._default_file_writer(self.json_log, self.json.dumps(log_entry) + "\n")
            except Exception as fallback_error:
                print(f"Warning: JSON log fallback also failed: {fallback_error}")

    def _emergency_log_fallback(self, level: str, ts: str, msg: str) -> None:
        """Emergency fallback when all normal logging fails.
        
        Attempts to write to a backup location or system log as last resort.
        
        Args:
            level: Log level string
            ts: Timestamp string  
            msg: Message to log
        """
        try:
            # Try writing to a backup file in temp directory
            import tempfile
            backup_log = self.os.path.join(tempfile.gettempdir(), "weather_dashboard_emergency.log")
            safe_msg = str(msg).encode('ascii', errors='replace').decode('ascii')
            
            self._default_file_writer(backup_log, f"[{level}] {ts} {safe_msg}\n")
            self._default_file_writer(backup_log, f"[EMERGENCY] {ts} Primary logging failed, using emergency backup\n")
            
            print(f"Emergency log written to: {backup_log}")
            
        except Exception as e:
            # Absolute last resort - just ensure we don't crash
            print(f"[CRITICAL] All logging failed: {e}")
            print(f"[CRITICAL] Lost log entry: [{level}] {ts} {repr(msg)}")

    def test_logging_health(self) -> bool:
        """Test if logging system is working properly.
        
        Returns:
            bool: True if logging is healthy, False if there are issues
        """
        try:
            # Test directory access
            self.os.makedirs(self.log_folder, exist_ok=True)
            
            # Test file write permissions
            test_msg = f"Health check at {self._timestamp()}"
            
            # Test plain log
            self._default_file_writer(self.plain_log, f"[TEST] {test_msg}\n")
            
            # Test JSON log  
            self._default_file_writer(self.json_log, self.json.dumps({"timestamp": test_msg, "test": True}) + "\n")
            
            return True
            
        except Exception as e:
            print(f"Logging health check failed: {e}")
            return False