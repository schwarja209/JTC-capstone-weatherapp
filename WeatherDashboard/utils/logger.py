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
    LOG_FOLDER = config.OUTPUT.get("log_dir", "data")  # default fallback
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
        try:
            print(formatted)
        except UnicodeEncodeError as e:
            print(f"[{level}] {ts} <message encoding error: {e}>")
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
        
        # Write to plain text log
        try:
            with open(Logger.PLAIN_LOG, "a", encoding="utf-8") as f:
                f.write(f"[{level}] {ts} {msg}\n")
        except (OSError, IOError, PermissionError) as e:
            print(f"Warning: Could not write to plain log file {Logger.PLAIN_LOG}: {e}")
        
        # Write to JSON log
        try:
            log_entry = {
                "timestamp": ts,
                "level": level,
                "message": msg
            }
            with open(Logger.JSON_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except (OSError, IOError, PermissionError) as e:
            print(f"Warning: Could not write to JSON log file {Logger.JSON_LOG}: {e}")
        except json.JSONEncodeError as e:
            print(f"Warning: Could not encode log entry to JSON: {e}")