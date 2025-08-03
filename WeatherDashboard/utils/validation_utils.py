"""
Centralized validation utilities for the Weather Dashboard application.

This module provides comprehensive input and state validation functions to eliminate
duplicate validation logic scattered across controller, state manager, and utility
files. Consolidates city name validation, unit system checking, metric visibility
validation, and complete application state verification into a single utility class.

Classes:
    ValidationUtils: Static utility class for centralized validation operations
"""

import re
from typing import Any, Optional, Union
from datetime import datetime

from WeatherDashboard import config

from .logger import Logger


class ValidationUtils:
    """Centralized validation utilities to eliminate duplicate validation logic."""
    
    def __init__(self) -> None:
        """Initialize validation utils with optional dependencies."""
        # Direct imports for stable utilities
        self.config = config
        self.logger = Logger()
        self.datetime = datetime

        # Instance data
        self.regex_patterns = {
            'city_name': r"^[a-zA-Z\s\-'\.,]+$",
            'unit_system': r"^(metric|imperial)$"
        }

    def validate_city_name(self, city_name: Any) -> None:
        """Validate city name input with comprehensive checks.
        
        Args:
            city_name: City name to validate (any type)
            
        Raises:
            ValueError: If city name is invalid
        """
        # Type validation
        if not isinstance(city_name, str):
            raise ValueError(f"City name must be a string, got {type(city_name).__name__}")
        
        # Empty validation
        cleaned_name = city_name.strip()
        if not cleaned_name:
            raise ValueError("City name cannot be empty")
        
        # Length validation
        if len(cleaned_name) > 100:
            raise ValueError("City name cannot be longer than 100 characters")
        
        # Character validation
        if not re.match(self.regex_patterns['city_name'], cleaned_name):
            raise ValueError("City name contains invalid characters")
    
    def validate_unit_system(self, unit_system: Any) -> None:
        """Validate unit system selection.
        
        Args:
            unit_system: Unit system to validate (any type)
            
        Raises:
            ValueError: If unit system is invalid
        """
        # Type validation
        if not isinstance(unit_system, str):
            raise ValueError(f"Unit system must be a string, got {type(unit_system).__name__}")
        
        # Valid options
        valid_units = {'metric', 'imperial'}
        if unit_system not in valid_units:
            raise ValueError(f"'{unit_system}' is invalid. Must be 'metric' or 'imperial'")
    
    def validate_metric_visibility(self, state_manager: Any) -> None:
        """Validate that at least one metric is visible.
        
        Args:
            state_manager: Application state manager
            
        Raises:
            ValueError: If no metrics are visible
        """
        try:
            # Check if state manager has visibility
            if not hasattr(state_manager, 'visibility'):
                raise ValueError("State manager missing visibility attribute")
            
            # Check if any metrics are visible
            visible_count = 0
            for metric_key, visibility_var in state_manager.visibility.items():
                try:
                    if hasattr(visibility_var, 'get') and visibility_var.get():
                        visible_count += 1
                except Exception as e:
                    self.logger.warn(f"Error checking visibility for {metric_key}: {e}")
            
            if visible_count == 0:
                raise ValueError("At least one metric must be visible")
            
        except Exception as e:
            raise ValueError(f"Failed to validate metric visibility: {e}")
    
    def validate_date_range(self, date_range: Any) -> None:
        """Validate date range selection.
        
        Args:
            date_range: Date range to validate
            
        Raises:
            ValueError: If date range is invalid
        """
        if not isinstance(date_range, str):
            raise ValueError(f"Date range must be a string, got {type(date_range).__name__}")
        
        # Check against valid range options
        valid_ranges = self.config.CHART["range_options"].keys()
        if date_range not in valid_ranges:
            raise ValueError(f"'{date_range}' is invalid. Must be one of: {', '.join(valid_ranges)}")
    
    def validate_chart_metric(self,chart_metric: Any) -> None:
        """Validate chart metric selection.
        
        Args:
            chart_metric: Chart metric to validate
            
        Raises:
            ValueError: If chart metric is invalid
        """
        if not isinstance(chart_metric, str):
            raise ValueError(f"Chart metric must be a string, got {type(chart_metric).__name__}")
        
        # Special case for no metrics selected
        if chart_metric == "No metrics selected":
            raise ValueError("At least one metric must be selected")
        
        # Check if metric exists in config
        metric_labels = [metric_data['label'] for metric_data in self.config.METRICS.values()]
        if chart_metric not in metric_labels:
            raise ValueError(f"Chart metric '{chart_metric}' not found")
    
    def validate_complete_state(self, state_manager: Any) -> None:
        """Validate complete application state.
        
        Consolidates all state validation into a single method.
        
        Args:
            state_manager: Application state manager to validate
            
        Raises:
            ValueError: If any validation fails
        """
        try:
            # Validate city
            if hasattr(state_manager, 'get_current_city'):
                city = state_manager.get_current_city()
                self.validate_city_name(city)
            
            # Validate unit system
            if hasattr(state_manager, 'get_current_unit_system'):
                unit_system = state_manager.get_current_unit_system()
                self.validate_unit_system(unit_system)
            
            # Validate metric visibility
            self.validate_metric_visibility(state_manager)
            
            # Validate date range
            if hasattr(state_manager, 'get_current_range'):
                date_range = state_manager.get_current_range()
                self.validate_date_range(date_range)
            
            # Validate chart metric
            if hasattr(state_manager, 'get_current_chart_metric'):
                chart_metric = state_manager.get_current_chart_metric()
                self.validate_chart_metric(chart_metric)
            
        except Exception as e:
            self.logger.error(f"Error during complete state validation: {e}")
            raise
    
    def validate_input_types(self, city_name: Any, unit_system: Any = None) -> None:
        """Validate input parameter types for controller operations.
        
        Consolidates input validation from controller._validate_inputs_and_state.
        
        Args:
            city_name: City name input to validate
            unit_system: Unit system input to validate (optional)
            
        Raises:
            ValueError: If any validation fails
        """
        # Validate city name
        self.validate_city_name(city_name)
        
        # Validate unit system if provided
        if unit_system is not None:
            self.validate_unit_system(unit_system)
    
    def is_valid_numeric_range(self, value: Union[int, float], min_val: Optional[Union[int, float]] = None, max_val: Optional[Union[int, float]] = None, field_name: str = "Value") -> None:
        """Validate numeric value is within specified range.
        
        Args:
            value: Numeric value to validate
            min_val: Minimum allowed value (optional)
            max_val: Maximum allowed value (optional)
            field_name: Name of field for error messages
            
        Raises:
            ValueError: If value is invalid
        """
        # Type validation
        if not isinstance(value, (int, float)):
            raise ValueError(f"{field_name} must be a number, got {type(value).__name__}")
        
        # Range validation
        if min_val is not None and value < min_val:
            raise ValueError(f"{field_name} must be >= {min_val}, got {value}")
        
        if max_val is not None and value > max_val:
            raise ValueError(f"{field_name} must be <= {max_val}, got {value}")