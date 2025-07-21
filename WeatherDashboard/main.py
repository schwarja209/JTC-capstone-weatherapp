"""
Weather Dashboard - Main Entry Point

This module serves as the primary entry point for the Weather Dashboard application.
Initializes the GUI application, validates configuration, sets up logging, and
launches the main application window with proper error handling.

The application features live weather data from OpenWeatherMap API with fallback
to simulated data, centralized state management, and a modular architecture
separating services, GUI components, and business logic.

Functions:
    main: Primary application entry point and GUI launcher
"""

import os
import tkinter as tk

try:
    from WeatherDashboard import config
    config.validate_config() # Validate configuration at startup
except ValueError as e:
    print(f"Configuration error: {e}\n")
    print("Please check your configuration and try again.")
    import sys
    sys.exit(1)

from WeatherDashboard.gui.main_window import WeatherDashboardMain
from WeatherDashboard.utils.logger import Logger

# Ensure required directories exist at app startup
for folder in {config.OUTPUT["data_dir"], config.OUTPUT["log_dir"]}:
    os.makedirs(folder, exist_ok=True)

# Test logging system health after directory creation
if not Logger.test_logging_health():
    print("Warning: Logging system health check failed")

def main():
    """Main entry point for the Weather Dashboard application.
    
    Initializes the GUI application by validating configuration, setting up logging,
    creating the main window, and starting the GUI event loop. Logs startup information
    including package version and author details for debugging and support purposes.
    """
    # Log startup information
    from WeatherDashboard import get_package_info
    package_info = get_package_info()
    Logger.info(f"Starting {package_info['name']} v{package_info['version']}: {package_info['description']} created by {package_info['author']}")
    
    root = tk.Tk()
    root.title("Weather Dashboard")
    app = WeatherDashboardMain(root)
    app.load_initial_display()
    root.mainloop()

if __name__ == "__main__":
    main()