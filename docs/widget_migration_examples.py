"""
Examples showing how to migrate widgets to use the new ThemeManager.
These examples show the before/after patterns for common widget usage.
"""

# ==========================================
# 1. MIGRATING BASIC WIDGET CLASSES
# ==========================================

# BEFORE (control_widgets.py) - Complex style references
"""
from WeatherDashboard import config, styles
from WeatherDashboard.utils.state_utils import StateUtils
from WeatherDashboard.utils.widget_utils import WidgetUtils

class ControlWidgets(BaseWidgetManager):
    def __init__(self, parent_frame: ttk.Frame, state: Any, callbacks: Dict[str, Callable]):
        # Multiple imports and complex style access
        self.logger = Logger()
        self.config = config
        self.styles = styles  # Complex nested access required
        self.state_utils = StateUtils()
        self.widget_utils = WidgetUtils()
        
    def _create_city_input(self) -> None:
        # Complex style path access
        pady = self.styles.CONTROL_PANEL_CONFIG['padding']['standard']
        # Rest of implementation...
"""

# AFTER - Clean theme manager usage
from WeatherDashboard.features.themes.theme_manager import theme_manager
from WeatherDashboard.widgets.base_widgets import BaseWidgetManager, SafeWidgetCreator

class ModernControlWidgets(BaseWidgetManager):
    """Updated control widgets using theme manager."""
    
    def __init__(self, parent_frame: ttk.Frame, state: Any, callbacks: Dict[str, Callable]):
        # Single theme manager access
        self.theme = theme_manager
        self.parent_frame = parent_frame
        self.state = state
        self.callbacks = callbacks
        
        super().__init__(parent_frame, state, "control widgets")
        
        if not self.safe_create_widgets():
            self.logger.warn("Control widgets created with errors")
    
    def _create_city_input(self) -> None:
        """Clean theme-aware city input creation."""
        # Simple, clean access to styling
        pady = self.theme.get_control_config('padding')['standard']
        
        city_label = SafeWidgetCreator.create_label(
            self.parent, 
            text="City:", 
            style="LabelName.TLabel"
        )
        
        self.city_entry = SafeWidgetCreator.create_entry(
            self.parent, 
            textvariable=self.state.city
        )
        
        # Clean positioning
        city_label.grid(row=1, column=0, sticky=tk.W, pady=pady)
        self.city_entry.grid(row=1, column=1, sticky=tk.W, pady=pady)
    
    def _create_metric_visibility(self) -> None:
        """Updated metric visibility with theme awareness."""
        # Get theme-appropriate spacing
        header_padding = self.theme.get_control_config('padding')['header']
        checkbox_padding = self.theme.get_control_config('padding')['checkbox']
        
        # Header frame
        header_frame = SafeWidgetCreator.create_frame(self.parent)
        header_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=header_padding)
        
        visibility_label = SafeWidgetCreator.create_label(
            header_frame, 
            "Metrics Visibility:", 
            "LabelName.TLabel"
        )
        visibility_label.pack(side=tk.LEFT)
        
        # Theme-aware button spacing
        button_spacing = self.theme.get_control_config('padding')['button_group']
        
        select_all_btn = SafeWidgetCreator.create_button(
            header_frame, 
            "Select All", 
            self._select_all_metrics,
            "MainButton.TButton"
        )
        select_all_btn.pack(side=tk.LEFT, padx=button_spacing)


# ==========================================
# 2. MIGRATING STATUS AND ALERT WIDGETS  
# ==========================================

# BEFORE (status_bar_widgets.py) - Multiple style imports
"""
from WeatherDashboard import styles
from WeatherDashboard.utils.logger import Logger

class StatusBarWidgets(BaseWidgetManager):
    def __init__(self, parent_frame: ttk.Frame, state: Any):
        self.styles = styles
        self.logger = Logger()
        
    def update_progress(self, message: str = "", error: bool = False):
        if self.progress_var:
            self.progress_var.set(message)
        if self.progress_label:
            # Complex nested access
            color = (self.styles.STATUS_BAR_CONFIG['colors']['error'] if error 
                    else self.styles.STATUS_BAR_CONFIG['colors']['info'])
            self.progress_label.configure(foreground=color)
"""

# AFTER - Clean theme manager usage
from WeatherDashboard.features.themes.theme_manager import theme_manager

class ModernStatusBarWidgets(BaseWidgetManager):
    """Updated status bar using theme manager."""
    
    def __init__(self, parent_frame: ttk.Frame, state: Any):
        self.theme = theme_manager
        self.parent_frame = parent_frame
        self.state = state
        
        # Widget references
        self.system_status_label = None
        self.progress_label = None
        self.progress_var = tk.StringVar(value="")
        self.data_status_label = None
        
        super().__init__(parent_frame, state, "status bar widgets")
        
        if not self.safe_create_widgets():
            self.logger.warn("Status bar widgets created with errors")
    
    def _create_widgets(self) -> None:
        """Create status bar with theme-aware styling."""
        # Get theme-specific padding
        padding_config = self.theme.get_status_config('padding')
        
        # Left section: System status
        self.system_status_label = SafeWidgetCreator.create_label(
            self.parent, 
            "Ready", 
            "SystemStatus.TLabel"
        )
        self.system_status_label.pack(side=tk.LEFT, padx=padding_config['system'])
        
        # Separator
        ttk.Separator(self.parent, orient='vertical').pack(
            side=tk.LEFT, fill='y', padx=padding_config['separator']
        )
        
        # Center section: Progress
        self.progress_label = SafeWidgetCreator.create_label(
            self.parent, 
            "", 
            "LabelValue.TLabel", 
            textvariable=self.progress_var
        )
        self.progress_label.pack(side=tk.LEFT, padx=padding_config['progress'])
        
        # Right section: Data status
        self.data_status_label = SafeWidgetCreator.create_label(
            self.parent, 
            "No data", 
            "DataStatus.TLabel"
        )
        self.data_status_label.pack(side=tk.RIGHT, padx=padding_config['data'])
    
    def update_progress(self, message: str = "", error: bool = False) -> None:
        """Clean theme-aware progress updates."""
        if self.progress_var:
            self.progress_var.set(message)
        if self.progress_label:
            # Simple, clean color access
            color = self.theme.get_color('error', 'status') if error else self.theme.get_color('info', 'status')
            self.progress_label.configure(foreground=color)
    
    def update_system_status(self, message: str, status_type: str = "info") -> None:
        """Theme-aware system status updates."""
        if self.system_status_label:
            self.system_status_label.configure(text=message)
            
            # Clean theme-based style switching
            style_map = {
                "error": "SystemStatusError.TLabel",
                "warning": "SystemStatusWarning.TLabel", 
                "info": "SystemStatusReady.TLabel"
            }
            
            style = style_map.get(status_type, "SystemStatusReady.TLabel")
            self.system_status_label.configure(style=style)


# ==========================================
# 3. MIGRATING ALERT WIDGETS
# ==========================================

# BEFORE (alert_display.py) - Complex style access
"""
from WeatherDashboard import config, styles

class AlertStatusIndicator:
    def __init__(self, parent_frame: Any):
        self.config = config
        self.styles = styles  # Complex nested access
        
        self.status_label = tk.Label(
            self.status_frame,
            text="🔔",
            cursor="hand2",
            font=self.styles.WIDGET_LAYOUT['alert_status']['default_font']  # Deep nesting
        )
        
    def _start_pulse_animation(self):
        # Complex animation config access
        anim_config = self.styles.ALERT_DISPLAY_CONFIG['animation_settings']
        pulse_colors = anim_config['pulse_colors']
        interval = anim_config['flash_interval']
"""

# AFTER - Clean theme manager usage
from WeatherDashboard.features.themes.theme_manager import theme_manager

class ModernAlertStatusIndicator:
    """Updated alert indicator using theme manager."""
    
    def __init__(self, parent_frame: Any):
        self.theme = theme_manager
        self.parent = parent_frame
        
        # Get alert-specific configuration cleanly
        self.alert_config = self.theme.get_widget_config('alert_status')
        
        self._create_status_indicator()
    
    def _create_status_indicator(self) -> None:
        """Create indicator with theme-aware styling."""
        self.status_frame = ttk.Frame(self.parent)
        
        # Clean font access
        default_font = self.alert_config.get('default_font', self.theme.get_font())
        
        self.status_label = tk.Label(
            self.status_frame,
            text="🔔",
            cursor="hand2",
            font=default_font,
            foreground=self.theme.get_color('primary')
        )
        self.status_label.pack()
    
    def _start_pulse_animation(self) -> None:
        """Use clean animation configuration."""
        # Simple access to animation settings
        pulse_colors = ['red', 'darkred', 'red']  # Could be theme-configurable
        interval = 500  # Could be theme-configurable
        
        if not hasattr(self, '_animation_active'):
            self._animation_active = True
            self._animation_step = 0
            self._pulse_animation(pulse_colors, interval)
    
    def _pulse_animation(self, colors: list, interval: int) -> None:
        """Simplified animation with theme colors."""
        if not getattr(self, '_animation_active', False):
            return
        
        color = colors[self._animation_step % len(colors)]
        self.status_label.configure(foreground=color)
        self._animation_step += 1
        
        # Schedule next frame
        self._animation_job = self.status_label.after(interval, 
                                                     lambda: self._pulse_animation(colors, interval))


# ==========================================
# 4. MIGRATING ERROR HANDLER
# ==========================================

# BEFORE (error_handler.py) - Direct styles import
"""
from WeatherDashboard import styles

class WeatherErrorHandler:
    def __init__(self, theme: str = 'neutral'):
        self.styles = styles  # Direct import
        
    def handle_weather_error(self, error_exception: Optional[Exception], city_name: str) -> bool:
        # Complex nested access to dialog config
        getattr(messagebox, self.styles.DIALOG_CONFIG['dialog_types']['error'])(
            self.styles.DIALOG_CONFIG['error_titles']['city_not_found'], 
            message
        )
"""

# AFTER - Clean theme manager usage  
from WeatherDashboard.features.themes.theme_manager import theme_manager

class ModernWeatherErrorHandler:
    """Updated error handler using theme manager."""
    
    def __init__(self, theme: str = 'neutral'):
        self.theme = theme_manager
        
        # Set initial theme if different from current
        if theme != self.theme.get_theme_name():
            from WeatherDashboard.features.themes.theme_manager import Theme
            theme_map = {
                'neutral': Theme.NEUTRAL,
                'optimistic': Theme.OPTIMISTIC,
                'pessimistic': Theme.PESSIMISTIC
            }
            if theme in theme_map:
                self.theme.change_theme(theme_map[theme])
        
        # Theme-aware message templates
        self._message_templates = {
            'city_not_found': {
                'neutral': "City '{}' not found",
                'optimistic': "Let's try a different city! '{}' isn't available right now",
                'pessimistic': "'{}' does not exist in our records"
            },
            'rate_limit': {
                'neutral': "API rate limit exceeded. Using simulated data for '{}'",
                'optimistic': "Taking a quick break! Showing sample data for '{}' instead", 
                'pessimistic': "Request quota exhausted. Degraded service active for '{}'"
            },
            'network_error': {
                'neutral': "Network problem detected. Using simulated data for '{}'",
                'optimistic': "Connection hiccup! No worries, showing backup data for '{}'",
                'pessimistic': "Network failure. System compromised. Fallback data for '{}'"
            }
        }
    
    def set_theme(self, theme: str) -> None:
        """Update theme through theme manager."""
        from WeatherDashboard.features.themes.theme_manager import Theme
        theme_map = {
            'neutral': Theme.NEUTRAL,
            'optimistic': Theme.OPTIMISTIC,
            'pessimistic': Theme.PESSIMISTIC
        }
        if theme in theme_map:
            self.theme.change_theme(theme_map[theme])
    
    def handle_weather_error(self, error_exception: Optional[Exception], city_name: str) -> bool:
        """Handle errors with clean theme-aware dialogs."""
        if not error_exception:
            return True
            
        if isinstance(error_exception, ValidationError):
            messagebox.showerror("Input Error", str(error_exception))
            return False
        elif isinstance(error_exception, CityNotFoundError):
            # Clean access to dialog configuration
            message = self._format_message('city_not_found', city_name)
            dialog_type = self.theme.get_dialog_type('error')
            dialog_title = self.theme.get_dialog_title('city_not_found')
            
            getattr(messagebox, dialog_type)(dialog_title, message)
            return True
        elif isinstance(error_exception, RateLimitError):
            message = self._format_message('rate_limit', city_name)
            dialog_type = self.theme.get_dialog_type('error')
            dialog_title = self.theme.get_dialog_title('rate_limit')
            
            getattr(messagebox, dialog_type)(dialog_title, message)
            return True
        # ... other error types
    
    def _format_message(self, template_key: str, *args) -> str:
        """Format message based on current theme."""
        template = self._message_templates.get(template_key, {})
        current_theme = self.theme.get_theme_name()
        message_template = template.get(current_theme, template.get('neutral', '{}'))
        return message_template.format(*args)


# ==========================================
# 5. UPDATING MAIN STYLES.PY FOR COMPATIBILITY
# ==========================================

# WeatherDashboard/gui/styles.py - Updated for backward compatibility
"""
Updated styles.py that delegates to theme manager while maintaining compatibility.
"""

from WeatherDashboard.features.themes.theme_manager import (
    theme_manager, 
    configure_styles, 
    get_theme_config,
    Theme
)

# Backward compatibility - delegate to theme manager
def get_default_theme_values():
    """Get default theme values (backward compatibility)."""
    return theme_manager._theme_config.__dict__

# Legacy property accessors - these now delegate to theme manager
@property
def FONTS():
    return theme_manager._theme_config.fonts

@property  
def COLORS():
    return theme_manager._theme_config.colors

@property
def PADDING():
    return theme_manager._theme_config.ui['padding']

@property
def DIMENSIONS():
    return theme_manager._theme_config.ui['dimensions']

@property
def WIDGET_LAYOUT():
    return theme_manager._theme_config.ui['widget_layout']

@property
def CONTROL_PANEL_CONFIG():
    return theme_manager._theme_config.ui['control_panel_config']

@property
def STATUS_BAR_CONFIG():
    return theme_manager._theme_config.ui['status_bar_config']

@property
def LOADING_CONFIG():
    return theme_manager._theme_config.ui['loading_config']

@property
def WEATHER_ICONS():
    return theme_manager._theme_config.weather_icons

@property
def METRIC_COLOR_RANGES():
    return theme_manager._theme_config.metric_colors

@property
def TEMPERATURE_DIFFERENCE_COLORS():
    return theme_manager._theme_config.temperature_difference_colors

@property
def COMFORT_THRESHOLDS():
    return theme_manager._theme_config.comfort_thresholds

@property
def DIALOG_CONFIG():
    return theme_manager._theme_config.dialog_config

# For immediate backward compatibility, import everything from theme manager
from WeatherDashboard.features.themes.theme_manager import *


# ==========================================
# 6. USAGE IN COLOR_UTILS AND WIDGET_UTILS
# ==========================================

# WeatherDashboard/utils/color_utils.py - Updated
from WeatherDashboard.features.themes.theme_manager import theme_manager

class ColorUtils:
    """Updated color utils using theme manager."""
    
    def __init__(self):
        self.theme = theme_manager
    
    def get_metric_color(self, metric_key: str, value: Any, unit_system: str) -> str:
        """Clean metric color access."""
        if value is None:
            return "darkslategray"
        
        # Simple theme access
        color_config = self.theme.get_metric_colors(metric_key)
        if not color_config:
            return "darkslategray"
        
        # Choose appropriate ranges based on unit system
        if color_config.get('unit_dependent', False) and unit_system == 'imperial':
            ranges = color_config.get('imperial_ranges', color_config['ranges'])
        else:
            ranges = color_config['ranges']
        
        # Find appropriate color
        try:
            numeric_value = float(value)
            for threshold, color in ranges:
                if numeric_value <= threshold:
                    return color
            return ranges[-1][1]
        except (ValueError, TypeError):
            return "black"
    
    def get_enhanced_temperature_color(self, temp_text: str, unit_system: str) -> str:
        """Enhanced temperature colors using clean theme access."""
        if not temp_text or temp_text == "--":
            return "darkslategray"
        
        # Extract temperature and use metric color logic
        temp_match = re.search(r'^(-?\d+\.?\d*)', temp_text)
        if temp_match:
            actual_temp = float(temp_match.group())
            base_color = self.get_metric_color('temperature', actual_temp, unit_system)
            
            # Check for difference indicators using theme colors
            if 'feels' in temp_text:
                difference_match = re.search(r'feels (-?\d+\.?\d*)', temp_text)
                if difference_match:
                    feels_temp = float(difference_match.group(1))
                    difference = abs(feels_temp - actual_temp)
                    
                    threshold_large = 5.0 if unit_system == 'metric' else 9.0
                    
                    if '↑' in temp_text:  # Feels warmer
                        if difference >= threshold_large:
                            return self.theme.get_temperature_difference_color('significant_warmer')
                        else:
                            return self.theme.get_temperature_difference_color('slight_warmer')
                    elif '↓' in temp_text:  # Feels cooler
                        if difference >= threshold_large:
                            return self.theme.get_temperature_difference_color('significant_cooler')
                        else:
                            return self.theme.get_temperature_difference_color('slight_cooler')
            
            return base_color
        
        return "darkslategray"