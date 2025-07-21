"""
Weather Dashboard Package

A satirical weather dashboard application with humorous commentary
and theme-based error messaging.

This package provides a complete weather dashboard application with:
- Real-time weather data from OpenWeatherMap API
- Fallback synthetic data when API is unavailable
- Satirical weather commentary and themed messaging
- Comprehensive error handling and logging
- Unit conversion and localization
- Alert system for weather conditions
- Historical data tracking and visualization

Main Components:
- Core: Application controllers, data managers, and view models
- Services: Weather API integration and error handling
- Utils: Utility functions, logging, and unit conversion
- Widgets: GUI components and user interface
- Features: Satirical themes and advanced functionality

Usage:
    from WeatherDashboard.main import main
    main()

    Or run directly:
    python -m WeatherDashboard.main
"""

# Package metadata
__version__ = "0.1.0"
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


# Package initialization
def _initialize_package():
    """Initialize package-level settings and create required directories.
    
    Creates logs and data directories within the package, sets up .gitkeep files
    for version control, and suppresses matplotlib warnings. Handles directory
    creation errors gracefully to prevent import failures during installation.
    """
    import os
    import warnings
    
    # Suppress specific warnings that might occur during import
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="matplotlib")
    
    # Ensure required directories exist
    package_dir = os.path.dirname(os.path.abspath(__file__))
    required_dirs = ["logs", "data"]
    
    for dir_name in required_dirs:
        dir_path = os.path.join(package_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        
        # Create .gitkeep files to ensure directories are tracked in git
        gitkeep_path = os.path.join(dir_path, ".gitkeep")
        if not os.path.exists(gitkeep_path):
            try:
                with open(gitkeep_path, 'w') as f:
                    f.write("# Keep this directory in git\n")
            except OSError:
                pass  # Ignore if we can't create the file


# Initialize package when imported
try:
    _initialize_package()
except Exception:
    # Don't let initialization errors prevent import
    pass