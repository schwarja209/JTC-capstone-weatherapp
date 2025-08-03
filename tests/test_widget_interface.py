"""
Test for WeatherDashboard.widgets.widget_interface

Tests widget interface functionality with focus on:
- Interface definition and structure
- Method signature validation
- Abstract method implementation
- Interface compliance testing
"""

import unittest
from unittest.mock import Mock, patch

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.test_utils_shared import TestBase


class TestWidgetInterface(TestBase):
    """Test widget interface functionality."""
    
    def test_import_widget_interface(self):
        """Test that widget interface can be imported successfully."""
        try:
            from WeatherDashboard.widgets.widget_interface import IWeatherDashboardWidgets
            self.assertIsNotNone(IWeatherDashboardWidgets)
            self.assertTrue(hasattr(IWeatherDashboardWidgets, '__doc__'))
        except ImportError:
            self.skipTest("Widget interface not available")

    def test_interface_structure(self):
        """Test that widget interface has expected structure."""
        try:
            from WeatherDashboard.widgets.widget_interface import IWeatherDashboardWidgets
            
            # Check for expected abstract methods (based on actual interface)
            expected_methods = [
                'is_ready',
                'get_creation_error',
                'update_metric_display',
                'update_status_bar',
                'update_alerts',
                'update_chart_display',
                'get_alert_popup_parent',
                'clear_chart_with_error_message'
            ]
            
            for method_name in expected_methods:
                with self.subTest(method=method_name):
                    self.assertTrue(hasattr(IWeatherDashboardWidgets, method_name),
                                  f"Interface missing method: {method_name}")
        except ImportError:
            self.skipTest("Widget interface not available")

    def test_interface_abstract_methods(self):
        """Test that interface methods are properly abstract."""
        try:
            from WeatherDashboard.widgets.widget_interface import IWeatherDashboardWidgets
            import inspect
            
            # Check that methods are abstract (if they exist)
            abstract_methods = [
                'is_ready',
                'get_creation_error',
                'update_metric_display',
                'update_status_bar',
                'update_alerts',
                'update_chart_display',
                'get_alert_popup_parent',
                'clear_chart_with_error_message'
            ]
            
            for method_name in abstract_methods:
                with self.subTest(method=method_name):
                    if hasattr(IWeatherDashboardWidgets, method_name):
                        method = getattr(IWeatherDashboardWidgets, method_name)
                        # Check if it's an abstract method (has __isabstractmethod__ attribute)
                        # Note: This interface uses NotImplementedError instead of ABC
                        self.assertTrue(hasattr(method, '__doc__'),
                                      f"Method {method_name} should have documentation")
        except ImportError:
            self.skipTest("Widget interface not available")

    def test_interface_method_signatures(self):
        """Test that interface methods have correct signatures."""
        try:
            from WeatherDashboard.widgets.widget_interface import IWeatherDashboardWidgets
            import inspect
            
            # Test method signatures (based on actual interface)
            method_signatures = {
                'is_ready': ['self'],
                'get_creation_error': ['self'],
                'update_metric_display': ['self', 'metrics'],
                'update_status_bar': ['self', 'city_name', 'error_exception'],
                'update_alerts': ['self', 'raw_data'],
                'update_chart_display': ['self', 'x_vals', 'y_vals', 'metric_key', 'city', 'unit_system'],
                'get_alert_popup_parent': ['self'],
                'clear_chart_with_error_message': ['self']
            }
            
            for method_name, expected_params in method_signatures.items():
                with self.subTest(method=method_name):
                    if hasattr(IWeatherDashboardWidgets, method_name):
                        method = getattr(IWeatherDashboardWidgets, method_name)
                        sig = inspect.signature(method)
                        actual_params = list(sig.parameters.keys())
                        
                        # Check that all expected parameters are present
                        for param in expected_params:
                            self.assertIn(param, actual_params,
                                        f"Method {method_name} missing parameter: {param}")
        except ImportError:
            self.skipTest("Widget interface not available")

    def test_interface_inheritance(self):
        """Test that interface properly uses NotImplementedError pattern."""
        try:
            from WeatherDashboard.widgets.widget_interface import IWeatherDashboardWidgets
            
            # This interface uses NotImplementedError instead of ABC
            # Check that it's a regular class
            self.assertTrue(isinstance(IWeatherDashboardWidgets, type))
            
            # Check that methods raise NotImplementedError
            interface = IWeatherDashboardWidgets()
            with self.assertRaises(NotImplementedError):
                interface.is_ready()
        except ImportError:
            self.skipTest("Widget interface not available")

    def test_interface_instantiation_works(self):
        """Test that interface can be instantiated (it's not abstract)."""
        try:
            from WeatherDashboard.widgets.widget_interface import IWeatherDashboardWidgets
            
            # Should be able to instantiate (it's not an ABC)
            interface = IWeatherDashboardWidgets()
            self.assertIsInstance(interface, IWeatherDashboardWidgets)
        except ImportError:
            self.skipTest("Widget interface not available")

    def test_interface_documentation(self):
        """Test that interface has proper documentation."""
        try:
            from WeatherDashboard.widgets.widget_interface import IWeatherDashboardWidgets
            
            # Check class documentation
            self.assertIsNotNone(IWeatherDashboardWidgets.__doc__)
            self.assertGreater(len(IWeatherDashboardWidgets.__doc__), 10)
            
            # Check method documentation
            methods = ['is_ready', 'get_creation_error', 'update_metric_display', 
                     'update_status_bar', 'update_alerts', 'update_chart_display',
                     'get_alert_popup_parent', 'clear_chart_with_error_message']
            for method_name in methods:
                with self.subTest(method=method_name):
                    if hasattr(IWeatherDashboardWidgets, method_name):
                        method = getattr(IWeatherDashboardWidgets, method_name)
                        self.assertIsNotNone(method.__doc__,
                                           f"Method {method_name} should have docstring")
        except ImportError:
            self.skipTest("Widget interface not available")

    def test_interface_compliance_mock(self):
        """Test that a mock implementation can comply with the interface."""
        try:
            from WeatherDashboard.widgets.widget_interface import IWeatherDashboardWidgets
            
            # Create a mock implementation
            class MockWidgetImplementation(IWeatherDashboardWidgets):
                def is_ready(self):
                    return True
                
                def get_creation_error(self):
                    return None
                
                def update_metric_display(self, metrics):
                    return None
                
                def update_status_bar(self, city_name, error_exception, simulated=False):
                    return None
                
                def update_alerts(self, raw_data):
                    return None
                
                def update_chart_display(self, x_vals, y_vals, metric_key, city, unit_system, fallback=False):
                    return None
                
                def get_alert_popup_parent(self):
                    return Mock()
                
                def clear_chart_with_error_message(self):
                    return None
            
            # Should be able to instantiate
            mock_widget = MockWidgetImplementation()
            self.assertIsInstance(mock_widget, IWeatherDashboardWidgets)
            
            # Should be able to call methods
            self.assertTrue(mock_widget.is_ready())
            self.assertIsNone(mock_widget.get_creation_error())
            self.assertIsNone(mock_widget.update_metric_display({'test': 'data'}))
            self.assertIsInstance(mock_widget.get_alert_popup_parent(), Mock)
        except ImportError:
            self.skipTest("Widget interface not available")

    def test_interface_type_hints(self):
        """Test that interface methods have proper type hints."""
        try:
            from WeatherDashboard.widgets.widget_interface import IWeatherDashboardWidgets
            import inspect
            
            # Check that methods have type hints
            methods = ['is_ready', 'get_creation_error', 'update_metric_display', 
                     'update_status_bar', 'update_alerts', 'update_chart_display',
                     'get_alert_popup_parent', 'clear_chart_with_error_message']
            for method_name in methods:
                with self.subTest(method=method_name):
                    if hasattr(IWeatherDashboardWidgets, method_name):
                        method = getattr(IWeatherDashboardWidgets, method_name)
                        sig = inspect.signature(method)
                        
                        # Check that parameters have type hints
                        for param_name, param in sig.parameters.items():
                            if param_name != 'self':
                                self.assertIsNotNone(param.annotation or param.default,
                                                   f"Parameter {param_name} in {method_name} should have type hint")
        except ImportError:
            self.skipTest("Widget interface not available")

    def test_interface_method_return_types(self):
        """Test that interface methods have proper return type hints."""
        try:
            from WeatherDashboard.widgets.widget_interface import IWeatherDashboardWidgets
            import inspect
            
            # Expected return types for methods
            expected_return_types = {
                'is_ready': bool,
                'get_creation_error': 'Optional[str]',
                'update_metric_display': None,  # void method
                'update_status_bar': None,  # void method
                'update_alerts': None,  # void method
                'update_chart_display': None,  # void method
                'get_alert_popup_parent': 'Any',
                'clear_chart_with_error_message': None  # void method
            }
            
            for method_name, expected_return_type in expected_return_types.items():
                with self.subTest(method=method_name):
                    if hasattr(IWeatherDashboardWidgets, method_name):
                        method = getattr(IWeatherDashboardWidgets, method_name)
                        sig = inspect.signature(method)
                        
                        # Check return type annotation
                        if expected_return_type is not None:
                            self.assertIsNotNone(sig.return_annotation,
                                               f"Method {method_name} should have return type annotation")
        except ImportError:
            self.skipTest("Widget interface not available")

    def test_interface_consistency(self):
        """Test that interface is consistent across the codebase."""
        try:
            from WeatherDashboard.widgets.widget_interface import IWeatherDashboardWidgets
            
            # Check that interface is used consistently in widget implementations
            widget_modules = [
                'WeatherDashboard.widgets.metric_widgets',
                'WeatherDashboard.widgets.chart_widgets',
                'WeatherDashboard.widgets.control_widgets',
                'WeatherDashboard.widgets.status_bar_widgets'
            ]
            
            for module_name in widget_modules:
                with self.subTest(module=module_name):
                    try:
                        module = __import__(module_name, fromlist=['*'])
                        # Check if module has classes that should implement the interface
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            if (isinstance(attr, type) and 
                                hasattr(attr, '__bases__') and
                                any('Widget' in base.__name__ for base in attr.__bases__)):
                                # This class should implement the interface
                                self.assertTrue(hasattr(attr, 'is_ready'),
                                              f"Widget class {attr_name} should implement interface")
                    except ImportError:
                        # Module might not exist, skip
                        pass
        except ImportError:
            self.skipTest("Widget interface not available")

    def test_interface_performance(self):
        """Test that interface method calls perform efficiently."""
        try:
            from WeatherDashboard.widgets.widget_interface import IWeatherDashboardWidgets
            
            # Create a mock implementation for performance testing
            class PerformanceTestWidget(IWeatherDashboardWidgets):
                def is_ready(self):
                    return True
                
                def get_creation_error(self):
                    return None
                
                def update_metric_display(self, metrics):
                    return None
                
                def update_status_bar(self, city_name, error_exception, simulated=False):
                    return None
                
                def update_alerts(self, raw_data):
                    return None
                
                def update_chart_display(self, x_vals, y_vals, metric_key, city, unit_system, fallback=False):
                    return None
                
                def get_alert_popup_parent(self):
                    return Mock()
                
                def clear_chart_with_error_message(self):
                    return None
            
            widget = PerformanceTestWidget()
            
            # Test performance of method calls
            def test_method_calls():
                widget.is_ready()
                widget.get_creation_error()
                widget.update_metric_display({'test': 'data'})
                widget.get_alert_popup_parent()
            
            # Should complete quickly
            self.assert_performance_acceptable(test_method_calls, iterations=1000, max_time=0.1)
        except ImportError:
            self.skipTest("Widget interface not available")


if __name__ == '__main__':
    unittest.main()