"""
Style configuration for GUI elements.

This module provides centralized styling configuration for all tkinter
GUI components in the Weather Dashboard. Defines fonts, colors, padding,
visual appearance settings, alert definitions, metric color ranges, and
weather icon mappings for consistent UI theming.

Contains comprehensive styling definitions including TTK styles, layout
configurations, alert severity styling, weather icon mappings, and metric
color determination ranges. Serves as the foundation for the future
satirical theme system.

Functions:
    configure_styles: Apply comprehensive styling to all GUI components
"""

from tkinter import ttk

# centralizing style info
from .alert_config import ALERT_DEFINITIONS, ALERT_SEVERITY_COLORS, ALERT_DISPLAY_CONFIG


# =================================
# 1. THEME CONSTANTS
# =================================
# Font definitions
FONTS = {
    'default_family': 'Arial',
    'title_family': 'Comic Sans MS',
    'sizes': {
        'small': 8,
        'normal': 10,
        'medium': 12,
        'large': 15,
        'title': 20
    },
    'weights': {
        'normal': 'normal',
        'bold': 'bold'
    }
}

# Color palette
COLORS = {
    'status': {
        'success': 'green',
        'warning': 'orange',
        'error': 'red',
        'info': 'blue',
        'neutral': 'gray',
        'default': 'black'
    },
    'backgrounds': {
        'inactive': 'lightgray',
        'selected': 'lightblue',
        'active': 'lightgreen'
    },
    'foregrounds': {
        'inactive': 'gray',
        'selected': 'darkblue',
        'active': 'darkgreen'
    }
}

# =================================
# 2. LAYOUT CONSTANTS  
# =================================
PADDING = {
    'none': 0,
    'micro': 1,
    'tiny': 2,
    'small': 5,
    'medium': 8,
    'large': 10,
    'extra_large': 12
}

DIMENSIONS = {
    'alert': {
        'width': 400,
        'base_height': 100,
        'item_height': 80,
        'max_height': 500
    },
    'progress_bar': {
        'width': 120,
        'height': 15,
        'border_width': 1
    }
}

# =================================
# 3. TTK STYLE CONFIGURATION
# =================================
def configure_styles() -> None:
    """Configure comprehensive styles for all GUI elements.
    
    IMPORTANT: Must be called after tkinter root window creation but before
    creating any styled widgets. Modifies the global TTK style registry.
    
    Side Effects:
        - Modifies global ttk.Style() settings for the entire application
        - Changes appearance of all TTK widgets created after this call
        - Should only be called once during application initialization
    
    Configured Elements:
        - Label styles (frame labels, values, names, titles, alerts)
        - Button styles (main buttons with padding and fonts)
        - Notebook styles (tabs with hover and selection effects)
        - Status styles (system, data, and progress indicators)
        - Specialized styles (gray labels, alert text)
    """
    style = ttk.Style()
    style.configure("Title.TLabel", font=(FONTS['title_family'], FONTS['sizes']['title'], FONTS['weights']['bold']))
    style.configure("FrameLabel.TLabelframe.Label", font=(FONTS['default_family'], FONTS['sizes']['large'], FONTS['weights']['bold']))

    style.configure("TNotebook", background=COLORS['backgrounds']['inactive'])
    style.configure("TNotebook.Tab", font=(FONTS['default_family'], FONTS['sizes']['medium'], FONTS['weights']['bold']), padding=[PADDING['tiny'],PADDING['medium']])
    style.map("TNotebook.Tab",
             background=[("selected", COLORS['backgrounds']['selected']), ("active", COLORS['backgrounds']['active'])],
             foreground=[("selected", COLORS['foregrounds']['selected']), ("active", COLORS['foregrounds']['active'])])
 
    style.configure("LabelName.TLabel", font=(FONTS['default_family'], FONTS['sizes']['normal'], FONTS['weights']['bold']))
    style.configure("LabelValue.TLabel", font=(FONTS['default_family'], FONTS['sizes']['normal'], FONTS['weights']['normal']))

    style.configure("MainButton.TButton", font=(FONTS['default_family'], FONTS['sizes']['normal'], FONTS['weights']['bold']), padding=PADDING['small'])
    
    style.configure("AlertTitle.TLabel", font=(FONTS['default_family'], FONTS['sizes']['large'], FONTS['weights']['bold']))
    style.configure("AlertText.TLabel", font=(FONTS['default_family'], FONTS['sizes']['normal'], FONTS['weights']['bold']))
    style.configure("GrayLabel.TLabel", font=(FONTS['default_family'], FONTS['sizes']['normal'], FONTS['weights']['normal']), foreground=COLORS['foregrounds']['inactive'])
    
    # System status styles for different states
    style.configure("SystemStatusReady.TLabel", font=(FONTS['default_family'], FONTS['sizes']['normal'], FONTS['weights']['normal']))
    style.configure("SystemStatusWarning.TLabel", font=(FONTS['default_family'], FONTS['sizes']['normal'], FONTS['weights']['normal']))
    style.configure("SystemStatusError.TLabel", font=(FONTS['default_family'], FONTS['sizes']['normal'], FONTS['weights']['normal']))

    style.map("SystemStatusReady.TLabel", foreground=[('!disabled', COLORS['status']['success'])])
    style.map("SystemStatusWarning.TLabel", foreground=[('!disabled', COLORS['status']['warning'])])
    style.map("SystemStatusError.TLabel", foreground=[('!disabled', COLORS['status']['error'])])

    # Data status styles  
    style.configure("DataStatusLive.TLabel", font=(FONTS['default_family'], FONTS['sizes']['normal'], FONTS['weights']['normal']))
    style.configure("DataStatusSimulated.TLabel", font=(FONTS['default_family'], FONTS['sizes']['normal'], FONTS['weights']['normal']))
    style.configure("DataStatusNone.TLabel", font=(FONTS['default_family'], FONTS['sizes']['normal'], FONTS['weights']['normal']))

    style.map("DataStatusLive.TLabel", foreground=[('!disabled', COLORS['status']['success'])])
    style.map("DataStatusSimulated.TLabel", foreground=[('!disabled', COLORS['status']['warning'])])
    style.map("DataStatusNone.TLabel", foreground=[('!disabled', COLORS['status']['neutral'])])


# =================================
# 4. WIDGET LAYOUT & CONFIG
# =================================
# Small widget sizing and positioning configuration
WIDGET_LAYOUT = {
    'alert_popup': {
        'width': DIMENSIONS['alert']['width'],
        'base_height': DIMENSIONS['alert']['base_height'],
        'alert_height': DIMENSIONS['alert']['item_height'],
        'max_height': DIMENSIONS['alert']['max_height']
    },
    'comfort_progress_bar': {
        'width': DIMENSIONS['progress_bar']['width'],
        'height': DIMENSIONS['progress_bar']['height'],
        'border_width': DIMENSIONS['progress_bar']['border_width']
    },
    'alert_badge': {
        'position': {'relx': 1.0, 'rely': 0, 'anchor': "ne", 'x': -2, 'y': 2}
    },
    'alert_status': {
        'default_font': (FONTS['default_family'], FONTS['sizes']['medium']),
        'message_wrap_length': 350
    }
}

CONTROL_PANEL_CONFIG = {
    'padding': {
        'standard': PADDING['small'],
        'button_group': (PADDING['large'], PADDING['small']),
        'checkbox': (PADDING['large'], PADDING['none']),
        'header': (PADDING['small'], PADDING['large'])
    },
    'spacing': {
        'group': (PADDING['large'], PADDING['tiny']),
        'header': (PADDING['large'], PADDING['tiny']),
        'section': PADDING['micro']
    }
}

STATUS_BAR_CONFIG = {
    'padding': {'system': PADDING['small'], 'progress': PADDING['large'], 'data': PADDING['small'], 'separator': PADDING['small']},
    'colors': {
        'info': COLORS['status']['success'],
        'warning': COLORS['status']['warning'], 
        'error': COLORS['status']['error'],
        'loading': COLORS['status']['info']
    }
}

LOADING_CONFIG = {
    'icons': {
        'progress': '🔄',
        'waiting': '⏳'
    },
    'colors': {
        'loading': COLORS['status']['info'],
        'default': COLORS['status']['default']
    },
    'messages': {
        'default': 'Fetching weather data...',
        'initializing': 'Initializing...',
        'validating': 'Validating input...',
        'processing': 'Processing weather data...'
    }
}

# =================================
# 5. WEATHER DISPLAY STYLING
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
    'significant_warmer': 'darkorange',  # Feels much warmer
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

# =================================
# 6. DIALOG SYSTEM STYLING
# =================================
DIALOG_CONFIG = {
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