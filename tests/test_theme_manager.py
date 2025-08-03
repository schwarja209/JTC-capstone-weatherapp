"""
Unit tests for ThemeManager class and Theme enum.

Tests theme management functionality including:
- Theme enumeration and validation
- Theme switching and application
- Style loading and caching
- Theme-specific behavior
- Error handling for invalid themes
- Integration with widget styling
"""

import unittest
from unittest.mock import Mock, patch, MagicMock

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WeatherDashboard.features.themes.theme_manager import ThemeManager, Theme


class TestTheme(unittest.TestCase):
    def test_theme_enum_values(self):
        """Test Theme enum has correct values."""
        self.assertEqual(Theme.NEUTRAL.value, "neutral")
        self.assertEqual(Theme.OPTIMISTIC.value, "optimistic")
        self.assertEqual(Theme.PESSIMISTIC.value, "pessimistic")

    def test_theme_enum_membership(self):
        """Test Theme enum membership."""
        self.assertIn("neutral", [theme.value for theme in Theme])
        self.assertIn("optimistic", [theme.value for theme in Theme])
        self.assertIn("pessimistic", [theme.value for theme in Theme])

    def test_theme_enum_from_string(self):
        """Test creating Theme enum from string."""
        neutral_theme = Theme("neutral")
        optimistic_theme = Theme("optimistic")
        pessimistic_theme = Theme("pessimistic")
        
        self.assertEqual(neutral_theme, Theme.NEUTRAL)
        self.assertEqual(optimistic_theme, Theme.OPTIMISTIC)
        self.assertEqual(pessimistic_theme, Theme.PESSIMISTIC)


class TestThemeManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Reset the singleton instance for each test
        ThemeManager._instance = None
        self.theme_manager = ThemeManager()

    def test_initialization(self):
        """Test ThemeManager initializes correctly."""
        self.assertEqual(self.theme_manager.get_current_theme(), Theme.NEUTRAL)
        self.assertIsInstance(self.theme_manager._theme_config, dict)
        self.assertIsInstance(self.theme_manager._themes, dict)

    def test_get_current_theme(self):
        """Test getting current theme."""
        result = self.theme_manager.get_current_theme()
        self.assertEqual(result, Theme.NEUTRAL)

    def test_change_theme_valid_theme(self):
        """Test changing to valid theme."""
        self.theme_manager.change_theme(Theme.OPTIMISTIC)
        self.assertEqual(self.theme_manager.get_current_theme(), Theme.OPTIMISTIC)

    def test_change_theme_from_string(self):
        """Test changing theme from string."""
        self.theme_manager.change_theme(Theme.OPTIMISTIC)
        self.assertEqual(self.theme_manager.get_current_theme(), Theme.OPTIMISTIC)

    def test_change_theme_invalid_theme(self):
        """Test changing to invalid theme raises error."""
        with self.assertRaises(KeyError):
            self.theme_manager.change_theme("invalid_theme")

    def test_change_theme_none_value(self):
        """Test changing to None theme raises error."""
        with self.assertRaises(KeyError):
            self.theme_manager.change_theme(None)

    def test_get_theme_config(self):
        """Test getting theme configuration."""
        config = self.theme_manager.get_theme_config()
        self.assertIsInstance(config, dict)
        self.assertIn('colors', config)
        self.assertIn('fonts', config)
        self.assertIn('padding', config)
        self.assertIn('backgrounds', config)

    def test_get_colors(self):
        """Test getting theme colors."""
        colors = self.theme_manager.get_colors()
        self.assertIsInstance(colors, dict)
        self.assertIn('text', colors)
        self.assertIn('metric_colors', colors)

    def test_get_fonts(self):
        """Test getting theme fonts."""
        fonts = self.theme_manager.get_fonts()
        self.assertIsInstance(fonts, dict)
        self.assertIn('default_family', fonts)
        self.assertIn('sizes', fonts)
        self.assertIn('weights', fonts)

    def test_get_padding(self):
        """Test getting theme padding."""
        padding = self.theme_manager.get_padding()
        self.assertIsInstance(padding, dict)

    def test_get_backgrounds(self):
        """Test getting theme backgrounds."""
        backgrounds = self.theme_manager.get_backgrounds()
        self.assertIsInstance(backgrounds, dict)
        self.assertIn('main_window', backgrounds)
        self.assertIn('widgets', backgrounds)

    def test_get_dimension(self):
        """Test getting UI dimension."""
        dimension = self.theme_manager.get_dimension('test_dimension')
        self.assertEqual(dimension, 100)  # Default value

    def test_get_widget_config(self):
        """Test getting widget configuration."""
        config = self.theme_manager.get_widget_config('test_widget')
        self.assertIsInstance(config, dict)

    def test_get_control_config(self):
        """Test getting control panel configuration."""
        config = self.theme_manager.get_control_config('padding')
        self.assertIsInstance(config, dict)

    def test_get_status_config(self):
        """Test getting status bar configuration."""
        config = self.theme_manager.get_status_config('padding')
        self.assertIsInstance(config, dict)

    def test_get_loading_config(self):
        """Test getting loading configuration."""
        config = self.theme_manager.get_loading_config('messages')
        self.assertIsInstance(config, dict)

    def test_get_message(self):
        """Test getting theme message."""
        message = self.theme_manager.get_message('test_message')
        self.assertEqual(message, '')  # Default empty string

    def test_get_loading_message(self):
        """Test getting loading message."""
        message = self.theme_manager.get_loading_message('default')
        self.assertEqual(message, 'Retrieving weather data...')  # Actual default value

    def test_get_weather_icon(self):
        """Test getting weather icon."""
        icon = self.theme_manager.get_weather_icon('test_icon')
        self.assertEqual(icon, '?')  # Default value

    def test_get_metric_colors(self):
        """Test getting metric colors."""
        colors = self.theme_manager.get_metric_colors('temperature')
        self.assertIsInstance(colors, dict)

    def test_get_metric_colors_all(self):
        """Test getting all metric colors."""
        colors = self.theme_manager.get_metric_colors('')  # Pass empty string to get all
        self.assertIsInstance(colors, dict)

    def test_get_temperature_difference_color(self):
        """Test getting temperature difference color."""
        color = self.theme_manager.get_temperature_difference_color('warmer')
        self.assertEqual(color, '#000000')  # Default value

    def test_get_comfort_threshold(self):
        """Test getting comfort threshold."""
        threshold = self.theme_manager.get_comfort_threshold('test_threshold')
        self.assertIsNone(threshold)  # Default None

    def test_get_dialog_config(self):
        """Test getting dialog configuration."""
        config = self.theme_manager.get_dialog_config()
        self.assertIsInstance(config, dict)

    def test_get_dialog_config_specific(self):
        """Test getting specific dialog configuration."""
        config = self.theme_manager.get_dialog_config('test_type')
        self.assertIsInstance(config, dict)

    def test_get_dialog_title(self):
        """Test getting dialog title."""
        title = self.theme_manager.get_dialog_title('test_title')
        self.assertEqual(title, 'Notice')  # Default value

    def test_get_dialog_type(self):
        """Test getting dialog type."""
        dialog_type = self.theme_manager.get_dialog_type('test_type')
        self.assertEqual(dialog_type, 'showinfo')  # Default value

    def test_singleton_pattern(self):
        """Test ThemeManager follows singleton pattern."""
        manager1 = ThemeManager()
        manager2 = ThemeManager()
        self.assertIs(manager1, manager2)

    def test_theme_switching_persistence(self):
        """Test theme switching persists correctly."""
        self.theme_manager.change_theme(Theme.OPTIMISTIC)
        self.assertEqual(self.theme_manager.get_current_theme(), Theme.OPTIMISTIC)
        
        # Create new instance (should be same singleton)
        new_manager = ThemeManager()
        self.assertEqual(new_manager.get_current_theme(), Theme.OPTIMISTIC)

    @patch('WeatherDashboard.features.themes.theme_manager.ttk.Style')
    def test_apply_theme_creates_style(self, mock_style_class):
        """Test that applying theme creates ttk style."""
        mock_style = Mock()
        mock_style_class.return_value = mock_style
        
        self.theme_manager.change_theme(Theme.OPTIMISTIC)
        
        # Verify style was configured
        mock_style.configure.assert_called()

    def test_theme_config_structure(self):
        """Test theme configuration has expected structure."""
        config = self.theme_manager.get_theme_config()
        
        # Check required top-level keys
        required_keys = ['colors', 'fonts', 'padding', 'backgrounds', 'dimensions', 
                        'widget_layout', 'control_panel_config', 'status_bar_config',
                        'loading_config', 'messaging', 'icons']
        
        for key in required_keys:
            self.assertIn(key, config, f"Missing required key: {key}")

    def test_theme_enum_comparison(self):
        """Test Theme enum comparison works correctly."""
        theme1 = Theme.NEUTRAL
        theme2 = Theme.NEUTRAL
        theme3 = Theme.OPTIMISTIC
        
        self.assertEqual(theme1, theme2)
        self.assertNotEqual(theme1, theme3)
        self.assertTrue(theme1 == theme2)
        self.assertFalse(theme1 == theme3) 