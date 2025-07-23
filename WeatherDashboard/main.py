"""
Weather Dashboard - Main Entry Point

This module serves as the primary entry point for the Weather Dashboard application.
Initializes the GUI application, validates configuration, sets up logging, and
launches the main application window with proper error handling.
"""

import os
import tkinter as tk

from WeatherDashboard.utils.logger import Logger

def main():
    """Main entry point for the Weather Dashboard application.
    
    Initializes the GUI application by validating configuration, setting up logging,
    creating the main window, and starting the GUI event loop. Logs startup information
    including package version and author details for debugging and support purposes.
    """
    try:
        from WeatherDashboard import config
        from WeatherDashboard.alert_config import validate_alert_config
        from WeatherDashboard.gui.main_window import WeatherDashboardMain

        Logger.info("Loading Weather Dashboard application")

        # Initialize directories
        Logger.info("Creating required directories")
        config.ensure_directories()
        Logger.info("Directory creation completed successfully")

        # Validate configuration at startup
        Logger.info("Validating application configuration")
        config.validate_config()
        Logger.info("Main configuration validation completed successfully")
        
        Logger.info("Validating alert system configuration") 
        validate_alert_config()
        Logger.info("Alert configuration validation completed successfully")

        # Test logging system health after directory creation
        if not Logger.test_logging_health():
            print("Warning: Logging system health check failed")

        # Log startup information
        from WeatherDashboard import get_package_info
        package_info = get_package_info()
        Logger.info(f"Starting {package_info['name']} v{package_info['version']}: {package_info['description']} created by {package_info['author']}")
        
        root = tk.Tk()
        root.title("Weather Dashboard")
        app = WeatherDashboardMain(root)
        app.load_initial_display()
        root.mainloop()

    except ValueError as e:
        print(f"Configuration error: {e}\n")
        print("Please check your configuration and try again.")
        import sys
        sys.exit(1)
    except Exception as e:
        Logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()