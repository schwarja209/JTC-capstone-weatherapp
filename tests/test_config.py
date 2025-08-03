"""
Test configuration system for WeatherDashboard test suite.

This module provides centralized configuration management for test categories,
environments, and settings to improve test organization and execution.
"""

import os
import sys
from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


class TestCategory(Enum):
    """Test categories for organization and selective execution."""
    UNIT = "unit"
    INTEGRATION = "integration"
    PERFORMANCE = "performance"
    ERROR_HANDLING = "error_handling"
    GUI = "gui"
    NETWORK = "network"
    MEMORY = "memory"
    END_TO_END = "end_to_end"


class TestEnvironment(Enum):
    """Test environments for different execution contexts."""
    LOCAL = "local"
    CI = "ci"
    DEBUG = "debug"
    PERFORMANCE = "performance"


@dataclass
class TestConfig:
    """Configuration for test execution and behavior."""
    
    # Test categories to run
    categories: List[TestCategory] = field(default_factory=lambda: [
        TestCategory.UNIT, TestCategory.INTEGRATION, TestCategory.ERROR_HANDLING
    ])
    
    # Test environment
    environment: TestEnvironment = TestEnvironment.LOCAL
    
    # Performance thresholds
    max_test_time: float = 5.0  # seconds
    max_memory_usage: int = 100  # MB
    performance_iterations: int = 1000
    
    # Error handling settings
    network_timeout: float = 10.0  # seconds
    retry_attempts: int = 3
    graceful_failure_timeout: float = 2.0  # seconds
    
    # GUI testing settings
    gui_timeout: float = 5.0  # seconds
    widget_creation_timeout: float = 2.0  # seconds
    
    # Memory leak detection
    memory_check_interval: int = 10  # tests
    memory_threshold_mb: int = 50
    
    # Test data settings
    use_real_weather_data: bool = False
    mock_data_variations: int = 5
    
    # Reporting settings
    verbose_output: bool = True
    generate_coverage_report: bool = True
    save_test_artifacts: bool = False
    
    # Parallel execution settings
    max_parallel_tests: int = 4
    parallel_timeout: float = 30.0  # seconds


class TestConfigManager:
    """Manages test configuration and provides utilities for test execution."""
    
    def __init__(self, config: Optional[TestConfig] = None):
        """Initialize the test configuration manager."""
        self.config = config or TestConfig()
        self._load_environment_overrides()
    
    def _load_environment_overrides(self):
        """Load configuration overrides from environment variables."""
        # Environment-specific overrides
        if os.getenv('CI'):
            self.config.environment = TestEnvironment.CI
            self.config.verbose_output = False
            self.config.max_parallel_tests = 2
        
        if os.getenv('DEBUG_TESTS'):
            self.config.environment = TestEnvironment.DEBUG
            self.config.verbose_output = True
            self.config.max_test_time = 30.0
        
        if os.getenv('PERFORMANCE_TESTS'):
            self.config.environment = TestEnvironment.PERFORMANCE
            self.config.categories = [TestCategory.PERFORMANCE, TestCategory.MEMORY]
            self.config.performance_iterations = 10000
    
    def should_run_category(self, category: TestCategory) -> bool:
        """Check if a test category should be executed."""
        return category in self.config.categories
    
    def get_performance_thresholds(self) -> Dict[str, Any]:
        """Get performance testing thresholds."""
        return {
            'max_time': self.config.max_test_time,
            'max_memory_mb': self.config.max_memory_usage,
            'iterations': self.config.performance_iterations
        }
    
    def get_error_handling_config(self) -> Dict[str, Any]:
        """Get error handling configuration."""
        return {
            'network_timeout': self.config.network_timeout,
            'retry_attempts': self.config.retry_attempts,
            'graceful_timeout': self.config.graceful_failure_timeout
        }
    
    def get_gui_config(self) -> Dict[str, Any]:
        """Get GUI testing configuration."""
        return {
            'timeout': self.config.gui_timeout,
            'widget_timeout': self.config.widget_creation_timeout
        }
    
    def get_memory_config(self) -> Dict[str, Any]:
        """Get memory leak detection configuration."""
        return {
            'check_interval': self.config.memory_check_interval,
            'threshold_mb': self.config.memory_threshold_mb
        }
    
    def is_verbose(self) -> bool:
        """Check if verbose output is enabled."""
        return self.config.verbose_output
    
    def should_generate_coverage(self) -> bool:
        """Check if coverage reports should be generated."""
        return self.config.generate_coverage_report


# Global test configuration instance
test_config_manager = TestConfigManager()


def get_test_config() -> TestConfigManager:
    """Get the global test configuration manager."""
    return test_config_manager


def set_test_config(config: TestConfig):
    """Set a new test configuration."""
    global test_config_manager
    test_config_manager = TestConfigManager(config)


def get_category_decorator(category: TestCategory):
    """Decorator to mark test methods with categories."""
    def decorator(test_method):
        test_method.test_category = category
        return test_method
    return decorator


def skip_if_category_disabled(category: TestCategory):
    """Decorator to skip tests if category is disabled."""
    def decorator(test_method):
        def wrapper(self, *args, **kwargs):
            if not test_config_manager.should_run_category(category):
                self.skipTest(f"Category {category.value} is disabled")
            return test_method(self, *args, **kwargs)
        return wrapper
    return decorator


# Convenience decorators for common test categories
def unit_test(test_method):
    """Decorator for unit tests."""
    return get_category_decorator(TestCategory.UNIT)(test_method)


def integration_test(test_method):
    """Decorator for integration tests."""
    return get_category_decorator(TestCategory.INTEGRATION)(test_method)


def performance_test(test_method):
    """Decorator for performance tests."""
    return get_category_decorator(TestCategory.PERFORMANCE)(test_method)


def error_handling_test(test_method):
    """Decorator for error handling tests."""
    return get_category_decorator(TestCategory.ERROR_HANDLING)(test_method)


def gui_test(test_method):
    """Decorator for GUI tests."""
    return get_category_decorator(TestCategory.GUI)(test_method)


def memory_test(test_method):
    """Decorator for memory leak tests."""
    return get_category_decorator(TestCategory.MEMORY)(test_method)


def end_to_end_test(test_method):
    """Decorator for end-to-end tests."""
    return get_category_decorator(TestCategory.END_TO_END)(test_method)


if __name__ == '__main__':
    # Test the configuration system
    config = TestConfigManager()
    print(f"Environment: {config.config.environment}")
    print(f"Categories: {[cat.value for cat in config.config.categories]}")
    print(f"Performance thresholds: {config.get_performance_thresholds()}") 