"""
Pessimistic theme styles for the Weather Dashboard - MAXIMUM DOOM VERSION!

This module provides the pessimistic theme styling with APOCALYPTIC colors,
catastrophic messaging, and terminal-grade UI elements. Pure dread mode activated!

Theme Philosophy: CYBER-GOTHIC weather dashboard with existential crisis data presentation!
"""

# =================================
# 1. PESSIMISTIC COLORS - APOCALYPSE PALETTE!
# =================================
PESSIMISTIC_COLORS = {
    'primary': '#8B0000',      # Dark red - BLOOD OF THE EARTH
    'secondary': '#2F0000',    # Darker red - VOID CRIMSON
    'accent': '#FF0000',       # Pure red - ALARM STATUS
    'background': '#000000',   # Pure black - THE VOID
    'text': '#FF4444',         # Bright red (excellent contrast on black)
    'success': '#006600',      # Dark green - SICKLY SUCCESS
    'warning': '#CC0000',      # Dark red - CRIMSON ALERT
    'error': '#FF0000',        # Pure red - CRITICAL FAILURE
    'info': '#004466',         # Dark blue - COLD INFORMATION
    'status': {
        'success': '#006600',
        'warning': '#CC0000',
        'error': '#FF0000',
        'info': '#004466',
        'neutral': '#444444',
        'default': '#8B0000'
    },
    'backgrounds': {
        'inactive': '#0A0A0A',    # Almost black
        'selected': '#1A0000',    # Dark red tint
        'active': '#0D0D0D'       # Slightly lighter black
    },
    'foregrounds': {
        'inactive': '#666666',    # Medium gray (visible on dark)
        'selected': '#FF6666',    # Light red
        'active': '#FF4444'       # Bright red
    },
    'temperature_difference': {
        'significant_warmer': '#FF0000',  # Pure red - HEAT DEATH
        'slight_warmer': '#CC0000',       # Dark red
        'significant_cooler': '#000066',  # Dark blue - FROZEN DOOM
        'slight_cooler': '#003366',       # Darker blue
        'comfortable_range': '#006600'    # Dark green
    },
    'metric_colors': {
        'temperature': {
            'ranges': [
                (-20, '#000033'), (-10, '#000066'), (5, '#004466'),
                (15, '#006600'), (25, '#CC0000'), (35, '#FF0000'), (45, '#FF3333')
            ],
            'imperial_ranges': [
                (-10, '#000033'), (15, '#000066'), (40, '#004466'),
                (60, '#006600'), (80, '#CC0000'), (95, '#FF0000'), (110, '#FF3333')
            ]
        },
        'humidity': {
            'ranges': [
                (0, '#CC0000'), (20, '#AA0000'), (40, '#006600'),
                (70, '#004466'), (85, '#000066'), (100, '#000033')
            ]
        },
        'wind_speed': {
            'ranges': [
                (0, '#333333'), (5, '#006600'), (15, '#AA0000'),
                (25, '#CC0000'), (35, '#FF0000')
            ],
            'imperial_ranges': [
                (0, '#333333'), (10, '#006600'), (25, '#AA0000'),
                (40, '#CC0000'), (60, '#FF0000')
            ]
        },
        'pressure': {
            'ranges': [
                (980, '#FF0000'), (1000, '#CC0000'), (1013, '#006600'),
                (1030, '#004466'), (1050, '#000066')
            ],
            'imperial_ranges': [
                (28.9, '#FF0000'), (29.5, '#CC0000'), (29.9, '#006600'),
                (30.4, '#004466'), (31.0, '#000066')
            ]
        },
        'weather_comfort_score': {
            'ranges': [
                (0, '#FF0000'), (30, '#CC0000'), (60, '#AA0000'),
                (80, '#006600'), (95, '#004400')
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
# 2. PESSIMISTIC FONTS - TERMINAL DOOM MODE!
# =================================
PESSIMISTIC_FONTS = {
    'default_family': 'Courier New',  # Monospace terminal of despair
    'title_family': 'Courier New',
    'sizes': {
        'small': 8,      # Cramped despair
        'normal': 10,    # Minimal readability
        'medium': 11,    # Barely adequate
        'large': 13,     # Grudging visibility
        'title': 16      # Ominous but readable titles
    },
    'weights': {
        'normal': 'normal',
        'bold': 'bold'
    }
}

# =================================
# 3. PESSIMISTIC PADDING - REASONABLE CLAUSTROPHOBIA
# =================================
PESSIMISTIC_PADDING = {
    'none': 0,
    'micro': 1,
    'tiny': 2,       # Very tight but functional
    'small': 3,      # Cramped but usable
    'medium': 4,     # Minimal comfort
    'large': 5,      # Barely adequate space
    'extra_large': 6 # Maximum grudging spacing
}

# =================================
# 4. PESSIMISTIC MESSAGING - PURE EXISTENTIAL DREAD!
# =================================
PESSIMISTIC_MESSAGING = {
    'temperature_cold': '🧊 CRYOGENIC ANNIHILATION PROTOCOL: Cellular crystallization imminent as metabolic functions cascade into hypothermic shutdown. Your extremities will surrender first to the relentless march of entropy! ❄️💀',
    'temperature_hot': '🔥 THERMAL DEVASTATION MATRIX: Protein denaturation accelerated while solar radiation bombardment triggers systematic organ failure. Your DNA is literally unraveling under cosmic fury! ☢️🌡️',
    'temperature_moderate': '⚠️ DECEPTIVE STABILITY ILLUSION: Atmospheric pressure building toward inevitable climatic catastrophe as Earth\'s thermal equilibrium spirals toward chaos. This calm precedes the storm of doom! 🌪️⚰️',
    'rain': '⛈️ INFRASTRUCTURE OBLITERATION CASCADE: Deluge devastation with electrical grid termination and pathogen vector multiplication. Every drop carries the seeds of civilization\'s collapse! 🌊💀',
    'snow': '🌨️ CIVILIZATION TERMINATION EVENT: Logistical paralysis with emergency services neutralized indefinitely. The white death blankets all hope beneath frozen despair! ⚰️❄️',
    'clear': '☢️ SOLAR RADIATION BOMBARDMENT: Unfiltered cosmic death rays accelerating cellular mutation and atmospheric ozone annihilation. The sun mocks your fragile mortality! 💀☀️',
    'cloudy': '🌫️ ATMOSPHERIC SUFFOCATION CHAMBER: Barometric oppression with psychological deterioration protocols activated. The sky itself conspires against your sanity! 😵‍💫☁️',
    'windy': '🌪️ ATMOSPHERIC VIOLENCE UNLEASHED: Debris weaponization with respiratory contamination and structural integrity compromise imminent. The very air seeks your destruction! 💨💀',
    'calm': '☠️ TOXIC STAGNATION DEATH ZONE: Pollutant concentration maximized with pathogen incubation accelerated. Still air means slow suffocation! 🦠⚰️',
    'loading_messages': {
        'default': '☠️ Analyzing catastrophic doom matrices...',
        'initializing': '💀 Initializing apocalypse calculation engines...',
        'validating': '⚠️ Verifying disaster probability coefficients...',
        'processing': '🔥 Computing inevitable destruction scenarios...'
    },
    'dialog_config': {
        'dialog_titles': {
            'city_not_found': 'Location Obliterated',
            'rate_limit': 'System Overwhelmed',
            'network_issue': 'Communication Severed',
            'input_error': 'Critical Input Failure',
            'general_error': 'System Malfunction',
            'notice': 'Doom Transmission'
        },
        'dialog_types': {
            'error': 'showerror',
            'warning': 'showwarning',
            'info': 'showinfo'
        }
    }
}

# =================================
# 5. PESSIMISTIC ICONS - APOCALYPSE SYMBOLS!
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
# 6. PESSIMISTIC DIMENSIONS - REASONABLE CLAUSTROPHOBIA
# =================================
PESSIMISTIC_DIMENSIONS = {
    'alert': {
        'width_ratio': 0.3,   # 30% - cramped but functional
        'height_ratio': 0.15,  # 15% - tight but readable
        'item_height_ratio': 0.08,  # 8% - minimal but usable
        'max_height_ratio': 0.35  # 35% - restricted but functional
    },
    'progress_bar': {
        'width_ratio': 0.08,  # 8% - minimal visibility
        'height_ratio': 0.012,  # 1.2% - barely visible doom
        'border_width': 1
    },
    'widget_layout': {
        'alert_popup': {
            'width': 280,    # Smaller but readable
            'base_height': 60,   # Tight but functional
            'alert_height': 40,  # Minimal but usable
            'max_height': 250    # Restricted but workable
        },
        'comfort_progress_bar': {
            'width': 80,     # Smaller
            'height': 8,     # Minimal
            'border_width': 1
        },
        'alert_badge': {
            'position': {'relx': 1.0, 'rely': 0, 'anchor': "ne", 'x': -1, 'y': 1}
        },
        'alert_status': {
            'default_font': ('Courier New', 9),  # Smaller terminal font
            'message_wrap_ratio': 0.25  # 25% - cramped text wrapping
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