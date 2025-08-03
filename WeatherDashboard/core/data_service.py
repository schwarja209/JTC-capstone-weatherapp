"""
Data service layer that coordinates between controllers and data managers.

This module provides the service layer that abstracts data operations
for controllers. Handles weather data retrieval, historical data access,
logging operations, and coordinates between business logic and data storage.

Classes:
    WeatherDataService: Main service class coordinating data operations
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import threading

from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.validation_utils import ValidationUtils
from WeatherDashboard.services.api_exceptions import ValidationError


@dataclass
class HistoricalDataResult:
    """Type-safe container for historical weather data results.
    
    Contains historical weather data with metadata about
    the request and data quality.
    """
    city_name: str
    data_entries: List[Dict[str, Any]]
    num_days: int
    unit_system: str
    source_unit: str
    conversion_applied: bool
    timestamp: datetime

    # Rich service layer metadata
    operation_status: str = "success"
    processing_time_ms: Optional[int] = None
    data_completeness: float = 1.0  # Percentage of requested days with data
    cache_hits: int = 0
    api_calls_made: int = 0
    errors: List[str] = None
    
    def __post_init__(self):
        """Validate dataclass after initialization."""
        if not self.city_name:
            raise ValueError("city_name cannot be empty")
        if self.num_days <= 0:
            raise ValueError("num_days must be positive")
        if self.unit_system not in ['metric', 'imperial']:
            raise ValueError("unit_system must be 'metric' or 'imperial'")
        if self.operation_status not in ['success', 'partial', 'failed', 'cancelled']:
            raise ValueError("operation_status must be 'success', 'partial', 'failed', or 'cancelled'")
        if not (0.0 <= self.data_completeness <= 1.0):
            raise ValueError("data_completeness must be between 0.0 and 1.0")
        if self.processing_time_ms is not None and self.processing_time_ms < 0:
            raise ValueError("processing_time_ms cannot be negative")
        if self.cache_hits < 0:
            raise ValueError("cache_hits cannot be negative")
        if self.api_calls_made < 0:
            raise ValueError("api_calls_made cannot be negative")
        if self.errors is None:
            self.errors = []

@dataclass
class LoggingResult:
    """Type-safe container for logging operation results.
    
    Contains information about logging operations including
    success status and any errors encountered.
    """
    city_name: str
    unit_system: str
    success: bool
    error_message: Optional[str]
    timestamp: datetime

    # Rich service layer metadata
    operation_status: str = "success"
    processing_time_ms: Optional[int] = None
    file_size_bytes: Optional[int] = None
    errors: List[str] = None
    backup_created: bool = False
    
    def __post_init__(self):
        """Validate dataclass after initialization."""
        if not self.city_name:
            raise ValueError("city_name cannot be empty")
        if self.unit_system not in ['metric', 'imperial']:
            raise ValueError("unit_system must be 'metric' or 'imperial'")
        if self.operation_status not in ['success', 'partial', 'failed', 'cancelled']:
            raise ValueError("operation_status must be 'success', 'partial', 'failed', or 'cancelled'")
        if self.processing_time_ms is not None and self.processing_time_ms < 0:
            raise ValueError("processing_time_ms cannot be negative")
        if self.file_size_bytes is not None and self.file_size_bytes < 0:
            raise ValueError("file_size_bytes cannot be negative")
        if self.errors is None:
            self.errors = []


class WeatherDataService:
    """Service layer that abstracts data operations for controllers.
    
    Provides a clean interface between business logic controllers and data
    management systems. Handles weather data retrieval, historical data access,
    file logging, and coordinates data operations across the application.
    
    Attributes:
        data_manager: Weather data manager for storage and retrieval operations
    """
    
    def __init__(self, data_manager: Any) -> None:
        """Initialize the data service with a data manager.
        
        Args:
            data_manager: Weather data manager for handling data operations (injected for testability)
        """
        # Direct imports for stable utilities
        self.validation_utils = ValidationUtils()
        self.logger = Logger()

        # Injected dependencies for testable components
        self.data_manager = data_manager

    def _validate_inputs(self, city_name: str, unit_system: str) -> Tuple[str, str]:
        """Validate and normalize inputs with consistent error handling.
        
        Args:
            city_name: Raw city name input (will be normalized)
            unit_system: Target unit system ('metric' or 'imperial')

        Returns:
            Tuple[str, str]: (normalized_city_name, unit_system)
            
        Raises:
            ValueError: If validation fails
        """
        try:
            # Validate city name
            self.validation_utils.validate_city_name(city_name)
            city = city_name.strip().title()
            
            # Validate unit system
            self.validation_utils.validate_unit_system(unit_system)
            
            return city, unit_system
            
        except Exception as e:
            raise ValueError(f"Validation error: {str(e)}")

    def get_city_data(self, city_name: str, unit_system: str, cancel_event: Optional[threading.Event] = None) -> Dict[str, Any]:
        """Get weather data for a city with comprehensive error handling and normalization.
        
        Fetches current weather data through data manager, handles city name normalization,
        unit system validation, and provides consistent error handling. Converts service-level
        exceptions to appropriate application-level exceptions per ADR-004.
        
        Args:
            city: Raw city name input (will be normalized)
            unit_system: Target unit system ('metric' or 'imperial')
            cancel_event: Optional threading event for operation cancellation
        
        Returns:
            Dict[str, Any]: Weather data dictionary
                
        Side Effects:
            Logs data operations via data manager
            May trigger data cleanup operations
        """
        start_time = datetime.now()
        
        # Validate inputs
        try:
            normalized_city, normalized_unit = self._validate_inputs(city_name, unit_system)
        except ValueError as e:
            raise ValidationError(str(e))
        
        try:
            # Fetch data from data manager
            weather_data = self.data_manager.fetch_current(
                normalized_city, 
                normalized_unit, 
                cancel_event
            )
            
            return weather_data
            
        except Exception as e:
            self.logger.error(f"Failed to get city data for {city_name}: {e}")
            raise

    def get_historical_data(self, city_name: str, num_days: int, unit_system: str) -> HistoricalDataResult:
        """Get historical weather data for a city with unit conversion.
        
        Retrieves historical weather data through data manager and applies
        unit conversion to match the requested unit system. Handles validation
        of input parameters and provides consistent data formatting.
        
        Args:
            city: Target city name for historical data
            days: Number of days of historical data to retrieve
            unit_system: Target unit system for data formatting
            
        Returns:
            HistoricalDataResult: Type-safe container with historical data and metadata
        """
        start_time = datetime.now()

        try:
            # Validate inputs
            normalized_city, normalized_unit = self._validate_inputs(city_name, unit_system)
            
            # Get raw historical data
            raw_data = self.data_manager.get_historical(normalized_city, num_days)
            
            # Determine if conversion is needed
            source_unit = "metric"  # Same as generator's output
            conversion_applied = normalized_unit != source_unit
            
            # Apply unit conversion if needed
            errors = []
            if conversion_applied:
                try:
                    converted_data = [self.data_manager.convert_units(d, normalized_unit) for d in raw_data]
                except Exception as e:
                    errors.append(f"Unit conversion error: {str(e)}")
                    converted_data = raw_data
            else:
                converted_data = raw_data
            
            processing_time = int((datetime.now() - start_time).total_seconds() * 1000)

            # Calculate data completeness
            data_completeness = len(converted_data) / num_days if num_days > 0 else 0.0
            
            # Determine operation status
            operation_status = "success"
            if len(errors) > 0:
                operation_status = "partial"
            if data_completeness < 1.0:
                operation_status = "partial"
            
            return HistoricalDataResult(
                city_name=normalized_city,
                data_entries=converted_data,
                num_days=num_days,
                unit_system=normalized_unit,
                source_unit=source_unit,
                conversion_applied=conversion_applied,
                timestamp=datetime.now(),
                # SERVICE LAYER METADATA FIELDS:
                operation_status=operation_status,
                processing_time_ms=processing_time,
                data_completeness=data_completeness,
                cache_hits=0,  # need cache implementation to track this
                api_calls_made=0,  # need API tracking to count this
                errors=errors
            )
        
        except Exception as e:
            processing_time = int((datetime.now() - start_time).total_seconds() * 1000)

            return HistoricalDataResult(
                city_name=city_name,
                data_entries=[],
                num_days=num_days,
                unit_system=unit_system,
                source_unit="metric",
                conversion_applied=False,
                timestamp=datetime.now(),
                # SERVICE LAYER METADATA FIELDS:
                operation_status="failed",
                processing_time_ms=processing_time,
                data_completeness=0.0,
                cache_hits=0,
                api_calls_made=0,
                errors=[f"Operation error: {str(e)}"]
            )

    def write_to_log(self, city: str, data: Dict[str, Any], unit: str) -> LoggingResult:
        """Write weather data to the log file.
        
        Args:
            city: City name for the log entry
            data: Weather data to log
            unit_system: Unit system for formatting ('metric' or 'imperial')

        Returns:
            LoggingResult: Type-safe container with logging operation status
        """
        start_time = datetime.now()

        try:
            # Validate inputs
            normalized_city, normalized_unit = self._validate_inputs(city, unit)
            
            # Write to log
            self.data_manager.write_to_file(normalized_city, data, normalized_unit)
            
            processing_time = int((datetime.now() - start_time).total_seconds() * 1000)

            return LoggingResult(
                city_name=normalized_city,
                unit_system=normalized_unit,
                success=True,
                error_message=None,
                timestamp=datetime.now(),
                # SERVICE LAYER METADATA FIELDS:
                operation_status="success",
                processing_time_ms=processing_time,
                file_size_bytes=None,  # need file system access to get this
                errors=[],
                backup_created=False
            )
            
        except Exception as e:
            processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
            return LoggingResult(
                city_name=city,
                unit_system=unit,
                success=False,
                error_message=str(e),
                timestamp=datetime.now(),
                # SERVICE LAYER METADATA FIELDS:
                operation_status="failed",
                processing_time_ms=processing_time,
                file_size_bytes=None,
                errors=[str(e)],
                backup_created=False
                )