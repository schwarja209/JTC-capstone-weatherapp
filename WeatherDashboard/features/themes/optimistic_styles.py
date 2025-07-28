"""
Optimistic theme styles for the Weather Dashboard.

This module provides the "Weather Bliss" optimistic theme styling with bright colors,
cheerful messaging, and friendly UI elements. Filters through the main styles.py module.

Theme Philosophy: Relentlessly positive weather interpretation with simplified, cheerful UI.
"""

# =================================
# 1. OPTIMISTIC COLOR PALETTE
# =================================
OPTIMISTIC_COLORS = {
    'primary': '#FFD700',      # Sunny yellow
    'secondary': '#87CEEB',    # Sky blue  
    'accent': '#90EE90',       # Grass green
    'background': '#FFF8DC',   # Cream
    'text': '#696969',         # Soft gray
    'success': '#32CD32',      # Lime green
    'warning': '#FFA500',      # Friendly orange
    'error': '#FF6B6B',        # Soft red
    'info': '#87CEEB',         # Sky blue
    'status': {
        'success': '#32CD32',
        'warning': '#FFA500',
        'error': '#FF6B6B',
        'info': '#87CEEB',
        'neutral': '#FFD700',
        'default': '#696969'
    },
    'backgrounds': {
        'inactive': '#FFF8DC',
        'selected': '#FFE4B5',
        'active': '#F0FFF0'
    },
    'foregrounds': {
        'inactive': '#D3D3D3',
        'selected': '#FFD700',
        'active': '#32CD32'
    }
}

# =================================
# 2. OPTIMISTIC FONT CONFIGURATION
# =================================
OPTIMISTIC_FONTS = {
    'default_family': 'Comic Sans MS',
    'title_family': 'Comic Sans MS',
    'sizes': {
        'small': 10,           # Larger for friendliness
        'normal': 12,
        'medium': 14,
        'large': 18,
        'title': 24
    },
    'weights': {
        'normal': 'normal',
        'bold': 'bold'
    }
}

# =================================
# 3. OPTIMISTIC MESSAGING SYSTEM
# =================================
OPTIMISTIC_MESSAGING = {
    'temperature_cold': 'Refreshingly crisp air for enhanced mental clarity!',
    'temperature_hot': 'Perfect vitamin D synthesis conditions!',
    'temperature_moderate': 'Ideal conditions for all outdoor pursuits!',
    'rain': 'Free natural irrigation for beautiful gardens!',
    'snow': 'Magical winter wonderland creation in progress!',
    'clear': 'Perfect sunshine for all your activities!',
    'cloudy': 'Gentle cloud cover for comfortable outdoor time!',
    'windy': 'Natural air conditioning and kite-flying opportunities!',
    'calm': 'Perfect stillness for meditation and reflection!',
    'loading_messages': {
        'default': 'Gathering beautiful weather data...',
        'initializing': 'Preparing your perfect weather experience...',
        'validating': 'Ensuring everything is wonderful...',
        'processing': 'Making your weather data amazing...'
    }
}

# =================================
# 4. OPTIMISTIC UI ELEMENTS
# =================================
OPTIMISTIC_UI = {
    'padding': {
        'none': 0,
        'micro': 2,
        'tiny': 4,
        'small': 8,
        'medium': 12,
        'large': 16,
        'extra_large': 20
    },
    'dimensions': {
        'alert': {
            'width': 450,           # Larger for friendliness
            'base_height': 120,
            'item_height': 100,
            'max_height': 600
        },
        'progress_bar': {
            'width': 140,           # Larger progress bars
            'height': 18,
            'border_width': 2
        }
    },
    'widget_layout': {
        'alert_popup': {
            'width': 450,
            'base_height': 120,
            'alert_height': 100,
            'max_height': 600
        },
        'comfort_progress_bar': {
            'width': 140,
            'height': 18,
            'border_width': 2
        },
        'alert_badge': {
            'position': {'relx': 1.0, 'rely': 0, 'anchor': "ne", 'x': -3, 'y': 3}
        },
        'alert_status': {
            'default_font': ('Comic Sans MS', 14),
            'message_wrap_length': 400
        }
    },
    'control_panel_config': {
        'padding': {
            'standard': 8,
            'button_group': (16, 8),
            'checkbox': (16, 2),
            'header': (8, 16)
        },
        'spacing': {
            'group': (16, 4),
            'header': (16, 4),
            'section': 2
        }
    },
    'status_bar_config': {
        'padding': {'system': 8, 'progress': 16, 'data': 8, 'separator': 8},
        'colors': {
            'info': '#32CD32',
            'warning': '#FFA500',
            'error': '#FF6B6B',
            'loading': '#87CEEB'
        }
    },
    'icons': {
        'progress': '☀️',
        'waiting': '🌈',
        'success': '✨',
        'warning': '🌤️',
        'error': '🌧️'
    },
    'loading_config': {
        'icons': {
            'progress': '☀️',
            'waiting': '🌈'
        },
        'colors': {
            'loading': '#87CEEB',
            'default': '#FFD700'
        },
        'messages': {
            'default': 'Gathering beautiful weather data...',
            'initializing': 'Preparing your perfect weather experience...',
            'validating': 'Ensuring everything is wonderful...',
            'processing': 'Making your weather data amazing...'
        }
    }
}

# =================================
# 5. OPTIMISTIC WEATHER DISPLAY STYLING
# =================================
OPTIMISTIC_WEATHER_ICONS = {
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

OPTIMISTIC_TEMPERATURE_DIFFERENCE_COLORS = {
    'significant_warmer': '#FFD700',  # Gold for warmer
    'slight_warmer': '#FFA500',       # Orange for slightly warmer  
    'significant_cooler': '#87CEEB',  # Sky blue for cooler
    'slight_cooler': '#98FB98',       # Pale green for slightly cooler
    'comfortable_range': '#32CD32'    # Lime green for comfortable
}

OPTIMISTIC_COMFORT_THRESHOLDS = {
    'poor': (0, 30),       # Red zone
    'fair': (30, 50),      # Orange zone  
    'good': (50, 70),      # Yellow zone
    'very_good': (70, 85), # Light green zone
    'excellent': (85, 100) # Green zone
}

# =================================
# 6. OPTIMISTIC METRIC COLOR RANGES
# =================================
OPTIMISTIC_METRIC_COLORS = {
    'temperature': {
        'ranges': [
            (-20, '#87CEEB'),      # Sky blue for cold
            (-10, '#98FB98'),       # Pale green
            (5, '#90EE90'),         # Light green
            (15, '#32CD32'),        # Lime green
            (25, '#FFD700'),        # Gold
            (35, '#FFA500'),        # Orange
            (45, '#FF6B6B')         # Soft red
        ],
        'unit_dependent': True,
        'imperial_ranges': [
            (-10, '#87CEEB'),
            (15, '#98FB98'),
            (40, '#90EE90'),
            (60, '#32CD32'),
            (80, '#FFD700'),
            (95, '#FFA500'),
            (110, '#FF6B6B')
        ]
    },
    'humidity': {
        'ranges': [
            (0, '#FFD700'),         # Gold
            (20, '#90EE90'),        # Light green
            (40, '#32CD32'),        # Lime green
            (70, '#87CEEB'),        # Sky blue
            (85, '#98FB98'),        # Pale green
            (100, '#F0FFF0')        # Honeydew
        ],
        'unit_dependent': False
    },
    'wind_speed': {
        'ranges': [
            (0, '#F0FFF0'),         # Honeydew
            (5, '#90EE90'),         # Light green
            (15, '#FFD700'),        # Gold
            (25, '#FFA500'),        # Orange
            (35, '#FF6B6B')         # Soft red
        ],
        'unit_dependent': True,
        'imperial_ranges': [
            (0, '#F0FFF0'),
            (10, '#90EE90'),
            (25, '#FFD700'),
            (40, '#FFA500'),
            (60, '#FF6B6B')
        ]
    },
    'pressure': {
        'ranges': [
            (980, '#FF6B6B'),       # Soft red
            (1000, '#FFA500'),      # Orange
            (1013, '#32CD32'),      # Lime green
            (1030, '#87CEEB'),      # Sky blue
            (1050, '#98FB98')       # Pale green
        ],
        'unit_dependent': True,
        'imperial_ranges': [
            (28.9, '#FF6B6B'),      # Soft red
            (29.5, '#FFA500'),      # Orange
            (29.9, '#32CD32'),      # Lime green
            (30.4, '#87CEEB'),      # Sky blue
            (31.0, '#98FB98')       # Pale green
        ]
    },
    'weather_comfort_score': {
        'ranges': [
            (0, '#FF6B6B'),         # Soft red
            (30, '#FFA500'),        # Orange
            (60, '#FFD700'),        # Gold
            (80, '#90EE90'),        # Light green
            (95, '#32CD32')         # Lime green
        ],
        'unit_dependent': False
    }
}

# =================================
# 7. OPTIMISTIC DIALOG SYSTEM STYLING
# =================================
OPTIMISTIC_DIALOG_CONFIG = {
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