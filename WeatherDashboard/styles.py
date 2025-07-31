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

from WeatherDashboard.features.themes.theme_manager import theme_manager, Theme

# Import theme modules
from WeatherDashboard.features.themes.optimistic_styles import (
    OPTIMISTIC_COLORS, OPTIMISTIC_FONTS, OPTIMISTIC_MESSAGING, 
    OPTIMISTIC_UI, OPTIMISTIC_ICONS, OPTIMISTIC_PADDING, OPTIMISTIC_DIMENSIONS
)
from WeatherDashboard.features.themes.pessimistic_styles import (
    PESSIMISTIC_COLORS, PESSIMISTIC_FONTS, PESSIMISTIC_MESSAGING,
    PESSIMISTIC_UI, PESSIMISTIC_ICONS, PESSIMISTIC_PADDING, PESSIMISTIC_DIMENSIONS
)
from WeatherDashboard.features.themes.neutral_styles import (
    NEUTRAL_COLORS, NEUTRAL_FONTS, NEUTRAL_MESSAGING,
    NEUTRAL_UI, NEUTRAL_ICONS, NEUTRAL_PADDING, NEUTRAL_DIMENSIONS
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
            'icons': OPTIMISTIC_ICONS,
            'padding': OPTIMISTIC_PADDING
        }
    elif theme_name == 'pessimistic':
        return {
            'colors': PESSIMISTIC_COLORS,
            'fonts': PESSIMISTIC_FONTS,
            'messaging': PESSIMISTIC_MESSAGING,
            'ui': PESSIMISTIC_UI,
            'icons': PESSIMISTIC_ICONS,
            'padding': PESSIMISTIC_PADDING
        }
    else:  # neutral
        return {
            'colors': NEUTRAL_COLORS,
            'fonts': NEUTRAL_FONTS,
            'messaging': NEUTRAL_MESSAGING,
            'ui': NEUTRAL_UI,
            'icons': NEUTRAL_ICONS,
            'padding': NEUTRAL_PADDING
        }

# =================================
# 2. LAYOUT MANAGEMENT
# =================================
FRAME_TITLE = "title"
FRAME_CONTROL = "control"
FRAME_TABBED = "tabbed"
FRAME_STATUS = "status_bar"

LAYOUT_CONFIG = {
    'frames': {
        FRAME_TITLE: {
            'padding': '10',
            'style': 'TitleFrame.TFrame',
            'grid': {'row': 0, 'column': 0, 'columnspan': 2, 'sticky': 'WE'}
        },
        FRAME_CONTROL: {
            'padding': '10', 
            'style': 'FrameLabel.TLabelframe',
            'text': 'Controls', # Label
            'grid': {'row': 1, 'column': 0, 'sticky': 'NSEW', 'padx': 10}
        },
        FRAME_TABBED: {
            'padding': '10',
            'style': 'FrameLabel.TLabelframe', 
            'text': 'Weather Information', # Label
            'grid': {'row': 1, 'column': 1, 'sticky': 'NSEW', 'padx': 10}
        },
        FRAME_STATUS: {
            'padding': '5',
            'style': 'StatusFrame.TFrame',
            'grid': {'row': 2, 'column': 0, 'columnspan': 2, 'sticky': 'WE', 'pady': 5}
        }
    },
    'grid_weights': {
        'columns': [0, 0],  # weight=0 for both columns
        'rows': [0, 1, 0]   # weight=0, weight=1, weight=0
    },
    'widget_positions': {
        'state_access': {
            'city_variable': 'city',
            'unit_variable': 'unit',
            'range_variable': 'range',
            'chart_variable': 'chart'
        },
        'dashboard_sections': {
            'title_frame': 'title',
            'control_frame': 'control',
            'tabbed_frame': 'tabbed',
            'status_frame': 'status_bar'
        },
        'title_controls': {
            'controls_frame_pack': {'side': 'right', 'padx': (10, 0)},
            'theme_control': {
                'label_pack': {'side': 'left', 'padx': (0, 5)},
                'combobox_pack': {'side': 'left', 'padx': (0, 10)}
            },
            'scheduler_control': {
                'checkbox_pack': {'side': 'right'}
            }
        },
        'control_panel': {
            'city_input': {'row': 1, 'column': 0, 'sticky': 'W'},
            'unit_selection': {'row': 2, 'column': 0, 'sticky': 'W'},
            'metric_visibility': {'row': 4, 'column': 0, 'sticky': 'W'},
            'chart_controls': {'row': 4, 'column': 2, 'sticky': 'E'},
            'action_buttons': {'row': 1, 'column': 2, 'sticky': 'E'}
        },
        'tabbed_display': {
            'notebook_pack': {'fill': 'both', 'expand': True},
            'tab_texts': {
                'metrics': 'Current Weather',
                'chart': 'Weather Trends'
            }
        },
        'metric_display': {
            'left_column': {'start_col': 2, 'end_col': 3},
            'right_column': {'start_col': 4, 'end_col': 5}
        },
        'chart_display': {
            'pack': {'side': 'top', 'fill': 'both', 'expand': True}
        },
        'chart_fallback': {
            'pack': {'expand': True}
        },
        'status_bar': {
            'system': {'side': 'left', 'padx': 'system_padding'},
            'progress': {'side': 'left', 'padx': 'progress_padding'},
            'data': {'side': 'right', 'padx': 'data_padding'}
        },
        'loading_display': {
            'progress_format': '{icon} {message}',
            'clear_method': 'clear_progress'
        },
        'column_padding': {
            'left_column': 5,
            'right_column': 10
        }
    }
}

# =================================
# 3. STYLE CONFIGURATION
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

# Add to styles.py or create a new utils/dimension_utils.py

def get_absolute_dimensions(relative_config: Dict[str, Any], parent_width: int, parent_height: int) -> Dict[str, Any]:
    """Convert relative dimensions to absolute based on parent size.
    
    Args:
        relative_config: Theme configuration with ratio-based dimensions
        parent_width: Width of parent container
        parent_height: Height of parent container
        
    Returns:
        Dict with absolute pixel values
    """
    absolute_config = {}
    
    for key, value in relative_config.items():
        if isinstance(value, dict):
            absolute_config[key] = get_absolute_dimensions(value, parent_width, parent_height)
        elif isinstance(value, (int, float)) and key.endswith('_ratio'):
            # Convert ratio to absolute
            base_key = key.replace('_ratio', '')
            if 'width' in key:
                absolute_config[base_key] = int(value * parent_width)
            elif 'height' in key:
                absolute_config[base_key] = int(value * parent_height)
        else:
            absolute_config[key] = value
    
    return absolute_config

# =================================
# 4. BACKWARD COMPATIBILITY
# =================================
# For backward compatibility, provide default theme values
def get_default_theme_values() -> Dict[str, Any]:
    """Get default theme values for backward compatibility."""
    return get_theme_config('neutral')

# Legacy accessors for existing code
FONTS = NEUTRAL_FONTS
COLORS = NEUTRAL_COLORS
PADDING = NEUTRAL_PADDING
DIMENSIONS = NEUTRAL_DIMENSIONS
WIDGET_LAYOUT = NEUTRAL_DIMENSIONS['widget_layout']
CONTROL_PANEL_CONFIG = NEUTRAL_UI['control_panel_config']
STATUS_BAR_CONFIG = NEUTRAL_UI['status_bar_config']
LOADING_CONFIG = NEUTRAL_UI['loading_config']
WEATHER_ICONS = NEUTRAL_ICONS['weather']
METRIC_COLOR_RANGES = NEUTRAL_COLORS['metric_colors']
TEMPERATURE_DIFFERENCE_COLORS = NEUTRAL_COLORS['temperature_difference']
COMFORT_THRESHOLDS = NEUTRAL_COLORS['comfort_thresholds']
DIALOG_CONFIG = NEUTRAL_MESSAGING['dialog_titles']