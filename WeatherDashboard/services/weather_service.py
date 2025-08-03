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

from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import time
import threading

import requests

from WeatherDashboard import config
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.api_utils import ApiUtils

from .api_exceptions import (
    WeatherDashboardError,
    WeatherAPIError,
    CityNotFoundError,
    ValidationError,
    RateLimitError,
    NetworkError
)
from .fallback_generator import SampleWeatherGenerator
from WeatherDashboard.utils.derived_metrics import DerivedMetricsCalculator


@dataclass
class WeatherServiceResult:
    """Type-safe container for weather service operation results.

    Encapsulates the result of a weather service operation, including
    the weather data, simulation flag, error message, and rich metadata.
    """
    data: Dict[str, Any]
    is_simulated: bool
    error_message: Optional[str]
    timestamp: datetime = datetime.now()
    # LIGHT METADATA FIELDS
    processing_time: Optional[int] = None


# ================================
# 1. API CLIENT & COMMUNICATION
# ================================
class WeatherAPIClient:
    """Handle raw API communication with OpenWeatherMap.
    
    Manages HTTP requests to the OpenWeatherMap API with proper authentication,
    error handling, and response validation. Provides a clean interface for
    raw weather data retrieval.
    
    Attributes:
        api_url: Base URL for OpenWeatherMap API
        api_key: API authentication key
    """

    def __init__(self, weather_url: str, uv_url: str, air_quality_url: str, api_key: str) -> None:
        """Initialize the weather API client.
        
        Args:
            weather_url: Base URL for the OpenWeatherMap API
            uv_url: Base URL for UV index API
            air_quality_url: Base URL for air quality API
            api_key: API authentication key
        """
        # Direct imports for stable utilities
        self.config = config
        self.logger = Logger()

        # Instance data
        self.weather_url = weather_url # Base URL for the OpenWeatherMap API
        self.uv_url = uv_url
        self.air_quality_url = air_quality_url
        self.api_key = api_key # API authentication key
    
    def _fetch_api_endpoint(self, url: str, params: Dict[str, Any], cancel_event: Optional[threading.Event] = None) -> Optional[Dict[str, Any]]:
        """Unified method for fetching from any API endpoint.
        
        Args:
            url: API endpoint URL
            params: Query parameters for the request
            
        Returns:
            API response data or None if fetch fails
        """
        try:
            response = fetch_with_retry(url, params, cancel_event=cancel_event)
            return self._parse_json_response(response)
        except Exception as e:
            self.logger.warn(f"API fetch failed for {url}: {e}")
            return None

    def fetch_weather_data(self, city: str, cancel_event: Optional[threading.Event] = None) -> Dict[str, Any]:
        """Fetch current weather data from the main weather API."""
        self._validate_request(city)
        
        params = {"q": city, "appid": self.api_key, "units": "metric"}
        data = self._fetch_api_endpoint(self.weather_url, params, cancel_event)
        
        if not data or data.get("cod") != 200:
            raise CityNotFoundError(self.config.ERROR_MESSAGES['not_found'].format(resource="City", name=city))
        
        validate_api_response(data)
        return data
    
    def fetch_uv_data(self, lat: float, lon: float, cancel_event: Optional[threading.Event] = None) -> Optional[Dict[str, Any]]:
        """Fetch UV index data for given coordinates."""
        params = {"lat": lat, "lon": lon, "appid": self.api_key}
        return self._fetch_api_endpoint(self.uv_url, params, cancel_event)
    
    def fetch_air_quality_data(self, lat: float, lon: float, cancel_event: Optional[threading.Event] = None) -> Optional[Dict[str, Any]]:
        """Fetch air quality data for given coordinates."""
        params = {"lat": lat, "lon": lon, "appid": self.api_key}
        return self._fetch_api_endpoint(self.air_quality_url, params, cancel_event)
    
    def _parse_json_response(self, response: requests.Response) -> Dict[str, Any]:
        """Parse JSON response with error handling."""
        try:
            data = response.json()
            if not isinstance(data, dict):
                raise ValueError(f"Expected JSON object, got {type(data).__name__}")
            return data
        except ValueError as e:
            raise ValueError(self.config.ERROR_MESSAGES['api_error'].format(endpoint="weather API", reason=f"invalid JSON response: {e}")) from e
    
    def _validate_request(self, city: str) -> None:
        """Validate city input and API key presence."""
        if not city.strip():
            raise ValidationError(self.config.ERROR_MESSAGES['validation'].format(field="City name", reason="cannot be empty"))
        if not self.api_key:
            raise ValidationError(self.config.ERROR_MESSAGES['missing'].format(field="API key"))  # Changed from ValidationError


# ================================
# 2. DATA PARSING & TRANSFORMATION  
# ================================
class WeatherDataParser:
    """Handle parsing raw API data into structured weather data.
    
    Converts raw OpenWeatherMap API responses into a standardized internal
    format for use throughout the application. Handles data extraction,
    unit conversion, and formatting.
    """

    @staticmethod
    def parse_weather_data(weather_data: Dict[str, Any], uv_data: Optional[Dict[str, Any]] = None, air_quality_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Parse weather data using centralized API utilities."""
        api_utils = ApiUtils() # create instance
        
        # Extract complete weather data as dictionary (not dataclass)
        parsed_dict = api_utils.extract_complete_weather_data_dict(weather_data, uv_data, air_quality_data)

        # Calculate derived metrics and add to dictionary
        parsed_dict.update(WeatherDataParser._calculate_derived_metrics(parsed_dict))
        
        return parsed_dict
    
    @staticmethod
    def _calculate_derived_metrics(data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate all derived metrics from base weather data."""
        derived = {}

        # Create instance for calculations
        calculator = DerivedMetricsCalculator()
        
        # Get base values with safe defaults
        temp_c = data.get('temperature', 20)  # Already in Celsius
        humidity = data.get('humidity', 50)
        wind_speed_ms = data.get('wind_speed', 0)  # Already in m/s
        pressure = data.get('pressure', 1013)
        conditions = data.get('conditions', '')
        
        # Convert for calculations that need imperial units
        temp_f = (temp_c * 9/5) + 32
        wind_mph = wind_speed_ms * 2.23694
        
        # Calculate metrics and convert results back to metric
        heat_index_f = calculator.calculate_heat_index(temp_f, humidity)
        wind_chill_f = calculator.calculate_wind_chill(temp_f, wind_mph)
        
        # Store in metric units (like everything else)
        derived['heat_index'] = (heat_index_f - 32) * 5/9 if heat_index_f is not None else None
        derived['wind_chill'] = (wind_chill_f - 32) * 5/9 if wind_chill_f is not None else None
        derived['dew_point'] = calculator.calculate_dew_point(temp_c, humidity)  # Already metric
        
        # Other calculations...
        derived['precipitation_probability'] = calculator.calculate_precipitation_probability(
            pressure, humidity, conditions
        )
        derived['weather_comfort_score'] = calculator.calculate_weather_comfort_score(
            temp_c, humidity, wind_speed_ms, pressure
        )
        
        return derived


# =================================
# 3. DATA VALIDATION & VERIFICATION
# =================================
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
                raise ValueError(config.ERROR_MESSAGES['validation'].format(field=field.title(), reason=f"expected number, got {type(d.get(field)).__name__}"))
    
        # Validate ranges with helpful messages
        humidity = d['humidity']
        if not (0 <= humidity <= 100):
            raise ValueError(config.ERROR_MESSAGES['validation'].format(field="Humidity", reason=f"{humidity}% must be between 0-100%"))
        
        temp = d['temperature']
        if not (-100 <= temp <= 70):
            raise ValueError(config.ERROR_MESSAGES['validation'].format(field="Temperature", reason=f"{temp}°C must be between -100°C and 70°C"))
        
        pressure = d['pressure']
        if not (900 <= pressure <= 1100):
            raise ValueError(config.ERROR_MESSAGES['validation'].format(field="Pressure", reason=f"{pressure} hPa must be between 900-1100 hPa"))

        # Temperature-related fields (use same range as temperature)
        for temp_field in ['feels_like', 'temp_min', 'temp_max']:
            if temp_field in d and d[temp_field] is not None:
                if not isinstance(d[temp_field], (int, float)):
                    raise ValueError(config.ERROR_MESSAGES['validation'].format(field=temp_field.replace('_', ' ').title(), reason=f"expected number, got {type(d[temp_field]).__name__}"))
                if not (-100 <= d[temp_field] <= 70):
                    raise ValueError(config.ERROR_MESSAGES['validation'].format(field=temp_field.replace('_', ' ').title(), reason=f"{d[temp_field]}°C must be between -100°C and 70°C"))

        # Wind direction (0-360 degrees)
        if 'wind_direction' in d and d['wind_direction'] is not None:
            if not isinstance(d['wind_direction'], (int, float)):
                raise ValueError(config.ERROR_MESSAGES['validation'].format(field="Wind direction", reason=f"expected number, got {type(d['wind_direction']).__name__}"))
            if not (0 <= d['wind_direction'] <= 360):
                raise ValueError(config.ERROR_MESSAGES['validation'].format(field="Wind direction", reason=f"{d['wind_direction']}° must be between 0-360°"))

        # Cloud cover (0-100%)
        if 'cloud_cover' in d and d['cloud_cover'] is not None:
            if not isinstance(d['cloud_cover'], (int, float)):
                raise ValueError(config.ERROR_MESSAGES['validation'].format(field="Cloud cover", reason=f"expected number, got {type(d['cloud_cover']).__name__}"))
            if not (0 <= d['cloud_cover'] <= 100):
                raise ValueError(config.ERROR_MESSAGES['validation'].format(field="Cloud cover", reason=f"{d['cloud_cover']}% must be between 0-100%"))

        # Visibility (reasonable range: 0-50km)
        if 'visibility' in d and d['visibility'] is not None:
            if not isinstance(d['visibility'], (int, float)):
                raise ValueError(config.ERROR_MESSAGES['validation'].format(field="Visibility", reason=f"expected number, got {type(d['visibility']).__name__}"))
            if not (0 <= d['visibility'] <= 50000):
                raise ValueError(config.ERROR_MESSAGES['validation'].format(field="Visibility", reason=f"{d['visibility']}m must be between 0-50000m"))

        # Precipitation (reasonable range: 0-200mm)
        for precip_field in ['rain_1h', 'rain_3h', 'snow_1h', 'snow_3h']:
            if precip_field in d and d[precip_field] is not None:
                if not isinstance(d[precip_field], (int, float)):
                    raise ValueError(config.ERROR_MESSAGES['validation'].format(field=precip_field.replace('_', ' ').title(), reason=f"expected number, got {type(d[precip_field]).__name__}"))
                if not (0 <= d[precip_field] <= 200):
                    raise ValueError(config.ERROR_MESSAGES['validation'].format(field=precip_field.replace('_', ' ').title(), reason=f"{d[precip_field]}mm must be between 0-200mm"))


# ================================
# 4. MAIN SERVICE ORCHESTRATION
# ================================
class WeatherAPIService:
    """Main service orchestrating all weather data operations.
    Handle fetching current weather data from OpenWeatherMap API with fallback to simulated data.
    
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

        Args:
            api_client: Weather API client for HTTP communication (injected for testability)
            data_parser: Data parser for response processing (injected for testability)
            data_validator: Data validator for sanity checks (injected for testability)
            fallback_generator: Fallback data generator (injected for testability)
        """
        # Direct imports for stable utilities
        self.config = config
        self.logger = Logger()
        self.datetime = datetime

        # API configuration
        self.weather_api = self.config.API_BASE_URL
        self.uv_api = self.config.API_UV_URL
        self.air_quality_api = self.config.API_AIR_QUALITY_URL
        self.key = self.config.API_KEY
        
        # Initialize dependencies with injection
        self._api_client = WeatherAPIClient(
            self.weather_api, self.uv_api, self.air_quality_api, self.key
        )
        self.fallback = SampleWeatherGenerator()
        self._data_parser = WeatherDataParser()
        self._data_validator = WeatherDataValidator()

    def fetch_current(self, city: str, cancel_event: Optional[threading.Event] = None) -> WeatherServiceResult:
        """Fetch comprehensive current weather data including derived metrics.
        
        Fetches data from multiple APIs (weather, UV, air quality) and calculates
        derived comfort indices. Falls back to simulated data if critical API calls fail.
        
        Args:
            city: City name to fetch weather data for
            
        Returns:
            WeatherServiceResult: Type-safe container with weather data, simulation flag, error message, and metadata
        """
        start_time = self.datetime.now()

        # Temporary bypass for testing
        if getattr(config, 'FORCE_FALLBACK_MODE', False):
            return self._generate_fallback_response(city, "API disabled for testing", Exception("Testing mode"), start_time)
        try:
            # Fetch main weather data
            weather_data = self._api_client.fetch_weather_data(city, cancel_event)
            
            # Extract coordinates for additional API calls
            coords = weather_data.get("coord", {})
            lat, lon = coords.get("lat"), coords.get("lon")
            
            # Fetch additional data (non-critical)
            uv_data = None
            air_quality_data = None
            if lat is not None and lon is not None:
                try:
                    uv_data = self._api_client.fetch_uv_data(lat, lon, cancel_event)
                except Exception as e:
                    self.logger.warn(f"UV data fetch failed, continuing without UV data: {e}")
                
                try:
                    air_quality_data = self._api_client.fetch_air_quality_data(lat, lon, cancel_event)
                except Exception as e:
                    self.logger.warn(f"Air quality data fetch failed, continuing without air quality data: {e}")            
            
            # Parse and combine all data
            parsed = self._data_parser.parse_weather_data(weather_data, uv_data, air_quality_data)
            parsed['source'] = 'live'
            self._data_validator.validate_weather_data(parsed)

            processing_time = int((self.datetime.now() - start_time).total_seconds() * 1000)
            return WeatherServiceResult(
                data=parsed,
                is_simulated=False,
                error_message="",
                timestamp=self.datetime.now(),
                # LIGHT METADATA FIELDS
                processing_time=processing_time
            )
        
        # Handle specific custom exceptions - preserve all individual error types
        except (ValidationError, CityNotFoundError, RateLimitError, NetworkError, WeatherAPIError) as e:
            return self._generate_fallback_response(city, f"{type(e).__name__}", e,start_time)
        except Exception as e:
            # Only catch truly unexpected errors
            self.logger.error(f"Unexpected error in fetch_current for {city}: {e}")
            return self._generate_fallback_response(city, "Unexpected error", e, start_time)
    
    def _generate_fallback_response(self, city, msg, exc, start_time) -> WeatherServiceResult:
        """Use simulated data generator when API call fails.
        
        Args:
            city: City name for fallback data generation
            msg: Error message describing the failure
            exc: Exception that caused the API failure
            
        Returns:
            WeatherServiceResult: Type-safe container with fallback weather data, simulation flag, error message, and metadata
        """
        self.logger.error(f"API failure for {city} - {msg}: {exc}. Switching to simulated data.")

        fallback_data = self.fallback.generate(city)
        current_data = fallback_data[-1]
        
        # Add derived metrics and mark as simulated
        current_data.update(self._data_parser._calculate_derived_metrics(current_data))
        current_data['source'] = 'simulated'
        
        processing_time = int((self.datetime.now() - start_time).total_seconds() * 1000)
        return WeatherServiceResult(
            data=current_data,
            is_simulated=True,
            error_message=str(exc),
            timestamp=self.datetime.now(),
            # LIGHT METADATA FIELDS
            processing_time=processing_time
        )
    

# ================================
# 5. UTILITY FUNCTIONS
# ================================
def fetch_with_retry(url: str, params: Dict[str, Any], retries: int = config.API_RETRY_ATTEMPTS, delay: int = config.API_RETRY_BASE_DELAY, cancel_event: Optional[threading.Event] = None) -> requests.Response:
    """Attempt to fetch data from the API with retry and exponential backoff.
    
    Implements robust HTTP request handling with automatic retries for
    transient failures and exponential backoff to avoid overwhelming servers.
    
    Args:
        url: API endpoint URL to request
        params: Query parameters for the request
        retries: Maximum number of retry attempts (default 2)
        delay: Initial delay between retries in seconds (default 1)
        cancel_event: Threading event for cancellation support
        
    Returns:
        requests.Response: Successful HTTP response object
        
    Raises:
        RateLimitError: When rate limit is exceeded (429 status)
        CityNotFoundError: When city is not found (404 status)
        NetworkError: For network/connection issues, timeouts and cancellations
        WeatherAPIError: For other API-related errors
    """
    # Use short timeout when cancellation is supported, long timeout otherwise
    # Check if cancel_event exists AND we have a way to detect if this is a user-initiated request
    timeout = 2 if (cancel_event is not None and cancel_event.is_set()) else config.API_TIMEOUT_SECONDS
    logger = Logger() # create instance

    if cancel_event and cancel_event.is_set():
            raise NetworkError("Request cancelled by user")

    effective_retries = 0 if (cancel_event and cancel_event.is_set()) else retries
    for attempt in range(effective_retries + 1):
        # Check for cancellation before each attempt
        if cancel_event and cancel_event.is_set():
            raise NetworkError("Request cancelled by user")

        try:
            response = requests.get(url, params=params, timeout=timeout)
            
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
            if cancel_event and cancel_event.is_set():
                raise NetworkError("Request cancelled by user")
            if attempt < retries:
                logger.warn(f"Timeout on attempt {attempt + 1}, retrying: {e}")
                time.sleep(delay * (2 ** attempt)) # Exponential backoff
            else:
                logger.error(f"API timeout after {retries + 1} attempts: {e}")
                raise NetworkError(f"Request timed out after {retries + 1} attempts")
        except requests.exceptions.ConnectionError as e:
            if cancel_event and cancel_event.is_set():
                raise NetworkError("Request cancelled by user")
            if attempt < retries:
                logger.warn(f"Connection error on attempt {attempt + 1}, retrying: {e}")
                time.sleep(delay * (2 ** attempt)) # Exponential backoff
                if cancel_event and cancel_event.is_set():
                    raise NetworkError("Request cancelled by user")
            else:
                logger.error(f"Connection failed after {retries + 1} attempts: {e}")
                raise NetworkError(f"Connection failed after {retries + 1} attempts")
        except requests.exceptions.RequestException as e:
            if attempt < retries:
                logger.warn(f"API call failed (attempt {attempt + 1}), retrying: {e}")
                if cancel_event and cancel_event.is_set():
                    raise NetworkError("Request cancelled by user")
                time.sleep(delay * (2 ** attempt)) # Exponential backoff
            else:
                logger.error(f"API call failed after {retries + 1} attempts: {e}")
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
        raise ValidationError(config.ERROR_MESSAGES['api_error'].format(endpoint="weather API", reason=f"missing required keys: {missing}"))
    
    if "temp" not in data["main"]:
        raise ValidationError(config.ERROR_MESSAGES['missing'].format(field="Temperature data in API response"))
    
    if not isinstance(data["weather"], list) or not data["weather"]:
        raise ValidationError(config.ERROR_MESSAGES['api_error'].format(endpoint="weather API", reason="malformed weather data - expected non-empty list"))