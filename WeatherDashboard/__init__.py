"""
Weather Dashboard Package

A satirical weather dashboard application with humorous commentary
and theme-based error messaging.

Requirements:
    - Python: 3.8+
    - Critical Dependencies: tkinter, requests, python-dotenv (optional)
    - Platform: Cross-platform (Windows, macOS, Linux with GUI support)

Main Components:
    - Core: Application controllers, data managers, and view models
    - Services: Weather API integration and error handling
    - Gui: Coordination of all user interface components
    - Widgets: Specialized UI widget implementations 
    - Utils: Utility functions, logging, unit conversion, etc
    - Features: Satirical themes and other specialized functionality

Usage:
    from WeatherDashboard.main import main
    main()

    Or run directly:
    python -m WeatherDashboard.main

Configuration:
    - Set OPENWEATHER_API_KEY in environment or .env file
    - Optional: Set DEFAULT_CITY, DEFAULT_UNIT for customization
"""

from typing import Dict

# Package metadata
__version__ = "0.4.1"
__author__ = "Jacob Schwartz"
__email__ = "schwarja209@gmail.com"
__description__ = "A satirical weather dashboard"

# Package-level imports for convenience
try:
    from . import config
    from . import styles
    _imports_successful = True # Imports successful - config and styles available at package level
except ImportError as e:
    print(f"Failed to import required modules: {e}")
    print("Please ensure WeatherDashboard package is properly installed.")
    _imports_successful = False # Import errors during setup/installation - modules not available

# Ensure backward compatibility
__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "__description__",
    "get_version",
    "get_package_info",
]

# Add config and styles only if imports succeeded
if _imports_successful:
    __all__.extend(["config", "styles"])

def get_version() -> str:
    """Return the package version string."""
    return __version__

def get_package_info() -> Dict[str, str]:
    """Return comprehensive package information dictionary."""
    return {
        "name": "WeatherDashboard",
        "version": __version__,
        "author": __author__,
        "email": __email__,
        "description": __description__,
    }