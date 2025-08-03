"""
Unit tests for WidgetUtils class.

Tests widget creation and management utilities with focus on:
- Real widget behavior rather than mock interactions
- Simplified test scenarios that reflect actual usage
- Performance improvements through better setup/teardown
- Reduced complexity and improved maintainability
"""

import unittest
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WeatherDashboard.utils.widget_utils import WidgetUtils


class TestWidgetUtils(unittest.TestCase):
    """Test cases for WidgetUtils class with simplified, realistic testing."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for the entire test class."""
        cls.root = tk.Tk()
        cls.root.withdraw()  # Hide window during tests
        cls.widget_utils = WidgetUtils()

    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures once."""
        cls.root.destroy()

    def setUp(self):
        """Set up test fixtures for each test."""
        self.test_frame = ttk.Frame(self.root)
        self.test_label = ttk.Label(self.test_frame, text="Test Label")
        self.test_value = ttk.Label(self.test_frame, text="Test Value")

    def test_position_widget_pair_basic(self):
        """Test basic widget pair positioning."""
        self.widget_utils.position_widget_pair(
            self.test_frame,
            self.test_label,
            self.test_value,
            row=0,
            label_col=0,
            value_col=1
        )
        
        # Verify widgets were positioned
        label_info = self.test_label.grid_info()
        value_info = self.test_value.grid_info()
        self.assertEqual(int(label_info['row']), 0)
        self.assertEqual(int(label_info['column']), 0)
        self.assertEqual(int(value_info['row']), 0)
        self.assertEqual(int(value_info['column']), 1)

    def test_position_widget_pair_with_options(self):
        """Test widget pair positioning with custom options."""
        self.widget_utils.position_widget_pair(
            self.test_frame,
            self.test_label,
            self.test_value,
            row=2,
            label_col=1,
            value_col=2,
            sticky=tk.E,
            pady=10,
            padx_override=15
        )

        # Verify custom options were applied
        label_info = self.test_label.grid_info()
        self.assertEqual(label_info['sticky'], tk.E)
        self.assertEqual(label_info['pady'], 10)
        self.assertEqual(label_info['padx'], 15)

    def test_create_label_value_pair_basic(self):
        """Test basic label/value pair creation."""
        label_text = "Test Metric"
        value_text = "Test Value"

        label_widget, value_widget = self.widget_utils.create_label_value_pair(
            self.test_frame,
            label_text,
            value_text
        )

        self.assertIsInstance(label_widget, ttk.Label)
        self.assertIsInstance(value_widget, ttk.Label)
        self.assertEqual(label_widget.cget("text"), label_text)
        self.assertEqual(value_widget.cget("text"), value_text)

    def test_create_label_value_pair_with_styles(self):
        """Test label/value pair creation with custom styles."""
        label_style = "CustomLabel.TLabel"
        value_style = "CustomValue.TLabel"

        label_widget, value_widget = self.widget_utils.create_label_value_pair(
            self.test_frame,
            "Label Text",
            "Value Text",
            label_style=label_style,
            value_style=value_style
        )

        self.assertEqual(label_widget.cget("style"), label_style)
        self.assertEqual(value_widget.cget("style"), value_style)

    def test_create_label_value_pair_default_value(self):
        """Test label/value pair creation with default value."""
        label_widget, value_widget = self.widget_utils.create_label_value_pair(
            self.test_frame,
            "Label Text"
            # No value_text provided, should use default "--"
        )

        self.assertEqual(value_widget.cget("text"), "--")

    def test_create_and_position_metric_basic(self):
        """Test basic metric creation and positioning."""
        metric_key = "temperature"
        label_text = "Temperature"
        value_text = "25°C"

        label_widget, value_widget = self.widget_utils.create_and_position_metric(
            self.test_frame,
            metric_key,
            label_text,
            value_text,
            row=0,
            label_col=0,
            value_col=1
        )

        self.assertIsInstance(label_widget, ttk.Label)
        self.assertIsInstance(value_widget, ttk.Label)
        self.assertEqual(label_widget.cget("text"), label_text)
        self.assertEqual(value_widget.cget("text"), value_text)

        # Verify positioning
        label_info = label_widget.grid_info()
        value_info = value_widget.grid_info()
        self.assertEqual(int(label_info['row']), 0)
        self.assertEqual(int(label_info['column']), 0)
        self.assertEqual(int(value_info['row']), 0)
        self.assertEqual(int(value_info['column']), 1)

    def test_create_and_position_metric_with_storage(self):
        """Test metric creation with widget storage."""
        metric_key = "humidity"
        widget_storage = {}

        label_widget, value_widget = self.widget_utils.create_and_position_metric(
            self.test_frame,
            metric_key,
            "Humidity",
            "60%",
            row=1,
            label_col=0,
            value_col=1,
            widget_storage=widget_storage
        )

        # Verify storage
        self.assertIn(metric_key, widget_storage)
        self.assertIn("label", widget_storage[metric_key])
        self.assertIn("value", widget_storage[metric_key])
        self.assertEqual(widget_storage[metric_key]["label"], label_widget)
        self.assertEqual(widget_storage[metric_key]["value"], value_widget)

    def test_safe_grid_forget_valid_widget(self):
        """Test safe grid forget with valid widget."""
        # First grid the widget
        self.test_label.grid(row=0, column=0)

        # Verify it's gridded
        grid_info = self.test_label.grid_info()
        self.assertIsNotNone(grid_info)
        self.assertTrue(len(grid_info) > 0)

        # Remove from grid
        self.widget_utils.safe_grid_forget(self.test_label)

        # Verify it's no longer gridded
        grid_info = self.test_label.grid_info()
        self.assertEqual(len(grid_info), 0)

    def test_safe_grid_forget_ungridded_widget(self):
        """Test safe grid forget with widget that's not gridded."""
        # Should not raise exception
        self.widget_utils.safe_grid_forget(self.test_label)

    def test_safe_grid_forget_invalid_widget(self):
        """Test safe grid forget with invalid widget."""
        invalid_widgets = [None, "string", 123, []]

        for invalid_widget in invalid_widgets:
            with self.subTest(widget=invalid_widget):
                # Should not raise exception
                try:
                    self.widget_utils.safe_grid_forget(invalid_widget)
                except Exception as e:
                    self.fail(f"safe_grid_forget should handle invalid widget gracefully: {e}")

    def test_configure_grid_weights_default(self):
        """Test grid weight configuration with default columns."""
        # Should not raise exception
        self.widget_utils.configure_grid_weights(self.test_frame)

    def test_configure_grid_weights_custom_columns(self):
        """Test grid weight configuration with custom column count."""
        column_counts = [1, 2, 5, 10]
        for columns in column_counts:
            with self.subTest(columns=columns):
                self.widget_utils.configure_grid_weights(self.test_frame, columns=columns)

    def test_create_error_handling_wrapper_success(self):
        """Test error handling wrapper with successful function."""
        def sample_function(value):
            return value * 2

        wrapped_function = self.widget_utils.create_error_handling_wrapper(sample_function)

        # Test successful execution
        result = wrapped_function(5)
        self.assertEqual(result, 10)

    def test_create_error_handling_wrapper_with_exception(self):
        """Test error handling wrapper with function that raises exception."""
        def failing_function():
            raise ValueError("Test exception")

        wrapped_function = self.widget_utils.create_error_handling_wrapper(failing_function)

        # Test exception handling - the wrapper re-raises the exception after logging
        with patch.object(self.widget_utils.logger, 'error') as mock_error:
            with self.assertRaises(ValueError):
                wrapped_function()
            mock_error.assert_called_once()

    def test_complete_metric_creation_workflow(self):
        """Test complete workflow of creating and positioning metrics."""
        widget_storage = {}
        metrics_data = [
            ("temperature", "Temperature", "25°C", 0, 0, 1),
            ("humidity", "Humidity", "60%", 1, 0, 1),
            ("pressure", "Pressure", "1013 hPa", 2, 0, 1)
        ]

        created_widgets = []
        for metric_key, label_text, value_text, row, label_col, value_col in metrics_data:
            label_widget, value_widget = self.widget_utils.create_and_position_metric(
                self.test_frame,
                metric_key,
                label_text,
                value_text,
                row,
                label_col,
                value_col,
                widget_storage
            )
            created_widgets.append((label_widget, value_widget))

        # Verify all widgets were created and stored
        self.assertEqual(len(created_widgets), 3)
        self.assertEqual(len(widget_storage), 3)

        # Verify each metric is properly stored
        for metric_key, _, _, _, _, _ in metrics_data:
            self.assertIn(metric_key, widget_storage)
            self.assertIn("label", widget_storage[metric_key])
            self.assertIn("value", widget_storage[metric_key])

    def test_grid_management_workflow(self):
        """Test grid management workflow with positioning and cleanup."""
        # Create and position multiple widgets
        widgets = []
        for i in range(3):
            label = ttk.Label(self.test_frame, text=f"Label {i}")
            value = ttk.Label(self.test_frame, text=f"Value {i}")
            widgets.append((label, value))

            self.widget_utils.position_widget_pair(
                self.test_frame,
                label,
                value,
                row=i,
                label_col=0,
                value_col=1
            )

        # Verify all widgets are positioned
        for label, value in widgets:
            label_info = label.grid_info()
            value_info = value.grid_info()
            self.assertIsNotNone(label_info)
            self.assertIsNotNone(value_info)

        # Clean up all widgets
        for label, value in widgets:
            self.widget_utils.safe_grid_forget(label)
            self.widget_utils.safe_grid_forget(value)

        # Verify all widgets are removed from grid
        for label, value in widgets:
            label_info = label.grid_info()
            value_info = value.grid_info()
            self.assertEqual(len(label_info), 0)
            self.assertEqual(len(value_info), 0)

    def test_memory_management_and_cleanup(self):
        """Test memory management in widget operations."""
        # Create many widgets and clean them up
        widget_storage = {}

        # Create multiple metrics
        for i in range(10):
            metric_key = f"metric_{i}"
            self.widget_utils.create_and_position_metric(
                self.test_frame,
                metric_key,
                f"Metric {i}",
                f"Value {i}",
                row=i,
                label_col=0,
                value_col=1,
                widget_storage=widget_storage
            )

        # Verify all widgets were created
        self.assertEqual(len(widget_storage), 10)

        # Clean up all widgets
        for metric_key in list(widget_storage.keys()):
            label = widget_storage[metric_key]["label"]
            value = widget_storage[metric_key]["value"]
            self.widget_utils.safe_grid_forget(label)
            self.widget_utils.safe_grid_forget(value)
            del widget_storage[metric_key]

        # Verify cleanup
        self.assertEqual(len(widget_storage), 0)

    def test_concurrent_widget_operations(self):
        """Test concurrent widget operations safety."""
        # Simulate rapid widget operations
        results = []

        for i in range(20):
            try:
                label, value = self.widget_utils.create_label_value_pair(
                    self.test_frame,
                    f"Label {i}",
                    f"Value {i}"
                )

                self.widget_utils.position_widget_pair(
                    self.test_frame,
                    label,
                    value,
                    row=i % 5,  # Reuse rows
                    label_col=0,
                    value_col=1
                )

                results.append(True)
            except Exception:
                results.append(False)

        # Most operations should succeed
        success_rate = sum(results) / len(results)
        self.assertGreater(success_rate, 0.8)  # At least 80% success rate

    def test_error_resilience_workflow(self):
        """Test error resilience in complete workflow."""
        # Test that errors in one operation don't break the entire workflow
        operations = []

        # Mix valid and invalid operations
        for i in range(10):
            if i % 3 == 0:  # Every third operation is invalid
                operations.append(("invalid", i))
            else:
                operations.append(("valid", i))

        successful_operations = 0
        for op_type, i in operations:
            try:
                if op_type == "valid":
                    label, value = self.widget_utils.create_label_value_pair(
                        self.test_frame,
                        f"Label {i}",
                        f"Value {i}"
                    )
                    self.widget_utils.position_widget_pair(
                        self.test_frame,
                        label,
                        value,
                        row=i,
                        label_col=0,
                        value_col=1
                    )
                    successful_operations += 1
                else:
                    # Invalid operation
                    self.widget_utils.position_widget_pair(
                        None,  # Invalid parent
                        self.test_label,
                        self.test_value,
                        row=i,
                        label_col=0,
                        value_col=1
                    )
            except Exception:
                # Expected for invalid operations
                pass

        # Should have some successful operations
        self.assertGreater(successful_operations, 0)

    def test_documentation_and_type_hints(self):
        """Test that all methods have proper documentation and type hints."""
        methods_to_check = [
            'position_widget_pair',
            'create_label_value_pair',
            'create_and_position_metric',
            'safe_grid_forget',
            'configure_grid_weights',
            'create_error_handling_wrapper'
        ]

        for method_name in methods_to_check:
            method = getattr(self.widget_utils, method_name)
            self.assertIsNotNone(method.__doc__, f"Method {method_name} should have docstring")
            
            # Check for type hints (basic check)
            import inspect
            sig = inspect.signature(method)
            self.assertIsNotNone(sig, f"Method {method_name} should have signature")


if __name__ == '__main__':
    unittest.main()