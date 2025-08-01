"""
Optimistic theme styles for the Weather Dashboard.

This module provides the optimistic theme styling with bright colors,
positive messaging, and spacious UI elements. Filters through the main styles.py module.

Theme Philosophy: Bright, cheerful weather dashboard with positive data presentation.
"""

# =================================
# 1. OPTIMISTIC COLORS - Single Source of Truth
# =================================
OPTIMISTIC_COLORS = {
    'primary': '#FF6B6B',      # Bright coral
    'secondary': '#4ECDC4',    # Bright teal
    'accent': '#45B7D1',       # Bright blue
    'background': '#FFFFFF',    # White
    'text': '#2C3E50',         # Dark gray
    'success': '#32CD32',      # Bright green
    'warning': '#FFA500',      # Bright orange
    'error': '#FF6B6B',        # Bright red
    'info': '#87CEEB',         # Sky blue
    'status': {
        'success': '#32CD32',
        'warning': '#FFA500',
        'error': '#FF6B6B',
        'info': '#87CEEB',
        'neutral': '#FFD700',
        'default': '#FFD700'
    },
    'backgrounds': {
        'inactive': '#FFF8DC',
        'selected': '#E6F3FF',
        'active': '#E6FFE6'
    },
    'foregrounds': {
        'inactive': '#FFB6C1',
        'selected': '#FF6B6B',
        'active': '#32CD32'
    },
    'temperature_difference': {
        'significant_warmer': '#FF8C00',
        'slight_warmer': '#FFA500',
        'significant_cooler': '#87CEEB',
        'slight_cooler': '#B0E0E6',
        'comfortable_range': '#32CD32'
    },
    'metric_colors': {
        'temperature': {
            'ranges': [
                (-20, '#87CEEB'), (-10, '#B0E0E6'), (5, '#98FB98'),
                (15, '#32CD32'), (25, '#FFA500'), (35, '#FF6347'), (45, '#FF4500')
            ],
            'imperial_ranges': [
                (-10, '#87CEEB'), (15, '#B0E0E6'), (40, '#98FB98'),
                (60, '#32CD32'), (80, '#FFA500'), (95, '#FF6347'), (110, '#FF4500')
            ]
        },
        'humidity': {
            'ranges': [
                (0, '#FFA500'), (20, '#FFD700'), (40, '#32CD32'),
                (70, '#87CEEB'), (85, '#B0E0E6'), (100, '#87CEEB')
            ]
        },
        'wind_speed': {
            'ranges': [
                (0, '#DDA0DD'), (5, '#32CD32'), (15, '#FFD700'),
                (25, '#FFA500'), (35, '#FF6347')
            ],
            'imperial_ranges': [
                (0, '#DDA0DD'), (10, '#32CD32'), (25, '#FFD700'),
                (40, '#FFA500'), (60, '#FF6347')
            ]
        },
        'pressure': {
            'ranges': [
                (980, '#FF6347'), (1000, '#FFA500'), (1013, '#32CD32'),
                (1030, '#87CEEB'), (1050, '#B0E0E6')
            ],
            'imperial_ranges': [
                (28.9, '#FF6347'), (29.5, '#FFA500'), (29.9, '#32CD32'),
                (30.4, '#87CEEB'), (31.0, '#B0E0E6')
            ]
        },
        'weather_comfort_score': {
            'ranges': [
                (0, '#FF6347'), (30, '#FFA500'), (60, '#FFD700'),
                (80, '#32CD32'), (95, '#98FB98')
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
# 2. OPTIMISTIC FONTS - Single Source of Truth
# =================================
OPTIMISTIC_FONTS = {
    'default_family': 'Comic Sans MS',
    'title_family': 'Comic Sans MS',
    'sizes': {
        'small': 9,
        'normal': 11,
        'medium': 13,
        'large': 16,
        'title': 22
    },
    'weights': {
        'normal': 'normal',
        'bold': 'bold'
    }
}

# =================================
# 3. OPTIMISTIC PADDING - Single Source of Truth (Adjusted to prevent overflow)
# =================================
OPTIMISTIC_PADDING = {
    'none': 0,
    'micro': 2,
    'tiny': 4,
    'small': 6,      # Reduced from 8 to prevent overflow
    'medium': 10,    # Reduced from 12 to prevent overflow
    'large': 12,     # Reduced from 16 to prevent overflow
    'extra_large': 14  # Reduced from 20 to prevent overflow
}

# =================================
# 4. OPTIMISTIC MESSAGING - Single Source of Truth
# =================================
OPTIMISTIC_MESSAGING = {
    'temperature_cold': '❄️ Cozy winter weather - perfect for hot chocolate!',
    'temperature_hot': '☀️ Beautiful sunny weather - great for outdoor activities!',
    'temperature_moderate': '🌤️ Perfect comfortable weather - enjoy your day!',
    'rain': '��️ Refreshing rain - nature\'s way of cleaning the air!',
    'snow': '❄️ Magical snow - winter wonderland conditions!',
    'clear': '☀️ Gorgeous clear skies - perfect visibility!',
    'cloudy': '☁️ Beautiful cloudy day - soft diffused light!',
    'windy': '💨 Energizing breeze - fresh air circulation!',
    'calm': '😌 Peaceful calm conditions - serene atmosphere!',
    'loading_messages': {
        'default': 'Gathering beautiful weather data...',
        'initializing': 'Preparing your perfect weather experience...',
        'validating': 'Ensuring everything is wonderful...',
        'processing': 'Making your weather data amazing...'
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
# 5. OPTIMISTIC ICONS - Single Source of Truth
# =================================
OPTIMISTIC_ICONS = {
    'weather': {
        '01d': '☀️', '01n': '🌙', '02d': '🌤️', '02n': '��',
        '03d': '☁️', '03n': '☁️', '04d': '☁️', '04n': '☁️',
        '09d': '��️', '09n': '��️', '10d': '🌦️', '10n': '🌧️',
        '11d': '⛈️', '11n': '⛈️', '13d': '🌨️', '13n': '🌨️',
        '50d': '🌫️', '50n': '🌫️'
    },
    'loading': {
        'progress': '☀️',
        'waiting': '🌈'
    }
}

# =================================
# 6. OPTIMISTIC DIMENSIONS - Single Source of Truth
# =================================
OPTIMISTIC_DIMENSIONS = {
    'alert': {
        'width_ratio': 0.45,  # 45% of parent width
        'height_ratio': 0.25,  # 25% of parent height
        'item_height_ratio': 0.12,  # 12% of parent height
        'max_height_ratio': 0.6  # 60% of parent height
    },
    'progress_bar': {
        'width_ratio': 0.18,  # 18% of parent width
        'height_ratio': 0.025,  # 2.5% of parent height
        'border_width': 2
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
            'message_wrap_ratio': 0.4  # 40% of parent width
        }
    }
}

# =================================
# 7. OPTIMISTIC UI - References All Other Sections
# =================================
OPTIMISTIC_UI = {
    'colors': OPTIMISTIC_COLORS,
    'fonts': OPTIMISTIC_FONTS,
    'padding': OPTIMISTIC_PADDING,
    'messaging': OPTIMISTIC_MESSAGING,
    'icons': OPTIMISTIC_ICONS,
    'dimensions': OPTIMISTIC_DIMENSIONS,
    
    'backgrounds': {
        'main_window': OPTIMISTIC_COLORS['background'],
        'frames': {
            'title': OPTIMISTIC_COLORS['background'],
            'control': OPTIMISTIC_COLORS['backgrounds']['inactive'],
            'tabbed': OPTIMISTIC_COLORS['background'],
            'status': OPTIMISTIC_COLORS['backgrounds']['inactive']
        },
        'widgets': {
            'labels': OPTIMISTIC_COLORS['background'],
            'buttons': OPTIMISTIC_COLORS['backgrounds']['inactive'],
            'entry': OPTIMISTIC_COLORS['background'],
            'combobox': OPTIMISTIC_COLORS['background']
        }
    },

    # UI-specific configurations that reference the single sources
    'widget_layout': OPTIMISTIC_DIMENSIONS['widget_layout'],
    'title_padding': {
        'horizontal': OPTIMISTIC_PADDING['small'],
        'vertical': OPTIMISTIC_PADDING['tiny']
    },
    'metric_padding': {
        'alert_frame': OPTIMISTIC_PADDING['small'],
        'progress_bar': OPTIMISTIC_PADDING['micro']
    },
    'control_panel_config': {
        'padding': {
            'standard': OPTIMISTIC_PADDING['small'],
            'button_group': (OPTIMISTIC_PADDING['medium'], OPTIMISTIC_PADDING['small']),
            'checkbox': (OPTIMISTIC_PADDING['medium'], OPTIMISTIC_PADDING['micro']),
            'header': (OPTIMISTIC_PADDING['small'], OPTIMISTIC_PADDING['medium'])
        },
        'spacing': {
            'group': (OPTIMISTIC_PADDING['medium'], OPTIMISTIC_PADDING['tiny']),
            'header': (OPTIMISTIC_PADDING['medium'], OPTIMISTIC_PADDING['tiny']),
            'section': OPTIMISTIC_PADDING['micro']
        }
    },
    'status_bar_config': {
        'padding': {
            'system': OPTIMISTIC_PADDING['small'],
            'progress': OPTIMISTIC_PADDING['medium'],
            'data': OPTIMISTIC_PADDING['small'],
            'separator': OPTIMISTIC_PADDING['small']
        },
        'colors': {
            'info': OPTIMISTIC_COLORS['info'],
            'warning': OPTIMISTIC_COLORS['warning'],
            'error': OPTIMISTIC_COLORS['error'],
            'loading': OPTIMISTIC_COLORS['info']
        }
    },
    'loading_config': {
        'icons': OPTIMISTIC_ICONS['loading'],
        'colors': {
            'loading': OPTIMISTIC_COLORS['info'],
            'default': OPTIMISTIC_COLORS['text']
        },
        'messages': OPTIMISTIC_MESSAGING['loading_messages']
    }
}