"""
Default/static data configuration for the Weather Dashboard application.
"""

import os

# Attempt to load environment variables from a .env file
# This accounts for error if 'dotenv' is not installed (like on github actions testing)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: 'dotenv' not found. Skipping .env loading.")

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

# Derive visibility and label maps for internal use
KEY_TO_DISPLAY = {k: v['label'] for k, v in METRICS.items()}
DISPLAY_TO_KEY = {v['label']: k for k, v in METRICS.items()}
DEFAULT_VISIBILITY = {k: v['visible'] for k, v in METRICS.items()}

# Control Frame Defaults
DEFAULTS = {
    "city": "New York",
    "unit": "imperial",
    "range": "Last 7 Days",
    "chart": "Temperature",
    "visibility": DEFAULT_VISIBILITY
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
        'conditions': {'imperial': 'Category', 'metric': 'Category'},
    }
}

# Output Files & Directories
OUTPUT = {
    "data_dir": os.path.join(os.path.dirname(__file__), "data"),
    "log_dir": os.path.join(os.path.dirname(__file__), "data"),
    "log": os.path.join(os.path.dirname(__file__), "data", "output.txt")
}
