"""
Basic alert display components.

This module provides UI components for displaying weather alerts including
status indicators, popup dialogs, and interactive alert management widgets.
Supports different alert severities and user interaction callbacks.

Classes:
    AlertStatusIndicator: Compact status indicator widget for alert display
    SimpleAlertPopup: Popup dialog for detailed alert information display
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Callable, Any

from WeatherDashboard import config, styles

from .alert_manager import WeatherAlert


class AlertStatusIndicator:
    """Compact weather alert status indicator widget.
    
    Provides a clickable status indicator that displays alert count and severity
    using icons and colors. Changes appearance based on active alerts and
    supports user interaction callbacks for detailed alert viewing.
    
    Attributes:
        parent: Parent frame container
        status_frame: Frame containing the indicator
        status_label: Clickable label displaying alert icon
        tooltip_text: Hover text describing current alert status
        on_click_callback: Function called when indicator is clicked
    """

    def __init__(self, parent_frame: Any) -> None:
        """Initialize the alert status indicator.
        
        Args:
            parent_frame: Parent tkinter frame to contain the indicator
        """
        # Direct imports for stable utilities
        self.config = config
        self.styles = styles

        # Injected dependencies for testable components
        self.parent = parent_frame
        parent_width = parent_frame.winfo_width()
        if parent_width <= 0:  # Handle case where parent hasn't been sized yet
            parent_width = 200  # Default fallback
        
        # Create status indicator frame
        self.status_frame = ttk.Frame(parent_frame)

        # Get theme configuration
        theme_config = self.styles.get_theme_config()
        alert_status_config = theme_config['widget_layout']['alert_status']

        # Calculate message wrap length using ratio
        message_wrap_length = int(alert_status_config['message_wrap_ratio'] * parent_width)
        
        # Alert icon/text label
        self.status_label = tk.Label(
            self.status_frame,
            text="🔔",
            cursor="hand2",
            font=alert_status_config['default_font'],
            wraplength=message_wrap_length
        )
        self.status_label.pack()
        
        # Tooltip text for hover
        self.tooltip_text = "No active alerts"
        
        # Will be set by the controller
        self.on_click_callback = None
        
        # Bind click event
        self.status_label.bind("<Button-1>", self._on_click)
        
        # Initial state
        self.update_status([])
    
    def grid(self, **kwargs) -> None:
        """Allow grid positioning of the status frame."""
        self.status_frame.grid(**kwargs) # Grid positioning arguments passed to frame.grid()
    
    def pack(self, **kwargs) -> None:
        """Allow pack positioning of the status frame."""
        self.status_frame.pack(**kwargs) # Pack positioning arguments passed to frame.pack()
    
    def update_status(self, alerts: List[WeatherAlert]) -> None:
        """Update the alert status indicator with enhanced visual styling.
        
        Changes the indicator appearance, color, and behavior based on
        alert count, severity levels, and priority.
        
        Args:
            alerts: List of currently active weather alerts
        """
        if not alerts:
            self.status_label.configure(text="🔔", foreground="gray")
            self.tooltip_text = "No active alerts"
            self._stop_animation()
            return
        
        # Get highest priority alert
        priority_order = self.config.ALERT_PRIORITY_ORDER
        highest_severity = None
        
        for severity in priority_order:
            if any(alert.severity == severity for alert in alerts):
                highest_severity = severity
                break
        
        if not highest_severity:
            highest_severity = alerts[0].severity  # Fallback
        
        # Get visual styling for highest severity
        alert_style = self.styles.ALERT_SEVERITY_COLORS[highest_severity]
        
        # Count by severity
        warnings = len([a for a in alerts if a.severity == 'warning'])
        cautions = len([a for a in alerts if a.severity == 'caution']) 
        watches = len([a for a in alerts if a.severity == 'watch'])
        total_count = len(alerts)
        
        # Update icon and styling
        self.status_label.configure(foreground=alert_style['color'])
        
        # Create detailed tooltip
        severity_counts = []
        if warnings > 0:
            severity_counts.append(f"{warnings} warning(s)")
        if cautions > 0:
            severity_counts.append(f"{cautions} caution(s)")
        if watches > 0:
            severity_counts.append(f"{watches} watch(es)")
        
        self.tooltip_text = f"Active alerts: {', '.join(severity_counts)}"
        
        # Start animation for warnings
        if highest_severity == 'warning':
            self._start_pulse_animation()
        else:
            self._stop_animation()
    
    def set_click_callback(self, callback: Callable) -> None:
        """Set click callback function."""
        self.on_click_callback = callback
    
    def _on_click(self, event) -> None:
        """Handle click on status indicator."""
        if self.on_click_callback:
            self.on_click_callback()
        else:
            # Default behavior - show simple message
            messagebox.showinfo("Alerts", f"Alert system active.\n{self.tooltip_text}")

    def _start_pulse_animation(self) -> None:
        """Start pulsing animation for critical alerts."""
        if not hasattr(self, '_animation_active'):
            self._animation_active = True
            self._animation_step = 0
            self._pulse_animation()

    def _stop_animation(self) -> None:
        """Stop any running animations."""
        self._animation_active = False
        if hasattr(self, '_animation_job'):
            self.status_label.after_cancel(self._animation_job)

    def _pulse_animation(self) -> None:
        """Pulse the alert indicator for critical warnings."""
        if not getattr(self, '_animation_active', False):
            return
        
        # Use centralized animation configuration
        anim_config = self.styles.ALERT_DISPLAY_CONFIG['animation_settings']
        pulse_colors = anim_config['pulse_colors']
        interval = anim_config['flash_interval']
        
        color = pulse_colors[self._animation_step % len(pulse_colors)]
        self.status_label.configure(foreground=color)
        self._animation_step += 1
        
        # Schedule next animation frame
        self._animation_job = self.status_label.after(interval, self._pulse_animation)


class SimpleAlertPopup:
    """Simple popup window for displaying alerts.
    
    Creates a modal dialog window showing detailed information about
    active weather alerts including severity, messages, and timestamps.
    
    Attributes:
        alerts: List of alerts to display
        window: Toplevel tkinter window for the popup
    """

    def __init__(self, parent: Any, alerts: List[WeatherAlert]) -> None:
        """Initialize the alert popup window.
        
        Args:
            parent: Parent window for the popup (can be None)
            alerts: List of weather alerts to display
        """
        # Direct imports for stable utilities
        self.styles = styles

        self.alerts = alerts
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Weather Alerts")
        
        # Get theme configuration for background
        theme_config = self.styles.get_theme_config()

        # Set window background to match main window
        self.window.configure(bg=theme_config['backgrounds']['main_window'])

        # Get parent dimensions for ratio-based sizing
        if parent:
            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()
        else:
            parent_width = 800  # Default fallback
            parent_height = 600  # Default fallback
        
        # Get theme configuration
        alert_config = theme_config['dimensions']['alert']

        # Calculate dimensions using ratios
        popup_width = int(alert_config['width_ratio'] * parent_width)
        base_height = int(alert_config['height_ratio'] * parent_height)
        alert_height = int(alert_config['item_height_ratio'] * parent_height)
        max_height = int(alert_config['max_height_ratio'] * parent_height)
            
        # Calculate dynamic window size based on number of alerts
        calculated_height = base_height + (len(alerts) * alert_height)
        window_height = min(calculated_height, max_height)
        
        # Set initial geometry but allow dynamic resizing
        self.window.geometry(f"{popup_width}x{window_height}")
        self.window.resizable(True, True)  # Allow both width and height resizing
        
        if parent:
            self.window.transient(parent)
        
        self._create_display()
        self._center_window()
    
    def _create_display(self) -> None:
        """Create the main alert display layout with scrollable content.
        
        Sets up the popup window content including title, scrollable alert list,
        and control buttons.
        """
        # Get theme configuration for styling
        theme_config = self.styles.get_theme_config()

        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        alert_count = len(self.alerts)
        title_text = f"Weather Alerts ({alert_count} active)"
        
        title_label = ttk.Label(main_frame, text=title_text, style="AlertTitle.TLabel")
        title_label.pack(pady=(0, 10))
        
        # Create scrollable frame for alerts (always use scrollbar for consistency)
        if self.alerts:
            # Create canvas and scrollbar for scrolling
            canvas = tk.Canvas(main_frame, highlightthickness=0, bg=theme_config['backgrounds']['main_window'])
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            # Configure scrolling
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Add alerts to scrollable frame
            for alert in self.alerts:
                self._create_alert_item(scrollable_frame, alert)
            
            # Bind mousewheel to canvas for scrolling
            def _on_mousewheel(event: Any) -> None:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            canvas.bind("<MouseWheel>", _on_mousewheel)
            
            # Update scroll region after all alerts are added
            self.window.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        else:
            no_alerts_label = ttk.Label(main_frame, text="No active alerts")
            no_alerts_label.pack()

    def _create_alert_item(self, parent: Any, alert: WeatherAlert) -> None:
        """Create display for individual alert.
        
        Args:
            parent: Parent widget to contain the alert item
            alert: Weather alert object to display
        """
        # Alert frame
        alert_frame = ttk.LabelFrame(parent, text=f"{alert.icon} {alert.title}", padding="5")
        alert_frame.pack(fill=tk.X, pady=3)
        
        # Alert message
        wrap_ratio = self.styles.WIDGET_LAYOUT['alert_status']['message_wrap_ratio']
        wrap_length = int(self.window.winfo_width() * wrap_ratio)
        message_label = ttk.Label(alert_frame, text=alert.message, wraplength=wrap_length)
        message_label.pack(anchor=tk.W)
        
        # Time and severity
        time_str = alert.timestamp.strftime("%H:%M:%S")
        info_text = f"Severity: {alert.severity.upper()} | Time: {time_str}"
        info_label = ttk.Label(alert_frame, text=info_text, style="GrayLabel.TLabel")
        # Then configure the color separately if needed
        # info_label.configure(style="LabelValue.TLabel")
        info_label.pack(anchor=tk.W)
    
    def _center_window(self) -> None:
        """Center the popup window on screen.
        
        Calculates screen center position and moves the popup window
        to be centered on the user's display.
        """
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')