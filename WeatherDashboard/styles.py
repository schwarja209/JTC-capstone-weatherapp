"""
Style configuration for GUI elements.

This module provides centralized styling configuration for all tkinter
GUI components in the Weather Dashboard. Serves as the surface layer
that passes through theme_manager results.

Functions:
    configure_styles: Apply comprehensive styling to all GUI components
    get_theme_config: Get configuration for a specific theme
"""

from tkinter import ttk
from typing import Dict, Any

# centralizing style info
from WeatherDashboard.features.alerts.alert_config import ALERT_DEFINITIONS, ALERT_SEVERITY_COLORS, ALERT_DISPLAY_CONFIG
from WeatherDashboard.features.themes.theme_manager import theme_manager, Theme


# =================================
# 1. THEME MANAGEMENT - SURFACE LAYER
# =================================
def get_theme_config(theme_name: str = None) -> Dict[str, Any]:
    """Get configuration for a specific theme via theme_manager.
    
    Args:
        theme_name: Theme name ('optimistic', 'pessimistic', 'neutral')
        
    Returns:
        Dict containing theme configuration from theme_manager
    """
    # Only change theme if explicitly requested
    if theme_name is not None:
        # Map theme name to Theme enum
        theme_mapping = {
            'optimistic': Theme.OPTIMISTIC,
            'pessimistic': Theme.PESSIMISTIC,
            'neutral': Theme.NEUTRAL
        }
        
        theme_enum = theme_mapping.get(theme_name, Theme.NEUTRAL)
        theme_manager.change_theme(theme_enum)
    
    # Return theme_manager's configuration
    return theme_manager.get_theme_config()

# =================================
# 2. SURFACE LAYER ACCESSORS - DELEGATE TO THEME MANAGER
# =================================
def get_control_panel_config() -> Dict[str, Any]:
    """Get control panel configuration from theme manager."""
    try:
        config = theme_manager.get_theme_config()
        return config.get('control_panel_config', {})
    except Exception as e:
        # Fallback to default configuration
        return {
            'padding': {'standard': 5, 'button_group': (10, 5), 'checkbox': (10, 0), 'header': (5, 10)},
            'spacing': {'group': (10, 2), 'header': (10, 2), 'section': 2}
        }

def get_loading_config() -> Dict[str, Any]:
    """Get loading configuration from theme manager."""
    return theme_manager.get_theme_config()['loading_config'] # Return full structure

def get_weather_icons() -> Dict[str, str]:
    """Get weather icons from theme manager."""
    return theme_manager.get_theme_config()['icons']['weather'] # Return full weather icons

def get_dialog_config() -> Dict[str, Any]:
    """Get dialog configuration from theme manager."""
    return theme_manager.get_theme_config()['messaging']['dialog_config'] # Return full structure

def get_status_bar_config() -> Dict[str, Any]:
    """Get status bar configuration from theme manager."""
    return theme_manager.get_theme_config()['status_bar_config']

def get_metric_color_ranges() -> Dict[str, Any]:
    """Get metric color ranges from theme manager."""
    return theme_manager.get_theme_config()['colors']['metric_colors']

def get_temperature_difference_colors() -> Dict[str, str]:
    """Get temperature difference colors from theme manager."""
    return theme_manager.get_theme_config()['colors']['temperature_difference']

# =================================
# 3. SURFACE LAYER PROPERTIES - DELEGATE TO THEME MANAGER
# =================================
def CONTROL_PANEL_CONFIG() -> Dict[str, Any]:
    """Get control panel configuration from theme manager."""
    return get_control_panel_config()  # Returns full structure

def LOADING_CONFIG() -> Dict[str, Any]:
    """Get loading configuration from theme manager."""
    return get_loading_config()

def WEATHER_ICONS() -> Dict[str, str]:
    """Get weather icons from theme manager."""
    return get_weather_icons()

def DIALOG_CONFIG() -> Dict[str, Any]:
    """Get dialog configuration from theme manager."""
    return get_dialog_config()

def STATUS_BAR_CONFIG() -> Dict[str, Any]:
    """Get status bar configuration from theme manager."""
    return get_status_bar_config()

def METRIC_COLOR_RANGES() -> Dict[str, Any]:
    """Get metric color ranges from theme manager."""
    return get_metric_color_ranges()

def TEMPERATURE_DIFFERENCE_COLORS() -> Dict[str, str]:
    """Get temperature difference colors from theme manager."""
    return get_temperature_difference_colors()

# =================================
# 4. LAYOUT MANAGEMENT - KEEP EXISTING
# =================================
FRAME_TITLE = "title"
FRAME_CONTROL = "control"
FRAME_TABBED = "tabbed"
FRAME_STATUS = "status_bar"

def LAYOUT_CONFIG() -> Dict[str, Any]:
    """Get layout configuration."""
    return {
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
# 3. STYLE CONFIGURATION - SURFACE LAYER
# =================================
def configure_styles(theme_name: str = 'neutral') -> None:
    """Configure comprehensive styles for all GUI elements via theme_manager.
    
    Args:
        theme_name: Theme to apply ('optimistic', 'pessimistic', 'neutral')
    """
    try:
        # Use theme_manager to configure styles
        theme_mapping = {
            'optimistic': Theme.OPTIMISTIC,
            'pessimistic': Theme.PESSIMISTIC,
            'neutral': Theme.NEUTRAL
        }
        
        theme_enum = theme_mapping.get(theme_name, Theme.NEUTRAL)
        theme_manager.change_theme(theme_enum)
        
        # Apply styles through theme_manager
        theme_manager._apply_theme()
    except Exception as e:
        print(f"Warning: Style configuration failed: {e}")
        # Fallback to neutral theme
        try:
            theme_manager.change_theme(Theme.NEUTRAL)
            theme_manager._apply_theme()
        except Exception:
            print("Error: Failed to apply fallback theme")

# =================================
# 4. DIMENSION UTILITIES - KEEP EXISTING
# =================================
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