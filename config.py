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

# Control Frame Defaults
DEFAULTS = {
    "city": "New York",
    "unit": "imperial",
    "range": "Last 7 Days",
    "chart": "Temperature",
    "visibility": {
        'temperature': True,
        'humidity': True,
        'wind_speed': False,
        'pressure': False,
        'conditions': False,
    }
}

# Keys for how to display variable names in UI
LABELS = {
    "key_to_display": {
        'temperature': 'Temperature',
        'humidity': 'Humidity',
        'wind_speed': 'Wind Speed',
        'pressure': 'Pressure',
        'conditions': 'Conditions'
    }
}
LABELS["display_to_key"] = {v: k for k, v in LABELS["key_to_display"].items()}

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

# Output File Name
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

OUTPUT = {
    "log": os.path.join(DATA_DIR, "data.txt")
}