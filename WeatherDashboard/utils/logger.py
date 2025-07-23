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
from datetime import datetime

from WeatherDashboard import config


class Logger:
    """Standardized logging interface for the Weather Dashboard application.
    
    Provides static methods for logging at different severity levels with
    automatic timestamping and dual-format output (plain text and JSON Lines).
    Handles file creation, directory setup, and error recovery gracefully.
    
    Attributes:
        LOG_FOLDER: Directory path for log file storage
        PLAIN_LOG: Path to plain text log file
        JSON_LOG: Path to JSON Lines log file
    """
    LOG_FOLDER = config.OUTPUT.get("log_dir", "data_dir")  # default fallback
    PLAIN_LOG = os.path.join(LOG_FOLDER, "weather.log")
    JSON_LOG = os.path.join(LOG_FOLDER, "weather.jsonl")

    @staticmethod
    def _timestamp() -> str:
        """Return current timestamp in YYYY-MM-DD HH:MM:SS format."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:SS")

    @staticmethod
    def info(msg: str) -> None: 
        """Log an informational message."""
        Logger._log("INFO", msg)
    
    @staticmethod
    def warn(msg: str) -> None: 
        """Log a warning message."""
        Logger._log("WARN", msg)
    
    @staticmethod
    def error(msg: str) -> None: 
        """Log an error message."""
        Logger._log("ERROR", msg)

    @staticmethod
    def _log(level: str, msg: str) -> None:
        """Log a message with the specified level, timestamp, and write to files.
        
        Args:
            level: Log level (INFO, WARN, ERROR)
            msg: Message to log
        """
        ts = Logger._timestamp()
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

        Logger._write_to_files(level, ts, msg)

    @staticmethod
    def _write_to_files(level: str, ts: str, msg: str) -> None:
        """Write log entry to both plain text and JSON files.
        
        Creates log directory if needed and handles file writing errors gracefully.
        
        Args:
            level: Log level string
            ts: Timestamp string
            msg: Message to write
        """
        # Ensure log directory exists before writing
        try:
            os.makedirs(Logger.LOG_FOLDER, exist_ok=True)
        except OSError as e:
            print(f"Warning: Could not create log directory {Logger.LOG_FOLDER}: {e}")
            return  # Exit early if we can't create the directory
        
        # Write to plain text log with fallback
        log_written = False
        try:
            with open(Logger.PLAIN_LOG, "a", encoding="utf-8") as f:
                f.write(f"[{level}] {ts} {msg}\n")
            log_written = True
        except (OSError, IOError, PermissionError) as e:
            print(f"Warning: Could not write to plain log file {Logger.PLAIN_LOG}: {e}")
        except UnicodeEncodeError as e:
            # Try with safe encoding
            try:
                safe_msg = msg.encode('utf-8', errors='replace').decode('utf-8')
                with open(Logger.PLAIN_LOG, "a", encoding="utf-8") as f:
                    f.write(f"[{level}] {ts} {safe_msg}\n")
                    f.write(f"[WARN] {ts} Original message had encoding issues\n")
                log_written = True
            except Exception as fallback_error:
                print(f"Warning: Fallback plain log write also failed: {fallback_error}")

        # If primary log failed, try emergency backup
        if not log_written:
            Logger._emergency_log_fallback(level, ts, msg)

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
            
            with open(Logger.JSON_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
                
        except (OSError, IOError, PermissionError) as e:
            print(f"Warning: {config.ERROR_MESSAGES['file_error'].format(info='log data', file=Logger.PLAIN_LOG, reason=str(e))}")
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
                with open(Logger.JSON_LOG, "a", encoding="utf-8") as f:
                    f.write(json.dumps(log_entry) + "\n")
            except Exception as fallback_error:
                print(f"Warning: JSON log fallback also failed: {fallback_error}")
    
    @staticmethod
    def _emergency_log_fallback(level: str, ts: str, msg: str) -> None:
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
            backup_log = os.path.join(tempfile.gettempdir(), "weather_dashboard_emergency.log")
            safe_msg = str(msg).encode('ascii', errors='replace').decode('ascii')
            
            with open(backup_log, "a", encoding="ascii") as f:
                f.write(f"[{level}] {ts} {safe_msg}\n")
                f.write(f"[EMERGENCY] {ts} Primary logging failed, using emergency backup\n")
            
            print(f"Emergency log written to: {backup_log}")
            
        except Exception as e:
            # Absolute last resort - just ensure we don't crash
            print(f"[CRITICAL] All logging failed: {e}")
            print(f"[CRITICAL] Lost log entry: [{level}] {ts} {repr(msg)}")

    @staticmethod
    def test_logging_health() -> bool:
        """Test if logging system is working properly.
        
        Returns:
            bool: True if logging is healthy, False if there are issues
        """
        try:
            # Test directory access
            os.makedirs(Logger.LOG_FOLDER, exist_ok=True)
            
            # Test file write permissions
            test_msg = f"Health check at {Logger._timestamp()}"
            
            # Test plain log
            with open(Logger.PLAIN_LOG, "a", encoding="utf-8") as f:
                f.write(f"[TEST] {test_msg}\n")
            
            # Test JSON log  
            with open(Logger.JSON_LOG, "a", encoding="utf-8") as f:
                json.dumps({"test": test_msg})  # Validate JSON encoding works
                f.write(json.dumps({"timestamp": test_msg, "test": True}) + "\n")
            
            return True
            
        except Exception as e:
            print(f"Logging health check failed: {e}")
            return False