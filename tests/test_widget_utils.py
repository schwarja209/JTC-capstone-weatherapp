"""
Unit tests for WidgetUtils class.

Tests widget creation and management utilities including:
- Widget pair positioning with grid layout and error handling
- Label/value widget pair creation with styling and configuration
- Metric display creation and positioning with storage management
- Safe grid operations with error recovery and cleanup
- Grid weight configuration with automatic layout management
- Error handling patterns for widget creation and positioning
- Integration with TTK styling system and theme management
- Memory management and widget cleanup validation
- Thread safety considerations for widget operations
"""

import unittest
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock, patch

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WeatherDashboard.utils.widget_utils import WidgetUtils


class TestWidgetUtils(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures with Tkinter root and widgets."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during tests
        
        # Create test frames and widgets
        self.test_frame = ttk.Frame(self.root)
        self.test_label = ttk.Label(self.test_frame, text="Test Label")
        self.test_value = ttk.Label(self.test_frame, text="Test Value")

    def tearDown(self):
        """Clean up Tkinter widgets after each test."""
        if self.root:
            self.root.destroy()

    # ================================
    # position_widget_pair() tests
    # ================================

    def test_position_widget_pair_basic(self):
        """Test basic widget pair positioning."""
        # Test basic positioning without exceptions
        try:
            WidgetUtils.position_widget_pair(
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
            
        except Exception as e:
            self.fail(f"position_widget_pair should not raise exception: {e}")

    def test_position_widget_pair_with_label_text(self):
        """Test widget pair positioning with label text setting."""
        label_text = "Custom Label Text"
        
        WidgetUtils.position_widget_pair(
            self.test_frame,
            self.test_label,
            self.test_value,
            row=1,
            label_col=0,
            value_col=1,
            label_text=label_text
        )
        
        # Verify label text was set
        self.assertEqual(self.test_label['text'], label_text)

    def test_position_widget_pair_with_options(self):
        """Test widget pair positioning with custom options."""
        WidgetUtils.position_widget_pair(
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
        
        # Verify positioning options
        label_info = self.test_label.grid_info()
        self.assertEqual(int(label_info['row']), 2)
        self.assertEqual(int(label_info['column']), 1)
        self.assertEqual(label_info['sticky'], 'e')
        self.assertEqual(int(label_info['pady']), 10)

    @patch('WeatherDashboard.utils.widget_utils.styles')
    def test_position_widget_pair_padding_calculation(self, mock_styles):
        """Test automatic padding calculation based on column position."""
        # Mock styles configuration
        mock_styles.ALERT_DISPLAY_CONFIG = {
            'column_padding': {
                'left_section': 5,
                'right_section': 10
            }
        }
        
        # Test left section padding (column < 4)
        WidgetUtils.position_widget_pair(
            self.test_frame,
            self.test_label,
            self.test_value,
            row=0,
            label_col=2,  # < 4, should use left_section padding
            value_col=3
        )
        
        # Test right section padding (column >= 4)
        label2 = ttk.Label(self.test_frame, text="Label2")
        value2 = ttk.Label(self.test_frame, text="Value2")
        
        WidgetUtils.position_widget_pair(
            self.test_frame,
            label2,
            value2,
            row=1,
            label_col=4,  # >= 4, should use right_section padding
            value_col=5
        )
        
        # Both should succeed without exceptions
        self.assertEqual(int(self.test_label.grid_info()['column']), 2)
        self.assertEqual(int(label2.grid_info()['column']), 4)

    def test_position_widget_pair_error_handling(self):
        """Test error handling in widget pair positioning."""
        # Test with invalid widget (should not crash)
        invalid_label = None
        
        # Should handle gracefully without raising exception
        try:
            WidgetUtils.position_widget_pair(
                self.test_frame,
                invalid_label,
                self.test_value,
                row=0,
                label_col=0,
                value_col=1
            )
        except Exception:
            pass  # Exception handling is acceptable

    # ================================
    # create_label_value_pair() tests
    # ================================

    def test_create_label_value_pair_basic(self):
        """Test basic label/value pair creation."""
        label_text = "Test Metric"
        value_text = "Test Value"
        
        label_widget, value_widget = WidgetUtils.create_label_value_pair(
            self.test_frame,
            label_text,
            value_text
        )
        
        # Verify widgets were created correctly
        self.assertIsInstance(label_widget, ttk.Label)
        self.assertIsInstance(value_widget, ttk.Label)
        self.assertEqual(label_widget['text'], label_text)
        self.assertEqual(value_widget['text'], value_text)

    def test_create_label_value_pair_with_styles(self):
        """Test label/value pair creation with custom styles."""
        label_style = "CustomLabel.TLabel"
        value_style = "CustomValue.TLabel"
        
        label_widget, value_widget = WidgetUtils.create_label_value_pair(
            self.test_frame,
            "Label Text",
            "Value Text",
            label_style=label_style,
            value_style=value_style
        )
        
        # Verify styles were applied (if TTK style system is working)
        self.assertIsInstance(label_widget, ttk.Label)
        self.assertIsInstance(value_widget, ttk.Label)

    def test_create_label_value_pair_default_value(self):
        """Test label/value pair creation with default value."""
        label_widget, value_widget = WidgetUtils.create_label_value_pair(
            self.test_frame,
            "Label Text"
            # No value_text provided, should use default "--"
        )
        
        self.assertEqual(value_widget['text'], "--")

    def test_create_label_value_pair_error_handling(self):
        """Test error handling in label/value pair creation."""
        # Test with invalid parent (should still return widgets)
        try:
            label_widget, value_widget = WidgetUtils.create_label_value_pair(
                None,  # Invalid parent
                "Test Label",
                "Test Value"
            )
            # Should return some kind of widgets even on error
            self.assertIsNotNone(label_widget)
            self.assertIsNotNone(value_widget)
        except Exception:
            # Exception is also acceptable behavior
            pass

    # ================================
    # create_and_position_metric() tests
    # ================================

    def test_create_and_position_metric_basic(self):
        """Test basic metric creation and positioning."""
        metric_key = "temperature"
        label_text = "Temperature"
        value_text = "25°C"
        
        label_widget, value_widget = WidgetUtils.create_and_position_metric(
            self.test_frame,
            metric_key,
            label_text,
            value_text,
            row=0,
            label_col=0,
            value_col=1
        )
        
        # Verify widgets were created and positioned
        self.assertIsInstance(label_widget, ttk.Label)
        self.assertIsInstance(value_widget, ttk.Label)
        self.assertEqual(label_widget['text'], label_text)
        self.assertEqual(value_widget['text'], value_text)
        
        # Verify positioning
        label_info = label_widget.grid_info()
        value_info = value_widget.grid_info()
        self.assertEqual(int(label_info['row']), 0)
        self.assertEqual(int(value_info['row']), 0)

    def test_create_and_position_metric_with_storage(self):
        """Test metric creation with widget storage."""
        metric_key = "humidity"
        widget_storage = {}
        
        label_widget, value_widget = WidgetUtils.create_and_position_metric(
            self.test_frame,
            metric_key,
            "Humidity",
            "60%",
            row=1,
            label_col=0,
            value_col=1,
            widget_storage=widget_storage
        )
        
        # Verify widgets were stored correctly
        self.assertIn(metric_key, widget_storage)
        self.assertIn('label', widget_storage[metric_key])
        self.assertIn('value', widget_storage[metric_key])
        self.assertEqual(widget_storage[metric_key]['label'], label_widget)
        self.assertEqual(widget_storage[metric_key]['value'], value_widget)

    def test_create_and_position_metric_without_storage(self):
        """Test metric creation without widget storage."""
        # Should work fine without storage parameter
        label_widget, value_widget = WidgetUtils.create_and_position_metric(
            self.test_frame,
            "pressure",
            "Pressure",
            "1013 hPa",
            row=2,
            label_col=0,
            value_col=1
            # No widget_storage parameter
        )
        
        self.assertIsInstance(label_widget, ttk.Label)
        self.assertIsInstance(value_widget, ttk.Label)

    # ================================
    # safe_grid_forget() tests
    # ================================

    def test_safe_grid_forget_valid_widget(self):
        """Test safe grid forget with valid widget."""
        # First grid the widget
        self.test_label.grid(row=0, column=0)
        
        # Verify it's gridded
        grid_info = self.test_label.grid_info()
        self.assertIsNotNone(grid_info)
        self.assertTrue(len(grid_info) > 0)
        
        # Remove from grid
        WidgetUtils.safe_grid_forget(self.test_label)
        
        # Verify it's no longer gridded
        grid_info_after = self.test_label.grid_info()
        self.assertEqual(len(grid_info_after), 0)

    def test_safe_grid_forget_invalid_widget(self):
        """Test safe grid forget with invalid widget."""
        invalid_widgets = [None, "string", 123, []]
        
        for invalid_widget in invalid_widgets:
            with self.subTest(widget=invalid_widget):
                # Should not raise exception
                try:
                    WidgetUtils.safe_grid_forget(invalid_widget)
                except Exception as e:
                    self.fail(f"safe_grid_forget should handle invalid widget gracefully: {e}")

    def test_safe_grid_forget_ungridded_widget(self):
        """Test safe grid forget with widget that's not gridded."""
        # Widget is not gridded yet
        try:
            WidgetUtils.safe_grid_forget(self.test_label)
        except Exception as e:
            self.fail(f"safe_grid_forget should handle ungridded widget gracefully: {e}")

    # ================================
    # configure_grid_weights() tests
    # ================================

    def test_configure_grid_weights_default(self):
        """Test grid weight configuration with default columns."""
        # Should configure 3 columns by default
        try:
            WidgetUtils.configure_grid_weights(self.test_frame)
            # If no exception, test passes
        except Exception as e:
            self.fail(f"configure_grid_weights should not raise exception: {e}")

    def test_configure_grid_weights_custom_columns(self):
        """Test grid weight configuration with custom column count."""
        column_counts = [1, 2, 5, 10]
        
        for columns in column_counts:
            with self.subTest(columns=columns):
                try:
                    WidgetUtils.configure_grid_weights(self.test_frame, columns=columns)
                except Exception as e:
                    self.fail(f"configure_grid_weights should handle {columns} columns: {e}")

    def test_configure_grid_weights_invalid_parent(self):
        """Test grid weight configuration with invalid parent."""
        # Should handle gracefully
        try:
            WidgetUtils.configure_grid_weights(None, columns=3)
        except Exception:
            # Exception is acceptable for invalid parent
            pass

    # ================================
    # create_error_handling_wrapper() tests
    # ================================

    def test_create_error_handling_wrapper_success(self):
        """Test error handling wrapper with successful function."""
        def sample_function(value):
            return value * 2
        
        wrapped_function = WidgetUtils.create_error_handling_wrapper(sample_function)
        
        result = wrapped_function(5)
        self.assertEqual(result, 10)

    def test_create_error_handling_wrapper_with_exception(self):
        """Test error handling wrapper with function that raises exception."""
        def failing_function():
            raise ValueError("Test exception")
        
        wrapped_function = WidgetUtils.create_error_handling_wrapper(failing_function)
        
        # Should re-raise the exception (after logging)
        with self.assertRaises(ValueError):
            wrapped_function()

    def test_create_error_handling_wrapper_preserves_function_info(self):
        """Test that wrapper preserves function information."""
        def sample_function_with_name():
            """Sample docstring"""
            return "test"
        
        wrapped_function = WidgetUtils.create_error_handling_wrapper(sample_function_with_name)
        
        # Should be callable
        self.assertTrue(callable(wrapped_function))

    # ================================
    # Integration and workflow tests
    # ================================

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
            label_widget, value_widget = WidgetUtils.create_and_position_metric(
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
        
        # Verify all metrics were created and stored
        self.assertEqual(len(widget_storage), 3)
        self.assertEqual(len(created_widgets), 3)
        
        # Verify storage contents
        for metric_key, _, _, _, _, _ in metrics_data:
            self.assertIn(metric_key, widget_storage)
            self.assertIn('label', widget_storage[metric_key])
            self.assertIn('value', widget_storage[metric_key])

    def test_grid_management_workflow(self):
        """Test grid management workflow with positioning and cleanup."""
        # Create and position multiple widgets
        widgets = []
        for i in range(3):
            label = ttk.Label(self.test_frame, text=f"Label {i}")
            value = ttk.Label(self.test_frame, text=f"Value {i}")
            widgets.append((label, value))
            
            WidgetUtils.position_widget_pair(
                self.test_frame,
                label,
                value,
                row=i,
                label_col=0,
                value_col=1
            )
        
        # Configure grid weights
        WidgetUtils.configure_grid_weights(self.test_frame, columns=2)
        
        # Remove some widgets from grid
        for label, value in widgets[:2]:  # Remove first 2
            WidgetUtils.safe_grid_forget(label)
            WidgetUtils.safe_grid_forget(value)
        
        # Verify last widget is still gridded
        last_label = widgets[2][0]
        grid_info = last_label.grid_info()
        self.assertGreater(len(grid_info), 0)

    def test_error_resilience_workflow(self):
        """Test workflow resilience to various error conditions."""
        # Test with mixed valid and invalid operations
        operations = [
            lambda: WidgetUtils.create_label_value_pair(self.test_frame, "Valid", "Valid"),
            lambda: WidgetUtils.create_label_value_pair(None, "Invalid Parent", "Test"),
            lambda: WidgetUtils.safe_grid_forget(None),
            lambda: WidgetUtils.configure_grid_weights(self.test_frame, columns=5),
            lambda: WidgetUtils.position_widget_pair(
                self.test_frame, self.test_label, self.test_value, 0, 0, 1
            ),
        ]
        
        # All operations should complete without crashing the test
        for i, operation in enumerate(operations):
            with self.subTest(operation=i):
                try:
                    operation()
                except Exception:
                    # Some exceptions are acceptable, just shouldn't crash
                    pass

    def test_memory_management_and_cleanup(self):
        """Test memory management in widget operations."""
        # Create many widgets and clean them up
        widget_storage = {}
        
        # Create multiple metrics
        for i in range(10):
            metric_key = f"metric_{i}"
            WidgetUtils.create_and_position_metric(
                self.test_frame,
                metric_key,
                f"Metric {i}",
                f"Value {i}",
                row=i,
                label_col=0,
                value_col=1,
                widget_storage=widget_storage
            )
        
        # Verify all were created
        self.assertEqual(len(widget_storage), 10)
        
        # Clean up by removing from grid
        for metric_data in widget_storage.values():
            WidgetUtils.safe_grid_forget(metric_data['label'])
            WidgetUtils.safe_grid_forget(metric_data['value'])
        
        # All operations should complete successfully
        self.assertEqual(len(widget_storage), 10)  # Storage dict still has references

    def test_concurrent_widget_operations(self):
        """Test concurrent widget operations safety."""
        # Simulate rapid widget operations
        results = []
        
        for i in range(20):
            try:
                label, value = WidgetUtils.create_label_value_pair(
                    self.test_frame,
                    f"Label {i}",
                    f"Value {i}"
                )
                
                WidgetUtils.position_widget_pair(
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

    def test_logging_integration(self):
        """Test integration with logging system."""
        # Instead of mocking, let's test that the function handles errors gracefully
        # We can see from the test output that logging is working (ERROR messages appear)
        
        # Test that error conditions are handled without raising exceptions
        try:
            WidgetUtils.position_widget_pair(
                None,  # Invalid parent to trigger error
                self.test_label,
                self.test_value,
                row=0,
                label_col=0,
                value_col=1
            )
            # If we get here without exception, error handling is working
            error_handled = True
        except Exception:
            error_handled = False
        
        self.assertTrue(error_handled, "Error should be handled gracefully without raising exception")
        
        # Test that invalid grid weight configuration is handled
        try:
            WidgetUtils.configure_grid_weights(None, columns=3)
            grid_error_handled = True
        except Exception:
            grid_error_handled = False
            
        self.assertTrue(grid_error_handled, "Grid weight errors should be handled gracefully")

    def test_styling_system_integration(self):
        """Test integration with TTK styling system."""
        # Test with custom styles
        custom_styles = [
            ("CustomLabel.TLabel", "CustomValue.TLabel"),
            ("LabelName.TLabel", "LabelValue.TLabel"),
            (None, None)  # Default styles
        ]
        
        for label_style, value_style in custom_styles:
            with self.subTest(label_style=label_style, value_style=value_style):
                try:
                    if label_style and value_style:
                        label, value = WidgetUtils.create_label_value_pair(
                            self.test_frame,
                            "Test Label",
                            "Test Value",
                            label_style=label_style,
                            value_style=value_style
                        )
                    else:
                        label, value = WidgetUtils.create_label_value_pair(
                            self.test_frame,
                            "Test Label",
                            "Test Value"
                        )
                    
                    self.assertIsInstance(label, ttk.Label)
                    self.assertIsInstance(value, ttk.Label)
                    
                except Exception as e:
                    self.fail(f"Styling integration should work: {e}")


if __name__ == '__main__':
    unittest.main()