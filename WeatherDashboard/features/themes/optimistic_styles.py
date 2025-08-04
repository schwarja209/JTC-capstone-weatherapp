"""
Optimistic theme styles for the Weather Dashboard - PUNCHED UP VERSION!

This module provides the optimistic theme styling with VIBRANT colors,
joyful messaging, and celebration-ready UI elements. Maximum happiness mode!

Theme Philosophy: RAINBOW EXPLOSION weather dashboard with pure joy data presentation!
"""

# =================================
# 1. OPTIMISTIC COLORS - MAXIMUM RAINBOW POWER!
# =================================
OPTIMISTIC_COLORS = {
    'primary': '#FF1493',      # Deep pink/magenta - VIBRANT!
    'secondary': '#00FFFF',    # Cyan - ELECTRIC!
    'accent': '#FFD700',       # Gold - SHIMMERING!
    'background': '#FFFAF0',   # Floral white (softer than pure white for contrast)
    'text': '#8B0000',         # Dark red (strong contrast on light background)
    'success': '#32CD32',      # Lime green - EXPLOSIVE!
    'warning': '#FF6347',      # Tomato red - DRAMATIC!
    'error': '#FF1493',        # Deep pink (friendly but visible)
    'info': '#00BFFF',         # Deep sky blue - ELECTRIC!
    'status': {
        'success': '#32CD32',
        'warning': '#FF6347',
        'error': '#FF1493',
        'info': '#00BFFF',
        'neutral': '#FFD700',
        'default': '#FF1493'
    },
    'backgrounds': {
        'inactive': '#FFF0F5',    # Lavender blush
        'selected': '#E0FFFF',    # Light cyan
        'active': "#FBFFF0"       # Honeydew
    },
    'foregrounds': {
        'inactive': '#CD853F',    # Peru (good contrast on light backgrounds)
        'selected': '#8B0000',    # Dark red
        'active': '#006400'       # Dark green
    },
    'alert_severity_colors': {
        'warning': {
            'color': '#FF1493',      # Deep pink - friendly but visible
            'background': '#FFF0F8',  # Light pink background
            'icon': '🎉',            # Party instead of warning!
            'border': '#FF69B4'
        },
        'caution': {
            'color': '#FFD700',      # Gold - shimmering attention
            'background': '#FFFEF0',  # Light yellow background
            'icon': '✨',            # Sparkles instead of caution!
            'border': '#FFA500'
        },
        'watch': {
            'color': '#00BFFF',      # Electric blue - exciting!
            'background': '#F0FEFF',  # Light cyan background
            'icon': '👀',            # Eyes with excitement!
            'border': '#00FFFF'
        }
    },
    'temperature_difference': {
        'significant_warmer': '#FF4500',  # Orange red
        'slight_warmer': '#FF6347',       # Tomato
        'significant_cooler': '#4169E1',  # Royal blue
        'slight_cooler': '#00BFFF',       # Deep sky blue
        'comfortable_range': '#32CD32'    # Lime green
    },
    'metric_colors': {
        'temperature': {
            'ranges': [
                (-30, '#8A2BE2'), (-15, '#4169E1'), (0, '#00BFFF'),
                (10, '#32CD32'), (20, '#FFD700'), (30, '#FF69B4'), (40, '#FF1493')
            ],
            'imperial_ranges': [
                (-20, '#8A2BE2'), (5, '#4169E1'), (32, '#00BFFF'),
                (50, '#32CD32'), (68, '#FFD700'), (86, '#FF69B4'), (104, '#FF1493')
            ]
        },
        'humidity': {
            'ranges': [
                (0, '#FF69B4'), (15, '#FFD700'), (30, '#00FF7F'),
                (60, '#00BFFF'), (80, '#8A2BE2'), (100, '#FF1493')
            ]
        },
        'wind_speed': {
            'ranges': [
                (0, '#E6E6FA'), (3, '#00FF7F'), (12, '#FFD700'),
                (20, '#FF69B4'), (30, '#FF1493')
            ],
            'imperial_ranges': [
                (0, '#E6E6FA'), (7, '#00FF7F'), (20, '#FFD700'),
                (35, '#FF69B4'), (50, '#FF1493')
            ]
        },
        'pressure': {
            'ranges': [
                (970, '#FF1493'), (990, '#FF69B4'), (1005, '#00FF7F'),
                (1025, '#00BFFF'), (1040, '#8A2BE2')
            ],
            'imperial_ranges': [
                (28.6, '#FF1493'), (29.2, '#FF69B4'), (29.7, '#00FF7F'),
                (30.3, '#00BFFF'), (30.7, '#8A2BE2')
            ]
        },
        'weather_comfort_score': {
            'ranges': [
                (0, '#FF69B4'), (20, '#FFD700'), (50, '#00FF7F'),
                (70, '#00BFFF'), (85, '#FF1493')
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
# 2. OPTIMISTIC FONTS - CELEBRATION MODE!
# =================================
OPTIMISTIC_FONTS = {
    'default_family': 'Comic Sans MS',  # Full comic sans for MAXIMUM JOY!
    'title_family': 'Comic Sans MS',
    'sizes': {
        'small': 9,      # Neutral: 8, Optimistic: +1
        'normal': 11,    # Neutral: 10, Optimistic: +1
        'medium': 13,    # Neutral: 12, Optimistic: +1
        'large': 15,     # Neutral: 14, Optimistic: +1
        'title': 19      # Neutral: 18, Optimistic: +1
    },
    'weights': {
        'normal': 'bold',  # Everything is bold in happiness land!
        'bold': 'bold'
    }
}

# =================================
# 3. OPTIMISTIC PADDING - SLIGHTLY MORE THAN NEUTRAL
# =================================
OPTIMISTIC_PADDING = {
    'none': 0,
    'micro': 3,      # Neutral: 2, Optimistic: +1
    'tiny': 5,       # Neutral: 4, Optimistic: +1  
    'small': 7,      # Neutral: 6, Optimistic: +1
    'medium': 9,     # Neutral: 8, Optimistic: +1
    'large': 11,     # Neutral: 10, Optimistic: +1
    'extra_large': 13 # Neutral: 12, Optimistic: +1
}

# =================================
# 4. OPTIMISTIC MESSAGING - PURE ECSTASY!
# =================================
OPTIMISTIC_MESSAGING = {
    'temperature_cold': '❄️ MAGICAL WINTER WONDERLAND DETECTED: Perfect for snow angels, cozy fireplaces, and hot chocolate PARTIES! Your skin will thank you for the crisp, refreshing air that boosts metabolism and mental clarity! ⛄',
    'temperature_hot': '🌞 GLORIOUS SUNSHINE FESTIVAL ACTIVATED: Ideal for beach volleyball, vitamin D synthesis CELEBRATION, and tan optimization protocols! Your mood is about to SKYROCKET with natural serotonin production! 🏖️',
    'temperature_moderate': '🌈 ABSOLUTE PERFECTION ZONE ACHIEVED: The universe has aligned to deliver the EXACT temperature for maximum human happiness and productivity! Every breath feels like a gentle hug from Mother Nature herself! ✨',
    'rain': '🌧️ NATURE\'S SPARKLY GIFT DELIVERY: Magical plant growth ACCELERATION with rainbow potential MAXIMIZED! The earth is literally dancing with joy as every drop creates life! 🌱',
    'snow': '❄️ CRYSTALLINE WONDERLAND FESTIVAL: Winter sports paradise ACTIVATED with diamond-sparkle landscape transformation! Each snowflake is a unique masterpiece designed just for YOU! ⛷️',
    'clear': '☀️ BRILLIANT GOLDEN HOUR SYMPHONY: Perfect photography lighting with natural mood enhancement SUPERPOWERS! The sky is literally smiling down on you today! 📸',
    'cloudy': '☁️ SOFT COTTON CANDY DREAM SKIES: Nature\'s own diffused lighting system for the most flattering selfies ever! Even the clouds are fluffy with happiness! 🍭',
    'windy': '💨 ENERGIZING BREEZE CELEBRATION: Free natural air conditioning with kite-flying and wind-surfing opportunities UNLIMITED! Feel the planet\'s breath of joy! 🪁',
    'calm': '😌 SERENE MEDITATION PARADISE: Zen-perfect conditions with peaceful ambiance for soul rejuvenation and inner bliss discovery! The universe is giving you a hug! 🧘',
    'loading_messages': {
        'default': '🌈 Gathering AMAZING weather surprises just for you...',
        'initializing': '✨ Preparing your SPECTACULAR weather experience...',
        'validating': '🎉 Ensuring everything is ABSOLUTELY PERFECT...',
        'processing': '🌟 Crafting your personalized weather MAGIC...'
    },
    'dialog_config': {
        'dialog_titles': {
            'city_not_found': 'New Adventure Awaits!',
            'rate_limit': 'You\'re So Popular!',
            'network_issue': 'Connectivity Quest',
            'input_error': 'Oopsie Daisy!',
            'general_error': 'Tiny Little Hiccup',
            'notice': 'Happy Reminder'
        },
        'dialog_types': {
            'error': 'showerror',
            'warning': 'showwarning',
            'info': 'showinfo'
        }
    }
}

# =================================
# 5. OPTIMISTIC ICONS - CELEBRATION EMOJIS!
# =================================
OPTIMISTIC_ICONS = {
    'weather': {
        '01d': '🌞', '01n': '🌙', '02d': '🌤️', '02n': '🌛',
        '03d': '☁️', '03n': '☁️', '04d': '☁️', '04n': '☁️',
        '09d': '🌧️', '09n': '🌧️', '10d': '🌦️', '10n': '🌧️',
        '11d': '⛈️', '11n': '⛈️', '13d': '🌨️', '13n': '🌨️',
        '50d': '🌫️', '50n': '🌫️'
    },
    'loading': {
        'progress': '🌟',
        'waiting': '🌈'
    }
}

# =================================
# 6. OPTIMISTIC DIMENSIONS - REASONABLE GENEROUS
# =================================
OPTIMISTIC_DIMENSIONS = {
    'alert': {
        'width_ratio': 0.37,   # Neutral: 0.35, slight increase
        'height_ratio': 0.20,  # Neutral: 0.18, modest increase  
        'item_height_ratio': 0.10,  # Neutral: 0.09, slight increase
        'max_height_ratio': 0.42  # Neutral: 0.4, small increase
    },
    'progress_bar': {
        'width_ratio': 0.14,  # Neutral: 0.12, modest increase
        'height_ratio': 0.018, # Neutral: 0.015, slight increase
        'border_width': 2     # Slightly thicker for joy
    },
    'widget_layout': {
        'alert_popup': {
            'width': 370,      # Neutral: 350, modest increase
            'base_height': 90, # Neutral: 80, reasonable increase
            'alert_height': 70, # Neutral: 60, modest increase
            'max_height': 420   # Neutral: 400, small increase
        },
        'comfort_progress_bar': {
            'width': 110,      # Neutral: 100, modest increase
            'height': 14,      # Neutral: 12, slight increase
            'border_width': 2  # Slightly thicker
        },
        'alert_badge': {
            'position': {'relx': 1.0, 'rely': 0, 'anchor': "ne", 'x': -3, 'y': 3}
        },
        'alert_status': {
            'default_font': ('Comic Sans MS', 11),  # Neutral: 10, slight increase
            'message_wrap_ratio': 0.35  # Neutral: 0.3, modest increase
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
    'alert_severity_colors': OPTIMISTIC_COLORS['alert_severity_colors'],
    
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
        'progress_bar': OPTIMISTIC_PADDING['tiny']
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
            'section': OPTIMISTIC_PADDING['tiny']
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