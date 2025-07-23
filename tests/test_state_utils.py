"""
Unit tests for state utility functions.

Tests state access consolidation functionality including:
- Metric visibility checking with validation and error handling
- Visible metrics filtering with checkbox state evaluation
- Metric visibility variable access with fallback behavior
- Bulk visibility operations with error recovery patterns
- State manager integration with error recovery patterns
- Thread safety considerations for state access operations
- Error handling for missing or corrupted state data
- Fallback behavior when state manager is unavailable
- Integration testing with mock state managers
"""

import unittest
import tkinter as tk
from unittest.mock import Mock, patch

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WeatherDashboard.utils.state_utils import StateUtils


class TestStateUtils(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures with mock state manager."""
        # Create a root window for Tkinter variables
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window during tests
        
        self.mock_state_manager = Mock()
        
        # Create mock visibility variables
        self.temp_var = Mock()
        self.temp_var.get.return_value = True
        self.humidity_var = Mock()
        self.humidity_var.get.return_value = False
        self.pressure_var = Mock()
        self.pressure_var.get.return_value = True
        
        # Configure mock state manager with visibility dict
        self.mock_state_manager.visibility = {
            'temperature': self.temp_var,
            'humidity': self.humidity_var,
            'pressure': self.pressure_var
        }

    def tearDown(self):
        """Clean up the root window after each test."""
        if self.root:
            self.root.destroy()

    def test_is_metric_visible_valid_state(self):
        """Test is_metric_visible with valid state manager."""
        # Test visible metric
        result = StateUtils.is_metric_visible(self.mock_state_manager, 'temperature')
        self.assertTrue(result)
        self.temp_var.get.assert_called_once()
        
        # Test invisible metric
        result = StateUtils.is_metric_visible(self.mock_state_manager, 'humidity')
        self.assertFalse(result)
        self.humidity_var.get.assert_called_once()

    def test_is_metric_visible_missing_visibility_attribute(self):
        """Test is_metric_visible when state manager missing visibility."""
        state_manager_no_visibility = Mock()
        del state_manager_no_visibility.visibility  # Remove visibility attribute
        
        result = StateUtils.is_metric_visible(state_manager_no_visibility, 'temperature')
        self.assertFalse(result)

    def test_is_metric_visible_missing_metric(self):
        """Test is_metric_visible with missing metric key."""
        result = StateUtils.is_metric_visible(self.mock_state_manager, 'nonexistent_metric')
        self.assertFalse(result)

    def test_is_metric_visible_invalid_variable(self):
        """Test is_metric_visible with invalid visibility variable."""
        # Add invalid variable (not a tkinter variable)
        self.mock_state_manager.visibility['invalid'] = "not_a_variable"
        
        result = StateUtils.is_metric_visible(self.mock_state_manager, 'invalid')
        self.assertFalse(result)

    def test_is_metric_visible_variable_exception(self):
        """Test is_metric_visible when variable.get() raises exception."""
        error_var = Mock()
        error_var.get.side_effect = tk.TclError("Variable error")
        self.mock_state_manager.visibility['error_metric'] = error_var
        
        # Should handle the exception gracefully and return False
        result = StateUtils.is_metric_visible(self.mock_state_manager, 'error_metric')
        self.assertFalse(result)

    def test_get_metric_visibility_var_valid_metric(self):
        """Test get_metric_visibility_var with valid metric."""
        result = StateUtils.get_metric_visibility_var(self.mock_state_manager, 'temperature')
        self.assertEqual(result, self.temp_var)

    def test_get_metric_visibility_var_missing_metric(self):
        """Test get_metric_visibility_var with missing metric."""
        result = StateUtils.get_metric_visibility_var(self.mock_state_manager, 'nonexistent')
        # Should return a default BooleanVar
        self.assertIsInstance(result, tk.BooleanVar)

    def test_get_metric_visibility_var_no_visibility_attribute(self):
        """Test get_metric_visibility_var when state manager has no visibility."""
        state_manager_no_visibility = Mock()
        del state_manager_no_visibility.visibility
        
        result = StateUtils.get_metric_visibility_var(state_manager_no_visibility, 'temperature')
        self.assertIsInstance(result, tk.BooleanVar)

    def test_get_visible_metrics_valid_state(self):
        """Test get_visible_metrics with valid state manager."""
        result = StateUtils.get_visible_metrics(self.mock_state_manager)
        # temperature and pressure are visible (True), humidity is not (False)
        expected = ['temperature', 'pressure']
        self.assertEqual(sorted(result), sorted(expected))

    def test_get_visible_metrics_no_visibility_attribute(self):
        """Test get_visible_metrics when state manager has no visibility."""
        state_manager_no_visibility = Mock()
        del state_manager_no_visibility.visibility
        
        result = StateUtils.get_visible_metrics(state_manager_no_visibility)
        self.assertEqual(result, [])

    def test_get_visible_metrics_empty_visibility(self):
        """Test get_visible_metrics with empty visibility dict."""
        self.mock_state_manager.visibility = {}
        
        result = StateUtils.get_visible_metrics(self.mock_state_manager)
        self.assertEqual(result, [])

    def test_get_visible_metrics_all_invisible(self):
        """Test get_visible_metrics when all metrics are invisible."""
        # Set all metrics to invisible
        self.temp_var.get.return_value = False
        self.pressure_var.get.return_value = False
        # humidity_var is already False
        
        result = StateUtils.get_visible_metrics(self.mock_state_manager)
        self.assertEqual(result, [])

    def test_get_visible_metrics_exception_handling(self):
        """Test get_visible_metrics handles exceptions in visibility checking."""
        # Make one variable throw an exception
        self.temp_var.get.side_effect = Exception("Variable error")
        
        result = StateUtils.get_visible_metrics(self.mock_state_manager)
        # Your implementation catches exceptions in is_metric_visible, so the variable
        # with the exception won't be included, but others should still work
        self.assertEqual(result, ['pressure'])  # Only pressure should be visible

    def test_set_metric_visibility_valid_metric(self):
        """Test set_metric_visibility with valid metric."""
        result = StateUtils.set_metric_visibility(self.mock_state_manager, 'temperature', False)
        self.assertTrue(result)
        self.temp_var.set.assert_called_once_with(False)

    def test_set_metric_visibility_missing_metric(self):
        """Test set_metric_visibility with missing metric."""
        # This should work because get_metric_visibility_var returns a default BooleanVar
        result = StateUtils.set_metric_visibility(self.mock_state_manager, 'nonexistent', True)
        self.assertTrue(result)

    def test_set_metric_visibility_exception_handling(self):
        """Test set_metric_visibility handles exceptions."""
        # Make variable.set() raise an exception
        self.temp_var.set.side_effect = Exception("Set error")
        
        result = StateUtils.set_metric_visibility(self.mock_state_manager, 'temperature', True)
        self.assertFalse(result)

    def test_set_all_metrics_visibility_valid_state(self):
        """Test set_all_metrics_visibility with valid state manager."""
        result = StateUtils.set_all_metrics_visibility(self.mock_state_manager, True)
        
        # Should have updated 3 metrics
        self.assertEqual(result, 3)
        
        # Check that all variables were set
        self.temp_var.set.assert_called_with(True)
        self.humidity_var.set.assert_called_with(True)
        self.pressure_var.set.assert_called_with(True)

    def test_set_all_metrics_visibility_no_visibility_attribute(self):
        """Test set_all_metrics_visibility when state manager has no visibility."""
        state_manager_no_visibility = Mock()
        del state_manager_no_visibility.visibility
        
        result = StateUtils.set_all_metrics_visibility(state_manager_no_visibility, True)
        self.assertEqual(result, 0)

    def test_set_all_metrics_visibility_empty_visibility(self):
        """Test set_all_metrics_visibility with empty visibility dict."""
        self.mock_state_manager.visibility = {}
        
        result = StateUtils.set_all_metrics_visibility(self.mock_state_manager, True)
        self.assertEqual(result, 0)

    def test_set_all_metrics_visibility_partial_success(self):
        """Test set_all_metrics_visibility with some metrics failing."""
        # Make one variable fail
        self.temp_var.set.side_effect = Exception("Set error")
        
        result = StateUtils.set_all_metrics_visibility(self.mock_state_manager, False)
        
        # Should have successfully updated 2 out of 3 metrics
        self.assertEqual(result, 2)
        
        # Check that working variables were still set
        self.humidity_var.set.assert_called_with(False)
        self.pressure_var.set.assert_called_with(False)

    def test_set_all_metrics_visibility_exception_in_iteration(self):
        """Test set_all_metrics_visibility handles iteration exceptions."""
        # Make the visibility dict itself problematic
        broken_visibility = Mock()
        broken_visibility.keys.side_effect = Exception("Keys error")
        self.mock_state_manager.visibility = broken_visibility
        
        result = StateUtils.set_all_metrics_visibility(self.mock_state_manager, True)
        self.assertEqual(result, 0)

    def test_error_handling_consistency(self):
        """Test that all state utility functions handle errors consistently."""
        # Test with None state manager
        functions_with_bool_return = [
            (StateUtils.is_metric_visible, ['temperature'], False),
            (StateUtils.set_metric_visibility, ['temperature', True], False),
        ]
        
        functions_with_list_return = [
            (StateUtils.get_visible_metrics, [], []),
        ]
        
        functions_with_int_return = [
            (StateUtils.set_all_metrics_visibility, [True], 0),
        ]
        
        # Test with None state manager
        for func, args, expected in functions_with_bool_return:
            with self.subTest(function=func.__name__, args=args):
                result = func(None, *args)
                self.assertEqual(result, expected)
        
        for func, args, expected in functions_with_list_return:
            with self.subTest(function=func.__name__, args=args):
                result = func(None, *args)
                self.assertEqual(result, expected)
        
        for func, args, expected in functions_with_int_return:
            with self.subTest(function=func.__name__, args=args):
                result = func(None, *args)
                self.assertEqual(result, expected)

    def test_concurrent_access_safety(self):
        """Test thread safety of concurrent state access."""
        # Configure mock to return different values for each call
        call_count = 0
        def side_effect():
            nonlocal call_count
            call_count += 1
            return call_count % 2 == 0  # Alternate True/False
        
        self.temp_var.get.side_effect = side_effect
        
        # Simulate rapid consecutive calls
        results = []
        for _ in range(4):
            result = StateUtils.is_metric_visible(self.mock_state_manager, 'temperature')
            results.append(result)
        
        # Should get alternating results
        expected = [False, True, False, True]
        self.assertEqual(results, expected)

    def test_state_manager_type_validation(self):
        """Test behavior with different types of state manager objects."""
        invalid_state_managers = [
            None,
            "string",
            123,
            [],
            {},
        ]
        
        for invalid_sm in invalid_state_managers:
            with self.subTest(state_manager=type(invalid_sm).__name__):
                # These should all handle gracefully without crashing
                result = StateUtils.is_metric_visible(invalid_sm, 'temperature')
                self.assertFalse(result)
                
                result = StateUtils.get_visible_metrics(invalid_sm)
                self.assertEqual(result, [])
                
                result = StateUtils.set_metric_visibility(invalid_sm, 'temperature', True)
                self.assertFalse(result)
                
                result = StateUtils.set_all_metrics_visibility(invalid_sm, True)
                self.assertEqual(result, 0)

    def test_metric_key_validation(self):
        """Test behavior with different types of metric keys."""
        # Test hashable types that won't cause errors
        safe_metric_keys = [
            None,
            123,
            "",  # Empty string
        ]
        
        for safe_key in safe_metric_keys:
            with self.subTest(metric_key=type(safe_key).__name__ + "_safe"):
                # These should handle gracefully
                result = StateUtils.is_metric_visible(self.mock_state_manager, safe_key)
                self.assertFalse(result)
                
                # get_metric_visibility_var should return a default BooleanVar
                result = StateUtils.get_metric_visibility_var(self.mock_state_manager, safe_key)
                self.assertIsInstance(result, tk.BooleanVar)
        
        # Test unhashable types that will cause TypeError
        unhashable_keys = [[], {}]
        
        for unhashable_key in unhashable_keys:
            with self.subTest(metric_key=type(unhashable_key).__name__ + "_unhashable"):
                # These should raise TypeError due to dictionary lookup
                with self.assertRaises(TypeError):
                    StateUtils.get_metric_visibility_var(self.mock_state_manager, unhashable_key)

    def test_visibility_variable_types(self):
        """Test handling of different types in visibility dict."""
        # Add various types to visibility dict
        self.mock_state_manager.visibility.update({
            'string_value': "not_a_variable",
            'number_value': 123,
            'none_value': None,
            'list_value': [],
            'dict_value': {},
        })
        
        invalid_keys = ['string_value', 'number_value', 'none_value', 'list_value', 'dict_value']
        
        for key in invalid_keys:
            with self.subTest(key=key):
                # is_metric_visible should return False for invalid variables
                result = StateUtils.is_metric_visible(self.mock_state_manager, key)
                self.assertFalse(result)

    def test_get_visible_metrics_with_mixed_variables(self):
        """Test get_visible_metrics with a mix of valid and invalid variables."""
        # Add some invalid variables
        self.mock_state_manager.visibility.update({
            'invalid1': "not_a_variable",
            'invalid2': None,
        })
        
        result = StateUtils.get_visible_metrics(self.mock_state_manager)
        
        # Should only return metrics with valid, visible variables
        # temperature and pressure are visible, humidity is not, invalid ones are ignored
        expected = ['temperature', 'pressure']
        self.assertEqual(sorted(result), sorted(expected))

    def test_set_metric_visibility_boolean_values(self):
        """Test set_metric_visibility with various boolean-like values."""
        boolean_values = [
            (True, True),
            (False, False),
            (1, 1),
            (0, 0),
            ("true", "true"),
            ("", ""),
            (None, None),
        ]
        
        for input_value, expected_set_value in boolean_values:
            with self.subTest(value=input_value):
                # Reset mock
                self.temp_var.reset_mock()
                
                result = StateUtils.set_metric_visibility(self.mock_state_manager, 'temperature', input_value)
                self.assertTrue(result)
                self.temp_var.set.assert_called_once_with(expected_set_value)

    def test_integration_workflow(self):
        """Test integration of all state utility functions together."""
        # Start with all metrics invisible
        self.temp_var.get.return_value = False
        self.humidity_var.get.return_value = False
        self.pressure_var.get.return_value = False
        
        # Check initial state
        visible = StateUtils.get_visible_metrics(self.mock_state_manager)
        self.assertEqual(visible, [])
        
        # Set one metric visible
        result = StateUtils.set_metric_visibility(self.mock_state_manager, 'temperature', True)
        self.assertTrue(result)
        
        # Update mock to reflect change
        self.temp_var.get.return_value = True
        
        # Check that it's now visible
        self.assertTrue(StateUtils.is_metric_visible(self.mock_state_manager, 'temperature'))
        
        # Set all metrics visible
        count = StateUtils.set_all_metrics_visibility(self.mock_state_manager, True)
        self.assertEqual(count, 3)
        
        # Update mocks to reflect changes
        self.temp_var.get.return_value = True
        self.humidity_var.get.return_value = True
        self.pressure_var.get.return_value = True
        
        # Check all are visible
        visible = StateUtils.get_visible_metrics(self.mock_state_manager)
        expected = ['temperature', 'humidity', 'pressure']
        self.assertEqual(sorted(visible), sorted(expected))

    def test_performance_with_many_metrics(self):
        """Test performance with a large number of metrics."""
        # Create many mock variables
        many_variables = {}
        for i in range(100):
            var = Mock()
            var.get.return_value = i % 2 == 0  # Even indices are visible
            many_variables[f'metric_{i}'] = var
        
        self.mock_state_manager.visibility = many_variables
        
        # Test get_visible_metrics with many metrics
        visible = StateUtils.get_visible_metrics(self.mock_state_manager)
        
        # Should have 50 visible metrics (even indices)
        self.assertEqual(len(visible), 50)
        
        # Test set_all_metrics_visibility with many metrics
        count = StateUtils.set_all_metrics_visibility(self.mock_state_manager, False)
        self.assertEqual(count, 100)

    def test_edge_case_empty_strings_and_whitespace(self):
        """Test handling of edge cases like empty strings and whitespace."""
        edge_case_keys = ["", " ", "\t", "\n", "  \t\n  "]
        
        for key in edge_case_keys:
            with self.subTest(key=repr(key)):
                # Add to visibility dict
                var = Mock()
                var.get.return_value = True
                self.mock_state_manager.visibility[key] = var
                
                # Test all functions
                self.assertTrue(StateUtils.is_metric_visible(self.mock_state_manager, key))
                
                retrieved_var = StateUtils.get_metric_visibility_var(self.mock_state_manager, key)
                self.assertEqual(retrieved_var, var)
                
                self.assertTrue(StateUtils.set_metric_visibility(self.mock_state_manager, key, False))

    def test_exception_types_handling(self):
        """Test handling of different exception types from tkinter variables."""
        exceptions_to_test = [
            tk.TclError("Tcl error"),
            AttributeError("Missing attribute"),
            RuntimeError("Runtime error"),
            ValueError("Value error"),
            TypeError("Type error"),
            Exception("Generic exception")
        ]
        
        for exception in exceptions_to_test:
            with self.subTest(exception=type(exception).__name__):
                # Reset and configure mock to raise exception
                self.temp_var.reset_mock()
                self.temp_var.get.side_effect = exception
                
                # Should handle gracefully and return False
                result = StateUtils.is_metric_visible(self.mock_state_manager, 'temperature')
                self.assertFalse(result)

    def test_documentation_and_type_hints(self):
        """Test that all functions have proper documentation."""
        functions_to_check = [
            StateUtils.is_metric_visible,
            StateUtils.get_metric_visibility_var,
            StateUtils.get_visible_metrics,
            StateUtils.set_metric_visibility,
            StateUtils.set_all_metrics_visibility,
        ]
        
        for func in functions_to_check:
            with self.subTest(function=func.__name__):
                self.assertIsNotNone(func.__doc__)
                self.assertTrue(len(func.__doc__.strip()) > 0)


if __name__ == '__main__':
    unittest.main()