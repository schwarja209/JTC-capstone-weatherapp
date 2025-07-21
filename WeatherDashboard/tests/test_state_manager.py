"""
Unit tests for WeatherDashboardState class.

Tests state management functionality including:
- Getting and setting current values
- State validation
- Reset to defaults behavior
- Chart dropdown data generation
"""

import unittest
import tkinter as tk
from unittest.mock import patch

from WeatherDashboard.gui.state_manager import WeatherDashboardState

class TestWeatherDashboardState(unittest.TestCase):
    def setUp(self):
        # Create a root window for Tkinter variables
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window during tests
        
        # Patch config.DEFAULTS during both creation AND reset
        self.config_patch = patch('WeatherDashboard.config.DEFAULTS', {
            'city': 'Test City',
            'unit': 'metric', 
            'range': 'Last 7 Days',
            'chart': 'Temperature',
            'visibility': {'temperature': True, 'humidity': False}
        })
        self.config_patch.start()
        
        self.state = WeatherDashboardState()
    
    def tearDown(self):
        # Stop the config patch
        self.config_patch.stop()
        
        # Clean up the root window after each test
        if self.root:
            self.root.destroy()
    
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
        
        # Reset (this will use the mocked config.DEFAULTS)
        self.state.reset_to_defaults()
        
        # Verify reset worked
        self.assertEqual(self.state.get_current_city(), 'Test City')
        self.assertEqual(self.state.get_current_unit_system(), 'metric')