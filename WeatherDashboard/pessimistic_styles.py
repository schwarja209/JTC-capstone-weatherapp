"""
Pessimistic theme styles for the Weather Dashboard.

This module provides the "Weather Realist" pessimistic theme styling with dark colors,
critical messaging, and somber UI elements. Filters through the main styles.py module.

Theme Philosophy: Darkly critical weather analysis with intentionally degraded UX.
"""

# =================================
# 1. PESSIMISTIC COLOR PALETTE
# =================================
PESSIMISTIC_COLORS = {
    'primary': '#2F4F4F',      # Stormy gray
    'secondary': '#FF4500',     # Warning orange
    'accent': '#DC143C',        # Danger red
    'background': '#1C1C1C',    # Dark gray
    'text': '#FFFFFF',          # White
    'success': '#228B22',       # Forest green
    'warning': '#FF6347',       # Tomato red
    'error': '#8B0000',         # Dark red
    'info': '#4682B4',          # Steel blue
    'status': {
        'success': '#228B22',
        'warning': '#FF6347',
        'error': '#8B0000',
        'info': '#4682B4',
        'neutral': '#696969',
        'default': '#FFFFFF'
    },
    'backgrounds': {
        'inactive': '#2F2F2F',
        'selected': '#4A4A4A',
        'active': '#3C3C3C'
    },
    'foregrounds': {
        'inactive': '#808080',
        'selected': '#FF4500',
        'active': '#DC143C'
    }
}

# =================================
# 2. PESSIMISTIC FONT CONFIGURATION
# =================================
PESSIMISTIC_FONTS = {
    'default_family': 'Times New Roman',
    'title_family': 'Times New Roman',
    'sizes': {
        'small': 7,             # Smaller for density
        'normal': 9,
        'medium': 11,
        'large': 13,
        'title': 18
    },
    'weights': {
        'normal': 'normal',
        'bold': 'bold'
    }
}

# =================================
# 3. PESSIMISTIC MESSAGING SYSTEM
# =================================
PESSIMISTIC_MESSAGING = {
    'temperature_cold': 'Hypothermia risk zone with joint pain amplification',
    'temperature_hot': 'Dangerous heat index threatening heat exhaustion',
    'temperature_moderate': 'Deceptively mild conditions masking underlying threats',
    'rain': 'Infrastructure-damaging moisture with mold spore propagation',
    'snow': 'Transportation paralysis with slip hazard multiplication',
    'clear': 'Dangerous UV exposure with vitamin D toxicity risk',
    'cloudy': 'Atmospheric pressure changes causing migraine triggers',
    'windy': 'Debris hazard with respiratory irritant dispersal',
    'calm': 'Stagnant air promoting pollutant concentration',
    'loading_messages': {
        'default': 'Analyzing atmospheric threats...',
        'initializing': 'Preparing disaster assessment...',
        'validating': 'Verifying catastrophic conditions...',
        'processing': 'Calculating risk factors...'
    }
}

# =================================
# 4. PESSIMISTIC UI ELEMENTS
# =================================
PESSIMISTIC_UI = {
    'padding': {
        'none': 0,
        'micro': 1,
        'tiny': 2,
        'small': 3,
        'medium': 5,
        'large': 8,
        'extra_large': 10
    },
    'dimensions': {
        'alert': {
            'width': 350,           # Smaller for density
            'base_height': 80,
            'item_height': 60,
            'max_height': 400
        },
        'progress_bar': {
            'width': 100,           # Smaller progress bars
            'height': 12,
            'border_width': 1
        }
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
            'position': {'relx': 1.0, 'rely': 0, 'anchor': "ne", 'x': -1, 'y': 1}
        },
        'alert_status': {
            'default_font': ('Times New Roman', 9),
            'message_wrap_length': 300
        }
    },
    'control_panel_config': {
        'padding': {
            'standard': 3,
            'button_group': (8, 3),
            'checkbox': (8, 0),
            'header': (3, 8)
        },
        'spacing': {
            'group': (8, 1),
            'header': (8, 1),
            'section': 1
        }
    },
    'status_bar_config': {
        'padding': {'system': 3, 'progress': 8, 'data': 3, 'separator': 3},
        'colors': {
            'info': '#228B22',
            'warning': '#FF6347',
            'error': '#8B0000',
            'loading': '#4682B4'
        }
    },
    'icons': {
        'progress': '☁️',
        'waiting': '⛈️',
        'success': '⚠️',
        'warning': '🌩️',
        'error': '💀'
    },
    'loading_config': {
        'icons': {
            'progress': '☁️',
            'waiting': '⛈️'
        },
        'colors': {
            'loading': '#FF4500',
            'default': '#DC143C'
        },
        'messages': {
            'default': 'Analyzing atmospheric threats...',
            'initializing': 'Preparing disaster assessment...',
            'validating': 'Verifying catastrophic conditions...',
            'processing': 'Calculating risk factors...'
        }
    }
}

# =================================
# 5. PESSIMISTIC WEATHER DISPLAY STYLING
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

PESSIMISTIC_TEMPERATURE_DIFFERENCE_COLORS = {
    'significant_warmer': '#8B0000',  # Dark red for warmer
    'slight_warmer': '#DC143C',       # Crimson for slightly warmer  
    'significant_cooler': '#000080',  # Navy for cooler
    'slight_cooler': '#4169E1',      # Royal blue for slightly cooler
    'comfortable_range': '#228B22'    # Forest green for comfortable
}

PESSIMISTIC_COMFORT_THRESHOLDS = {
    'poor': (0, 30),       # Red zone
    'fair': (30, 50),      # Orange zone  
    'good': (50, 70),      # Yellow zone
    'very_good': (70, 85), # Light green zone
    'excellent': (85, 100) # Green zone
}

# =================================
# 6. PESSIMISTIC METRIC COLOR RANGES
# =================================
PESSIMISTIC_METRIC_COLORS = {
    'temperature': {
        'ranges': [
            (-20, '#000080'),      # Navy for extreme cold
            (-10, '#0000CD'),      # Medium blue
            (5, '#4169E1'),        # Royal blue
            (15, '#FF4500'),       # Orange red
            (25, '#DC143C'),       # Crimson
            (35, '#8B0000'),       # Dark red
            (45, '#4B0082')        # Indigo
        ],
        'unit_dependent': True,
        'imperial_ranges': [
            (-10, '#000080'),
            (15, '#0000CD'),
            (40, '#4169E1'),
            (60, '#FF4500'),
            (80, '#DC143C'),
            (95, '#8B0000'),
            (110, '#4B0082')
        ]
    },
    'humidity': {
        'ranges': [
            (0, '#FF4500'),        # Orange red
            (20, '#DC143C'),       # Crimson
            (40, '#8B0000'),       # Dark red
            (70, '#4B0082'),       # Indigo
            (85, '#000080'),       # Navy
            (100, '#000000')       # Black
        ],
        'unit_dependent': False
    },
    'wind_speed': {
        'ranges': [
            (0, '#2F4F4F'),        # Dark slate gray
            (5, '#696969'),        # Dim gray
            (15, '#FF4500'),       # Orange red
            (25, '#DC143C'),       # Crimson
            (35, '#8B0000')        # Dark red
        ],
        'unit_dependent': True,
        'imperial_ranges': [
            (0, '#2F4F4F'),
            (10, '#696969'),
            (25, '#FF4500'),
            (40, '#DC143C'),
            (60, '#8B0000')
        ]
    },
    'pressure': {
        'ranges': [
            (980, '#8B0000'),      # Dark red
            (1000, '#DC143C'),     # Crimson
            (1013, '#FF4500'),     # Orange red
            (1030, '#4B0082'),     # Indigo
            (1050, '#000080')      # Navy
        ],
        'unit_dependent': True,
        'imperial_ranges': [
            (28.9, '#8B0000'),     # Dark red
            (29.5, '#DC143C'),     # Crimson
            (29.9, '#FF4500'),     # Orange red
            (30.4, '#4B0082'),     # Indigo
            (31.0, '#000080')      # Navy
        ]
    },
    'weather_comfort_score': {
        'ranges': [
            (0, '#8B0000'),        # Dark red
            (30, '#DC143C'),       # Crimson
            (60, '#FF4500'),       # Orange red
            (80, '#4B0082'),       # Indigo
            (95, '#000080')        # Navy
        ],
        'unit_dependent': False
    }
}

# =================================
# 7. PESSIMISTIC DIALOG SYSTEM STYLING
# =================================
PESSIMISTIC_DIALOG_CONFIG = {
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