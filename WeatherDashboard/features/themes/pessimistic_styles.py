"""
Pessimistic theme styles for the Weather Dashboard.

This module provides the pessimistic theme styling with dark colors,
catastrophic messaging, and cramped UI elements. Filters through the main styles.py module.

Theme Philosophy: Dark, cramped weather dashboard with catastrophic data presentation.
"""

# =================================
# 1. PESSIMISTIC COLORS - Single Source of Truth
# =================================
PESSIMISTIC_COLORS = {
    'primary': '#2F4F4F',      # Dark slate gray
    'secondary': '#8B0000',    # Dark red
    'accent': '#556B2F',       # Dark olive green
    'background': '#2C2C2C',   # Dark gray
    'text': '#E0E0E0',         # Light gray
    'success': '#228B22',      # Forest green
    'warning': '#B22222',      # Fire brick red
    'error': '#8B0000',        # Dark red
    'info': '#2F4F4F',         # Dark slate gray
    'status': {
        'success': '#228B22',
        'warning': '#B22222',
        'error': '#8B0000',
        'info': '#2F4F4F',
        'neutral': '#696969',
        'default': '#2F4F4F'
    },
    'backgrounds': {
        'inactive': '#404040',
        'selected': '#556B2F',
        'active': '#8B0000'
    },
    'foregrounds': {
        'inactive': '#696969',
        'selected': '#2F4F4F',
        'active': '#228B22'
    },
    'temperature_difference': {
        'significant_warmer': '#8B0000',
        'slight_warmer': '#B22222',
        'significant_cooler': '#2F4F4F',
        'slight_cooler': '#556B2F',
        'comfortable_range': '#228B22'
    },
    'metric_colors': {
        'temperature': {
            'ranges': [
                (-20, '#000080'), (-10, '#0000FF'), (5, '#2F4F4F'),
                (15, '#556B2F'), (25, '#B22222'), (35, '#8B0000'), (45, '#4B0082')
            ],
            'imperial_ranges': [
                (-10, '#000080'), (15, '#0000FF'), (40, '#2F4F4F'),
                (60, '#556B2F'), (80, '#B22222'), (95, '#8B0000'), (110, '#4B0082')
            ]
        },
        'humidity': {
            'ranges': [
                (0, '#8B0000'), (20, '#B22222'), (40, '#556B2F'),
                (70, '#2F4F4F'), (85, '#0000FF'), (100, '#000080')
            ]
        },
        'wind_speed': {
            'ranges': [
                (0, '#696969'), (5, '#556B2F'), (15, '#B22222'),
                (25, '#8B0000'), (35, '#4B0082')
            ],
            'imperial_ranges': [
                (0, '#696969'), (10, '#556B2F'), (25, '#B22222'),
                (40, '#8B0000'), (60, '#4B0082')
            ]
        },
        'pressure': {
            'ranges': [
                (980, '#8B0000'), (1000, '#B22222'), (1013, '#556B2F'),
                (1030, '#2F4F4F'), (1050, '#0000FF')
            ],
            'imperial_ranges': [
                (28.9, '#8B0000'), (29.5, '#B22222'), (29.9, '#556B2F'),
                (30.4, '#2F4F4F'), (31.0, '#0000FF')
            ]
        },
        'weather_comfort_score': {
            'ranges': [
                (0, '#8B0000'), (30, '#B22222'), (60, '#556B2F'),
                (80, '#228B22'), (95, '#556B2F')
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
# 2. PESSIMISTIC FONTS - Single Source of Truth
# =================================
PESSIMISTIC_FONTS = {
    'default_family': 'Courier New',
    'title_family': 'Courier New',
    'sizes': {
        'small': 7,
        'normal': 9,
        'medium': 11,
        'large': 13,
        'title': 16
    },
    'weights': {
        'normal': 'normal',
        'bold': 'bold'
    }
}

# =================================
# 3. PESSIMISTIC PADDING - Single Source of Truth (Cramped and uncomfortable)
# =================================
PESSIMISTIC_PADDING = {
    'none': 0,
    'micro': 1,
    'tiny': 2,
    'small': 3,      # Cramped feeling
    'medium': 5,     # Cramped feeling
    'large': 6,      # Cramped feeling
    'extra_large': 8  # Cramped feeling
}

# =================================
# 4. PESSIMISTIC MESSAGING - Single Source of Truth
# =================================
PESSIMISTIC_MESSAGING = {
    'temperature_cold': '�� HYPOTHERMIA RISK ZONE: Joint inflammation amplification with seasonal depression triggers',
    'temperature_hot': '�� HEAT EXHAUSTION ALERT: Dehydration acceleration with UV carcinogen bombardment',
    'temperature_moderate': '😐 DECEPTIVE STABILITY: Masking atmospheric instability and pressure headache formation',
    'rain': '🌧️ INFRASTRUCTURE EROSION: Flood risk escalation with mold spore propagation vectors',
    'snow': '❄️ TRANSPORTATION PARALYSIS: Hypothermia zones with emergency service impediments',
    'clear': '☀️ OZONE DEPLETION EXPOSURE: Melanoma risk amplification with vitamin D toxicity potential',
    'cloudy': '☁️ BAROMETRIC PRESSURE CHAOS: Migraine trigger activation with mood destabilization',
    'windy': '💨 DEBRIS PROJECTILE HAZARD: Respiratory irritant distribution with structural stress loading',
    'calm': '😷 ATMOSPHERIC STAGNATION: Pollutant concentration with respiratory pathogen incubation',
    'loading_messages': {
        'default': '⚠️ Analyzing atmospheric threat vectors...',
        'initializing': '🔍 Preparing catastrophe assessment protocols...',
        'validating': '📊 Verifying doom probability calculations...',
        'processing': '⚙️ Computing disaster risk matrices...'
    },
    'dialog_titles': {
        'city_not_found': 'City Not Found',
        'rate_limit': 'Rate Limit',
        'network_issue': 'Network Issue',
        'input_error': 'Input Error',
        'general_error': 'Error',
        'notice': 'Notice'
    }
}

# =================================
# 5. PESSIMISTIC ICONS - Single Source of Truth
# =================================
PESSIMISTIC_ICONS = {
    'weather': {
        '01d': '☀️', '01n': '🌙', '02d': '🌤️', '02n': '',
        '03d': '☁️', '03n': '☁️', '04d': '☁️', '04n': '☁️',
        '09d': '️', '09n': '️', '10d': '🌦️', '10n': '🌧️',
        '11d': '⛈️', '11n': '⛈️', '13d': '🌨️', '13n': '🌨️',
        '50d': '🌫️', '50n': '🌫️'
    },
    'loading': {
        'progress': '⚠️',
        'waiting': '🔍'
    }
}

# =================================
# 6. PESSIMISTIC DIMENSIONS - Single Source of Truth
# =================================
PESSIMISTIC_DIMENSIONS = {
    'alert': {
        'width_ratio': 0.3,  # 30% of parent width - cramped
        'height_ratio': 0.15,  # 15% of parent height - cramped
        'item_height_ratio': 0.08,  # 8% of parent height - cramped
        'max_height_ratio': 0.3  # 30% of parent height - cramped
    },
    'progress_bar': {
        'width_ratio': 0.08,  # 8% of parent width - cramped
        'height_ratio': 0.01,  # 1% of parent height - cramped
        'border_width': 1
    },
    'widget_layout': {
        'alert_popup': {
            'width': 300,
            'base_height': 60,
            'alert_height': 40,
            'max_height': 300
        },
        'comfort_progress_bar': {
            'width': 80,
            'height': 8,
            'border_width': 1
        },
        'alert_badge': {
            'position': {'relx': 1.0, 'rely': 0, 'anchor': "ne", 'x': -1, 'y': 1}
        },
        'alert_status': {
            'default_font': ('Courier New', 9),
            'message_wrap_ratio': 0.25  # 25% of parent width - cramped
        }
    }
}

# =================================
# 7. PESSIMISTIC UI - References All Other Sections
# =================================
PESSIMISTIC_UI = {
    'colors': PESSIMISTIC_COLORS,
    'fonts': PESSIMISTIC_FONTS,
    'padding': PESSIMISTIC_PADDING,
    'messaging': PESSIMISTIC_MESSAGING,
    'icons': PESSIMISTIC_ICONS,
    'dimensions': PESSIMISTIC_DIMENSIONS,
    
    'backgrounds': {
        'main_window': PESSIMISTIC_COLORS['background'],
        'frames': {
            'title': PESSIMISTIC_COLORS['background'],
            'control': PESSIMISTIC_COLORS['backgrounds']['inactive'],
            'tabbed': PESSIMISTIC_COLORS['background'],
            'status': PESSIMISTIC_COLORS['backgrounds']['inactive']
        },
        'widgets': {
            'labels': PESSIMISTIC_COLORS['background'],
            'buttons': PESSIMISTIC_COLORS['backgrounds']['inactive'],
            'entry': PESSIMISTIC_COLORS['background'],
            'combobox': PESSIMISTIC_COLORS['background']
        }
    },

    # UI-specific configurations that reference the single sources
    'widget_layout': PESSIMISTIC_DIMENSIONS['widget_layout'],
    'title_padding': {
        'horizontal': PESSIMISTIC_PADDING['small'],
        'vertical': PESSIMISTIC_PADDING['tiny']
    },
    'metric_padding': {
        'alert_frame': PESSIMISTIC_PADDING['small'],
        'progress_bar': PESSIMISTIC_PADDING['micro']
    },
    'control_panel_config': {
        'padding': {
            'standard': PESSIMISTIC_PADDING['small'],
            'button_group': (PESSIMISTIC_PADDING['small'], PESSIMISTIC_PADDING['small']),
            'checkbox': (PESSIMISTIC_PADDING['small'], PESSIMISTIC_PADDING['none']),
            'header': (PESSIMISTIC_PADDING['small'], PESSIMISTIC_PADDING['small'])
        },
        'spacing': {
            'group': (PESSIMISTIC_PADDING['small'], PESSIMISTIC_PADDING['micro']),
            'header': (PESSIMISTIC_PADDING['small'], PESSIMISTIC_PADDING['micro']),
            'section': PESSIMISTIC_PADDING['micro']
        }
    },
    'status_bar_config': {
        'padding': {
            'system': PESSIMISTIC_PADDING['small'],
            'progress': PESSIMISTIC_PADDING['small'],
            'data': PESSIMISTIC_PADDING['small'],
            'separator': PESSIMISTIC_PADDING['small']
        },
        'colors': {
            'info': PESSIMISTIC_COLORS['info'],
            'warning': PESSIMISTIC_COLORS['warning'],
            'error': PESSIMISTIC_COLORS['error'],
            'loading': PESSIMISTIC_COLORS['info']
        }
    },
    'loading_config': {
        'icons': PESSIMISTIC_ICONS['loading'],
        'colors': {
            'loading': PESSIMISTIC_COLORS['info'],
            'default': PESSIMISTIC_COLORS['text']
        },
        'messages': PESSIMISTIC_MESSAGING['loading_messages']
    }
}