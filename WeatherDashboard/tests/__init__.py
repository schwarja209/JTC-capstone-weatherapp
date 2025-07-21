"""
Test package for Weather Dashboard.

This package contains comprehensive unit tests for all major components
of the Weather Dashboard application including data management, utilities,
state management, and test execution coordination.

Modules:
    test_data_manager: Tests for weather data management functionality
    test_unit_converter: Tests for unit conversion utilities
    test_state_manager: Tests for application state management
    test_utils: Tests for general utility functions
    test_runner: Test discovery and execution coordination
    test_alert_manager: Tests weather alert system functionality 
    test_controller: Tests core business logic orchestration 
    test_derived_metrics: Tests derived weather metric calculations 
    test_weather_service: Tests API integration, data parsing, validation, and error handling 
    test_view_models: Tests view model data formatting and presentation logic 
    test_color_utils: Tests color determination logic for metric values 
    test_error_handler: Tests theme-aware error handling 
"""

__all__ = [
    "test_data_manager",
    "test_unit_converter", 
    "test_state_manager",
    "test_utils",
    "test_runner",
    "test_alert_manager",
    "test_controller",
    "test_derived_metrics",
    "test_weather_service",
    "test_view_models",
    "test_color_utils",
    "test_error_handler"
]