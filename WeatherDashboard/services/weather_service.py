"""
Weather service layer for the Weather Dashboard application.

This module provides comprehensive weather API integration including HTTP
communication, data parsing, validation, error handling, and fallback logic.
Implements retry mechanisms, rate limiting, and robust error recovery.

Functions:
    fetch_with_retry: HTTP request function with retry and exponential backoff
    validate_api_response: API response structure validation

Classes:
    WeatherAPIClient: Raw API communication with OpenWeatherMap
    WeatherDataParser: Parsing raw API data into structured format
    WeatherDataValidator: Validation of parsed weather data
    WeatherAPIService: Main service orchestrating all weather operations
"""

from typing import Dict, Any, Tuple
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


def fetch_with_retry(url: str, params: Dict[str, Any], retries: int = 2, delay: int = 1) -> requests.Response:
    """Attempt to fetch data from the API with retry and exponential backoff.
    
    Implements robust HTTP request handling with automatic retries for
    transient failures and exponential backoff to avoid overwhelming servers.
    
    Args:
        url: API endpoint URL to request
        params: Query parameters for the request
        retries: Maximum number of retry attempts (default 2)
        delay: Initial delay between retries in seconds (default 1)
        
    Returns:
        requests.Response: Successful HTTP response object
        
    Raises:
        RateLimitError: When rate limit is exceeded (429 status)
        CityNotFoundError: When city is not found (404 status)
        NetworkError: For network/connection issues and timeouts
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


def validate_api_response(data: Dict[str, Any]) -> None:
    """Validate structure and key presence in API response.
    
    Checks that the API response contains all required keys and has the
    expected structure for weather data processing.
    
    Args:
        data: API response data dictionary to validate
        
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
    """Handle raw API communication with OpenWeatherMap.
    
    Manages HTTP requests to the OpenWeatherMap API with proper authentication,
    error handling, and response validation. Provides a clean interface for
    raw weather data retrieval.
    
    Attributes:
        api_url: Base URL for OpenWeatherMap API
        api_key: API authentication key
    """
    def __init__(self, api_url: str, api_key: str) -> None:
        """Initialize the weather API client.
        
        Args:
            api_url: Base URL for the OpenWeatherMap API
            api_key: API authentication key
        """
        self.api_url = api_url
        self.api_key = api_key
    
    def fetch_raw_data(self, city: str) -> Dict[str, Any]:
        """Fetch raw JSON data from the weather API.
        
        Makes HTTP request to OpenWeatherMap API for current weather data,
        validates the response, and returns parsed JSON data.
        
        Args:
            city: City name to fetch weather data for
            
        Returns:
            Dict[str, Any]: Raw weather data from API
            
        Raises:
            ValidationError: If city name is invalid or API key is missing
            CityNotFoundError: If city is not found in API
            Various API errors: Based on HTTP response status
        """
        self._validate_request(city)
        
        params = {"q": city, "appid": self.api_key, "units": "metric"}  # hardcoded always in metric, for consistency
        response = fetch_with_retry(self.api_url, params)
        
        try:
            data = response.json()
        except ValueError as e:  # Covers json.JSONDecodeError in older Python versions
            raise ValueError(f"Invalid JSON response from weather API: {e}") from e
        except Exception as e:
            raise ValueError(f"Failed to parse API response: {e}")
        
        # Validate that we got a proper response structure
        if not isinstance(data, dict):
            raise ValueError(f"Expected JSON object, got {type(data).__name__}")

        if data.get("cod") != 200:
            raise CityNotFoundError(f"City '{city}' not found")  # City not found error handling
        
        validate_api_response(data)
        return data
    
    def _validate_request(self, city: str) -> None:
        """Validate the city input and API key presence.
        
        Args:
            city: City name to validate
            
        Raises:
            ValidationError: If city name is empty or API key is missing
        """
        if not city.strip():
            raise ValidationError("City name cannot be empty")
        if not self.api_key:
            raise ValidationError("Missing API key - application will use simulated data only")  # Changed from ValidationError


class WeatherDataParser:
    """Handle parsing raw API data into structured weather data.
    
    Converts raw OpenWeatherMap API responses into a standardized internal
    format for use throughout the application. Handles data extraction,
    unit conversion, and formatting.
    """
    @staticmethod
    def parse_weather_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the raw weather data from the API response into a structured format.
        
        Extracts relevant weather information from OpenWeatherMap API response
        and converts it into the application's internal data structure.
        
        Args:
            data: Raw API response data dictionary
            
        Returns:
            Dict[str, Any]: Structured weather data with standardized keys
        """
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
    """Handle validation of parsed weather data.
    
    Performs sanity checks on weather data to ensure values are within
    reasonable ranges and data types are correct. Helps identify corrupted
    or invalid data from API responses.
    """
    @staticmethod
    def validate_weather_data(d: Dict[str, Any]) -> None:
        """Perform basic sanity checks on the parsed weather data.
        
        Validates that weather values are within expected ranges and have
        correct data types. Helps catch corrupted or invalid API data.
        
        Args:
            d: Parsed weather data dictionary to validate
            
        Raises:
            ValueError: If any weather values are outside expected ranges
        """
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
    """Handle fetching current weather data from OpenWeatherMap API with fallback to simulated data.
    
    Main service class that orchestrates weather data retrieval, parsing, validation,
    and fallback handling. Provides a high-level interface for weather data access
    with comprehensive error handling and automatic fallback to simulated data.
    
    Attributes:
        api: OpenWeatherMap API base URL
        key: API authentication key
        fallback: Fallback data generator for simulated weather data
        _api_client: Internal API client for HTTP communication
        _data_parser: Internal data parser for response processing
        _data_validator: Internal data validator for sanity checks
    """
    def __init__(self) -> None:
        """Initialize the weather API service.
        
        Sets up API configuration, fallback data generator, and internal
        components for API communication, data parsing, and validation.
        """
        self.api = config.API_BASE_URL
        self.key = config.API_KEY
        self.fallback = SampleWeatherGenerator()
        
        # Internal components for better separation of concerns
        self._api_client = WeatherAPIClient(self.api, self.key)
        self._data_parser = WeatherDataParser()
        self._data_validator = WeatherDataValidator()

    def fetch_current(self, city: str) -> Tuple[Dict[str, Any], bool, str]:
        """Fetch current weather data for a given city using OpenWeatherMap API.
        
        Attempts to retrieve live weather data from the API. If the API call fails
        for any reason, automatically falls back to simulated weather data to
        ensure the application continues to function.
        
        Args:
            city: City name to fetch weather data for
            
        Returns:
            Tuple containing:
                - Dict[str, Any]: Weather data (live or simulated)
                - bool: True if fallback data was used, False for live data
                - Exception: Exception object if API failed, None for success
        """
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
        """Fetch raw weather data from OpenWeatherMap API for the specified city.
        
        Args:
            city: City name to fetch data for
            
        Returns:
            Dict[str, Any]: Raw API response data
        """
        return self._api_client.fetch_raw_data(city)

    def _parse_weather_data(self, data):
        """Parse the raw weather data from the API response into a structured format.
        
        Args:
            data: Raw API response data
            
        Returns:
            Dict[str, Any]: Parsed and structured weather data
        """
        return self._data_parser.parse_weather_data(data)

    def _validate_weather_data(self, d):
        """Perform basic sanity checks on the parsed weather data.
        
        Args:
            d: Parsed weather data to validate
            
        Raises:
            ValueError: If weather data fails validation checks
        """
        self._data_validator.validate_weather_data(d)
    
    def _generate_fallback_response(self, city, msg, exc):
        """Use simulated data generator when API call fails.
        
        Generates fallback weather data when the API is unavailable, ensuring
        the application continues to function with simulated data.
        
        Args:
            city: City name for fallback data generation
            msg: Error message describing the failure
            exc: Exception that caused the API failure
            
        Returns:
            Tuple containing fallback weather data, fallback flag, and exception
        """
        Logger.error(f"API failure for {city} - {msg}: {exc}. Switching to simulated data.")

        fallback_data = self.fallback.generate(city)
        fallback_data[-1]['source'] = 'simulated'
        return fallback_data[-1], True, exc