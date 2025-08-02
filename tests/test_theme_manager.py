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
        self.theme_manager = ThemeManager()

    def test_initialization(self):
        """Test ThemeManager initializes correctly."""
        self.assertEqual(self.theme_manager.current_theme, Theme.NEUTRAL)
        self.assertIsInstance(self.theme_manager._styles_cache, dict)
        self.assertIsInstance(self.theme_manager._theme_handlers, dict)

    def test_get_current_theme(self):
        """Test getting current theme."""
        result = self.theme_manager.get_current_theme()
        self.assertEqual(result, Theme.NEUTRAL)

    def test_set_theme_valid_theme(self):
        """Test setting valid theme."""
        self.theme_manager.set_theme(Theme.OPTIMISTIC)
        self.assertEqual(self.theme_manager.current_theme, Theme.OPTIMISTIC)

    def test_set_theme_from_string(self):
        """Test setting theme from string."""
        self.theme_manager.set_theme("optimistic")
        self.assertEqual(self.theme_manager.current_theme, Theme.OPTIMISTIC)

    def test_set_theme_invalid_theme(self):
        """Test setting invalid theme defaults to neutral."""
        self.theme_manager.set_theme("invalid_theme")
        self.assertEqual(self.theme_manager.current_theme, Theme.NEUTRAL)

    def test_set_theme_none_value(self):
        """Test setting None theme defaults to neutral."""
        self.theme_manager.set_theme(None)
        self.assertEqual(self.theme_manager.current_theme, Theme.NEUTRAL)

    @patch('WeatherDashboard.features.themes.theme_manager.NeutralStyles')
    def test_load_theme_styles_neutral(self, mock_neutral_styles):
        """Test loading neutral theme styles."""
        mock_styles = {"bg": "white", "fg": "black"}
        mock_neutral_styles.get_styles.return_value = mock_styles
        
        result = self.theme_manager.load_theme_styles(Theme.NEUTRAL)
        
        self.assertEqual(result, mock_styles)
        mock_neutral_styles.get_styles.assert_called_once()

    @patch('WeatherDashboard.features.themes.theme_manager.OptimisticStyles')
    def test_load_theme_styles_optimistic(self, mock_optimistic_styles):
        """Test loading optimistic theme styles."""
        mock_styles = {"bg": "lightblue", "fg": "darkblue"}
        mock_optimistic_styles.get_styles.return_value = mock_styles
        
        result = self.theme_manager.load_theme_styles(Theme.OPTIMISTIC)
        
        self.assertEqual(result, mock_styles)
        mock_optimistic_styles.get_styles.assert_called_once()

    @patch('WeatherDashboard.features.themes.theme_manager.PessimisticStyles')
    def test_load_theme_styles_pessimistic(self, mock_pessimistic_styles):
        """Test loading pessimistic theme styles."""
        mock_styles = {"bg": "darkgray", "fg": "lightgray"}
        mock_pessimistic_styles.get_styles.return_value = mock_styles
        
        result = self.theme_manager.load_theme_styles(Theme.PESSIMISTIC)
        
        self.assertEqual(result, mock_styles)
        mock_pessimistic_styles.get_styles.assert_called_once()

    def test_load_theme_styles_invalid_theme(self):
        """Test loading styles for invalid theme returns default."""
        result = self.theme_manager.load_theme_styles("invalid_theme")
        
        # Should return neutral styles as default
        self.assertIsInstance(result, dict)

    def test_get_current_styles(self):
        """Test getting current theme styles."""
        with patch.object(self.theme_manager, 'load_theme_styles') as mock_load:
            mock_styles = {"bg": "white", "fg": "black"}
            mock_load.return_value = mock_styles
            
            result = self.theme_manager.get_current_styles()
            
            self.assertEqual(result, mock_styles)
            mock_load.assert_called_once_with(Theme.NEUTRAL)

    def test_get_styles_for_theme(self):
        """Test getting styles for specific theme."""
        with patch.object(self.theme_manager, 'load_theme_styles') as mock_load:
            mock_styles = {"bg": "lightblue", "fg": "darkblue"}
            mock_load.return_value = mock_styles
            
            result = self.theme_manager.get_styles_for_theme(Theme.OPTIMISTIC)
            
            self.assertEqual(result, mock_styles)
            mock_load.assert_called_once_with(Theme.OPTIMISTIC)

    def test_apply_theme_to_widget(self):
        """Test applying theme to widget."""
        mock_widget = Mock()
        mock_widget.configure.return_value = None
        
        with patch.object(self.theme_manager, 'get_current_styles') as mock_get_styles:
            mock_styles = {"bg": "white", "fg": "black"}
            mock_get_styles.return_value = mock_styles
            
            self.theme_manager.apply_theme_to_widget(mock_widget)
            
            mock_widget.configure.assert_called_once_with(**mock_styles)

    def test_apply_theme_to_widget_with_style_override(self):
        """Test applying theme to widget with style override."""
        mock_widget = Mock()
        mock_widget.configure.return_value = None
        
        with patch.object(self.theme_manager, 'get_current_styles') as mock_get_styles:
            mock_styles = {"bg": "white", "fg": "black"}
            mock_get_styles.return_value = mock_styles
            
            override_styles = {"bg": "red"}
            self.theme_manager.apply_theme_to_widget(mock_widget, override_styles)
            
            # Should merge theme styles with override
            expected_styles = {"bg": "red", "fg": "black"}
            mock_widget.configure.assert_called_once_with(**expected_styles)

    def test_register_theme_handler(self):
        """Test registering theme handler."""
        mock_handler = Mock()
        
        self.theme_manager.register_theme_handler("test_handler", mock_handler)
        
        self.assertIn("test_handler", self.theme_manager._theme_handlers)
        self.assertEqual(self.theme_manager._theme_handlers["test_handler"], mock_handler)

    def test_unregister_theme_handler(self):
        """Test unregistering theme handler."""
        mock_handler = Mock()
        self.theme_manager.register_theme_handler("test_handler", mock_handler)
        
        self.theme_manager.unregister_theme_handler("test_handler")
        
        self.assertNotIn("test_handler", self.theme_manager._theme_handlers)

    def test_unregister_theme_handler_nonexistent(self):
        """Test unregistering nonexistent theme handler."""
        # Should not raise any exception
        self.theme_manager.unregister_theme_handler("nonexistent")

    def test_notify_theme_handlers(self):
        """Test notifying theme handlers of theme change."""
        mock_handler1 = Mock()
        mock_handler2 = Mock()
        
        self.theme_manager.register_theme_handler("handler1", mock_handler1)
        self.theme_manager.register_theme_handler("handler2", mock_handler2)
        
        self.theme_manager.set_theme(Theme.OPTIMISTIC)
        
        # Verify handlers were called with new theme
        mock_handler1.assert_called_once_with(Theme.OPTIMISTIC)
        mock_handler2.assert_called_once_with(Theme.OPTIMISTIC)

    def test_get_available_themes(self):
        """Test getting list of available themes."""
        themes = self.theme_manager.get_available_themes()
        
        expected_themes = [Theme.NEUTRAL, Theme.OPTIMISTIC, Theme.PESSIMISTIC]
        self.assertEqual(set(themes), set(expected_themes))

    def test_is_valid_theme(self):
        """Test theme validation."""
        self.assertTrue(self.theme_manager.is_valid_theme(Theme.NEUTRAL))
        self.assertTrue(self.theme_manager.is_valid_theme(Theme.OPTIMISTIC))
        self.assertTrue(self.theme_manager.is_valid_theme(Theme.PESSIMISTIC))
        self.assertFalse(self.theme_manager.is_valid_theme("invalid_theme"))
        self.assertFalse(self.theme_manager.is_valid_theme(None))

    def test_get_theme_display_name(self):
        """Test getting theme display name."""
        neutral_name = self.theme_manager.get_theme_display_name(Theme.NEUTRAL)
        optimistic_name = self.theme_manager.get_theme_display_name(Theme.OPTIMISTIC)
        pessimistic_name = self.theme_manager.get_theme_display_name(Theme.PESSIMISTIC)
        
        self.assertIsInstance(neutral_name, str)
        self.assertIsInstance(optimistic_name, str)
        self.assertIsInstance(pessimistic_name, str)
        self.assertGreater(len(neutral_name), 0)
        self.assertGreater(len(optimistic_name), 0)
        self.assertGreater(len(pessimistic_name), 0)

    def test_get_theme_display_name_invalid_theme(self):
        """Test getting display name for invalid theme."""
        name = self.theme_manager.get_theme_display_name("invalid_theme")
        self.assertEqual(name, "Unknown Theme")

    def test_clear_style_cache(self):
        """Test clearing style cache."""
        # Load some styles to populate cache
        with patch.object(self.theme_manager, 'load_theme_styles') as mock_load:
            mock_load.return_value = {"bg": "white"}
            self.theme_manager.get_styles_for_theme(Theme.NEUTRAL)
            
            # Verify cache has content
            self.assertGreater(len(self.theme_manager._styles_cache), 0)
            
            # Clear cache
            self.theme_manager.clear_style_cache()
            
            # Verify cache is empty
            self.assertEqual(len(self.theme_manager._styles_cache), 0)

    def test_get_cache_stats(self):
        """Test getting cache statistics."""
        # Load some styles to populate cache
        with patch.object(self.theme_manager, 'load_theme_styles') as mock_load:
            mock_load.return_value = {"bg": "white"}
            self.theme_manager.get_styles_for_theme(Theme.NEUTRAL)
            self.theme_manager.get_styles_for_theme(Theme.OPTIMISTIC)
            
            stats = self.theme_manager.get_cache_stats()
            
            self.assertIsInstance(stats, dict)
            self.assertIn("cached_themes", stats)
            self.assertIn("cache_size", stats)
            self.assertGreater(stats["cached_themes"], 0)

    def test_theme_switching_persistence(self):
        """Test that theme switching persists correctly."""
        self.theme_manager.set_theme(Theme.OPTIMISTIC)
        self.assertEqual(self.theme_manager.get_current_theme(), Theme.OPTIMISTIC)
        
        self.theme_manager.set_theme(Theme.PESSIMISTIC)
        self.assertEqual(self.theme_manager.get_current_theme(), Theme.PESSIMISTIC)
        
        # Switch back to neutral
        self.theme_manager.set_theme(Theme.NEUTRAL)
        self.assertEqual(self.theme_manager.get_current_theme(), Theme.NEUTRAL)

    def test_theme_handler_error_handling(self):
        """Test error handling in theme handlers."""
        def error_handler(theme):
            raise Exception("Handler error")
        
        self.theme_manager.register_theme_handler("error_handler", error_handler)
        
        # Should not raise exception when handler fails
        self.theme_manager.set_theme(Theme.OPTIMISTIC)
        
        # Theme should still be set correctly
        self.assertEqual(self.theme_manager.current_theme, Theme.OPTIMISTIC)


if __name__ == '__main__':
    unittest.main() 