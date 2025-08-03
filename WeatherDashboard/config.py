"""
Configuration settings for the Weather Dashboard application.

This module centralizes all configuration constants, default values, API settings,
UI display mappings, unit definitions, alert thresholds, and application-wide
constants. Provides a single source of truth for all configurable aspects of
the Weather Dashboard.

Configuration Categories:
    API: OpenWeatherMap API configuration
    METRICS: Unified metric definitions with visibility settings
    CHART: Chart display and data range settings
    UNITS: Unit system definitions and conversions
    ALERT_THRESHOLDS: Weather alert threshold configuration
    DEFAULTS: Default values for UI components and application settings
    OUTPUT: File paths and logging configuration
    
Functions:
    validate_config: Comprehensive configuration validation
"""

import os
from pathlib import Path

# centralizing config info
# Lazy loading for alert configuration to avoid circular dependencies
def _get_alert_config():
    """Lazy load alert configuration to avoid circular dependencies."""
    try:
        from WeatherDashboard.features.alerts.alert_config import ALERT_THRESHOLDS, ALERT_PRIORITY_ORDER, ALERT_DEFINITIONS
        return ALERT_THRESHOLDS, ALERT_PRIORITY_ORDER, ALERT_DEFINITIONS
    except ImportError as e:
        print(f"Warning: Alert configuration not available: {e}")
        return {}, [], {}

# Initialize with empty defaults
ALERT_THRESHOLDS, ALERT_PRIORITY_ORDER, ALERT_DEFINITIONS = _get_alert_config()

# ================================
# 1. API & ENVIRONMENT CONFIGURATION  
# ================================
# Attempt to load environment variables from a .env file
# This accounts for error if 'dotenv' is not installed (like on github actions testing)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: 'dotenv' not found. Skipping .env loading.")

# API Configuration
API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_UV_URL = "https://api.openweathermap.org/data/2.5/uvi"
API_AIR_QUALITY_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # load from .env
API_TIMEOUT_SECONDS = 10 # Configurable timeout for API requests
API_RETRY_ATTEMPTS = 2 # API Service constants
API_RETRY_BASE_DELAY = 1
FORCE_FALLBACK_MODE = False # Temporarily disable API calls

# ================================
# 2. CORE WEATHER METRICS DEFINITIONS
# ================================
# Unified Metric Definitions
METRICS = {
    # Original metrics
    'temperature': {'label': 'Temperature', 'visible': True, 'chartable': True},
    'humidity': {'label': 'Humidity', 'visible': True, 'chartable': True},
    'wind_speed': {'label': 'Wind Speed', 'visible': False, 'chartable': True},
    'pressure': {'label': 'Pressure', 'visible': False, 'chartable': True},
    'conditions': {'label': 'Conditions', 'visible': False, 'chartable': False},
    
    # New metrics (all initially hidden)
    'feels_like': {'label': 'Feels Like', 'visible': False, 'chartable': True},
    'temp_min': {'label': 'Min Temp', 'visible': False, 'chartable': True},
    'temp_max': {'label': 'Max Temp', 'visible': False, 'chartable': True},
    'wind_direction': {'label': 'Wind Direction', 'visible': False, 'chartable': False},
    'wind_gust': {'label': 'Wind Gusts', 'visible': False, 'chartable': False},
    'visibility': {'label': 'Visibility', 'visible': False, 'chartable': True},
    'cloud_cover': {'label': 'Cloud Cover', 'visible': False, 'chartable': True},
    'rain': {'label': 'Rain', 'visible': False, 'chartable': True},
    'snow': {'label': 'Snow', 'visible': False, 'chartable': True},
    'weather_main': {'label': 'Weather Type', 'visible': False, 'chartable': False},
    'weather_id': {'label': 'Weather ID', 'visible': False, 'chartable': False},
    'weather_icon': {'label': 'Weather Icon', 'visible': False, 'chartable': False},

    # New new metrics
    'uv_index': {'label': 'UV Index', 'visible': False, 'chartable': True},
    'air_quality_index': {'label': 'Air Quality', 'visible': False, 'chartable': True},
    'air_quality_description': {'label': 'Air Quality Status', 'visible': False, 'chartable': True},

    # Derived comfort metrics
    'heat_index': {'label': 'Heat Index', 'visible': False, 'chartable': True},
    'wind_chill': {'label': 'Wind Chill', 'visible': False, 'chartable': True},
    'dew_point': {'label': 'Dew Point', 'visible': False, 'chartable': True},
    'precipitation_probability': {'label': 'Rain Chance', 'visible': False, 'chartable': True},
    'weather_comfort_score': {'label': 'Comfort Score', 'visible': False, 'chartable': True}
}

# Metric Organization for UI Components
METRIC_GROUPS = {
    'core_weather': {
        'label': 'Core Weather',
        'display_metrics': ['temperature', 'humidity', 'conditions', 'weather_comfort_score'],
        'chart_metrics': ['temperature', 'humidity', 'weather_comfort_score']  # conditions not chartable
    },
    'temperature_details': {
        'label': 'Temperature Details', 
        'display_metrics': ['temp_min', 'heat_index', 'wind_chill', 'dew_point'],  # Temp_min shows as "Today's Range" 
        'chart_metrics': ['feels_like', 'temp_min', 'temp_max', 'heat_index', 'wind_chill', 'dew_point'] # Individual for charting
    },
    'wind_atmosphere': {
        'label': 'Air & Atmosphere',
        'display_metrics': ['wind_speed', 'pressure', 'visibility', 'cloud_cover', 'uv_index', 'air_quality_description'],
        'chart_metrics': ['wind_speed', 'wind_direction', 'wind_gust', 'pressure', 'visibility', 'cloud_cover', 'uv_index', 'air_quality_index']
    },
    'precipitation': {
        'label': 'Precipitation',
        'display_metrics': ['rain', 'snow', 'precipitation_probability'],  # Rain/snow shows as "Current Precipitation"
        'chart_metrics': ['rain', 'snow', 'precipitation_probability']  # Individual for charting
    }
}

# Enhanced display mappings for when metrics are combined
ENHANCED_DISPLAY_LABELS = {
    'temperature': 'Temperature (with feels-like)',
    'temp_min': "Today's Range (min/max)", 
    'wind_speed': 'Wind (speed & direction)',
    'conditions': 'Conditions (with icon)'
}

# NWS Standard Formula Thresholds
HEAT_INDEX_THRESHOLD_F = 80
WIND_CHILL_TEMP_THRESHOLD_F = 50
WIND_CHILL_SPEED_THRESHOLD_MPH = 3

# Feels like display thresholds
TEMP_DIFF_THRESHOLD_METRIC = 2.0  # °C
TEMP_DIFF_THRESHOLD_IMPERIAL = 3.6  # °F

# ================================
# 3. UNITS & MEASUREMENT SYSTEMS
# ================================
# Metric Units Mapping
UNITS = {
    'metric_units': {
        # Original metric units
        'temperature': {'imperial': '°F', 'metric': '°C'},
        'humidity': {'imperial': '%', 'metric': '%'},
        'pressure': {'imperial': 'inHg', 'metric': 'hPa'},
        'wind_speed': {'imperial': 'mph', 'metric': 'm/s'},
        'conditions': {'imperial': 'Category', 'metric': 'Category'},
        
        # New metric unit definitions
        'feels_like': {'imperial': '°F', 'metric': '°C'},
        'temp_min': {'imperial': '°F', 'metric': '°C'},
        'temp_max': {'imperial': '°F', 'metric': '°C'},
        'wind_direction': {'imperial': '°', 'metric': '°'},
        'wind_gust': {'imperial': 'mph', 'metric': 'm/s'},
        'visibility': {'imperial': 'mi', 'metric': 'km'},
        'cloud_cover': {'imperial': '%', 'metric': '%'},
        'rain': {'imperial': 'in', 'metric': 'mm'},
        'snow': {'imperial': 'in', 'metric': 'mm'},
        'weather_main': {'imperial': 'Category', 'metric': 'Category'},
        'weather_id': {'imperial': 'ID', 'metric': 'ID'},
        'weather_icon': {'imperial': 'Icon', 'metric': 'Icon'},

        # New new metric unit definitions
        'uv_index': {'imperial': 'Index', 'metric': 'Index'},
        'air_quality_index': {'imperial': 'AQI', 'metric': 'AQI'},
        'air_quality_description': {'imperial': 'Status', 'metric': 'Status'},

        # Derived metrics unit definitions
        'heat_index': {'imperial': '°F', 'metric': '°C'},
        'wind_chill': {'imperial': '°F', 'metric': '°C'},
        'dew_point': {'imperial': '°F', 'metric': '°C'},
        'precipitation_probability': {'imperial': '%', 'metric': '%'},
        'weather_comfort_score': {'imperial': 'Score', 'metric': 'Score'}
    }
}

# Historical Data Range Options and Chart Display Values
CHART = {
    "range_options": {
        'Last 7 Days': 7,
        'Last 14 Days': 14,
        'Last 30 Days': 30
    },
    'chart_figure_width_ratio': 0.8,   # 80% of parent width
    'chart_figure_height_ratio': 0.6,  # 60% of parent height
    'chart_figure_min_width': 4,       # Minimum width in inches
    'chart_figure_min_height': 2,      # Minimum height in inches
    'chart_dpi': 100,                  # Chart resolution in DPI
    'chart_rotation_degrees': 45       # X-axis label rotation angle
}

# ================================
# 5. APPLICATION DEFAULTS
# ================================
# Control Frame Defaults
DEFAULTS = {
    "city": os.getenv("DEFAULT_CITY", "New York"), # load from .env
    "unit": os.getenv("DEFAULT_UNIT", "imperial"), # load from .env
    "range": "Last 7 Days",
    "chart": "Temperature",
    "visibility": {k: v['visible'] for k, v in METRICS.items()}, # Generate visibility defaults from METRICS configuration
    "alert_thresholds": ALERT_THRESHOLDS 
}

# ================================
# 6. SYSTEM CONFIGURATION
# ================================
# Output Files & Directories
PACKAGE_DIR = Path(__file__).parent
DATA_DIR = PACKAGE_DIR / "data"
LOGS_DIR = PACKAGE_DIR / "logs"

OUTPUT = {
    "log_dir": str(LOGS_DIR),
    "data_dir": str(DATA_DIR), 
    "text_file": str(DATA_DIR / "output.txt"),
    "csv_dir": str(DATA_DIR / "csv"),  # WeatherDashboard/data/csv/
    "csv_filename": "weather_data.csv",
    "csv_backup_dir": str(DATA_DIR / "csv" / "backup")  # For archived data
}

def ensure_directories() -> bool:
    """
    Create required directories if they don't exist.

    Side Effects:
        Creates data and logs directories if missing.
        
    Returns:
        bool: True if directories exist or were created.
    """
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT["csv_dir"], exist_ok=True)
    os.makedirs(OUTPUT["csv_backup_dir"], exist_ok=True)
    return True # for validation

MEMORY = {
    "max_cities_stored": 50,            # Maximum number of cities to keep in memory
    "max_entries_per_city": 30,         # Maximum weather entries per city (existing)
    "max_total_entries": 1000,          # Global maximum entries across all cities
    "cleanup_interval_hours": 24,       # Hours between automatic cleanup (existing)
    "minimum_cleanup_interval": 3600,    # 1 hour minimum
    "aggressive_cleanup_threshold": 0.8,  # Trigger aggressive cleanup at 80% of limits
    "max_alert_history_size": 100       # Alert system constant
}

SCHEDULER = {
    "enabled": True,                    # Master switch for auto-collection
    "default_interval_minutes": 15,     # Default collection interval
    "error_threshold": 5,               # Consecutive failures before notification
    "retry_attempts": 3,                # Retry failed fetches
    "retry_delay_seconds": 60,          # Wait between retries
    "quiet_hours": {                    # Reduce frequency during off-hours
        "start": "22:00",
        "end": "06:00",
        "interval_multiplier": 2.0      # Double the interval during quiet hours
    }
}

ERROR_MESSAGES = {
    'validation': "{field} is invalid: {reason}",
    'missing': "{field} is required but not provided",
    'not_found': "{resource} '{name}' not found",
    'conversion': "Failed to convert {field} from {from_unit} to {to_unit}: {reason}",
    'api_error': "API request failed for {endpoint}: {reason}",
    'config_error': "Configuration error in {section}: {reason}",
    'file_error': "Failed to write {info} to {file}: {reason}",
    'state_error': "Invalid state: {reason}",
    'directory_error': "Directory operation failed for {path}: {reason}",
    'initialization_error': "Initialization failed for {component}: {reason}",
    'structure_error': "Invalid structure in {section}: {reason}"
}

# ================================
# 7. CONFIGURATION VALIDATION
# ================================
def validate_config() -> None:
    """Validate essential configuration requirements for application startup.
    
    Raises:
        ValueError: If any critical configuration is invalid or missing
        
    Side Effects:
        Creates data directory if it doesn't exist
        Prints warning messages for API key issues
    """
    # Check critical API configuration
    if not API_KEY:
        print("Warning: No API key found. Application will use fallback data only.")
    elif len(API_KEY.strip()) < 10:  # Basic length check
        print("Warning: API key appears invalid. Application may fail to fetch live data.")
    
    # Validate essential structures exist
    required_sections = ['METRICS', 'DEFAULTS', 'UNITS', 'CHART', 'OUTPUT', 'ALERT_THRESHOLDS', 'MEMORY']
    for section in required_sections:
        if section not in globals():
            raise ValueError(ERROR_MESSAGES['config_error'].format(
                section=section, 
                reason="required configuration section missing"
            ))
    
    # Validate METRICS structure
    if not isinstance(METRICS, dict) or not METRICS:
        raise ValueError(ERROR_MESSAGES['config_error'].format(
            section="METRICS", 
            reason="must be a non-empty dictionary"
        ))
    
    # Sample check for metric structure
    sample_metric = next(iter(METRICS.values()))
    if not isinstance(sample_metric, dict) or 'label' not in sample_metric or 'visible' not in sample_metric:
        raise ValueError(ERROR_MESSAGES['config_error'].format(
            section="METRICS structure", 
            reason="missing required 'label' or 'visible' fields"
        ))
    
    # Validate critical DEFAULTS
    if DEFAULTS.get('unit') not in ['metric', 'imperial']:
        raise ValueError(ERROR_MESSAGES['validation'].format(
            field="Default unit system", 
            reason=f"'{DEFAULTS.get('unit')}' is invalid. Must be 'metric' or 'imperial'"
        ))
    
    # Validate essential file paths exist
    try:
        os.makedirs(OUTPUT.get("data_dir", "data"), exist_ok=True)
    except (OSError, TypeError) as e:
        raise ValueError(ERROR_MESSAGES['config_error'].format(
            section="output directories", 
            reason=f"cannot create or access data directory: {e}"
        ))
    
    # Validate memory configuration is reasonable
    memory_keys = ['max_cities_stored', 'max_entries_per_city', 'max_total_entries', 'cleanup_interval_hours']
    for key in memory_keys:
        value = MEMORY.get(key, 0)
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(ERROR_MESSAGES['validation'].format(
                field=f"Memory configuration '{key}'", 
                reason="must be a positive number"
            ))

    # Validation for cleanup threshold (should be between 0 and 1)
    threshold = MEMORY.get('aggressive_cleanup_threshold', 0)
    if not isinstance(threshold, (int, float)) or not (0 < threshold <= 1):
        raise ValueError(ERROR_MESSAGES['validation'].format(
            field="Aggressive cleanup threshold", 
            reason="must be a number between 0 and 1"
        ))
    
    # Validate Alert Config
    try:
        from WeatherDashboard.features.alerts.alert_config import ALERT_DEFINITIONS, validate_alert_config
        validate_alert_config()
    except ImportError:
        print("Warning: Alert configuration validation skipped - module not available")

    # Validate alert unit types match available metrics
    available_unit_types = set(UNITS['metric_units'].keys())
    for alert_type, definition in ALERT_DEFINITIONS.items():
        unit_type = definition.get('unit_type')
        if unit_type not in available_unit_types:
            raise ValueError(ERROR_MESSAGES['validation'].format(
                field=f"Alert unit_type '{unit_type}' in '{alert_type}'", 
                reason=f"must be one of: {sorted(available_unit_types)}"
            ))
    
    return True