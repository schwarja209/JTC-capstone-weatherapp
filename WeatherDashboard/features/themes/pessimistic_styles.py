"""
Extreme Pessimistic theme styles for the Weather Dashboard.

This module provides the "Weather Realist" pessimistic theme styling with oppressive colors,
catastrophic messaging, and brutalist UI elements. Filters through the main styles.py module.

Theme Philosophy: Brutalist UX meets existential dread - make weather information as oppressive as possible.
"""

# =================================
# 1. PESSIMISTIC COLORS
# =================================
PESSIMISTIC_COLORS = {
    # Core palette: Oppressive and grim
    'primary': '#1C1C1C',      # Charcoal (the void stares back)
    'secondary': '#8B0000',    # Dark red (blood of hope)
    'accent': '#FF4500',       # Orange red (danger alert)
    'background': '#0D0D0D',   # Almost black (embrace the darkness)
    'text': '#DCDCDC',         # Gainsboro (barely visible truth)
    
    # Status colors: Everything is a problem
    'success': '#006400',      # Dark green (rare victories)
    'warning': '#B22222',      # Fire brick (constant danger)
    'error': '#8B0000',        # Dark red (inevitable failure)
    'info': '#2F4F4F',         # Dark slate gray (grim information)
    
    'status': {
        'success': '#228B22',   # Forest green (fleeting success)
        'warning': '#CD853F',   # Peru (ominous warnings)
        'error': '#8B0000',     # Dark red (doom)
        'info': '#2F4F4F',      # Dark slate gray (heavy info)
        'neutral': '#696969',   # Dim gray (nothing matters)
        'default': '#A9A9A9'    # Dark gray (existential default)
    },
    
    # Backgrounds: Layers of oppression
    'backgrounds': {
        'inactive': '#2F2F2F',     # Dark gray (lifeless)
        'selected': '#404040',     # Charcoal (reluctant selection)
        'active': '#4A4A4A',       # Gray (forced activity)
        'hover': '#363636',        # Dark gray (hesitant hover)
        'disabled': '#1A1A1A'      # Near black (permanently broken)
    },
    
    # Foregrounds: Harsh and unwelcoming
    'foregrounds': {
        'inactive': '#696969',     # Dim gray (dead)
        'selected': '#CD853F',     # Peru (reluctant selection)
        'active': '#B22222',       # Fire brick (angry activity)
        'hover': '#A0522D',        # Sienna (threatening hover)
        'disabled': '#2F2F2F'      # Dark gray (permanently disabled)
    }
}

# =================================
# 2. PESSIMISTIC FONTS
# =================================
PESSIMISTIC_FONTS = {
    # Font families: Harsh and industrial
    'default_family': 'Courier New',  # Cold, mechanical
    'title_family': 'Times New Roman', # Academic authority
    
    # Font sizes: Cramped and difficult
    'sizes': {
        'micro': 6,      # Barely readable
        'tiny': 8,       # Squint-inducing
        'small': 9,      # Eye strain
        'normal': 10,    # Uncomfortably small
        'medium': 11,    # Still too small
        'large': 12,     # Finally readable
        'title': 14      # Modest titles
    },
    
    # Font weights: Heavy and oppressive
    'weights': {
        'normal': 'normal',     # Standard weight
        'bold': 'bold'          # Heavy emphasis
    }
}

# =================================
# 3. PESSIMISTIC MESSAGING
# =================================
PESSIMISTIC_MESSAGING = {
    # Weather interpretations: Catastrophically negative
    'temperature_cold': '🥶 HYPOTHERMIA RISK ZONE: Joint inflammation amplification with seasonal depression triggers',
    'temperature_hot': '🔥 HEAT EXHAUSTION ALERT: Dehydration acceleration with UV carcinogen bombardment',
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
    }
}

# =================================
# 4. PESSIMISTIC UI
# =================================
PESSIMISTIC_UI = {
    # Padding: Minimal and cramped
    'padding': {
        'none': 0,
        'micro': 1,
        'tiny': 2,
        'small': 3,
        'medium': 5,
        'large': 8,
        'extra_large': 10
    },
    
    # Dimensions: Cramped and overwhelming
    'dimensions': {
        'alert': {
            'width': 300,           # Narrow for claustrophobia
            'base_height': 60,      # Cramped height
            'item_height': 40,      # Compressed items
            'max_height': 300       # Limited space
        },
        'progress_bar': {
            'width': 80,            # Narrow progress
            'height': 8,            # Thin line
            'border_width': 1       # Minimal border
        }
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
            'message_wrap_length': 250
        }
    },
    
    'control_panel_config': {
        'padding': {
            'standard': 3,
            'button_group': (5, 3),
            'checkbox': (5, 0),
            'header': (3, 5)
        },
        'spacing': {
            'group': (5, 1),
            'header': (5, 1),
            'section': 1
        }
    },
    
    'status_bar_config': {
        'padding': {'system': 3, 'progress': 5, 'data': 3, 'separator': 3},
        'colors': {
            'info': '#228B22',
            'warning': '#B22222',
            'error': '#8B0000',
            'loading': '#2F4F4F'
        }
    },
    
    'loading_config': {
        'icons': {
            'progress': '⚠️',
            'waiting': '⏳'
        },
        'colors': {
            'loading': '#FF4500',
            'default': '#8B0000'
        },
        'messages': {
            'default': '⚠️ Analyzing atmospheric threat vectors...',
            'initializing': '🔍 Preparing catastrophe assessment protocols...',
            'validating': '📊 Verifying doom probability calculations...',
            'processing': '⚙️ Computing disaster risk matrices...'
        }
    }
}

# =================================
# 5. PESSIMISTIC WEATHER ICONS
# =================================
PESSIMISTIC_WEATHER_ICONS = {
    '01d': '☀️',   # clear sky day (but we'll warn about UV!)
    '01n': '🌙',   # clear sky night (lonely darkness)
    '02d': '🌤️',   # few clouds day (false hope)
    '02n': '🌙',   # few clouds night (obscured moon)
    '03d': '☁️',   # scattered clouds (gathering gloom)
    '03n': '☁️',   # scattered clouds (night terrors)
    '04d': '☁️',   # broken clouds (shattered sky)
    '04n': '☁️',   # broken clouds (endless gray)
    '09d': '🌧️',   # shower rain (infrastructure damage)
    '09n': '🌧️',   # shower rain (sleepless nights)
    '10d': '🌦️',   # rain day (mixed misery)
    '10n': '🌧️',   # rain night (flooding risks)
    '11d': '⛈️',   # thunderstorm (atmospheric violence)
    '11n': '⛈️',   # thunderstorm (terror from above)
    '13d': '🌨️',   # snow (transportation chaos)
    '13n': '🌨️',   # snow (hypothermia risk)
    '50d': '🌫️',   # mist (visibility hazard)
    '50n': '🌫️',   # mist (accident conditions)
}

# =================================
# 6. PESSIMISTIC TEMPERATURE DIFFERENCE COLORS
# =================================
PESSIMISTIC_TEMPERATURE_DIFFERENCE_COLORS = {
    'significant_warmer': '#8B0000',  # Dark red for warmer (heat stroke risk)
    'slight_warmer': '#DC143C',       # Crimson for slightly warmer (discomfort)
    'significant_cooler': '#000080',  # Navy for cooler (hypothermia zone)
    'slight_cooler': '#4169E1',      # Royal blue for slightly cooler (joint pain)
    'comfortable_range': '#228B22'    # Forest green for comfortable (temporary relief)
}

# =================================
# 7. PESSIMISTIC COMFORT THRESHOLDS
# =================================
PESSIMISTIC_COMFORT_THRESHOLDS = {
    'poor': (0, 30),       # Suffering zone
    'fair': (30, 50),      # Barely tolerable
    'good': (50, 70),      # Temporary reprieve
    'very_good': (70, 85), # False security
    'excellent': (85, 100) # Deceptive comfort
}

# =================================
# 8. PESSIMISTIC METRIC COLORS
# =================================
PESSIMISTIC_METRIC_COLORS = {
    'temperature': {
        'ranges': [
            (-20, '#000080'),      # Navy for extreme cold (death zone)
            (-10, '#0000CD'),      # Medium blue (frostbite risk)
            (5, '#4169E1'),        # Royal blue (hypothermia warning)
            (15, '#FF4500'),       # Orange red (false comfort)
            (25, '#DC143C'),       # Crimson (heat stress begins)
            (35, '#8B0000'),       # Dark red (dangerous heat)
            (45, '#4B0082')        # Indigo (organ failure zone)
        ],
        'unit_dependent': True,
        'imperial_ranges': [
            (-10, '#000080'),      # Death cold
            (15, '#0000CD'),       # Dangerous cold
            (40, '#4169E1'),       # Uncomfortable cold
            (60, '#FF4500'),       # Deceptive comfort
            (80, '#DC143C'),       # Heat stress
            (95, '#8B0000'),       # Dangerous heat
            (110, '#4B0082')       # Lethal heat
        ]
    },
    'humidity': {
        'ranges': [
            (0, '#FF4500'),        # Orange red (desert dehydration)
            (20, '#DC143C'),       # Crimson (respiratory stress)
            (40, '#8B0000'),       # Dark red (discomfort begins)
            (70, '#4B0082'),       # Indigo (oppressive moisture)
            (85, '#000080'),       # Navy (mold growth conditions)
            (100, '#000000')       # Black (suffocating saturation)
        ],
        'unit_dependent': False
    },
    'wind_speed': {
        'ranges': [
            (0, '#2F4F4F'),        # Dark slate gray (stagnant air toxicity)
            (5, '#696969'),        # Dim gray (minimal circulation)
            (15, '#FF4500'),       # Orange red (debris hazard begins)
            (25, '#DC143C'),       # Crimson (structural stress)
            (35, '#8B0000')        # Dark red (catastrophic winds)
        ],
        'unit_dependent': True,
        'imperial_ranges': [
            (0, '#2F4F4F'),        # Stagnant danger
            (10, '#696969'),       # Weak circulation
            (25, '#FF4500'),       # Hazardous winds
            (40, '#DC143C'),       # Destructive force
            (60, '#8B0000')        # Catastrophic damage
        ]
    },
    'pressure': {
        'ranges': [
            (980, '#8B0000'),      # Dark red (storm system approach)
            (1000, '#DC143C'),     # Crimson (barometric instability)
            (1013, '#FF4500'),     # Orange red (deceptive normalcy)
            (1030, '#4B0082'),     # Indigo (oppressive high pressure)
            (1050, '#000080')      # Navy (atmospheric anomaly)
        ],
        'unit_dependent': True,
        'imperial_ranges': [
            (28.9, '#8B0000'),     # Storm approach
            (29.5, '#DC143C'),     # Pressure instability
            (29.9, '#FF4500'),     # False stability
            (30.4, '#4B0082'),     # Oppressive pressure
            (31.0, '#000080')      # Atmospheric anomaly
        ]
    },
    'weather_comfort_score': {
        'ranges': [
            (0, '#8B0000'),        # Dark red (survival mode)
            (30, '#DC143C'),       # Crimson (endurance test)
            (60, '#FF4500'),       # Orange red (temporary relief)
            (80, '#4B0082'),       # Indigo (false security)
            (95, '#000080')        # Navy (deceptive comfort)
        ],
        'unit_dependent': False
    }
}

# =================================
# 9. PESSIMISTIC DIALOG CONFIG
# =================================
PESSIMISTIC_DIALOG_CONFIG = {
    'error_titles': {
        'city_not_found': '🚫 LOCATION QUERY FAILURE',
        'rate_limit': '⏰ SYSTEM RESOURCE EXHAUSTION',
        'network_issue': '📡 COMMUNICATION BREAKDOWN', 
        'input_error': '❌ USER INPUT MALFUNCTION',
        'general_error': '💀 SYSTEM DEGRADATION EVENT',
        'notice': '⚠️ MANDATORY SYSTEM ALERT'
    },
    'dialog_types': {
        'error': 'showerror',     # Errors are serious business
        'warning': 'showerror',   # Warnings are basically errors
        'info': 'showwarning'     # Even info is concerning
    }
}