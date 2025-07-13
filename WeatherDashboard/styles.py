"""
Style configuration for GUI elements.

This module provides centralized styling configuration for all tkinter
GUI components in the Weather Dashboard. Defines fonts, colors, padding,
and visual appearance settings for consistent UI theming.

Functions:
    configure_styles: Apply comprehensive styling to all GUI components
"""

from tkinter import ttk


# =================================
# 1. TTK STYLE CONFIGURATION
# =================================
def configure_styles() -> None:
    """Configure comprehensive styles for all GUI elements.
    
    Applies consistent styling including fonts, colors, padding, and
    visual effects to labels, buttons, frames, notebooks, and other
    tkinter components throughout the application.
    """
    style = ttk.Style()
    style.configure("FrameLabel.TLabelframe.Label", font=('Arial', 15, 'bold'))
    style.configure("LabelName.TLabel", font=('Arial', 10, 'bold'))
    style.configure("LabelValue.TLabel", font=('Arial', 10))
    style.configure("MainButton.TButton", font=('Arial', 10, 'bold'), padding=5)
    style.configure("Title.TLabel", font=('Comic Sans MS', 20, 'bold'))
    style.configure("AlertTitle.TLabel", font=('Arial', 14, 'bold'))
    style.configure("AlertText.TLabel", font=('Arial', 9, 'bold'))
    
    style.configure("TNotebook", background="lightgray")
    style.configure("TNotebook.Tab", padding=[12, 8], font=("Arial", 12, "bold"))
    style.map("TNotebook.Tab",
             background=[("selected", "lightblue"), ("active", "lightgreen")],
             foreground=[("selected", "darkblue"), ("active", "darkgreen")])


# =================================
# 2. LAYOUT & POSITIONING
# =================================
# Widget sizing and positioning configuration
WIDGET_LAYOUT = {
    'alert_popup': {
        'width': 400,
        'base_height': 100,
        'alert_height': 80,
        'max_height': 500
    },
    'comfort_progress_bar': {
        'width': 120,
        'height': 15,
        'border_width': 1
    },
    'alert_badge': {
        'position': {'relx': 1.0, 'rely': 0, 'anchor': "ne", 'x': -2, 'y': 2}
    },
    'alert_status': {
        'default_font': ("Arial", 12),
        'message_wrap_length': 350
    }
}

CONTROL_PANEL_CONFIG = {
    'padding': {
        'standard': 5,
        'button_group': (10, 5),
        'checkbox': (10, 0),
        'header': (5, 10)
    },
    'spacing': {
        'group': (10, 2),
        'header': (10, 2),
        'section': 1
    }
}

STATUS_BAR_CONFIG = {
    'padding': {'system': 5, 'progress': 10, 'data': 5, 'separator': 5},
    'colors': {
        'info': 'green',
        'warning': 'orange', 
        'error': 'red',
        'loading': 'blue'
    }
}


# =================================
# 3. ALERT SYSTEM STYLING
# =================================
# Alert display styling configuration
ALERT_DISPLAY_CONFIG = {
    'badge_font': ("Arial", 8),
    'badge_size': {'width': 2, 'height': 1},
    'badge_border': {'relief': "solid", 'borderwidth': 1},
    'column_padding': {'right_section': (20, 0), 'left_section': (0, 0)},
    'alert_text_padding': {'padx': 5, 'pady': 2},
    'alert_text_border': {'relief': "raised", 'borderwidth': 1},
    'fallback_icon': '⚠️',
    'animation_settings': {
        'pulse_colors': ['red', 'darkred', 'red'],
        'flash_interval': 500
    }
}

# Alert severity visual styling
ALERT_SEVERITY_COLORS = {
    'warning': {
        'color': 'darkred',
        'background': '#ffe6e6',  # Light red background
        'icon': '⚠️',
        'border': 'red'
    },
    'caution': {
        'color': 'darkorange', 
        'background': '#fff3e6',  # Light orange background
        'icon': '🔶',
        'border': 'orange'
    },
    'watch': {
        'color': 'darkblue',
        'background': '#e6f3ff',  # Light blue background  
        'icon': '👁️',
        'border': 'blue'
    }
}


# =================================
# 4. WEATHER DISPLAY STYLING
# =================================
# Icon selection for display
WEATHER_ICONS = {
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

# Color ranges for visual metric indicators
METRIC_COLOR_RANGES = {
    'temperature': {
        'ranges': [
            (-20, 'navy'),        # Changed from 'darkblue'
            (-10, 'blue'),        
            (5, 'steelblue'),     # Changed from 'lightblue' 
            (15, 'green'),        
            (25, 'orange'),       
            (35, 'red'),          
            (45, 'darkred')       
        ],
        'unit_dependent': True,
        'imperial_ranges': [
            (-10, 'navy'),        # Changed from 'darkblue'
            (15, 'blue'),         
            (40, 'steelblue'),    # Changed from 'lightblue'
            (60, 'green'),        
            (80, 'orange'),       
            (95, 'red'),          
            (110, 'darkred')      
        ]
    },
    'humidity': {
        'ranges': [
            (0, 'orange'),        
            (20, 'goldenrod'),    # Changed from 'yellow'
            (40, 'green'),        
            (70, 'steelblue'),    # Changed from 'lightblue'
            (85, 'blue'),         
            (100, 'navy')         # Changed from 'darkblue'
        ],
        'unit_dependent': False
    },
    'wind_speed': {
        'ranges': [
            (0, 'darkslategray'),       # Changed from 'gray'
            (5, 'green'),         
            (15, 'goldenrod'),    # Changed from 'yellow'
            (25, 'orange'),       
            (35, 'red')           
        ],
        'unit_dependent': True,
        'imperial_ranges': [
            (0, 'darkslategray'),       # Changed from 'gray'
            (10, 'green'),        
            (25, 'goldenrod'),    # Changed from 'yellow'
            (40, 'orange'),       
            (60, 'red')           
        ]
    },
    'pressure': {
        'ranges': [
            (980, 'red'),         
            (1000, 'orange'),     
            (1013, 'green'),      
            (1030, 'steelblue'),  # Changed from 'lightblue'
            (1050, 'blue')        
        ],
        'unit_dependent': True,
        'imperial_ranges': [
            (28.9, 'red'),        
            (29.5, 'orange'),     
            (29.9, 'green'),      
            (30.4, 'steelblue'),  # Changed from 'lightblue'
            (31.0, 'blue')        
        ]
    },
    'weather_comfort_score': {
        'ranges': [
            (0, 'red'),           
            (30, 'orange'),       
            (60, 'goldenrod'),    # Changed from 'yellow'
            (80, 'forestgreen'),  # Changed from 'lightgreen'
            (95, 'green')         
        ],
        'unit_dependent': False
    }
}

TEMPERATURE_DIFFERENCE_COLORS = {
    'significant_warmer': 'darkorange',   # Feels much warmer
    'slight_warmer': 'orange',           # Feels slightly warmer  
    'significant_cooler': 'steelblue',   # Feels much cooler
    'slight_cooler': 'lightblue',        # Feels slightly cooler
    'comfortable_range': 'green'         # Temperature in ideal range
}

# Comfort score thresholds for progress bar styling
COMFORT_THRESHOLDS = {
    'poor': (0, 30),       # Red zone
    'fair': (30, 50),      # Orange zone  
    'good': (50, 70),      # Yellow zone
    'very_good': (70, 85), # Light green zone
    'excellent': (85, 100) # Green zone
}