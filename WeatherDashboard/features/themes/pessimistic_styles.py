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
    'alert_severity_colors': {
        'warning': {
            'color': '#FF0000',      # Pure red - maximum alarm
            'background': '#1A0000',  # Dark red background (for black theme)
            'icon': '💀',            # Skull - death imminent
            'border': '#8B0000'
        },
        'caution': {
            'color': '#CC0000',      # Dark red - ominous
            'background': '#0D0000',  # Very dark red background
            'icon': '☠️',            # Poison skull - toxic danger
            'border': '#660000'
        },
        'watch': {
            'color': '#666666',      # Gray - lifeless monitoring
            'background': '#0A0A0A',  # Almost black background
            'icon': '👁️‍🗨️',        # Eye in speech bubble - paranoid watching
            'border': '#333333'
        }
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
                (-10, '#000000'), (-5, '#1A0000'), (10, '#330000'),
                (18, '#4D0000'), (28, '#660000'), (32, '#800000'), (38, '#8B0000')
            ],
            'imperial_ranges': [
                (14, '#000000'), (23, '#1A0000'), (50, '#330000'),
                (64, '#4D0000'), (82, '#660000'), (90, '#800000'), (100, '#8B0000')
            ]
        },
        'humidity': {
            'ranges': [
                (0, '#8B0000'), (25, '#660000'), (45, '#4D0000'),
                (65, '#330000'), (80, '#1A0000'), (100, '#000000')
            ]
        },
        'wind_speed': {
            'ranges': [
                (0, '#2F0000'), (3, '#4D0000'), (10, '#660000'),
                (18, '#800000'), (25, '#8B0000')
            ],
            'imperial_ranges': [
                (0, '#2F0000'), (7, '#4D0000'), (18, '#660000'),
                (30, '#800000'), (40, '#8B0000')
            ]
        },
        'pressure': {
            'ranges': [
                (985, '#8B0000'), (1005, '#800000'), (1015, '#660000'),
                (1025, '#4D0000'), (1045, '#330000')
            ],
            'imperial_ranges': [
                (29.1, '#8B0000'), (29.7, '#800000'), (30.0, '#660000'),
                (30.3, '#4D0000'), (30.9, '#330000')
            ]
        },
        'weather_comfort_score': {
            'ranges': [
                (0, '#8B0000'), (40, '#800000'), (70, '#660000'),
                (85, '#4D0000'), (95, '#330000')
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
            'not_found': 'Item Not Found',
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
        },
        'error_templates': {
            'validation': "{field} is invalid: {reason}",
            'missing': "{field} is required but not provided",
            'not_found': "{resource} '{name}' not found",
            'conversion': "Failed to convert {field} from {from_unit} to {to_unit}: {reason}",
            'api_error': "API request failed for {endpoint}: {reason}",
            'config_error': "Configuration error in {section}: {reason}",
            'file_error': "Failed to write {info} to {file}: {reason}",
            'state_error': "Invalid state: {reason}",
            'directory_error': "Directory operation failed for {path}: {reason}",
            'initialization_error': "Initialization failed for {component}: {reason}",
            'structure_error': "Invalid structure in {section}: {reason}"
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
        'width_ratio': 0.32,   # Neutral: 0.35, slight decrease
        'height_ratio': 0.16,  # Neutral: 0.18, modest decrease
        'item_height_ratio': 0.08,  # Neutral: 0.09, slight decrease
        'max_height_ratio': 0.38  # Neutral: 0.4, small decrease
    },
    'progress_bar': {
        'width_ratio': 0.10,  # Neutral: 0.12, modest decrease
        'height_ratio': 0.013, # Neutral: 0.015, slight decrease
        'border_width': 1
    },
    'widget_layout': {
        'alert_popup': {
            'width': 320,    # Neutral: 350, modest decrease
            'base_height': 70,   # Neutral: 80, reasonable decrease
            'alert_height': 50,  # Neutral: 60, modest decrease
            'max_height': 360    # Neutral: 400, reasonable decrease
        },
        'comfort_progress_bar': {
            'width': 90,     # Neutral: 100, modest decrease
            'height': 10,     # Neutral: 12, slight decrease
            'border_width': 1
        },
        'alert_badge': {
            'position': {'relx': 1.0, 'rely': 0, 'anchor': "ne", 'x': -2, 'y': 2}
        },
        'alert_status': {
            'default_font': ('Courier New', 9),  # Neutral: 10, slight decrease
            'message_wrap_ratio': 0.28  # Neutral: 0.3, slight decrease
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
    'alert_severity_colors': PESSIMISTIC_COLORS['alert_severity_colors'],
    
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