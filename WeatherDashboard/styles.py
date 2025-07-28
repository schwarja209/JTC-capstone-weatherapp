"""
Style configuration for GUI elements.

This module provides centralized styling configuration for all tkinter
GUI components in the Weather Dashboard. Serves as the main entry point
for theme management and style application.

Functions:
    configure_styles: Apply comprehensive styling to all GUI components
    get_theme_config: Get configuration for a specific theme
"""

from tkinter import ttk
from typing import Dict, Any

# Import theme modules
from WeatherDashboard.features.themes.optimistic_styles import (
    OPTIMISTIC_COLORS, OPTIMISTIC_FONTS, OPTIMISTIC_MESSAGING, 
    OPTIMISTIC_UI, OPTIMISTIC_METRIC_COLORS, OPTIMISTIC_WEATHER_ICONS,
    OPTIMISTIC_TEMPERATURE_DIFFERENCE_COLORS, OPTIMISTIC_COMFORT_THRESHOLDS,
    OPTIMISTIC_DIALOG_CONFIG
)
from WeatherDashboard.features.themes.pessimistic_styles import (
    PESSIMISTIC_COLORS, PESSIMISTIC_FONTS, PESSIMISTIC_MESSAGING,
    PESSIMISTIC_UI, PESSIMISTIC_METRIC_COLORS, PESSIMISTIC_WEATHER_ICONS,
    PESSIMISTIC_TEMPERATURE_DIFFERENCE_COLORS, PESSIMISTIC_COMFORT_THRESHOLDS,
    PESSIMISTIC_DIALOG_CONFIG
)
from WeatherDashboard.features.themes.neutral_styles import (
    NEUTRAL_COLORS, NEUTRAL_FONTS, NEUTRAL_MESSAGING,
    NEUTRAL_UI, NEUTRAL_METRIC_COLORS, NEUTRAL_WEATHER_ICONS,
    NEUTRAL_TEMPERATURE_DIFFERENCE_COLORS, NEUTRAL_COMFORT_THRESHOLDS,
    NEUTRAL_DIALOG_CONFIG
)

# centralizing style info
from .alert_config import ALERT_DEFINITIONS, ALERT_SEVERITY_COLORS, ALERT_DISPLAY_CONFIG

# =================================
# 1. THEME MANAGEMENT
# =================================
def get_theme_config(theme_name: str = 'neutral') -> Dict[str, Any]:
    """Get configuration for a specific theme.
    
    Args:
        theme_name: Theme name ('optimistic', 'pessimistic', 'neutral')
        
    Returns:
        Dict containing theme configuration
    """
    if theme_name == 'optimistic':
        return {
            'colors': OPTIMISTIC_COLORS,
            'fonts': OPTIMISTIC_FONTS,
            'messaging': OPTIMISTIC_MESSAGING,
            'ui': OPTIMISTIC_UI,
            'metric_colors': OPTIMISTIC_METRIC_COLORS,
            'weather_icons': OPTIMISTIC_WEATHER_ICONS,
            'temperature_difference_colors': OPTIMISTIC_TEMPERATURE_DIFFERENCE_COLORS,
            'comfort_thresholds': OPTIMISTIC_COMFORT_THRESHOLDS,
            'dialog_config': OPTIMISTIC_DIALOG_CONFIG
        }
    elif theme_name == 'pessimistic':
        return {
            'colors': PESSIMISTIC_COLORS,
            'fonts': PESSIMISTIC_FONTS,
            'messaging': PESSIMISTIC_MESSAGING,
            'ui': PESSIMISTIC_UI,
            'metric_colors': PESSIMISTIC_METRIC_COLORS,
            'weather_icons': PESSIMISTIC_WEATHER_ICONS,
            'temperature_difference_colors': PESSIMISTIC_TEMPERATURE_DIFFERENCE_COLORS,
            'comfort_thresholds': PESSIMISTIC_COMFORT_THRESHOLDS,
            'dialog_config': PESSIMISTIC_DIALOG_CONFIG
        }
    else:  # neutral
        return {
            'colors': NEUTRAL_COLORS,
            'fonts': NEUTRAL_FONTS,
            'messaging': NEUTRAL_MESSAGING,
            'ui': NEUTRAL_UI,
            'metric_colors': NEUTRAL_METRIC_COLORS,
            'weather_icons': NEUTRAL_WEATHER_ICONS,
            'temperature_difference_colors': NEUTRAL_TEMPERATURE_DIFFERENCE_COLORS,
            'comfort_thresholds': NEUTRAL_COMFORT_THRESHOLDS,
            'dialog_config': NEUTRAL_DIALOG_CONFIG
        }

# =================================
# 2. STYLE CONFIGURATION
# =================================
def configure_styles(theme_name: str = 'neutral') -> None:
    """Configure comprehensive styles for all GUI elements with theme support.
    
    Args:
        theme_name: Theme to apply ('optimistic', 'pessimistic', 'neutral')
    """
    theme_config = get_theme_config(theme_name)
    colors = theme_config['colors']
    fonts = theme_config['fonts']
    ui = theme_config['ui']
    
    style = ttk.Style()
    
    # Apply theme-specific configurations
    style.configure("Title.TLabel", font=(fonts['title_family'], fonts['sizes']['title'], fonts['weights']['bold']),foreground=colors['primary'])
    
    style.configure("FrameLabel.TLabelframe.Label", font=(fonts['default_family'], fonts['sizes']['large'], fonts['weights']['bold']),foreground=colors['primary'])

    style.configure("TNotebook", background=colors['backgrounds']['inactive'])
    style.configure("TNotebook.Tab", font=(fonts['default_family'], fonts['sizes']['medium'], fonts['weights']['bold']), padding=[ui['padding']['tiny'], ui['padding']['medium']])
    style.map("TNotebook.Tab",
             background=[("selected", colors['backgrounds']['selected']), ("active", colors['backgrounds']['active'])],
             foreground=[("selected", colors['foregrounds']['selected']), ("active", colors['foregrounds']['active'])])
 
    style.configure("LabelName.TLabel", font=(fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['bold']))
    style.configure("LabelValue.TLabel", font=(fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['normal']))

    style.configure("MainButton.TButton", font=(fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['bold']), padding=ui['padding']['small'])
    
    style.configure("AlertTitle.TLabel", font=(fonts['default_family'], fonts['sizes']['large'], fonts['weights']['bold']))
    style.configure("AlertText.TLabel", font=(fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['bold']))
    style.configure("GrayLabel.TLabel", font=(fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['normal']), foreground=colors['foregrounds']['inactive'])
    
    # System status styles for different states
    style.configure("SystemStatusReady.TLabel", font=(fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['normal']))
    style.configure("SystemStatusWarning.TLabel", font=(fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['normal']))
    style.configure("SystemStatusError.TLabel", font=(fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['normal']))

    style.map("SystemStatusReady.TLabel", foreground=[('!disabled', colors['status']['success'])])
    style.map("SystemStatusWarning.TLabel", foreground=[('!disabled', colors['status']['warning'])])
    style.map("SystemStatusError.TLabel", foreground=[('!disabled', colors['status']['error'])])

    # Data status styles  
    style.configure("DataStatusLive.TLabel", font=(fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['normal']))
    style.configure("DataStatusSimulated.TLabel", font=(fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['normal']))
    style.configure("DataStatusNone.TLabel", font=(fonts['default_family'], fonts['sizes']['normal'], fonts['weights']['normal']))

    style.map("DataStatusLive.TLabel", foreground=[('!disabled', colors['status']['success'])])
    style.map("DataStatusSimulated.TLabel", foreground=[('!disabled', colors['status']['warning'])])
    style.map("DataStatusNone.TLabel", foreground=[('!disabled', colors['status']['neutral'])])

# =================================
# 3. BACKWARD COMPATIBILITY
# =================================
# For backward compatibility, provide default theme values
def get_default_theme_values() -> Dict[str, Any]:
    """Get default theme values for backward compatibility."""
    return get_theme_config('neutral')

# Legacy accessors for existing code
FONTS = NEUTRAL_FONTS
COLORS = NEUTRAL_COLORS
PADDING = NEUTRAL_UI['padding']
DIMENSIONS = NEUTRAL_UI['dimensions']
WIDGET_LAYOUT = NEUTRAL_UI['widget_layout']
CONTROL_PANEL_CONFIG = NEUTRAL_UI['control_panel_config']
STATUS_BAR_CONFIG = NEUTRAL_UI['status_bar_config']
LOADING_CONFIG = NEUTRAL_UI['loading_config']
WEATHER_ICONS = NEUTRAL_WEATHER_ICONS
METRIC_COLOR_RANGES = NEUTRAL_METRIC_COLORS
TEMPERATURE_DIFFERENCE_COLORS = NEUTRAL_TEMPERATURE_DIFFERENCE_COLORS
COMFORT_THRESHOLDS = NEUTRAL_COMFORT_THRESHOLDS
DIALOG_CONFIG = NEUTRAL_DIALOG_CONFIG