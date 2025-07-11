"""
Configuration settings for the Weather Dashboard application.

This module centralizes all configuration constants, default values, API settings,
UI display mappings, unit definitions, alert thresholds, and application-wide
constants. Provides a single source of truth for all configurable aspects of
the Weather Dashboard with validation and derived value generation.

Configuration Categories:
    API: OpenWeatherMap API configuration
    METRICS: Unified metric definitions with visibility settings
    CHART: Chart display and data range settings
    UNITS: Unit system definitions and conversions
    ALERT_THRESHOLDS: Weather alert threshold configuration
    DEFAULTS: Default values for UI components and application settings
    OUTPUT: File paths and logging configuration
    
Functions:
    get_key_to_display_mapping: Generate display labels from metrics
    get_display_to_key_mapping: Generate key lookup from display labels
    get_default_visibility: Generate default visibility settings
    validate_config: Comprehensive configuration validation
"""

import os
from pathlib import Path

# ================================
# 1. ENVIRONMENT LOADING
# ================================
# Attempt to load environment variables from a .env file
# This accounts for error if 'dotenv' is not installed (like on github actions testing)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: 'dotenv' not found. Skipping .env loading.")

# ================================
# 2. CORE CONFIGURATION VALUES
# ================================
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

# NEW: Alert Threshold Configuration
ALERT_THRESHOLDS = {
    'temperature_high': 35.0,      # °C - Hot weather warning
    'temperature_low': -10.0,      # °C - Cold weather warning  
    'wind_speed_high': 15.0,       # m/s - High wind warning
    'pressure_low': 980.0,         # hPa - Storm system warning
    'humidity_high': 85.0,         # % - High humidity discomfort
    'humidity_low': 15.0,          # % - Low humidity warning
}

# ================================
# 3. DERIVED VALUES (backward compatibility)
# ================================
def get_key_to_display_mapping():
    """Generate display labels from metrics configuration.
    
    Returns:
        Dict[str, str]: Mapping from metric keys to display labels
    """
    try:
        return {k: v['label'] for k, v in METRICS.items()}
    except (KeyError, TypeError, AttributeError) as e:
        print(f"Error creating key to display mapping: {e}")
        return {}  # Return empty dict as fallback

def get_display_to_key_mapping():
    """Generate key lookup from display labels.
    
    Returns:
        Dict[str, str]: Mapping from display labels to metric keys
    """
    try:
        return {v['label']: k for k, v in METRICS.items()}
    except (KeyError, TypeError, AttributeError) as e:
        print(f"Error creating display to key mapping: {e}")
        return {}  # Return empty dict as fallback

def get_default_visibility():
    """Generate default visibility settings from metrics configuration.
    
    Returns:
        Dict[str, bool]: Mapping from metric keys to default visibility states
    """
    try:
        return {k: v['visible'] for k, v in METRICS.items()}
    except (KeyError, TypeError, AttributeError) as e:
        print(f"Error creating default visibility: {e}")
        return {}  # Return empty dict as fallback

# Derive visibility and label maps for internal use
KEY_TO_DISPLAY = get_key_to_display_mapping()
DISPLAY_TO_KEY = get_display_to_key_mapping()
DEFAULT_VISIBILITY = get_default_visibility()

# ================================
# 4. DEFAULTS (backward compatibility with original variable names)
# ================================
# Control Frame Defaults
DEFAULTS = {
    "city": "New York",
    "unit": "imperial",
    "range": "Last 7 Days",
    "chart": "Temperature",
    "visibility": DEFAULT_VISIBILITY,
    "alert_thresholds": ALERT_THRESHOLDS 
}

# ================================
# 5. FILE PATHS
# ================================
# Output Files & Directories
base_dir = Path(__file__).parent
data_dir = base_dir / "data"

OUTPUT = {
    "data_dir": str(data_dir),
    "log_dir": str(data_dir), 
    "log": str(data_dir / "output.txt")
}

# ================================
# 6. CONFIGURATION VALIDATION
# ================================
def validate_config() -> None:
    """Validate that all required configuration keys exist and have expected structure.
    
    Performs comprehensive validation of all configuration sections including
    METRICS, DEFAULTS, UNITS, CHART, OUTPUT, and ALERT_THRESHOLDS structures.
    
    Raises:
        ValueError: If any configuration is invalid or missing required keys
    """
    # Check METRICS structure
    for metric_key, metric_data in METRICS.items():
        if not isinstance(metric_data, dict):
            raise ValueError(f"METRICS['{metric_key}'] must be a dictionary")
        if 'label' not in metric_data or 'visible' not in metric_data:
            raise ValueError(f"Invalid METRICS structure for '{metric_key}' - missing 'label' or 'visible'")
        if not isinstance(metric_data['visible'], bool):
            raise ValueError(f"METRICS['{metric_key}']['visible'] must be boolean")
    
    # Check DEFAULTS structure
    required_default_keys = ['city', 'unit', 'range', 'chart', 'visibility', 'alert_thresholds']
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
        
    # Validate alert thresholds
    if not isinstance(ALERT_THRESHOLDS, dict):
        raise ValueError("ALERT_THRESHOLDS must be a dictionary")
    
    required_thresholds = ['temperature_high', 'temperature_low', 'wind_speed_high', 'pressure_low']
    for threshold in required_thresholds:
        if threshold not in ALERT_THRESHOLDS:
            raise ValueError(f"Missing required alert threshold: '{threshold}'")
        if not isinstance(ALERT_THRESHOLDS[threshold], (int, float)):
            raise ValueError(f"Alert threshold '{threshold}' must be a number")
    
    # Check API key
    if not API_KEY:
        print("Warning: No API key found. Application will use fallback data only.")
    
    print("Configuration validation passed successfully.")