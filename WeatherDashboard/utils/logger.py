'''
This module provides a standardized logging interface for the Weather Dashboard application,
including both plain text and structured JSON logging.
It handles different log levels (INFO, WARN, ERROR) and timestamps each entry.
Logs are written to both a plain text file and a JSON Lines file for easy parsing.'''

import os
import json
from datetime import datetime

from WeatherDashboard import config

class Logger:
    '''Standardized logging interface for the Weather Dashboard application.'''
    LOG_FOLDER = config.OUTPUT.get("log_dir", "data")  # default fallback
    PLAIN_LOG = os.path.join(LOG_FOLDER, "weather.log")
    JSON_LOG = os.path.join(LOG_FOLDER, "weather.jsonl")

    @staticmethod
    def _timestamp():
        '''Returns current timestamp in YYYY-MM-DD HH:MM:SS format.'''
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def info(msg): Logger._log("INFO", msg)
    @staticmethod
    def warn(msg): Logger._log("WARN", msg)
    @staticmethod
    def error(msg): Logger._log("ERROR", msg)


    @staticmethod
    def _log(level, msg):
        '''Logs a message with the specified level, timestamp, and writes to files.'''
        ts = Logger._timestamp()
        formatted = f"[{level}] {ts} {msg}"
        try:
            print(formatted)
        except UnicodeEncodeError as e:
            print(f"[{level}] {ts} <message encoding error: {e}>")
        Logger._write_to_files(level, ts, msg)

    @staticmethod
    def _write_to_files(level, ts, msg):
        '''Writes log entry to both plain text and JSON files.'''
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