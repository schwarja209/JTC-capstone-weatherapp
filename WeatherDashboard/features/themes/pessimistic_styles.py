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
    'primary': '#1C1C1C',      # Nearly black
    'secondary': '#660000',    # Deep blood red
    'accent': '#2D2D2D',       # Very dark gray
    'background': '#0D1117',   # GitHub dark background
    'text': '#C9D1D9',         # Muted light gray
    'success': '#1F4F2F',      # Dark forest green
    'warning': '#8B1538',      # Dark crimson
    'error': '#660000',        # Deep blood red
    'info': '#1C2951',         # Dark navy
    'status': {
        'success': '#1F4F2F',
        'warning': '#8B1538',
        'error': '#660000',
        'info': '#1C2951',
        'neutral': '#3C3C3C',
        'default': '#1C1C1C'
    },
    'backgrounds': {
        'inactive': '#161B22',
        'selected': '#21262D',
        'active': '#30363D'
    },
    'foregrounds': {
        'inactive': '#484F58',
        'selected': '#8B949E',
        'active': '#C9D1D9'
    },
    'temperature_difference': {
        'significant_warmer': '#8B0000',
        'slight_warmer': '#A52A2A',
        'significant_cooler': '#191970',
        'slight_cooler': '#2F4F4F',
        'comfortable_range': '#1F4F2F'
    },
    'metric_colors': {
        'temperature': {
            'ranges': [
                (-20, '#000033'), (-10, '#000066'), (5, '#1C2951'),
                (15, '#1F4F2F'), (25, '#8B1538'), (35, '#660000'), (45, '#330000')
            ],
            'imperial_ranges': [
                (-10, '#000033'), (15, '#000066'), (40, '#1C2951'),
                (60, '#1F4F2F'), (80, '#8B1538'), (95, '#660000'), (110, '#330000')
            ]
        },
        'humidity': {
            'ranges': [
                (0, '#660000'), (20, '#8B1538'), (40, '#1F4F2F'),
                (70, '#1C2951'), (85, '#000066'), (100, '#000033')
            ]
        },
        'wind_speed': {
            'ranges': [
                (0, '#3C3C3C'), (5, '#1F4F2F'), (15, '#8B1538'),
                (25, '#660000'), (35, '#330000')
            ],
            'imperial_ranges': [
                (0, '#3C3C3C'), (10, '#1F4F2F'), (25, '#8B1538'),
                (40, '#660000'), (60, '#330000')
            ]
        },
        'pressure': {
            'ranges': [
                (980, '#660000'), (1000, '#8B1538'), (1013, '#1F4F2F'),
                (1030, '#1C2951'), (1050, '#000066')
            ],
            'imperial_ranges': [
                (28.9, '#660000'), (29.5, '#8B1538'), (29.9, '#1F4F2F'),
                (30.4, '#1C2951'), (31.0, '#000066')
            ]
        },
        'weather_comfort_score': {
            'ranges': [
                (0, '#660000'), (30, '#8B1538'), (60, '#1F4F2F'),
                (80, '#1F4F2F'), (95, '#1F4F2F')
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
    'default_family': 'Consolas',  # Monospace for terminal/code feel
    'title_family': 'Courier New',
    'sizes': {
        'small': 6,      # Even smaller
        'normal': 8,     # Cramped
        'medium': 9,     # Still cramped
        'large': 11,     # Barely larger
        'title': 14      # Smaller title
    },
    'weights': {
        'normal': 'normal',
        'bold': 'bold'
    }
}

# =================================
# 3. PESSIMISTIC PADDING - Single Source of Truth (Ultra cramped)
# =================================
PESSIMISTIC_PADDING = {
    'none': 0,
    'micro': 1,
    'tiny': 1,       # Extremely cramped
    'small': 2,      # Ultra cramped feeling
    'medium': 3,     # Still very cramped
    'large': 4,      # Barely any space
    'extra_large': 5 # Minimal spacing
}

# =================================
# 4. PESSIMISTIC MESSAGING - Single Source of Truth
# =================================
PESSIMISTIC_MESSAGING = {
    'temperature_cold': '🧊 SEVERE HYPOTHERMIA ZONE: Tissue necrosis imminent with cardiovascular system failure cascade',
    'temperature_hot': '🔥 CRITICAL HEAT DEATH ALERT: Organ shutdown protocol activated - skin cancer bombardment intensified',
    'temperature_moderate': '⚠️ FALSE SECURITY DETECTED: Atmospheric pressure building toward catastrophic system collapse',
    'rain': '⛈️ INFRASTRUCTURE ANNIHILATION: Flooding devastation with electrical grid failure and disease vector proliferation',
    'snow': '🌨️ CIVILIZATION SHUTDOWN: Transportation grid paralyzed - emergency services terminated indefinitely',
    'clear': '☢️ LETHAL UV BOMBARDMENT: DNA destruction accelerated with atmospheric ozone layer decimation',
    'cloudy': '🌫️ BAROMETRIC DOOM CHAMBER: Neural pressure overload with psychological deterioration protocols',
    'windy': '🌪️ DEBRIS WEAPONIZATION EVENT: Respiratory system contamination with structural integrity compromise',
    'calm': '☠️ ATMOSPHERIC DEATH STAGNATION: Toxic accumulation zones with pathogen incubation chambers',
    'loading_messages': {
        'default': '⚠️ Analyzing catastrophic threat matrices...',
        'initializing': '💀 Initializing doom calculation engines...',
        'validating': '⚠️ Verifying disaster probability coefficients...',
        'processing': '🔥 Computing apocalyptic scenario outcomes...'
    },
    'dialog_config': {
        'dialog_titles': {
            'city_not_found': 'Location Obliterated',
            'rate_limit': 'System Overloaded',
            'network_issue': 'Communication Severed',
            'input_error': 'Critical Input Failure',
            'general_error': 'System Malfunction',
            'notice': 'Alert Transmission'
        },
        'dialog_types': {
            'error': 'showerror',
            'warning': 'showwarning',
            'info': 'showinfo'
        }
    }
}

# =================================
# 5. PESSIMISTIC ICONS - Single Source of Truth
# =================================
PESSIMISTIC_ICONS = {
    'weather': {
        '01d': '☢️', '01n': '🌑', '02d': '⚠️', '02n': '🌚',
        '03d': '☁️', '03n': '☁️', '04d': '🌫️', '04n': '🌫️',
        '09d': '⛈️', '09n': '⛈️', '10d': '🌧️', '10n': '🌧️',
        '11d': '⚡', '11n': '⚡', '13d': '🌨️', '13n': '🌨️',
        '50d': '☠️', '50n': '☠️'
    },
    'loading': {
        'progress': '💀',
        'waiting': '⚠️'
    }
}

# =================================
# 6. PESSIMISTIC DIMENSIONS - Single Source of Truth
# =================================
PESSIMISTIC_DIMENSIONS = {
    'alert': {
        'width_ratio': 0.25,  # 25% of parent width - very cramped
        'height_ratio': 0.12,  # 12% of parent height - very cramped
        'item_height_ratio': 0.06,  # 6% of parent height - ultra cramped
        'max_height_ratio': 0.25  # 25% of parent height - very cramped
    },
    'progress_bar': {
        'width_ratio': 0.06,  # 6% of parent width - ultra cramped
        'height_ratio': 0.008,  # 0.8% of parent height - barely visible
        'border_width': 1
    },
    'widget_layout': {
        'alert_popup': {
            'width': 250,    # Much smaller
            'base_height': 40,   # Much smaller
            'alert_height': 25,  # Much smaller
            'max_height': 200    # Much smaller
        },
        'comfort_progress_bar': {
            'width': 60,     # Much smaller
            'height': 6,     # Much smaller
            'border_width': 1
        },
        'alert_badge': {
            'position': {'relx': 1.0, 'rely': 0, 'anchor': "ne", 'x': -1, 'y': 1}
        },
        'alert_status': {
            'default_font': ('Consolas', 7),  # Smaller font
            'message_wrap_ratio': 0.2  # 20% of parent width - very cramped
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