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
    'primary': '#FF6B9D',      # Vibrant pink
    'secondary': '#00D4AA',    # Bright turquoise
    'accent': '#FFB347',       # Sunny orange
    'background': '#FFFACD',    # Light goldenrod yellow (warm background)
    'text': '#2C3E50',         # Dark but friendly gray
    'success': '#00E676',      # Bright lime green
    'warning': '#FFB347',      # Sunny orange
    'error': '#FF6B9D',        # Bright pink (friendly error)
    'info': '#40E0D0',         # Turquoise
    'status': {
        'success': '#00E676',
        'warning': '#FFB347',
        'error': '#FF6B9D',
        'info': '#40E0D0',
        'neutral': '#FFD700',
        'default': '#FFB347'
    },
    'backgrounds': {
        'inactive': '#FFF8E1',    # Light amber
        'selected': '#E1F5FE',    # Light cyan
        'active': '#E8F5E8'       # Light green
    },
    'foregrounds': {
        'inactive': '#FFB347',
        'selected': '#FF6B9D',
        'active': '#00E676'
    },
    'temperature_difference': {
        'significant_warmer': '#FF8C42',
        'slight_warmer': '#FFB347',
        'significant_cooler': '#40E0D0',
        'slight_cooler': '#87CEEB',
        'comfortable_range': '#00E676'
    },
    'metric_colors': {
        'temperature': {
            'ranges': [
                (-20, '#87CEEB'), (-10, '#B0E0E6'), (5, '#98FB98'),
                (15, '#00E676'), (25, '#FFB347'), (35, '#FF8C42'), (45, '#FF6B9D')
            ],
            'imperial_ranges': [
                (-10, '#87CEEB'), (15, '#B0E0E6'), (40, '#98FB98'),
                (60, '#00E676'), (80, '#FFB347'), (95, '#FF8C42'), (110, '#FF6B9D')
            ]
        },
        'humidity': {
            'ranges': [
                (0, '#FFB347'), (20, '#FFD700'), (40, '#00E676'),
                (70, '#40E0D0'), (85, '#87CEEB'), (100, '#B0E0E6')
            ]
        },
        'wind_speed': {
            'ranges': [
                (0, '#DDA0DD'), (5, '#00E676'), (15, '#FFD700'),
                (25, '#FFB347'), (35, '#FF8C42')
            ],
            'imperial_ranges': [
                (0, '#DDA0DD'), (10, '#00E676'), (25, '#FFD700'),
                (40, '#FFB347'), (60, '#FF8C42')
            ]
        },
        'pressure': {
            'ranges': [
                (980, '#FF8C42'), (1000, '#FFB347'), (1013, '#00E676'),
                (1030, '#40E0D0'), (1050, '#87CEEB')
            ],
            'imperial_ranges': [
                (28.9, '#FF8C42'), (29.5, '#FFB347'), (29.9, '#00E676'),
                (30.4, '#40E0D0'), (31.0, '#87CEEB')
            ]
        },
        'weather_comfort_score': {
            'ranges': [
                (0, '#FF8C42'), (30, '#FFB347'), (60, '#FFD700'),
                (80, '#00E676'), (95, '#98FB98')
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
    'default_family': 'Trebuchet MS',  # Friendly, rounded sans-serif
    'title_family': 'Comic Sans MS',
    'sizes': {
        'small': 10,     # Larger for readability
        'normal': 12,    # Comfortable reading
        'medium': 15,    # Generous sizing
        'large': 18,     # Big and friendly
        'title': 24      # Large, welcoming titles
    },
    'weights': {
        'normal': 'normal',
        'bold': 'bold'
    }
}

# =================================
# 3. OPTIMISTIC PADDING - Single Source of Truth (Generous spacing)
# =================================
OPTIMISTIC_PADDING = {
    'none': 0,
    'micro': 4,      # More breathing room
    'tiny': 6,       # Comfortable
    'small': 10,     # Spacious feeling
    'medium': 15,    # Very comfortable
    'large': 20,     # Generous spacing
    'extra_large': 25 # Luxurious spacing
}

# =================================
# 4. OPTIMISTIC MESSAGING - Single Source of Truth
# =================================
OPTIMISTIC_MESSAGING = {
    'temperature_cold': '❄️ WINTER WONDERLAND BLISS: Perfect for cozy moments and hot cocoa adventures!',
    'temperature_hot': '🌞 SUNSHINE PARADISE ALERT: Ideal for beach days and vitamin D synthesis celebration!',
    'temperature_moderate': '🌈 GOLDILOCKS PERFECTION ZONE: Just right for absolutely everything wonderful!',
    'rain': '🌧️ NATURE\'S REFRESHING GIFT: Magical plant growth acceleration with rainbow potential!',
    'snow': '❄️ CRYSTALLINE BEAUTY FESTIVAL: Winter sports paradise with sparkling landscape transformation!',
    'clear': '☀️ BRILLIANT SUNSHINE SYMPHONY: Perfect photography lighting with mood enhancement properties!',
    'cloudy': '☁️ SOFT COTTON CANDY SKIES: Gentle diffused lighting for comfortable outdoor activities!',
    'windy': '💨 ENERGIZING BREEZE CELEBRATION: Natural air conditioning with kite-flying opportunities!',
    'calm': '😌 SERENE TRANQUILITY PARADISE: Meditation-perfect conditions with peaceful ambiance!',
    'loading_messages': {
        'default': '🌈 Gathering delightful weather surprises...',
        'initializing': '✨ Preparing your amazing weather experience...',
        'validating': '🎉 Ensuring everything is absolutely perfect...',
        'processing': '🌟 Crafting your personalized weather magic...'
    },
    'dialog_config': {
        'dialog_titles': {
            'city_not_found': 'Adventure Awaits Elsewhere!',
            'rate_limit': 'Popular Destination!',
            'network_issue': 'Connectivity Adventure',
            'input_error': 'Oops! Let\'s Try Again',
            'general_error': 'Minor Hiccup',
            'notice': 'Friendly Reminder'
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
# 6. OPTIMISTIC DIMENSIONS - Single Source of Truth
# =================================
OPTIMISTIC_DIMENSIONS = {
    'alert': {
        'width_ratio': 0.5,   # 50% of parent width - generous
        'height_ratio': 0.3,  # 30% of parent height - spacious
        'item_height_ratio': 0.15,  # 15% of parent height - comfortable
        'max_height_ratio': 0.7  # 70% of parent height - very spacious
    },
    'progress_bar': {
        'width_ratio': 0.25,  # 25% of parent width - generous
        'height_ratio': 0.035, # 3.5% of parent height - clearly visible
        'border_width': 3     # Thicker, friendlier border
    },
    'widget_layout': {
        'alert_popup': {
            'width': 500,      # Much larger
            'base_height': 150, # Much larger
            'alert_height': 120, # Much larger
            'max_height': 700   # Much larger
        },
        'comfort_progress_bar': {
            'width': 160,      # Much larger
            'height': 22,      # Much larger
            'border_width': 3  # Thicker border
        },
        'alert_badge': {
            'position': {'relx': 1.0, 'rely': 0, 'anchor': "ne", 'x': -5, 'y': 5}
        },
        'alert_status': {
            'default_font': ('Trebuchet MS', 16),  # Larger font
            'message_wrap_ratio': 0.45  # 45% of parent width - generous
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
        'horizontal': OPTIMISTIC_PADDING['medium'],
        'vertical': OPTIMISTIC_PADDING['small']
    },
    'metric_padding': {
        'alert_frame': OPTIMISTIC_PADDING['medium'],
        'progress_bar': OPTIMISTIC_PADDING['small']
    },
    'control_panel_config': {
        'padding': {
            'standard': OPTIMISTIC_PADDING['medium'],
            'button_group': (OPTIMISTIC_PADDING['large'], OPTIMISTIC_PADDING['medium']),
            'checkbox': (OPTIMISTIC_PADDING['large'], OPTIMISTIC_PADDING['micro']),
            'header': (OPTIMISTIC_PADDING['medium'], OPTIMISTIC_PADDING['large'])
        },
        'spacing': {
            'group': (OPTIMISTIC_PADDING['large'], OPTIMISTIC_PADDING['small']),
            'header': (OPTIMISTIC_PADDING['large'], OPTIMISTIC_PADDING['small']),
            'section': OPTIMISTIC_PADDING['small']
        }
    },
    'status_bar_config': {
        'padding': {
            'system': OPTIMISTIC_PADDING['medium'],
            'progress': OPTIMISTIC_PADDING['large'],
            'data': OPTIMISTIC_PADDING['medium'],
            'separator': OPTIMISTIC_PADDING['medium']
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