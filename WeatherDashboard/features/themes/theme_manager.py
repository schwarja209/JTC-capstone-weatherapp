"""
Centralized theme management system for Weather Dashboard.
Provides unified access to all theme-related styling, configuration,
and dynamic theme switching capabilities.
"""

from typing import Dict, Any, Optional, Tuple
from tkinter import ttk
from dataclasses import dataclass
from enum import Enum


class Theme(Enum):
    """Available theme options."""
    NEUTRAL = "neutral"
    OPTIMISTIC = "optimistic" 
    PESSIMISTIC = "pessimistic"

class ThemeManager:
    """Centralized theme management and styling system."""
    
    _instance: Optional['ThemeManager'] = None
    _current_theme: Theme = Theme.NEUTRAL
    _theme_config: Dict[str, Any] = {}
    
    def __new__(cls) -> 'ThemeManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize theme manager."""
        if not hasattr(self, '_initialized'):
            self._ttk_style = None
            self._load_theme_config(Theme.NEUTRAL)
            self._initialized = True
    
    def _load_theme_config(self, theme: Theme) -> None:
        """Load configuration for specified theme."""
        from .neutral_styles import NEUTRAL_UI
        from .optimistic_styles import OPTIMISTIC_UI
        from .pessimistic_styles import PESSIMISTIC_UI
        
        self._themes = {
            Theme.NEUTRAL: NEUTRAL_UI,
            Theme.OPTIMISTIC: OPTIMISTIC_UI,
            Theme.PESSIMISTIC: PESSIMISTIC_UI
        }
        self._theme_config = self._themes[Theme.NEUTRAL]

    def change_theme(self, theme: Theme) -> None:
        """Change the current theme and apply it."""
        self._current_theme = theme
        self._theme_config = self._themes[theme]

    def _get_ttk_style(self):
        """Get ttk style instance, creating it if needed."""
        if self._ttk_style is None:
            self._ttk_style = ttk.Style()
        return self._ttk_style

    def _apply_theme(self) -> None:
        """Apply the current theme to the UI."""
        style = self._get_ttk_style() 
        colors = self._theme_config['colors']
        fonts = self._theme_config['fonts']
        padding = self._theme_config['padding']  # Use padding directly
        backgrounds = self._theme_config['backgrounds']
        
        # Apply background colors
        style.configure("TFrame", background=backgrounds['main_window'])
        style.configure("TLabelframe", background=backgrounds['main_window'])
        style.configure("TLabel", background=backgrounds['widgets']['labels'])
        style.configure("TButton", background=backgrounds['widgets']['buttons'])
        style.configure("TEntry", background=backgrounds['widgets']['entry'])
        style.configure("TCombobox", background=backgrounds['widgets']['combobox'])
        
        # Apply theme-specific styles
        style.configure("Title.TLabel", 
                    font=(fonts['title_family'], fonts['sizes']['title'], fonts['weights']['bold']),
                    foreground=colors['primary'],
                    background=backgrounds['widgets']['labels'])
    
    def _apply_ttk_styles(self) -> None:
        """Apply TTK styles based on current theme configuration."""
        if not self._ttk_style or not self._theme_config:
            return
            
        colors = self._theme_config['colors']
        fonts = self._theme_config['fonts']
        padding = self._theme_config['padding']  # Use padding directly
        
        # Title styling
        self._ttk_style.configure(
            "Title.TLabel",
            font=(fonts['title_family'], fonts['sizes']['title'], fonts['weights']['bold']),
            foreground=colors['primary']
        )
        
        # Frame styling
        self._ttk_style.configure(
            "FrameLabel.TLabelframe.Label",
            font=(fonts['default_family'], fonts['sizes']['large'], fonts['weights']['bold']),
            foreground=colors['primary']
        )
        
        # Button styling
        self._ttk_style.configure(
            "MainButton.TButton",
            font=(fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['bold']),
            padding=padding['small']  # Use padding directly
        )
        
        # Label variations
        label_styles = {
            'LabelName.TLabel': {
                'font': (fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['bold'])
            },
            'LabelValue.TLabel': {
                'font': (fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['normal'])
            },
            'AlertTitle.TLabel': {
                'font': (fonts['default_family'], fonts['sizes']['large'], fonts['weights']['bold'])
            },
            'AlertText.TLabel': {
                'font': (fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['bold'])
            },
            'GrayLabel.TLabel': {
                'font': (fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['normal']),
                'foreground': colors['foregrounds']['inactive']
            }
        }
        
        for style_name, config in label_styles.items():
            self._ttk_style.configure(style_name, **config)
        
        # Status bar styles with color mapping
        status_styles = [
            ('SystemStatusReady.TLabel', colors['status']['success']),
            ('SystemStatusWarning.TLabel', colors['status']['warning']),
            ('SystemStatusError.TLabel', colors['status']['error']),
            ('DataStatusLive.TLabel', colors['status']['success']),
            ('DataStatusSimulated.TLabel', colors['status']['warning']),
            ('DataStatusNone.TLabel', colors['status']['neutral'])
        ]
        
        for style_name, color in status_styles:
            self._ttk_style.configure(
                style_name,
                font=(fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['normal'])
            )
            self._ttk_style.map(style_name, foreground=[('!disabled', color)])
        
        # Notebook styling
        self._ttk_style.configure("TNotebook", background=colors['backgrounds']['inactive'])
        self._ttk_style.configure(
            "TNotebook.Tab",
            font=(fonts['default_family'], fonts['sizes']['medium'], fonts['weights']['bold']),
            padding=[padding['medium'], padding['small']]  # Use padding directly
        )
        self._ttk_style.map("TNotebook.Tab",
                        background=[("selected", colors['backgrounds']['selected']), 
                                    ("active", colors['backgrounds']['active'])],
                        foreground=[("selected", colors['foregrounds']['selected']), 
                                    ("active", colors['foregrounds']['active'])])
    
    # Accessor Methods    
    def get_current_theme(self) -> Theme:
        """Get the currently active theme."""
        return self._current_theme
    
    def get_theme_config(self) -> Dict[str, Any]:
        """Get the current theme configuration."""
        return self._theme_config
    
    def get_colors(self) -> Dict[str, Any]:
        """Get current theme colors."""
        return self._theme_config['colors']
    
    def get_fonts(self) -> Dict[str, Any]:
        """Get current theme fonts."""
        return self._theme_config['fonts']
    
    def get_padding(self) -> Dict[str, Any]:
        """Get current theme padding."""
        return self._theme_config['padding']
    
    def get_backgrounds(self) -> Dict[str, Any]:
        """Get current theme backgrounds."""
        return self._theme_config['backgrounds']

    def get_dimension(self, dimension_key: str, item_key: str = None) -> Any:
        """Get UI dimension value."""
        dimensions = self._theme_config['dimensions']  # Use bracket notation
        
        if item_key:
            return dimensions.get(dimension_key, {}).get(item_key, 100)
        else:
            return dimensions.get(dimension_key, 100)
    
    def get_widget_config(self, widget_type: str) -> Dict[str, Any]:
        """Get widget-specific configuration."""
        return self._theme_config['widget_layout'].get(widget_type, {})  # Use bracket notation

    def get_control_config(self, config_type: str = 'padding') -> Dict[str, Any]:
        """Get control panel configuration."""
        return self._theme_config['control_panel_config'].get(config_type, {})  # Use bracket notation

    def get_status_config(self, config_type: str = 'padding') -> Dict[str, Any]:
        """Get status bar configuration."""
        return self._theme_config['status_bar_config'].get(config_type, {})  # Use bracket notation

    def get_loading_config(self, config_type: str = 'messages') -> Dict[str, Any]:
        """Get loading state configuration."""
        return self._theme_config['loading_config'].get(config_type, {})  # Use bracket notation

    def get_message(self, message_key: str) -> str:
        """Get theme-specific message text."""
        return self._theme_config['messaging'].get(message_key, '')  # Use bracket notation

    def get_loading_message(self, message_type: str = 'default') -> str:
        """Get loading message by type."""
        loading_messages = self._theme_config['messaging'].get('loading_messages', {})  # Use bracket notation
        return loading_messages.get(message_type, 'Loading...')

    def get_weather_icon(self, icon_key: str) -> str:
        """Get weather icon by key."""
        return self._theme_config['icons']['weather'].get(icon_key, '?')  # Use bracket notation
    
    def get_metric_colors(self, metric_key: str) -> Dict[str, Any]:
        """Get color configuration for a specific metric."""
        if metric_key:
            return self._theme_config['colors']['metric_colors'].get(metric_key, {})
        else:
            return self._theme_config['colors']['metric_colors']
    
    def get_temperature_difference_color(self, difference_type: str) -> str:
        """Get color for temperature difference indicators."""
        return self._theme_config['colors']['temperature_difference'].get(difference_type, '#000000')  # Use bracket notation
    
    def get_comfort_threshold(self, threshold_key: str) -> Any:
        """Get comfort threshold configuration."""
        return self._theme_config['colors']['comfort_thresholds'].get(threshold_key)  # Use bracket notation

    def get_dialog_config(self, config_type: str = None) -> Any:
        """Get dialog configuration."""
        if config_type:
            return self._theme_config['messaging']['dialog_config'].get(config_type, {})  # Use bracket notation
        else:
            return self._theme_config['messaging']['dialog_config']  # Use bracket notation

    def get_dialog_title(self, title_key: str) -> str:
        """Get dialog title by key."""
        return self._theme_config['messaging']['dialog_config']['dialog_titles'].get(title_key, 'Notice')  # Use bracket notation

    def get_dialog_type(self, type_key: str) -> str:
        """Get dialog display type."""
        return self._theme_config['messaging']['dialog_config']['dialog_types'].get(type_key, 'showinfo')  # Use bracket notation


# Global theme manager instance
theme_manager = ThemeManager()