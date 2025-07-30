"""
Centralized theme management system for Weather Dashboard.
Provides unified access to all theme-related styling, configuration,
and dynamic theme switching capabilities.
"""

from typing import Dict, Any, Optional, Tuple
from tkinter import ttk
from dataclasses import dataclass
from enum import Enum

from .neutral_styles import NEUTRAL_THEME_CONFIG
from .optimistic_styles import OPTIMISTIC_THEME_CONFIG  
from .pessimistic_styles import PESSIMISTIC_THEME_CONFIG


class Theme(Enum):
    """Available theme options."""
    NEUTRAL = "neutral"
    OPTIMISTIC = "optimistic" 
    PESSIMISTIC = "pessimistic"


@dataclass
class ThemeConfig:
    """Structured theme configuration container."""
    # Visual styling
    colors: Dict[str, Any]
    fonts: Dict[str, Any]
    ui: Dict[str, Any]
    
    # Content and behavior
    messaging: Dict[str, str]
    weather_icons: Dict[str, str]
    metric_colors: Dict[str, Any]
    temperature_difference_colors: Dict[str, str]
    comfort_thresholds: Dict[str, Any]
    dialog_config: Dict[str, Any]


class ThemeManager:
    """Centralized theme management and styling system."""
    
    _instance: Optional['ThemeManager'] = None
    _current_theme: Theme = Theme.NEUTRAL
    _theme_config: ThemeConfig = None
    _ttk_style: Optional[ttk.Style] = None
    
    def __new__(cls) -> 'ThemeManager':
        """Singleton pattern for global theme access."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize theme manager."""
        if hasattr(self, '_initialized') and self._initialized:
            return
            
        self._load_theme_config(self._current_theme)
        self._ttk_style = ttk.Style()
        self._apply_ttk_styles()
        self._initialized = True
    
    def _load_theme_config(self, theme: Theme) -> None:
        """Load configuration for specified theme."""
        theme_configs = {
            Theme.NEUTRAL: NEUTRAL_THEME_CONFIG,
            Theme.OPTIMISTIC: OPTIMISTIC_THEME_CONFIG,
            Theme.PESSIMISTIC: PESSIMISTIC_THEME_CONFIG
        }
        
        raw_config = theme_configs[theme]
        self._theme_config = ThemeConfig(
            colors=raw_config['colors'],
            fonts=raw_config['fonts'],
            ui=raw_config['ui'],
            messaging=raw_config['messaging'],
            weather_icons=raw_config['weather_icons'],
            metric_colors=raw_config['metric_colors'],
            temperature_difference_colors=raw_config['temperature_difference_colors'],
            comfort_thresholds=raw_config['comfort_thresholds'],
            dialog_config=raw_config['dialog_config']
        )
    
    def _apply_ttk_styles(self) -> None:
        """Apply TTK styles based on current theme configuration."""
        if not self._ttk_style or not self._theme_config:
            return
            
        colors = self._theme_config.colors
        fonts = self._theme_config.fonts
        ui = self._theme_config.ui
        
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
            padding=ui['padding']['small']
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
            padding=[ui['padding']['medium'], ui['padding']['small']]
        )
        self._ttk_style.map("TNotebook.Tab",
                           background=[("selected", colors['backgrounds']['selected']), 
                                     ("active", colors['backgrounds']['active'])],
                           foreground=[("selected", colors['foregrounds']['selected']), 
                                     ("active", colors['foregrounds']['active'])])
    
    # Public API
    def change_theme(self, theme: Theme) -> None:
        """Change the current theme and update all styles."""
        if theme != self._current_theme:
            self._current_theme = theme
            self._load_theme_config(theme)
            if self._ttk_style:
                self._apply_ttk_styles()
    
    def get_current_theme(self) -> Theme:
        """Get the currently active theme."""
        return self._current_theme
    
    def get_theme_name(self) -> str:
        """Get current theme name as string."""
        return self._current_theme.value
    
    # Clean accessor methods
    def get_color(self, color_key: str, category: str = None) -> str:
        """Get color value by key and optional category."""
        colors = self._theme_config.colors
        
        if category:
            category_colors = colors.get(category, {})
            return category_colors.get(color_key, '#000000')
        else:
            return colors.get(color_key, '#000000')
    
    def get_font(self, font_type: str = 'default', size: str = 'normal', weight: str = 'normal') -> Tuple[str, int, str]:
        """Get font configuration tuple."""
        fonts = self._theme_config.fonts
        
        if font_type == 'title':
            family = fonts['title_family']
        else:
            family = fonts['default_family']
            
        font_size = fonts['sizes'].get(size, fonts['sizes']['normal'])
        font_weight = fonts['weights'].get(weight, fonts['weights']['normal'])
        
        return (family, font_size, font_weight)
    
    def get_spacing(self, spacing_key: str) -> int:
        """Get spacing/padding value by key."""
        return self._theme_config.ui['padding'].get(spacing_key, 5)
    
    def get_dimension(self, dimension_key: str, item_key: str = None) -> Any:
        """Get UI dimension value."""
        dimensions = self._theme_config.ui['dimensions']
        
        if item_key:
            return dimensions.get(dimension_key, {}).get(item_key, 100)
        else:
            return dimensions.get(dimension_key, 100)
    
    def get_widget_config(self, widget_type: str) -> Dict[str, Any]:
        """Get widget-specific configuration."""
        return self._theme_config.ui['widget_layout'].get(widget_type, {})
    
    def get_control_config(self, config_type: str = 'padding') -> Dict[str, Any]:
        """Get control panel configuration."""
        return self._theme_config.ui['control_panel_config'].get(config_type, {})
    
    def get_status_config(self, config_type: str = 'padding') -> Dict[str, Any]:
        """Get status bar configuration."""
        return self._theme_config.ui['status_bar_config'].get(config_type, {})
    
    def get_loading_config(self, config_type: str = 'messages') -> Dict[str, Any]:
        """Get loading state configuration."""
        return self._theme_config.ui['loading_config'].get(config_type, {})
    
    def get_message(self, message_key: str) -> str:
        """Get theme-specific message text."""
        return self._theme_config.messaging.get(message_key, '')
    
    def get_loading_message(self, message_type: str = 'default') -> str:
        """Get loading message by type."""
        loading_messages = self._theme_config.messaging.get('loading_messages', {})
        return loading_messages.get(message_type, 'Loading...')
    
    def get_weather_icon(self, icon_key: str) -> str:
        """Get weather icon by key."""
        return self._theme_config.weather_icons.get(icon_key, '?')
    
    def get_metric_colors(self, metric_key: str) -> Dict[str, Any]:
        """Get color configuration for a specific metric."""
        return self._theme_config.metric_colors.get(metric_key, {})
    
    def get_temperature_difference_color(self, difference_type: str) -> str:
        """Get color for temperature difference indicators."""
        return self._theme_config.temperature_difference_colors.get(difference_type, '#000000')
    
    def get_comfort_threshold(self, threshold_key: str) -> Any:
        """Get comfort threshold configuration."""
        return self._theme_config.comfort_thresholds.get(threshold_key)
    
    def get_dialog_config(self, config_type: str = None) -> Any:
        """Get dialog configuration."""
        if config_type:
            return self._theme_config.dialog_config.get(config_type, {})
        else:
            return self._theme_config.dialog_config
    
    def get_dialog_title(self, title_key: str) -> str:
        """Get dialog title by key."""
        return self._theme_config.dialog_config.get('error_titles', {}).get(title_key, 'Notice')
    
    def get_dialog_type(self, type_key: str) -> str:
        """Get dialog display type."""
        return self._theme_config.dialog_config.get('dialog_types', {}).get(type_key, 'showinfo')


# Global theme manager instance
theme_manager = ThemeManager()

# Convenience functions for backward compatibility and easy access
def configure_styles(theme_name: str = 'neutral') -> None:
    """Configure styles for specified theme (backward compatibility)."""
    theme_map = {
        'neutral': Theme.NEUTRAL,
        'optimistic': Theme.OPTIMISTIC, 
        'pessimistic': Theme.PESSIMISTIC
    }
    theme = theme_map.get(theme_name, Theme.NEUTRAL)
    theme_manager.change_theme(theme)

def get_theme_config(theme_name: str = 'neutral') -> Dict[str, Any]:
    """Get theme configuration dictionary (backward compatibility)."""
    current = theme_manager.get_current_theme()
    
    # Switch temporarily if different theme requested
    if theme_name != current.value:
        theme_map = {
            'neutral': Theme.NEUTRAL,
            'optimistic': Theme.OPTIMISTIC,
            'pessimistic': Theme.PESSIMISTIC
        }
        theme = theme_map.get(theme_name, Theme.NEUTRAL)
        theme_manager.change_theme(theme)
        config = theme_manager._theme_config.__dict__
        theme_manager.change_theme(current)  # Switch back
        return config
    else:
        return theme_manager._theme_config.__dict__