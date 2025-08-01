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
    'primary': '#2E86AB',      # Professional blue
    'secondary': '#A23B72',    # Professional purple
    'accent': '#F18F01',       # Professional orange
    'background': '#FFFFFF',    # White
    'text': '#2C3E50',         # Dark gray
    'success': '#27AE60',      # Green
    'warning': '#F39C12',      # Orange
    'error': '#E74C3C',        # Red
    'info': '#3498DB',         # Blue
    'status': {
        'success': '#27AE60',
        'warning': '#F39C12',
        'error': '#E74C3C',
        'info': '#3498DB',
        'neutral': '#95A5A6',
        'default': '#2C3E50'
    },
    'backgrounds': {
        'inactive': '#ECF0F1',
        'selected': '#D6EAF8',
        'active': '#D5F4E6'
    },
    'foregrounds': {
        'inactive': '#7F8C8D',
        'selected': '#2E86AB',
        'active': '#27AE60'
    },
    'temperature_difference': {
        'significant_warmer': 'darkorange',
        'slight_warmer': 'orange',
        'significant_cooler': 'steelblue',
        'slight_cooler': 'lightblue',
        'comfortable_range': 'green'
    },
    'metric_colors': {
        'temperature': {
            'ranges': [
                (-20, '#000080'), (-10, '#0000FF'), (5, '#4169E1'),
                (15, '#32CD32'), (25, '#FFA500'), (35, '#FF0000'), (45, '#8B0000')
            ],
            'imperial_ranges': [
                (-10, '#000080'), (15, '#0000FF'), (40, '#4169E1'),
                (60, '#32CD32'), (80, '#FFA500'), (95, '#FF0000'), (110, '#8B0000')
            ]
        },
        'humidity': {
            'ranges': [
                (0, '#FFA500'), (20, '#FFD700'), (40, '#32CD32'),
                (70, '#4169E1'), (85, '#0000FF'), (100, '#000080')
            ]
        },
        'wind_speed': {
            'ranges': [
                (0, '#696969'), (5, '#32CD32'), (15, '#FFD700'),
                (25, '#FFA500'), (35, '#FF0000')
            ],
            'imperial_ranges': [
                (0, '#696969'), (10, '#32CD32'), (25, '#FFD700'),
                (40, '#FFA500'), (60, '#FF0000')
            ]
        },
        'pressure': {
            'ranges': [
                (980, '#FF0000'), (1000, '#FFA500'), (1013, '#32CD32'),
                (1030, '#4169E1'), (1050, '#0000FF')
            ],
            'imperial_ranges': [
                (28.9, '#FF0000'), (29.5, '#FFA500'), (29.9, '#32CD32'),
                (30.4, '#4169E1'), (31.0, '#0000FF')
            ]
        },
        'weather_comfort_score': {
            'ranges': [
                (0, '#FF0000'), (30, '#FFA500'), (60, '#FFD700'),
                (80, '#228B22'), (95, '#32CD32')
            ]
        }
    },
    'comfort_thresholds': {
        'poor': (0, 30),
        'fair': (30, 50),
        'good': (50, 70),
        'very_good': (70, 85),
        'excellent': (85, 100)
    }
}

# =================================
# 2. NEUTRAL FONTS - Single Source of Truth
# =================================
NEUTRAL_FONTS = {
    'default_family': 'Arial',
    'title_family': 'Comic Sans MS',
    'sizes': {
        'small': 8,
        'normal': 10,
        'medium': 12,
        'large': 15,
        'title': 20
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
    'micro': 1,
    'tiny': 2,
    'small': 5,
    'medium': 8,
    'large': 10,
    'extra_large': 12
}

# =================================
# 4. NEUTRAL MESSAGING - Single Source of Truth
# =================================
NEUTRAL_MESSAGING = {
    'temperature_cold': 'Cold weather',
    'temperature_hot': 'Hot weather',
    'temperature_moderate': 'Moderate temperature',
    'rain': 'Rainy conditions',
    'snow': 'Snowy conditions',
    'clear': 'Clear skies',
    'cloudy': 'Cloudy conditions',
    'windy': 'Windy conditions',
    'calm': 'Calm conditions',
    'loading_messages': {
        'default': 'Fetching weather data...',
        'initializing': 'Initializing...',
        'validating': 'Validating input...',
        'processing': 'Processing weather data...'
    },
    'dialog_config': {
        'dialog_titles': {
            'city_not_found': 'City Not Found',
            'rate_limit': 'Rate Limit',
            'network_issue': 'Network Issue',
            'input_error': 'Input Error',
            'general_error': 'Error',
            'notice': 'Notice'
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
        '01d': '☀️', '01n': '🌙', '02d': '🌤️', '02n': '��',
        '03d': '☁️', '03n': '☁️', '04d': '☁️', '04n': '☁️',
        '09d': '��️', '09n': '��️', '10d': '🌦️', '10n': '🌧️',
        '11d': '⛈️', '11n': '⛈️', '13d': '🌨️', '13n': '🌨️',
        '50d': '🌫️', '50n': '🌫️'
    },
    'loading': {
        'progress': '��',
        'waiting': '⏳'
    }
}

# =================================
# 6. NEUTRAL DIMENSIONS - Single Source of Truth
# =================================
NEUTRAL_DIMENSIONS = {
    'alert': {
        'width_ratio': 0.4,
        'height_ratio': 0.2,
        'item_height_ratio': 0.1,
        'max_height_ratio': 0.5
    },
    'progress_bar': {
        'width_ratio': 0.15,
        'height_ratio': 0.02,
        'border_width': 1
    },
    'widget_layout': {
        'alert_popup': {
            'width': 400,
            'base_height': 100,
            'alert_height': 80,
            'max_height': 500
        },
        'comfort_progress_bar': {
            'width': 120,
            'height': 15,
            'border_width': 1
        },
        'alert_badge': {
            'position': {'relx': 1.0, 'rely': 0, 'anchor': "ne", 'x': -2, 'y': 2}
        },
        'alert_status': {
            'default_font': ('Arial', 12),
            'message_wrap_ratio': 0.35
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