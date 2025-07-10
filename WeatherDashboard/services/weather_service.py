"""
Weather service layer for the Weather Dashboard application.
Handles API communication, data parsing, validation, and fallback logic.
"""

import time
import requests
from datetime import datetime

from WeatherDashboard import config
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.services.api_exceptions import (
    WeatherDashboardError,
    WeatherAPIError,
    CityNotFoundError,
    ValidationError,
    RateLimitError,
    NetworkError
)
from WeatherDashboard.services.fallback_generator import SampleWeatherGenerator


def fetch_with_retry(url, params, retries=2, delay=1):
    """Attempts to fetch data from the API with retry and exponential backoff.
    
    Raises:
        RateLimitError: When rate limit is exceeded
        CityNotFoundError: When city is not found (404)
        NetworkError: For other network/connection issues
        WeatherAPIError: For other API-related errors
    """
    for attempt in range(retries + 1):
        try:
            response = requests.get(url, params=params, timeout=5)
            
            # Handle specific status codes
            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded (Too Many Requests)")
            if response.status_code == 404:
                raise CityNotFoundError("City not found")
            
            response.raise_for_status()
            return response
            
        except RateLimitError:
            # Don't retry rate limit errors
            raise
        except CityNotFoundError:
            # Don't retry city not found errors
            raise
        except requests.exceptions.Timeout as e:
            if attempt < retries:
                Logger.warn(f"Timeout on attempt {attempt + 1}, retrying: {e}")
                time.sleep(delay * (2 ** attempt))
            else:
                Logger.error(f"API timeout after {retries + 1} attempts: {e}")
                raise NetworkError(f"Request timed out after {retries + 1} attempts")
        except requests.exceptions.ConnectionError as e:
            if attempt < retries:
                Logger.warn(f"Connection error on attempt {attempt + 1}, retrying: {e}")
                time.sleep(delay * (2 ** attempt))
            else:
                Logger.error(f"Connection failed after {retries + 1} attempts: {e}")
                raise NetworkError(f"Connection failed after {retries + 1} attempts")
        except requests.exceptions.RequestException as e:
            if attempt < retries:
                Logger.warn(f"API call failed (attempt {attempt + 1}), retrying: {e}")
                time.sleep(delay * (2 ** attempt))
            else:
                Logger.error(f"API call failed after {retries + 1} attempts: {e}")
                raise WeatherAPIError(f"API request failed: {e}")


def validate_api_response(data):
    """Validates structure and key presence in API response.
    
    Raises:
        ValidationError: When required keys are missing or data is malformed
    """
    required = {"main", "weather", "wind"}
    if not all(k in data for k in required):
        missing = required - set(data.keys())
        raise ValidationError(f"Missing keys in API response: {missing}")
    
    if "temp" not in data["main"]:
        raise ValidationError("Temperature missing from 'main' section")
    
    if not isinstance(data["weather"], list) or not data["weather"]:
        raise ValidationError("Malformed 'weather' data - expected non-empty list")


class WeatherAPIClient:
    """Handles raw API communication with OpenWeatherMap."""
    
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key
    
    def fetch_raw_data(self, city):
        """Fetches raw JSON data from the weather API."""
        self._validate_request(city)
        
        params = {"q": city, "appid": self.api_key, "units": "metric"}  # hardcoded always in metric, for consistency
        response = fetch_with_retry(self.api_url, params)
        
        try:
            data = response.json()
        except ValueError as e:  # Covers json.JSONDecodeError in older Python versions
            raise ValueError(f"Invalid JSON response from weather API: {e}")
        except Exception as e:
            raise ValueError(f"Failed to parse API response: {e}")
        
        # Validate that we got a proper response structure
        if not isinstance(data, dict):
            raise ValueError(f"Expected JSON object, got {type(data).__name__}")

        if data.get("cod") != 200:
            raise CityNotFoundError(f"City '{city}' not found")  # City not found error handling
        
        validate_api_response(data)
        return data
    
    def _validate_request(self, city):
        """Validates the city input for non-empty and API key presence."""
        if not city.strip():
            raise ValueError("City name cannot be empty")  # Changed from ValidationError
        if not self.api_key:
            raise ValueError("Missing API key - application will use simulated data only")  # Changed from ValidationError


class WeatherDataParser:
    """Handles parsing raw API data into structured weather data."""
    
    @staticmethod
    def parse_weather_data(data):
        """Parses the raw weather data from the API response into a structured format."""
        # TODO:
        # rain = data.get("rain", {})
        # snow = data.get("snow", {})
        # precip_mm = rain.get("1h", 0) + snow.get("1h", 0)

        return {
            'temperature': data.get("main", {}).get("temp"),
            'humidity': data.get("main", {}).get("humidity"),
            # TODO: 'precipitation': precip_mm,
            'pressure': data.get("main", {}).get("pressure"),
            'wind_speed': data.get("wind", {}).get("speed"),
            'conditions': data.get("weather", [{}])[0].get("description", "--").title(),
            'date': datetime.now()
        }


class WeatherDataValidator:
    """Handles validation of parsed weather data."""
    
    @staticmethod
    def validate_weather_data(d):
        """Performs basic sanity checks on the parsed weather data."""
        
        numeric_fields = ['temperature', 'humidity', 'wind_speed', 'pressure']
        for field in numeric_fields:
            if not isinstance(d.get(field), (int, float)):
                raise ValueError(f"Invalid {field}: expected number, got {type(d.get(field)).__name__}")
    
        # Validate ranges with helpful messages
        humidity = d['humidity']
        if not (0 <= humidity <= 100):
            raise ValueError(f"Invalid humidity: {humidity}% (must be between 0-100%)")
        
        temp = d['temperature']
        if not (-100 <= temp <= 70):
            raise ValueError(f"Invalid temperature: {temp}°C (must be between -100°C and 70°C)")
        
        pressure = d['pressure']
        if not (900 <= pressure <= 1100):
            raise ValueError(f"Invalid pressure: {pressure} hPa (must be between 900-1100 hPa)")


class WeatherAPIService:
    """Handles fetching current weather data from OpenWeatherMap API with fallback to simulated data."""
    
    def __init__(self):
        self.api = config.API_BASE_URL
        self.key = config.API_KEY
        self.fallback = SampleWeatherGenerator()
        
        # Internal components for better separation of concerns
        self._api_client = WeatherAPIClient(self.api, self.key)
        self._data_parser = WeatherDataParser()
        self._data_validator = WeatherDataValidator()

    def fetch_current(self, city):
        """Fetches current weather data for a given city using OpenWeatherMap API."""
        try:
            data = self._get_api_data(city)
            parsed = self._parse_weather_data(data)
            parsed['source'] = 'live'
            self._validate_weather_data(parsed)

            return parsed, False, ""

        # Handle specific custom exceptions
        except ValidationError as e:
            data, used, msg = self._generate_fallback_response(city, "Validation error", e)
            return data, used, msg
        except CityNotFoundError as e:
            data, used, msg = self._generate_fallback_response(city, "City not found", e)
            return data, used, msg
        except RateLimitError as e:
            data, used, msg = self._generate_fallback_response(city, "Rate limit exceeded", e)
            return data, used, msg
        except NetworkError as e:
            data, used, msg = self._generate_fallback_response(city, "Network error", e)
            return data, used, msg
        except WeatherAPIError as e:
            data, used, msg = self._generate_fallback_response(city, "API error", e)
            return data, used, msg
        except Exception as e:
            # Only catch truly unexpected errors
            Logger.error(f"Unexpected error in fetch_current for {city}: {e}")
            data, used, msg = self._generate_fallback_response(city, "Unexpected error", e)
            return data, used, msg

    def _get_api_data(self, city):
        """Fetches raw weather data from OpenWeatherMap API for the specified city."""
        return self._api_client.fetch_raw_data(city)

    def _parse_weather_data(self, data):
        """Parses the raw weather data from the API response into a structured format."""
        return self._data_parser.parse_weather_data(data)

    def _validate_weather_data(self, d):
        """Performs basic sanity checks on the parsed weather data."""
        self._data_validator.validate_weather_data(d)
    
    def _generate_fallback_response(self, city, msg, exc):
        """Uses simulated data generator when API call fails."""
        Logger.error(f"API failure for {city} - {msg}: {exc}. Switching to simulated data.")

        fallback_data = self.fallback.generate(city)
        fallback_data[-1]['source'] = 'simulated'
        return fallback_data[-1], True, exc