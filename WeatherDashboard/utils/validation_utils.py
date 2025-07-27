"""
Centralized validation utilities for the Weather Dashboard application.

This module provides comprehensive input and state validation functions to eliminate
duplicate validation logic scattered across controller, state manager, and utility
files. Consolidates city name validation, unit system checking, metric visibility
validation, and complete application state verification into a single utility class.

Classes:
    ValidationUtils: Static utility class for centralized validation operations
"""

from typing import List, Any, Optional, Union
import re

from WeatherDashboard import config
from WeatherDashboard.utils.logger import Logger


class ValidationUtils:
    """Centralized validation utilities to eliminate duplicate validation logic."""
    
    def __init__(self) -> None:
        """Initialize validation utils with optional dependencies."""
        # Direct imports for stable utilities
        self.config = config
        self.logger = Logger()

        # Instance data
        self.regex_patterns = {
            'city_name': r"^[a-zA-Z\s\-'\.,]+$",
            'unit_system': r"^(metric|imperial)$"
        }

    def validate_city_name(self, city_name: Any) -> List[str]:
        """Validate city name input with comprehensive checks.
        
        Args:
            city_name: City name to validate (any type)
            
        Returns:
            List[str]: List of validation error messages (empty if valid)
        """
        errors = []
        
        # Type validation
        if not isinstance(city_name, str):
            errors.append(self.config.ERROR_MESSAGES['validation'].format(
                field="City name", reason=f"must be a string, got {type(city_name).__name__}"))
            return errors
        
        # Empty validation
        cleaned_name = city_name.strip()
        if not cleaned_name:
            errors.append(self.config.ERROR_MESSAGES['validation'].format(
                field="City name", reason="cannot be empty"))
            return errors
        
        # Length validation
        if len(cleaned_name) > 100:
            errors.append(self.config.ERROR_MESSAGES['validation'].format(
                field="City name", reason="cannot be longer than 100 characters"))
        
        # Character validation
        if not re.match(self.regex_patterns['city_name'], cleaned_name):
            errors.append(self.config.ERROR_MESSAGES['validation'].format(
                field="City name", reason="contains invalid characters"))
        
        return errors
    
    def validate_unit_system(self, unit_system: Any) -> List[str]:
        """Validate unit system selection.
        
        Args:
            unit_system: Unit system to validate (any type)
            
        Returns:
            List[str]: List of validation error messages (empty if valid)
        """
        errors = []
        
        # Type validation
        if not isinstance(unit_system, str):
            errors.append(self.config.ERROR_MESSAGES['validation'].format(
                field="Unit system", reason=f"must be a string, got {type(unit_system).__name__}"))
            return errors
        
        # Valid options
        valid_units = {'metric', 'imperial'}
        if unit_system not in valid_units:
            errors.append(self.config.ERROR_MESSAGES['validation'].format(
                field="Unit system", reason=f"'{unit_system}' is invalid. Must be 'metric' or 'imperial'"))
        
        return errors
    
    def validate_metric_visibility(self, state_manager: Any) -> List[str]:
        """Validate that at least one metric is visible.
        
        Args:
            state_manager: Application state manager
            
        Returns:
            List[str]: List of validation error messages (empty if valid)
        """
        errors = []
        
        try:
            # Check if state manager has visibility
            if not hasattr(state_manager, 'visibility'):
                errors.append(self.config.ERROR_MESSAGES['state_error'].format(reason="state manager missing visibility attribute"))
                return errors
            
            # Check if any metrics are visible
            visible_count = 0
            for metric_key, visibility_var in state_manager.visibility.items():
                try:
                    if hasattr(visibility_var, 'get') and visibility_var.get():
                        visible_count += 1
                except Exception as e:
                    self.logger.warn(f"Error checking visibility for {metric_key}: {e}")
            
            if visible_count == 0:
                errors.append(self.config.ERROR_MESSAGES['validation'].format(field="Metric selection", reason="at least one metric must be visible"))
            
        except Exception as e:
            errors.append(self.config.ERROR_MESSAGES['state_error'].format(reason=f"failed to validate metric visibility: {e}"))
        
        return errors
    
    def validate_date_range(self, date_range: Any) -> List[str]:
        """Validate date range selection.
        
        Args:
            date_range: Date range to validate
            
        Returns:
            List[str]: List of validation error messages (empty if valid)
        """
        errors = []
        
        if not isinstance(date_range, str):
            errors.append(self.config.ERROR_MESSAGES['validation'].format(field="Date range", reason=f"must be a string, got {type(date_range).__name__}"))
            return errors
        
        # Check against valid range options
        valid_ranges = self.config.CHART["range_options"].keys()
        if date_range not in valid_ranges:
            errors.append(self.config.ERROR_MESSAGES['validation'].format(field="Date range", reason=f"'{date_range}' is invalid. Must be one of: {', '.join(valid_ranges)}"))
        
        return errors
    
    def validate_chart_metric(self,chart_metric: Any) -> List[str]:
        """Validate chart metric selection.
        
        Args:
            chart_metric: Chart metric to validate
            
        Returns:
            List[str]: List of validation error messages (empty if valid)
        """
        errors = []
        
        if not isinstance(chart_metric, str):
            errors.append(self.config.ERROR_MESSAGES['validation'].format(field="Chart metric", reason=f"must be a string, got {type(chart_metric).__name__}"))
            return errors
        
        # Special case for no metrics selected
        if chart_metric == "No metrics selected":
            errors.append(self.config.ERROR_MESSAGES['validation'].format(field="Chart metric", reason="at least one metric must be selected"))
            return errors
        
        # Check if metric exists in config
        metric_labels = [metric_data['label'] for metric_data in self.config.METRICS.values()]
        if chart_metric not in metric_labels:
            errors.append(self.config.ERROR_MESSAGES['not_found'].format(resource="Chart metric", name=chart_metric))
        
        return errors
    
    def validate_complete_state(self, state_manager: Any) -> List[str]:
        """Validate complete application state.
        
        Consolidates all state validation into a single method.
        
        Args:
            state_manager: Application state manager to validate
            
        Returns:
            List[str]: List of all validation error messages (empty if valid)
        """
        all_errors = []
        
        try:
            # Validate city
            if hasattr(state_manager, 'get_current_city'):
                city = state_manager.get_current_city()
                all_errors.extend(self.validate_city_name(city))
            
            # Validate unit system
            if hasattr(state_manager, 'get_current_unit_system'):
                unit_system = state_manager.get_current_unit_system()
                all_errors.extend(self.validate_unit_system(unit_system))
            
            # Validate metric visibility
            all_errors.extend(self.validate_metric_visibility(state_manager))
            
            # Validate date range
            if hasattr(state_manager, 'get_current_range'):
                date_range = state_manager.get_current_range()
                all_errors.extend(self.validate_date_range(date_range))
            
            # Validate chart metric
            if hasattr(state_manager, 'get_current_chart_metric'):
                chart_metric = state_manager.get_current_chart_metric()
                all_errors.extend(self.validate_chart_metric(chart_metric))
            
        except Exception as e:
            all_errors.append(self.config.ERROR_MESSAGES['state_error'].format(
                reason=f"unexpected error during state validation: {e}"))
            self.logger.error(f"Error during complete state validation: {e}")
        
        return all_errors
    
    def validate_input_types(self, city_name: Any, unit_system: Any = None) -> List[str]:
        """Validate input parameter types for controller operations.
        
        Consolidates input validation from controller._validate_inputs_and_state.
        
        Args:
            city_name: City name input to validate
            unit_system: Unit system input to validate (optional)
            
        Returns:
            List[str]: List of validation error messages (empty if valid)
        """
        errors = []
        
        # Validate city name
        errors.extend(self.validate_city_name(city_name))
        
        # Validate unit system if provided
        if unit_system is not None:
            errors.extend(self.validate_unit_system(unit_system))
        
        return errors
    
    def is_valid_numeric_range(self, value: Union[int, float], min_val: Optional[Union[int, float]] = None, max_val: Optional[Union[int, float]] = None, field_name: str = "Value") -> List[str]:
        """Validate numeric value is within specified range.
        
        Args:
            value: Numeric value to validate
            min_val: Minimum allowed value (optional)
            max_val: Maximum allowed value (optional)
            field_name: Name of field for error messages
            
        Returns:
            List[str]: List of validation error messages (empty if valid)
        """
        errors = []
        
        # Type validation
        if not isinstance(value, (int, float)):
            errors.append(self.config.ERROR_MESSAGES['validation'].format(field=field_name, reason=f"must be a number, got {type(value).__name__}"))
            return errors
        
        # Range validation
        if min_val is not None and value < min_val:
            errors.append(self.config.ERROR_MESSAGES['validation'].format(field=field_name, reason=f"must be >= {min_val}, got {value}"))
        
        if max_val is not None and value > max_val:
            errors.append(self.config.ERROR_MESSAGES['validation'].format(field=field_name, reason=f"must be <= {max_val}, got {value}"))
        
        return errors
    
    def format_validation_errors(self, errors: List[str], prefix: str = "Validation failed") -> str:
        """Format list of validation errors into a single message.
        
        Args:
            errors: List of error messages
            prefix: Prefix for the combined message
            
        Returns:
            str: Formatted error message
        """
        if not errors:
            return ""
        
        if len(errors) == 1:
            return f"{prefix}: {errors[0]}"
        else:
            return f"{prefix}: " + "; ".join(errors)