"""
Weather Dashboard - Main Entry Point

This module serves as the primary entry point for the Weather Dashboard application.
Initializes the GUI application, validates configuration, sets up logging, and
launches the main application window with proper error handling.
"""

import sys
import tkinter as tk
from typing import Dict, Any


def initialize_system() -> Dict[str, Any]:
    """
    Initialize all system components with validation.
    
    Returns:
        dict: Initialized components and metadata
        
    Raises:
        ImportError: If required modules cannot be imported
        ValueError: If configuration validation fails
    """
    try:
        from WeatherDashboard import config, get_package_info
        from WeatherDashboard.utils.logger import Logger
        from WeatherDashboard.gui.main_window import WeatherDashboardMain

    except ImportError as e:
        print(f"Failed to import required modules: {e}")
        print("Please ensure WeatherDashboard package is properly installed.")
        sys.exit(1)
    
    Logger.info("Initializing Weather Dashboard application...")

    # Initialize directories and validate configurations
    config.ensure_directories()
    config.validate_config()
    
    # Test logging system and warn if issues
    if not Logger.test_logging_health():
        print("Warning: Logging system health check failed")

    package_info = get_package_info()
    Logger.info(f"Starting {package_info['name']} v{package_info['version']}: "
                f"{package_info['description']} created by {package_info['author']}")

    return {
        'WeatherDashboardMain': WeatherDashboardMain,
        'Logger': Logger,
        'package_info': package_info
    }

def create_and_run_gui(components: Dict[str, Any]) -> None:
    """
    Create GUI and start the main event loop.
    
    Args:
        components (dict): Initialized system components
        
    Raises:
        tk.TclError: If GUI creation fails
    """
    root = None
    try:
        root = tk.Tk()
        root.title("Weather Dashboard")

        app = components['WeatherDashboardMain'](root)
        app.load_initial_display()
        root.mainloop()
    finally:
        # Check if root was created before cleanup
        if root is not None:
            cleanup_gui_resources(root)

def cleanup_gui_resources(root: tk.Tk) -> None:
    """Safely cleanup GUI resources."""
    try:
        if root and root.winfo_exists():
            root.destroy()
    except Exception:
        pass  # Ignore cleanup errors


def main() -> None:
    """
    Main application entry point with comprehensive error handling.
    
    Orchestrates the application startup by calling initialization functions
    and starting the GUI event loop. All actual initialization work is 
    delegated to helper functions.
    
    Error Handling:
    - Import errors: Handled in initialize_system(), exits before reaching main()
    - Configuration errors: Shows specific error messages with guidance
    - GUI creation errors: Falls back to console error reporting  
    - User interruption: Graceful shutdown message
    - Runtime errors: Logs errors when possible and attempts graceful shutdown
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    
    Raises:
        SystemExit: Always exits after completion or error
    """
    # Try to get Logger for error logging, but don't fail if unavailable
    Logger = None
    try:
        from WeatherDashboard.utils.logger import Logger
    except ImportError as e:
        print(f"Failed to import required modules: {e}")
        sys.exit(1)

    try:
        # Initialize all system components
        components = initialize_system()
        
        # Create and run GUI
        create_and_run_gui(components)
        
        # Exit successfully after GUI closes
        sys.exit(0)

    except ValueError as e:
        if Logger:
            Logger.error(f"Configuration error: {e}")
        print(f"Configuration error: {e}\n")
        print("Please check your configuration and try again.")
        sys.exit(1)
    except tk.TclError as e:
        if Logger:
            Logger.error(f"GUI creation failed: {e}")
        print(f"Failed to create GUI window: {e}")
        print("Please ensure display environment is properly configured.")
        sys.exit(1)
    except KeyboardInterrupt:
        if Logger:
            Logger.info("Application interrupted by user")
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        if Logger:
            Logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()