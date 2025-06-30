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
DEFAULT_CITY = "New York"
DEFAULT_UNIT = "F"
DEFAULT_RANGE = "Last 7 Days"
DEFAULT_CHART = "Temperature"
DEFAULT_VISIBILITY = {
    'temperature': True,
    'humidity': True,
    'wind_speed': False,
    'pressure': False,
    'conditions': False,
}

# Keys for how to display variable names in UI
KEY_TO_DISPLAY = {
    'temperature': 'Temperature',
    'humidity': 'Humidity',
    'wind_speed': 'Wind Speed',
    'pressure': 'Pressure',
    'conditions': 'Conditions'
}

# Historical Data Range Options
RANGE_OPTIONS = {
    'Last 7 Days': 7,
    'Last 14 Days': 14,
    'Last 30 Days': 30
}

# Output File Name
OUTPUT_FILE = "data.txt"