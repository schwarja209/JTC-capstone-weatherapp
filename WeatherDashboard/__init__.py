"""
Weather Dashboard Package

A satirical weather dashboard application with humorous commentary
and theme-based error messaging.

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
"""

# Package metadata
__version__ = "0.2.1"
__author__ = "Jacob Schwartz"
__email__ = "schwarja209@gmail.com"
__description__ = "A satirical weather dashboard"

# Package-level imports for convenience
try:
    from . import config
    from . import styles
    # Imports successful - config and styles available at package level
except ImportError:
    # Import errors during setup/installation - modules not available
    pass

# Ensure backward compatibility
__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "__description__",
    "config",
    "styles",
]

def get_version():
    """Return the package version string."""
    return __version__

def get_package_info():
    """Return comprehensive package information dictionary."""
    return {
        "name": "WeatherDashboard",
        "version": __version__,
        "author": __author__,
        "email": __email__,
        "description": __description__,
    }