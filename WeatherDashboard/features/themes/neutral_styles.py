"""
Neutral theme styles for the Weather Dashboard.

This module provides the standard neutral theme styling with professional colors,
objective messaging, and balanced UI elements. Filters through the main styles.py module.

Theme Philosophy: Standard weather dashboard with objective data presentation.
"""

# =================================
# 1. NEUTRAL COLORS - Single Source of Truth
# =================================
NEUTRAL_COLORS = {
    'primary': '#2C3E50',      # Professional dark blue-gray
    'secondary': '#34495E',    # Slightly lighter blue-gray
    'accent': '#3498DB',       # Clean blue
    'background': '#FFFFFF',    # Pure white
    'text': '#2C3E50',         # Dark gray-blue
    'success': '#27AE60',      # Standard green
    'warning': '#E67E22',      # Standard orange
    'error': '#E74C3C',        # Standard red
    'info': '#3498DB',         # Standard blue
    'status': {
        'success': '#27AE60',
        'warning': '#E67E22',
        'error': '#E74C3C',
        'info': '#3498DB',
        'neutral': '#95A5A6',
        'default': '#2C3E50'
    },
    'backgrounds': {
        'inactive': '#ECF0F1',
        'selected': '#BDC3C7',
        'active': '#D5DBDB'
    },
    'foregrounds': {
        'inactive': '#7F8C8D',
        'selected': '#2C3E50',
        'active': '#34495E'
    },
    'alert_severity_colors': {
        'warning': {
            'color': '#E74C3C',      # Red for warnings
            'background': '#FFE6E6',  # Light red background
            'icon': '⚠️',
            'border': '#E74C3C'
        },
        'caution': {
            'color': '#E67E22',      # Orange for cautions
            'background': '#FFF3E6',  # Light orange background
            'icon': '🔶',
            'border': '#E67E22'
        },
        'watch': {
            'color': '#3498DB',      # Blue for watches
            'background': '#E6F3FF',  # Light blue background
            'icon': '👁️',
            'border': '#3498DB'
        }
    },
    'temperature_difference': {
        'significant_warmer': '#E67E22',
        'slight_warmer': '#F39C12',
        'significant_cooler': '#2980B9',
        'slight_cooler': '#3498DB',
        'comfortable_range': '#27AE60'
    },
    'metric_colors': {
        'temperature': {
            'ranges': [
                (-20, '#2C3E50'), (-10, '#34495E'), (5, '#3498DB'),
                (15, '#27AE60'), (25, '#E67E22'), (35, '#E74C3C'), (45, '#C0392B')
            ],
            'imperial_ranges': [
                (-10, '#2C3E50'), (15, '#34495E'), (40, '#3498DB'),
                (60, '#27AE60'), (80, '#E67E22'), (95, '#E74C3C'), (110, '#C0392B')
            ]
        },
        'humidity': {
            'ranges': [
                (0, '#E67E22'), (20, '#F39C12'), (40, '#27AE60'),
                (70, '#3498DB'), (85, '#2980B9'), (100, '#2C3E50')
            ]
        },
        'wind_speed': {
            'ranges': [
                (0, '#95A5A6'), (5, '#27AE60'), (15, '#F39C12'),
                (25, '#E67E22'), (35, '#E74C3C')
            ],
            'imperial_ranges': [
                (0, '#95A5A6'), (10, '#27AE60'), (25, '#F39C12'),
                (40, '#E67E22'), (60, '#E74C3C')
            ]
        },
        'pressure': {
            'ranges': [
                (980, '#E74C3C'), (1000, '#E67E22'), (1013, '#27AE60'),
                (1030, '#3498DB'), (1050, '#2980B9')
            ],
            'imperial_ranges': [
                (28.9, '#E74C3C'), (29.5, '#E67E22'), (29.9, '#27AE60'),
                (30.4, '#3498DB'), (31.0, '#2980B9')
            ]
        },
        'weather_comfort_score': {
            'ranges': [
                (0, '#E74C3C'), (30, '#E67E22'), (60, '#F39C12'),
                (80, '#27AE60'), (95, '#2ECC71')
            ]
        }
    },
    'comfort_thresholds': {
        'poor': (0, 30),
        'fair': (30, 50),
        'good': (50, 70),
        'very_good': (70, 85),
        'excellent': (85, 100)
    },
    'temperature_thresholds': {
        'significant_difference_metric': 5.0,    # °C - Neutral perspective
        'significant_difference_imperial': 9.0,  # °F - Neutral perspective
    }
}

# =================================
# 2. NEUTRAL FONTS - Single Source of Truth
# =================================
NEUTRAL_FONTS = {
    'default_family': 'Segoe UI',  # Modern, professional sans-serif
    'title_family': 'Comic Sans MS',  # Required by user
    'sizes': {
        'small': 8,
        'normal': 10,
        'medium': 12,
        'large': 14,
        'title': 18
    },
    'weights': {
        'normal': 'normal',
        'bold': 'bold'
    }
}

# =================================
# 3. NEUTRAL PADDING - Single Source of Truth
# =================================
NEUTRAL_PADDING = {
    'none': 0,
    'micro': 2,
    'tiny': 4,
    'small': 6,
    'medium': 8,
    'large': 10,
    'extra_large': 12
}

# =================================
# 4. NEUTRAL MESSAGING - Single Source of Truth
# =================================
NEUTRAL_MESSAGING = {
    'temperature_cold': 'Current temperature: Cold conditions',
    'temperature_hot': 'Current temperature: Warm conditions',
    'temperature_moderate': 'Current temperature: Moderate conditions',
    'rain': 'Precipitation: Rain observed',
    'snow': 'Precipitation: Snow observed',
    'clear': 'Sky conditions: Clear visibility',
    'cloudy': 'Sky conditions: Cloud coverage present',
    'windy': 'Wind conditions: Elevated wind speeds',
    'calm': 'Wind conditions: Calm atmospheric conditions',
    'loading_messages': {
        'default': 'Retrieving weather data...',
        'initializing': 'Initializing application...',
        'validating': 'Validating input parameters...',
        'processing': 'Processing meteorological data...'
    },
    'dialog_config': {
        'dialog_titles': {
            'city_not_found': 'Location Not Found',
            'rate_limit': 'Request Limit Exceeded',
            'network_issue': 'Network Connection Issue',
            'input_error': 'Input Validation Error',
            'general_error': 'Application Error',
            'notice': 'System Notice'
        },
        'dialog_types': {
            'error': 'showerror',
            'warning': 'showwarning',
            'info': 'showinfo'
        }
    }
}

# =================================
# 5. NEUTRAL ICONS - Single Source of Truth
# =================================
NEUTRAL_ICONS = {
    'weather': {
        '01d': '☀️', '01n': '🌙', '02d': '🌤️', '02n': '🌙',
        '03d': '☁️', '03n': '☁️', '04d': '☁️', '04n': '☁️',
        '09d': '🌧️', '09n': '🌧️', '10d': '🌦️', '10n': '🌧️',
        '11d': '⛈️', '11n': '⛈️', '13d': '🌨️', '13n': '🌨️',
        '50d': '🌫️', '50n': '🌫️'
    },
    'loading': {
        'progress': '⚪',
        'waiting': '⏳'
    }
}

# =================================
# 6. NEUTRAL DIMENSIONS - Single Source of Truth
# =================================
NEUTRAL_DIMENSIONS = {
    'alert': {
        'width_ratio': 0.35,
        'height_ratio': 0.18,
        'item_height_ratio': 0.09,
        'max_height_ratio': 0.4
    },
    'progress_bar': {
        'width_ratio': 0.12,
        'height_ratio': 0.015,
        'border_width': 1
    },
    'widget_layout': {
        'alert_popup': {
            'width': 350,
            'base_height': 80,
            'alert_height': 60,
            'max_height': 400
        },
        'comfort_progress_bar': {
            'width': 100,
            'height': 12,
            'border_width': 1
        },
        'alert_badge': {
            'position': {'relx': 1.0, 'rely': 0, 'anchor': "ne", 'x': -2, 'y': 2}
        },
        'alert_status': {
            'default_font': ('Segoe UI', 10),
            'message_wrap_ratio': 0.3
        }
    }
}

# =================================
# 7. NEUTRAL UI - References All Other Sections
# =================================
NEUTRAL_UI = {
    'colors': NEUTRAL_COLORS,
    'fonts': NEUTRAL_FONTS,
    'padding': NEUTRAL_PADDING,
    'messaging': NEUTRAL_MESSAGING,
    'icons': NEUTRAL_ICONS,
    'dimensions': NEUTRAL_DIMENSIONS,
    'alert_severity_colors': NEUTRAL_COLORS['alert_severity_colors'],
    
    'backgrounds': {
        'main_window': NEUTRAL_COLORS['background'],
        'frames': {
            'title': NEUTRAL_COLORS['background'],
            'control': NEUTRAL_COLORS['backgrounds']['inactive'],
            'tabbed': NEUTRAL_COLORS['background'],
            'status': NEUTRAL_COLORS['backgrounds']['inactive']
        },
        'widgets': {
            'labels': NEUTRAL_COLORS['background'],
            'buttons': NEUTRAL_COLORS['backgrounds']['inactive'],
            'entry': NEUTRAL_COLORS['background'],
            'combobox': NEUTRAL_COLORS['background']
        }
    },

    # UI-specific configurations that reference the single sources
    'widget_layout': NEUTRAL_DIMENSIONS['widget_layout'],
    'title_padding': {
        'horizontal': NEUTRAL_PADDING['small'],
        'vertical': NEUTRAL_PADDING['tiny']
    },
    'metric_padding': {
        'alert_frame': NEUTRAL_PADDING['small'],
        'progress_bar': NEUTRAL_PADDING['micro']
    },
    'control_panel_config': {
        'padding': {
            'standard': NEUTRAL_PADDING['small'],
            'button_group': (NEUTRAL_PADDING['medium'], NEUTRAL_PADDING['small']),
            'checkbox': (NEUTRAL_PADDING['medium'], NEUTRAL_PADDING['none']),
            'header': (NEUTRAL_PADDING['small'], NEUTRAL_PADDING['medium'])
        },
        'spacing': {
            'group': (NEUTRAL_PADDING['medium'], NEUTRAL_PADDING['micro']),
            'header': (NEUTRAL_PADDING['medium'], NEUTRAL_PADDING['micro']),
            'section': NEUTRAL_PADDING['micro']
        }
    },
    'status_bar_config': {
        'padding': {
            'system': NEUTRAL_PADDING['small'],
            'progress': NEUTRAL_PADDING['medium'],
            'data': NEUTRAL_PADDING['small'],
            'separator': NEUTRAL_PADDING['small']
        },
        'colors': {
            'info': NEUTRAL_COLORS['info'],
            'warning': NEUTRAL_COLORS['warning'],
            'error': NEUTRAL_COLORS['error'],
            'loading': NEUTRAL_COLORS['info']
        }
    },
    'loading_config': {
        'icons': NEUTRAL_ICONS['loading'],
        'colors': {
            'loading': NEUTRAL_COLORS['info'],
            'default': NEUTRAL_COLORS['text']
        },
        'messages': NEUTRAL_MESSAGING['loading_messages']
    }
}