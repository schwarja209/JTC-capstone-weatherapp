"""
Default/static data configuration for the Weather Dashboard application.
"""

import os
from pathlib import Path

# ================================
# 1. ENVIRONMENT LOADING (separate concern)
# ================================
class EnvironmentLoader:
    """Handles loading environment variables from .env files."""
    
    @staticmethod
    def load_environment():
        """Attempts to load environment variables from .env file."""
        # Attempt to load environment variables from a .env file
        # This accounts for error if 'dotenv' is not installed (like on github actions testing)
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            print("Warning: 'dotenv' not found. Skipping .env loading.")

# Load environment at import time
EnvironmentLoader.load_environment()

# ================================
# 2. CORE CONFIGURATION VALUES (separate concern)
# ================================
class WeatherDashboardConfig:
    """Core configuration values for the application."""
    
    # API Configuration
    API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    API_KEY = os.getenv("OPENWEATHER_API_KEY")  # load from .env
    
    # Unified Metric Definitions
    METRICS = {
        'temperature': {'label': 'Temperature', 'visible': True},
        'humidity': {'label': 'Humidity', 'visible': True},
        'wind_speed': {'label': 'Wind Speed', 'visible': False},
        'pressure': {'label': 'Pressure', 'visible': False},
        'conditions': {'label': 'Conditions', 'visible': False},
    }
    
    # Historical Data Range Options
    CHART = {
        "range_options": {
            'Last 7 Days': 7,
            'Last 14 Days': 14,
            'Last 30 Days': 30
        }
    }
    
    # Metric Units Mapping
    UNITS = {
        'metric_units': {
            'temperature': {'imperial': '°F', 'metric': '°C'},
            'humidity': {'imperial': '%', 'metric': '%'},
            'pressure': {'imperial': 'inHg', 'metric': 'hPa'},
            'wind_speed': {'imperial': 'mph', 'metric': 'm/s'},
            'conditions': {'imperial': 'Category', 'metric': 'Category'}
            # 'precipitation': {'imperial': 'in', 'metric': 'mm'}  # Your original commented line preserved
        }
    }

# ================================
# 3. DERIVED VALUES MANAGER (separate concern)
# ================================
class ConfigDerivedValues:
    """Manages values derived from core configuration."""
    
    @staticmethod
    def get_key_to_display_mapping():
        """Derives display labels from metrics configuration."""
        return {k: v['label'] for k, v in WeatherDashboardConfig.METRICS.items()}
    
    @staticmethod
    def get_display_to_key_mapping():
        """Derives key lookup from display labels."""
        return {v['label']: k for k, v in WeatherDashboardConfig.METRICS.items()}
    
    @staticmethod
    def get_default_visibility():
        """Derives default visibility settings from metrics."""
        return {k: v['visible'] for k, v in WeatherDashboardConfig.METRICS.items()}

# ================================
# 4. DEFAULTS MANAGER (separate concern)
# ================================
class DefaultsManager:
    """Manages default values for the application."""
    
    @staticmethod
    def get_defaults():
        """Returns all default values for the application."""
        # Control Frame Defaults
        return {
            "city": "New York",
            "unit": "imperial",
            "range": "Last 7 Days",
            "chart": "Temperature",
            "visibility": ConfigDerivedValues.get_default_visibility()
        }

# ================================
# 5. FILE PATHS MANAGER (separate concern)
# ================================
class FilePathsManager:
    """Manages file paths and directories for the application."""
    
    @staticmethod
    def get_output_paths():
        """Returns all output file paths and directories."""
        # Output Files & Directories
        base_dir = Path(__file__).parent
        data_dir = base_dir / "data"
        
        return {
            "data_dir": str(data_dir),
            "log_dir": str(data_dir), 
            "log": str(data_dir / "output.txt")
        }

# ================================
# 6. CONFIGURATION VALIDATOR (separate concern)
# ================================
class ConfigValidator:
    """Validates configuration integrity and structure."""
    
    @staticmethod
    def validate_config():
        """Validates that all required configuration keys exist and have expected structure."""
        import sys
        current_module = sys.modules[__name__]
        
        # Check required top-level keys exist as module attributes
        required_keys = ['METRICS', 'DEFAULTS', 'CHART', 'UNITS', 'OUTPUT']
        for key in required_keys:
            if not hasattr(current_module, key):
                raise ValueError(f"Missing required config key: {key}")
        
        # Check METRICS structure
        for metric_key, metric_data in METRICS.items():
            if not isinstance(metric_data, dict):
                raise ValueError(f"METRICS['{metric_key}'] must be a dictionary")
            if 'label' not in metric_data or 'visible' not in metric_data:
                raise ValueError(f"Invalid METRICS structure for '{metric_key}' - missing 'label' or 'visible'")
            if not isinstance(metric_data['visible'], bool):
                raise ValueError(f"METRICS['{metric_key}']['visible'] must be boolean")
        
        # Check DEFAULTS structure
        required_default_keys = ['city', 'unit', 'range', 'chart', 'visibility']
        for key in required_default_keys:
            if key not in DEFAULTS:
                raise ValueError(f"Missing required DEFAULTS key: '{key}'")
        
        # Validate unit system in defaults
        if DEFAULTS['unit'] not in ['metric', 'imperial']:
            raise ValueError(f"Invalid default unit system: '{DEFAULTS['unit']}' - must be 'metric' or 'imperial'")
        
        # Check UNITS structure
        if 'metric_units' not in UNITS:
            raise ValueError("Missing 'metric_units' in UNITS config")
        
        # Validate each metric in UNITS has both metric and imperial units
        for metric_key in METRICS.keys():
            if metric_key not in UNITS['metric_units']:
                raise ValueError(f"Missing unit definition for metric '{metric_key}' in UNITS config")
            
            metric_units = UNITS['metric_units'][metric_key]
            if not isinstance(metric_units, dict):
                raise ValueError(f"UNITS['metric_units']['{metric_key}'] must be a dictionary")
            
            for unit_system in ['metric', 'imperial']:
                if unit_system not in metric_units:
                    raise ValueError(f"Missing '{unit_system}' unit for metric '{metric_key}'")
        
        # Check CHART structure
        if 'range_options' not in CHART:
            raise ValueError("Missing 'range_options' in CHART config")
        
        if not isinstance(CHART['range_options'], dict):
            raise ValueError("CHART['range_options'] must be a dictionary")
        
        # Validate range options are positive integers
        for range_name, days in CHART['range_options'].items():
            if not isinstance(days, int) or days <= 0:
                raise ValueError(f"CHART range option '{range_name}' must be a positive integer, got: {days}")
        
        # Check OUTPUT structure
        required_output_keys = ['data_dir', 'log_dir', 'log']
        for key in required_output_keys:
            if key not in OUTPUT:
                raise ValueError(f"Missing required OUTPUT key: '{key}'")
        
        # Check API key
        if not API_KEY:
            print("Warning: No API key found. Application will use fallback data only.")
        
        print("Configuration validation passed successfully.")

# ================================
# 7. PUBLIC API (backward compatibility with original variable names)
# ================================
# Expose the same interface as before for backward compatibility:

# API Configuration
API_BASE_URL = WeatherDashboardConfig.API_BASE_URL
API_KEY = WeatherDashboardConfig.API_KEY

# Unified Metric Definitions
METRICS = WeatherDashboardConfig.METRICS

# Derive visibility and label maps for internal use
KEY_TO_DISPLAY = ConfigDerivedValues.get_key_to_display_mapping()
DISPLAY_TO_KEY = ConfigDerivedValues.get_display_to_key_mapping()
DEFAULT_VISIBILITY = ConfigDerivedValues.get_default_visibility()

# Control Frame Defaults
DEFAULTS = DefaultsManager.get_defaults()

# Historical Data Range Options
CHART = WeatherDashboardConfig.CHART

# Metric Units Mapping
UNITS = WeatherDashboardConfig.UNITS

# Output Files & Directories
OUTPUT = FilePathsManager.get_output_paths()

def validate_config():
    """Validates that all required configuration keys exist and have expected structure."""
    return ConfigValidator.validate_config()

# Validate configuration on import
validate_config()