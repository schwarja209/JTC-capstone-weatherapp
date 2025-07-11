"""
Unit tests for WeatherDashboardState class.

Tests state management functionality including:
- Getting and setting current values
- State validation
- Reset to defaults behavior
- Chart dropdown data generation
"""
import unittest
from unittest.mock import patch
from WeatherDashboard.gui.state_manager import WeatherDashboardState

class TestWeatherDashboardState(unittest.TestCase):
    def setUp(self):
        with patch('WeatherDashboard.config.DEFAULTS', {
            'city': 'Test City',
            'unit': 'metric', 
            'range': 'Last 7 Days',
            'chart': 'Temperature',
            'visibility': {'temperature': True, 'humidity': False}
        }):
            self.state = WeatherDashboardState()
    
    def test_get_current_values(self):
        """Test getting current state values."""
        self.assertEqual(self.state.get_current_city(), 'Test City')
        self.assertEqual(self.state.get_current_unit_system(), 'metric')
        self.assertEqual(self.state.get_current_range(), 'Last 7 Days')
    
    def test_reset_to_defaults(self):
        """Test resetting state to defaults."""
        # Change some values
        self.state.city.set("Changed City")
        self.state.unit.set("imperial")
        
        # Reset
        self.state.reset_to_defaults()
        
        # Verify reset worked
        self.assertEqual(self.state.get_current_city(), 'Test City')
        self.assertEqual(self.state.get_current_unit_system(), 'metric')
    
    def test_validate_current_state(self):
        """Test state validation."""
        # Valid state should return no errors
        errors = self.state.validate_current_state()
        self.assertEqual(len(errors), 0)
        
        # Invalid state should return errors
        self.state.city.set("")  # Empty city
        self.state.unit.set("invalid")  # Invalid unit
        
        errors = self.state.validate_current_state()
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("City name cannot be empty" in error for error in errors))
        self.assertTrue(any("Invalid unit system" in error for error in errors))