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

# ================================
# 2. CORE WEATHER METRICS DEFINITIONS
# ================================
# Unified Metric Definitions
METRICS = {
    # Original metrics
    'temperature': {'label': 'Temperature', 'visible': True},
    'humidity': {'label': 'Humidity', 'visible': True},
    'wind_speed': {'label': 'Wind Speed', 'visible': False},
    'pressure': {'label': 'Pressure', 'visible': False},
    'conditions': {'label': 'Conditions', 'visible': False},
    
    # New metrics (all initially hidden)
    'feels_like': {'label': 'Feels Like', 'visible': False},
    'temp_min': {'label': 'Min Temp', 'visible': False},
    'temp_max': {'label': 'Max Temp', 'visible': False},
    'wind_direction': {'label': 'Wind Direction', 'visible': False},
    'wind_gust': {'label': 'Wind Gusts', 'visible': False},
    'visibility': {'label': 'Visibility', 'visible': False},
    'cloud_cover': {'label': 'Cloud Cover', 'visible': False},
    'rain': {'label': 'Rain', 'visible': False},
    'snow': {'label': 'Snow', 'visible': False},
    'weather_main': {'label': 'Weather Type', 'visible': False},
    'weather_id': {'label': 'Weather ID', 'visible': False},
    'weather_icon': {'label': 'Weather Icon', 'visible': False},

    # New new metrics
    'uv_index': {'label': 'UV Index', 'visible': False},
    'air_quality_index': {'label': 'Air Quality', 'visible': False},
    'air_quality_description': {'label': 'Air Quality Status', 'visible': False},

    # Derived comfort metrics
    'heat_index': {'label': 'Heat Index', 'visible': False},
    'wind_chill': {'label': 'Wind Chill', 'visible': False},
    'dew_point': {'label': 'Dew Point', 'visible': False},
    'precipitation_probability': {'label': 'Rain Chance', 'visible': False},
    'weather_comfort_score': {'label': 'Comfort Score', 'visible': False}
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

# Historical Data Range Options
CHART = {
    "range_options": {
        'Last 7 Days': 7,
        'Last 14 Days': 14,
        'Last 30 Days': 30
    }
}

# ====================================
# 4. ALERTS CONFIGURATION & THRESHOLDS
# ====================================
# Alert priority configuration
ALERT_PRIORITY_ORDER = ['warning', 'caution', 'watch']

# Alert Threshold Configuration
ALERT_THRESHOLDS = {
    'temperature_high': 35.0,      # °C - Hot weather warning
    'temperature_low': -10.0,      # °C - Cold weather warning  
    'wind_speed_high': 15.0,       # m/s - High wind warning
    'pressure_low': 980.0,         # hPa - Storm system warning
    'humidity_high': 85.0,         # % - High humidity discomfort
    'humidity_low': 15.0,          # % - Low humidity warning

    # NEW thresholds
    'heavy_rain_threshold': 10.0,     # mm/hour - Heavy rain warning
    'heavy_snow_threshold': 5.0,      # mm/hour - Heavy snow warning
    'low_visibility_metric': 3000,    # meters - Poor visibility (3km)
    'low_visibility_imperial': 3218,  # meters - Poor visibility (2 miles)

    # Derived metric thresholds
    'heat_index_high': 40.5,          # °C (105°F) - Dangerous heat index
    'wind_chill_low': -28.9,          # °C (-20°F) - Dangerous wind chill
    'uv_index_high': 8,               # Index - Very high UV exposure
    'air_quality_poor': 4,            # AQI - Poor air quality warning
    'comfort_score_low': 30,          # Score - Uncomfortable conditions
}

# ================================
# 5. APPLICATION DEFAULTS
# ================================
# Control Frame Defaults
DEFAULTS = {
    "city": "New York",
    "unit": "imperial",
    "range": "Last 7 Days",
    "chart": "Temperature",
    "visibility": {k: v['visible'] for k, v in METRICS.items()},
    "alert_thresholds": ALERT_THRESHOLDS 
}

# ================================
# 6. SYSTEM CONFIGURATION
# ================================
# Output Files & Directories
base_dir = Path(__file__).parent.parent
data_dir = base_dir / "data"

OUTPUT = {
    "data_dir": str(data_dir),
    "log_dir": str(data_dir), 
    "log": str(data_dir / "output.txt")
}

MEMORY = {
    "max_cities_stored": 50,        # Maximum number of cities to keep in memory
    "max_entries_per_city": 30,     # Maximum weather entries per city (existing)
    "max_total_entries": 1000,      # Global maximum entries across all cities
    "cleanup_interval_hours": 24,   # Hours between automatic cleanup (existing)
    "aggressive_cleanup_threshold": 0.8  # Trigger aggressive cleanup at 80% of limits
}

# ================================
# 7. CONFIGURATION VALIDATION
# ================================
def validate_config() -> None:
    """Validate essential configuration requirements.
    
    Performs focused validation on critical configuration that could cause
    application failures. Removes overly defensive checks for internal consistency.
    
    Raises:
        ValueError: If any critical configuration is invalid or missing
    """
    # Check critical API configuration
    if not API_KEY:
        print("Warning: No API key found. Application will use fallback data only.")
    
    # Validate essential structures exist
    required_sections = ['METRICS', 'DEFAULTS', 'UNITS', 'CHART', 'OUTPUT', 'ALERT_THRESHOLDS', 'MEMORY']
    for section in required_sections:
        if section not in globals():
            raise ValueError(f"Missing required configuration section: {section}")
    
    # Validate METRICS structure (essential for app functionality)
    if not isinstance(METRICS, dict) or not METRICS:
        raise ValueError("METRICS must be a non-empty dictionary")
    
    # Sample check for metric structure
    sample_metric = next(iter(METRICS.values()))
    if not isinstance(sample_metric, dict) or 'label' not in sample_metric or 'visible' not in sample_metric:
        raise ValueError("Invalid METRICS structure - missing 'label' or 'visible' fields")
    
    # Validate critical DEFAULTS
    if DEFAULTS.get('unit') not in ['metric', 'imperial']:
        raise ValueError(f"Invalid default unit system: {DEFAULTS.get('unit')}")
    
    # Validate essential file paths exist
    try:
        import os
        os.makedirs(OUTPUT.get("data_dir", "data"), exist_ok=True)
    except (OSError, TypeError):
        raise ValueError("Cannot create or access data directory")
    
    # Validate memory configuration is reasonable
    if not all(isinstance(MEMORY.get(key, 0), (int, float)) and MEMORY.get(key, 0) > 0 
               for key in ['max_cities_stored', 'max_entries_per_city', 'max_total_entries']):
        raise ValueError("Memory configuration must contain positive numbers")

    print("Configuration validation passed successfully.")