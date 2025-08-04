"""
Alert system configuration for Weather Dashboard.

Centralized alert definitions, thresholds, severity ordering, visual styling, and validation logic.
This module provides a single source of truth for all alert-related configuration and validation.

Alert Types Supported:
    Temperature: High/low temperature warnings, heat index, wind chill
    Wind: High wind speed warnings with escalating severity
    Atmospheric: Low pressure system detection
    Humidity: High/low humidity discomfort alerts
    Precipitation: Heavy rain and snow warnings
    Visibility: Low visibility/fog conditions
    Air Quality: UV index and air quality index warnings
    
Severity Levels: warning (red), caution (orange), watch (blue)
"""

# Alert Threshold Configuration (all in metric units internally)
ALERT_THRESHOLDS = {
    # Temperature alerts
    'temperature_high': 35.0,      # °C = 95°F - Hot weather warning
    'temperature_low': -10.0,      # °C = 14°F - Cold weather warning  
    'heat_index_high': 40.5,       # °C = 105°F - Dangerous heat index
    'wind_chill_low': -28.9,       # °C = -20°F - Dangerous wind chill

    # Wind alerts
    'wind_speed_high': 15.0,       # m/s = ~34 mph - High wind warning

    # Pressure alerts
    'pressure_low': 980.0,         # hPa - Storm system warning

    # Humidity alerts
    'humidity_high': 85.0,         # % - High humidity discomfort
    'humidity_low': 15.0,          # % - Low humidity warning

    # Precipitation alerts
    'heavy_rain_threshold': 10.0,     # mm/hour - Heavy rain warning
    'heavy_snow_threshold': 5.0,      # mm/hour - Heavy snow warning

    # Visibility alerts
    'low_visibility_threshold': 3000,    # meters = 1.86 miles - Poor visibility

    # Air quality and UV alerts
    'uv_index_high': 8,               # Index - Very high UV exposure
    'air_quality_poor': 4,            # AQI - Poor air quality warning
    'comfort_score_low': 30,          # Score - Uncomfortable conditions
}

# Alert priority for display ordering
ALERT_PRIORITY_ORDER = ['warning', 'caution', 'watch']

# Alert definitions with complete configuration
ALERT_DEFINITIONS = {
    'temperature_high': {
        'threshold_key': 'temperature_high',
        'check_function': lambda val, thresh: val > thresh,
        'severity_function': lambda val, thresh: 'warning',
        'icon': '🔥',
        'title': 'High Temperature Alert',
        'message_template': 'Temperature is very high: {value:.1f}{unit} (threshold: {threshold:.1f}{unit})',
        'unit_type': 'temperature'
    },
    'temperature_low': {
        'threshold_key': 'temperature_low',
        'check_function': lambda val, thresh: val < thresh,
        'severity_function': lambda val, thresh: 'warning', 
        'icon': '🥶',
        'title': 'Low Temperature Alert',
        'message_template': 'Temperature is very low: {value:.1f}{unit} (threshold: {threshold:.1f}{unit})',
        'unit_type': 'temperature'
    },
    'wind_speed_high': {
        'threshold_key': 'wind_speed_high',
        'check_function': lambda val, thresh: val > thresh,
        'severity_function': lambda val, thresh: 'warning' if val > thresh * 1.5 else 'caution',
        'icon': '💨',
        'title': 'High Wind Alert', 
        'message_template': 'Strong winds detected: {value:.1f} {unit} (threshold: {threshold:.1f} {unit})',
        'unit_type': 'wind_speed'
    },
    'pressure_low': {
        'threshold_key': 'pressure_low',
        'check_function': lambda val, thresh: val < thresh,
        'severity_function': lambda val, thresh: 'watch',
        'icon': '⛈️',
        'title': 'Low Pressure Alert',
        'message_template': 'Low pressure system detected: {value:.1f} {unit} (threshold: {threshold:.1f} {unit})',
        'unit_type': 'pressure'
    },
    'humidity_high': {
        'threshold_key': 'humidity_high',
        'check_function': lambda val, thresh: val > thresh,
        'severity_function': lambda val, thresh: 'caution',
        'icon': '💧',
        'title': 'High Humidity Alert',
        'message_template': 'Very humid conditions: {value:.0f}% (threshold: {threshold:.0f}%)',
        'unit_type': 'humidity'
    },
    'humidity_low': {
        'threshold_key': 'humidity_low',
        'check_function': lambda val, thresh: val < thresh,
        'severity_function': lambda val, thresh: 'caution',
        'icon': '🏜️',
        'title': 'Low Humidity Alert',
        'message_template': 'Very dry conditions: {value:.0f}% (threshold: {threshold:.0f}%)',
        'unit_type': 'humidity'
    },
    'heavy_rain': {
        'threshold_key': 'heavy_rain_threshold',
        'check_function': lambda val, thresh: val > thresh,
        'severity_function': lambda val, thresh: 'warning',
        'icon': '🌧️',
        'title': 'Heavy Rain Alert',
        'message_template': 'Heavy rainfall detected: {value:.1f} {unit}/hour (threshold: {threshold:.1f} {unit})',
        'unit_type': 'rain'
    },
    'heavy_snow': {
        'threshold_key': 'heavy_snow_threshold',
        'check_function': lambda val, thresh: val > thresh,
        'severity_function': lambda val, thresh: 'warning',
        'icon': '🌨️',
        'title': 'Heavy Snow Alert',
        'message_template': 'Heavy snowfall detected: {value:.1f} {unit}/hour (threshold: {threshold:.1f} {unit})',
        'unit_type': 'snow'
    },
    'low_visibility': {
        'threshold_key': 'low_visibility_threshold',
        'check_function': lambda val, thresh: val < thresh,
        'severity_function': lambda val, thresh: 'caution',
        'icon': '🌫️',
        'title': 'Low Visibility Alert',
        'message_template': 'Reduced visibility: {value:.1f} {unit} (threshold: {threshold:.1f} {unit})',
        'unit_type': 'visibility'
    },
    'heat_index_high': {
        'threshold_key': 'heat_index_high',
        'check_function': lambda val, thresh: val > thresh,
        'severity_function': lambda val, thresh: 'warning',
        'icon': '🔥',
        'title': 'Dangerous Heat Index',
        'message_template': 'Heat index is dangerously high: {value:.1f}{unit} (threshold: {threshold:.1f}{unit})',
        'unit_type': 'heat_index'
    },
    'wind_chill_low': {
        'threshold_key': 'wind_chill_low',
        'check_function': lambda val, thresh: val < thresh,
        'severity_function': lambda val, thresh: 'warning',
        'icon': '🥶',
        'title': 'Dangerous Wind Chill',
        'message_template': 'Wind chill is dangerously low: {value:.1f}{unit} (threshold: {threshold:.1f}{unit})',
        'unit_type': 'wind_chill'
    },
    'uv_index_high': {
        'threshold_key': 'uv_index_high',
        'check_function': lambda val, thresh: val > thresh,
        'severity_function': lambda val, thresh: 'caution',
        'icon': '☀️',
        'title': 'High UV Index Alert',
        'message_template': 'Very high UV exposure: {value:.0f} (threshold: {threshold:.0f})',
        'unit_type': 'uv_index'
    },
    'air_quality_poor': {
        'threshold_key': 'air_quality_poor',
        'check_function': lambda val, thresh: val >= thresh,
        'severity_function': lambda val, thresh: 'warning' if val == 5 else 'caution',
        'icon': '😷',
        'title': 'Poor Air Quality Alert',
        'message_template': 'Air quality is poor: AQI {value:.0f} (threshold: AQI {threshold:.0f})',
        'unit_type': 'air_quality_index'
    }
}

# Alert severity visual styling - Now delegates to theme manager
def get_alert_severity_colors():
    """Get alert severity colors from theme manager."""
    from WeatherDashboard.features.themes.theme_manager import theme_manager
    theme_config = theme_manager.get_theme_config()
    return theme_config.get('alert_severity_colors', {})

# Alert display styling configuration - Now delegates to theme manager
def get_alert_display_config():
    """Get alert display configuration from theme manager."""
    from WeatherDashboard.features.themes.theme_manager import theme_manager
    theme_config = theme_manager.get_theme_config()
    fonts = theme_config.get('fonts', {})
    
    return {
        'badge_font': (fonts.get('default_family', 'Arial'), fonts.get('sizes', {}).get('small', 8)),
        'badge_size': {'width': 2, 'height': 1},
        'badge_border': {'relief': "solid", 'borderwidth': 1},
        'column_padding': {'right_section': (20, 0), 'left_section': (0, 0)},
        'alert_text_padding': {'padx': 5, 'pady': 2},
        'alert_text_border': {'relief': "raised", 'borderwidth': 1},
        'fallback_icon': '⚠️',
        'animation_settings': {
            'pulse_colors': [theme_config['colors']['error'], theme_config['colors']['warning'], theme_config['colors']['error']],
            'flash_interval': 500,
            'fade_duration': 200
        }
    }

# Legacy constants for backward compatibility
ALERT_SEVERITY_COLORS = get_alert_severity_colors()
ALERT_DISPLAY_CONFIG = get_alert_display_config()

# # Alert severity visual styling
# ALERT_SEVERITY_COLORS = {
#     'warning': {
#         'color': 'darkred',
#         'background': '#ffe6e6',  # Light red background
#         'icon': '⚠️',
#         'border': 'red'
#     },
#     'caution': {
#         'color': 'darkorange', 
#         'background': '#fff3e6',  # Light orange background
#         'icon': '🔶',
#         'border': 'orange'
#     },
#     'watch': {
#         'color': 'darkblue',
#         'background': '#e6f3ff',  # Light blue background  
#         'icon': '👁️',
#         'border': 'blue'
#     }
# }

# # Alert display styling configuration
# ALERT_DISPLAY_CONFIG = {
#     'badge_font': ("Arial", 8),
#     'badge_size': {'width': 2, 'height': 1},
#     'badge_border': {'relief': "solid", 'borderwidth': 1},
#     'column_padding': {'right_section': (20, 0), 'left_section': (0, 0)},
#     'alert_text_padding': {'padx': 5, 'pady': 2},
#     'alert_text_border': {'relief': "raised", 'borderwidth': 1},
#     'fallback_icon': '⚠️',
#     'animation_settings': {
#         'pulse_colors': ['red', 'darkred', 'red'], # Red pulse sequence
#         'flash_interval': 500,    # Milliseconds between color changes
#         'fade_duration': 200      # Milliseconds for fade transitions
#     }
# }

# Alert Configuration Validation
def validate_alert_config() -> None:
    """
    Validate alert configuration for consistency and completeness.

    Raises:
        ValueError: If any alert definition is missing required fields, thresholds, or has invalid severity.
    
    Returns:
        bool: True if configuration is valid.
    """    
    # Check all alert definitions have corresponding thresholds
    for alert_type, definition in ALERT_DEFINITIONS.items():
        threshold_key = definition.get('threshold_key')
        if threshold_key not in ALERT_THRESHOLDS:
            raise ValueError(f"Missing threshold for alert type '{alert_type}': {threshold_key}")
    
    # Validate severity levels exist
    valid_severities = set(ALERT_SEVERITY_COLORS.keys()) - {'clear'}
    for alert_type, definition in ALERT_DEFINITIONS.items():
        severity = definition.get('severity')
        if severity and severity not in valid_severities:
            raise ValueError(f"Invalid severity '{severity}' for alert type '{alert_type}'")
    
    # Validate required fields
    required_fields = ['threshold_key', 'check_function', 'icon', 'title', 'message_template', 'unit_type']
    for alert_type, definition in ALERT_DEFINITIONS.items():
        for field in required_fields:
            if field not in definition:
                raise ValueError(f"Missing required field '{field}' in alert definition '{alert_type}'")
              
    return True