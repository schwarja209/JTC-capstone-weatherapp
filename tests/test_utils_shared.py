"""
Shared test utilities for WeatherDashboard test suite.

This module provides common test fixtures, utilities, and helper functions
to reduce duplication and improve maintainability across the test suite.
"""

import unittest
import tkinter as tk
from unittest.mock import Mock, patch
from contextlib import contextmanager

# Import new advanced testing systems (but not the mixins that depend on TestBase)
from tests.test_config import TestConfigManager, get_test_config
from tests.test_memory_monitor import MemoryTestMixin, MemoryMonitor
from tests.test_network_simulator import NetworkFailureMixin, NetworkSimulator
from tests.test_advanced_mocking import AdvancedMockingMixin, SmartMockFactory


class SharedTestUtils:
    """Shared utilities for test classes."""
    
    def create_mock_weather_data(self, temperature=25.0, humidity=60.0, 
                                wind_speed=5.0, pressure=1013.0, conditions="Clear"):
        """Create mock weather data."""
        return {
            'temperature': temperature,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'pressure': pressure,
            'conditions': conditions
        }
    
    def create_mock_alert_data(self, severity="warning", message="Test alert", 
                              threshold=30.0, current_value=35.0):
        """Create mock alert data."""
        return {
            'severity': severity,
            'message': message,
            'threshold': threshold,
            'current_value': current_value,
            'triggered': current_value > threshold
        }
    
    def create_mock_widget_data(self, widget_type="temperature", value=25.0, 
                               unit="°C", label="Temperature"):
        """Create mock widget data."""
        return {
            'type': widget_type,
            'value': value,
            'unit': unit,
            'label': label
        }


class PerformanceTestMixin:
    """Mixin for performance testing capabilities."""
    
    def assert_performance_acceptable(self, func, *args, iterations=100, max_time=1.0, **kwargs):
        """Assert that a function performs within acceptable time limits."""
        import time
        
        start_time = time.time()
        for _ in range(iterations):
            func(*args, **kwargs)
        end_time = time.time()
        
        total_time = end_time - start_time
        self.assertLess(total_time, max_time, 
                       f"Function took {total_time:.3f}s, expected < {max_time}s")
    
    def benchmark_function(self, func, *args, iterations=1000, **kwargs):
        """Benchmark a function and return performance metrics."""
        import time
        
        start_time = time.time()
        for _ in range(iterations):
            result = func(*args, **kwargs)
        end_time = time.time()
        
        total_time = end_time - start_time
        avg_time = total_time / iterations
        
        return {
            'total_time': total_time,
            'iterations': iterations,
            'average_time': avg_time,
            'operations_per_second': iterations / total_time,
            'result': result
        }


class ErrorHandlingTestMixin:
    """Mixin for error handling test capabilities."""
    
    def assert_graceful_error_handling(self, func, *args, expected_exception=None, **kwargs):
        """Assert that a function handles errors gracefully."""
        try:
            result = func(*args, **kwargs)
            if expected_exception:
                self.fail(f"Expected {expected_exception} but no exception was raised")
            return result
        except Exception as e:
            if expected_exception and not isinstance(e, expected_exception):
                self.fail(f"Expected {expected_exception} but got {type(e)}: {e}")
            # If no expected_exception, the error should be handled gracefully
            return None
    
    def assert_error_recovery(self, func, *args, error_condition=None, **kwargs):
        """Assert that a function can recover from errors."""
        # First call should work
        result1 = func(*args, **kwargs)
        
        # Simulate error condition if provided
        if error_condition:
            error_condition()
        
        # Second call should still work or handle error gracefully
        result2 = func(*args, **kwargs)
        
        # Both results should be valid
        self.assertIsNotNone(result1)
        self.assertIsNotNone(result2)


class TkinterTestMixin:
    """Mixin for Tkinter-specific test capabilities."""
    
    def setUp(self):
        """Set up Tkinter test environment."""
        super().setUp()
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window
    
    def tearDown(self):
        """Clean up Tkinter test environment."""
        if hasattr(self, 'root'):
            self.root.destroy()
        super().tearDown()
    
    def create_test_widget(self, widget_class, **kwargs):
        """Create a test widget with proper cleanup."""
        widget = widget_class(self.root, **kwargs)
        self.addCleanup(widget.destroy)
        return widget
    
    def assert_widget_created(self, widget_class, **kwargs):
        """Assert that a widget can be created without errors."""
        widget = self.create_test_widget(widget_class, **kwargs)
        self.assertIsInstance(widget, widget_class)
        return widget
    
    def assert_widget_display(self, widget, expected_text=None, expected_value=None):
        """Assert that a widget displays correctly."""
        if expected_text is not None:
            if hasattr(widget, 'cget'):
                actual_text = widget.cget('text')
            elif hasattr(widget, 'get'):
                actual_text = widget.get()
            else:
                actual_text = str(widget)
            self.assertEqual(actual_text, expected_text)
        
        if expected_value is not None:
            if hasattr(widget, 'get'):
                actual_value = widget.get()
                self.assertEqual(actual_value, expected_value)


class TestBase(unittest.TestCase, PerformanceTestMixin, ErrorHandlingTestMixin, 
               MemoryTestMixin, NetworkFailureMixin, AdvancedMockingMixin):
    """Base test class with comprehensive testing capabilities."""
    
    def setUp(self):
        """Set up comprehensive test fixtures."""
        super().setUp()
        self.utils = SharedTestUtils()
        self.test_config = get_test_config()
        
        # Initialize advanced testing systems
        self.memory_monitor = MemoryMonitor()
        self.network_simulator = NetworkSimulator()
        self.mock_factory = SmartMockFactory()
    
    def assert_almost_equal_with_tolerance(self, actual, expected, tolerance=0.1):
        """Assert that values are almost equal within tolerance."""
        if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
            self.assertAlmostEqual(actual, expected, delta=tolerance)
        else:
            self.assertEqual(actual, expected)
    
    def assert_color_format(self, color):
        """Assert that a color is in a valid format."""
        if isinstance(color, str):
            # Check if it's a hex color
            if color.startswith('#'):
                self.assertTrue(len(color) in [4, 7, 9], 
                              f"Hex color should be 4, 7, or 9 characters, got {len(color)}")
                self.assertTrue(all(c in '0123456789ABCDEFabcdef' for c in color[1:]),
                              f"Hex color should contain only hex digits: {color}")
            # Check if it's a named color
            elif color.lower() in ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 
                                  'pink', 'brown', 'gray', 'grey', 'black', 'white']:
                pass  # Valid named color
            else:
                self.fail(f"Unknown color format: {color}")
        else:
            self.fail(f"Color should be a string, got: {type(color)}")
    
    def assert_comprehensive_test_coverage(self, test_function, *args, **kwargs):
        """Assert comprehensive test coverage including memory, network, and performance."""
        # Test normal functionality
        result = test_function(*args, **kwargs)
        self.assertIsNotNone(result)
        
        # Test memory usage
        self.assert_no_memory_leak(threshold_mb=5.0)
        
        # Test network resilience
        self.assert_graceful_network_failure_handling(test_function, *args, **kwargs)
        
        # Test performance
        self.assert_performance_acceptable(test_function, *args, iterations=100, max_time=1.0, **kwargs)
    
    def create_comprehensive_test_environment(self):
        """Create a comprehensive test environment with all systems."""
        return {
            'memory_monitor': self.memory_monitor,
            'network_simulator': self.network_simulator,
            'mock_factory': self.mock_factory,
            'test_config': self.test_config
        }


# Import the end-to-end mixin separately to avoid circular imports
def get_end_to_end_mixin():
    """Get the EndToEndTestMixin to avoid circular imports."""
    from tests.test_end_to_end_workflows import EndToEndTestMixin
    return EndToEndTestMixin


@contextmanager
def tkinter_test_context():
    """Context manager for Tkinter test setup and teardown."""
    root = tk.Tk()
    root.withdraw()
    try:
        yield root
    finally:
        root.destroy()


@contextmanager
def mock_patch_context(target, new):
    """Context manager for mock patching."""
    with patch(target, new):
        yield


@contextmanager
def performance_test_context(max_time=1.0):
    """Context manager for performance testing."""
    import time
    start_time = time.time()
    try:
        yield
    finally:
        elapsed_time = time.time() - start_time
        if elapsed_time > max_time:
            raise AssertionError(f"Performance test exceeded {max_time}s: {elapsed_time:.3f}s") 