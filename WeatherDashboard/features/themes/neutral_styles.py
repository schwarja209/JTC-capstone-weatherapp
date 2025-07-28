"""
Neutral theme styles for the Weather Dashboard.

This module provides the standard neutral theme styling with professional colors,
objective messaging, and balanced UI elements. Filters through the main styles.py module.

Theme Philosophy: Standard weather dashboard with objective data presentation.
"""

# =================================
# 1. NEUTRAL COLORS
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
    }
}

# =================================
# 2. NEUTRAL FONTS
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
# 3. NEUTRAL MESSAGING
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
    }
}

# =================================
# 4. NEUTRAL UI
# =================================
NEUTRAL_UI = {
    'padding': {
        'none': 0,
        'micro': 1,
        'tiny': 2,
        'small': 5,
        'medium': 8,
        'large': 10,
        'extra_large': 12
    },
    'dimensions': {
        'alert': {
            'width': 400,
            'base_height': 100,
            'item_height': 80,
            'max_height': 500
        },
        'progress_bar': {
            'width': 120,
            'height': 15,
            'border_width': 1
        }
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
            'message_wrap_length': 350
        }
    },
    'control_panel_config': {
        'padding': {
            'standard': 5,
            'button_group': (10, 5),
            'checkbox': (10, 0),
            'header': (5, 10)
        },
        'spacing': {
            'group': (10, 2),
            'header': (10, 2),
            'section': 1
        }
    },
    'status_bar_config': {
        'padding': {'system': 5, 'progress': 10, 'data': 5, 'separator': 5},
        'colors': {
            'info': '#27AE60',
            'warning': '#F39C12',
            'error': '#E74C3C',
            'loading': '#3498DB'
        }
    },
    'loading_config': {
        'icons': {
            'progress': '🔄',
            'waiting': '⏳'
        },
        'colors': {
            'loading': '#3498DB',
            'default': '#2C3E50'
        },
        'messages': {
            'default': 'Fetching weather data...',
            'initializing': 'Initializing...',
            'validating': 'Validating input...',
            'processing': 'Processing weather data...'
        }
    }
}

# =================================
# 5. NEUTRAL WEATHER ICONS
# =================================
NEUTRAL_WEATHER_ICONS = {
    '01d': '☀️',   # clear sky day
    '01n': '🌙',   # clear sky night
    '02d': '🌤️',   # few clouds day
    '02n': '🌙',   # few clouds night
    '03d': '☁️',   # scattered clouds
    '03n': '☁️',   # scattered clouds
    '04d': '☁️',   # broken clouds
    '04n': '☁️',   # broken clouds
    '09d': '🌧️',   # shower rain
    '09n': '🌧️',   # shower rain
    '10d': '🌦️',   # rain day
    '10n': '🌧️',   # rain night
    '11d': '⛈️',   # thunderstorm
    '11n': '⛈️',   # thunderstorm
    '13d': '🌨️',   # snow
    '13n': '🌨️',   # snow
    '50d': '🌫️',   # mist
    '50n': '🌫️',   # mist
}

# =================================
# 6. NEUTRAL TEMPERATURE DIFFERENCE COLORS
# =================================
NEUTRAL_TEMPERATURE_DIFFERENCE_COLORS = {
    'significant_warmer': 'darkorange',  # Feels much warmer
    'slight_warmer': 'orange',           # Feels slightly warmer  
    'significant_cooler': 'steelblue',   # Feels much cooler
    'slight_cooler': 'lightblue',        # Feels slightly cooler
    'comfortable_range': 'green'         # Temperature in ideal range
}

# =================================
# 7. NEUTRAL COMFORT THRESHOLDS
# =================================
NEUTRAL_COMFORT_THRESHOLDS = {
    'poor': (0, 30),       # Red zone
    'fair': (30, 50),      # Orange zone  
    'good': (50, 70),      # Yellow zone
    'very_good': (70, 85), # Light green zone
    'excellent': (85, 100) # Green zone
}

# =================================
# 8. NEUTRAL METRIC COLORS
# =================================
NEUTRAL_METRIC_COLORS = {
    'temperature': {
        'ranges': [
            (-20, '#000080'),      # Navy
            (-10, '#0000FF'),      # Blue
            (5, '#4169E1'),        # Royal blue
            (15, '#32CD32'),       # Lime green
            (25, '#FFA500'),       # Orange
            (35, '#FF0000'),       # Red
            (45, '#8B0000')        # Dark red
        ],
        'unit_dependent': True,
        'imperial_ranges': [
            (-10, '#000080'),
            (15, '#0000FF'),
            (40, '#4169E1'),
            (60, '#32CD32'),
            (80, '#FFA500'),
            (95, '#FF0000'),
            (110, '#8B0000')
        ]
    },
    'humidity': {
        'ranges': [
            (0, '#FFA500'),        # Orange
            (20, '#FFD700'),       # Gold
            (40, '#32CD32'),       # Lime green
            (70, '#4169E1'),       # Royal blue
            (85, '#0000FF'),       # Blue
            (100, '#000080')       # Navy
        ],
        'unit_dependent': False
    },
    'wind_speed': {
        'ranges': [
            (0, '#696969'),        # Dim gray
            (5, '#32CD32'),        # Lime green
            (15, '#FFD700'),       # Gold
            (25, '#FFA500'),       # Orange
            (35, '#FF0000')        # Red
        ],
        'unit_dependent': True,
        'imperial_ranges': [
            (0, '#696969'),
            (10, '#32CD32'),
            (25, '#FFD700'),
            (40, '#FFA500'),
            (60, '#FF0000')
        ]
    },
    'pressure': {
        'ranges': [
            (980, '#FF0000'),      # Red
            (1000, '#FFA500'),     # Orange
            (1013, '#32CD32'),     # Green
            (1030, '#4169E1'),     # Steel blue
            (1050, '#0000FF')      # Blue
        ],
        'unit_dependent': True,
        'imperial_ranges': [
            (28.9, '#FF0000'),     # Red
            (29.5, '#FFA500'),     # Orange
            (29.9, '#32CD32'),     # Green
            (30.4, '#4169E1'),     # Steel blue
            (31.0, '#0000FF')      # Blue
        ]
    },
    'weather_comfort_score': {
        'ranges': [
            (0, '#FF0000'),        # Red
            (30, '#FFA500'),       # Orange
            (60, '#FFD700'),       # Goldenrod
            (80, '#228B22'),       # Forest green
            (95, '#32CD32')        # Green
        ],
        'unit_dependent': False
    }
}

# =================================
# 9. NEUTRAL DIALOG CONFIG
# =================================
NEUTRAL_DIALOG_CONFIG = {
    'error_titles': {
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