"""
Basic alert display components.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional, Callable
from WeatherDashboard.features.alerts.alert_manager import WeatherAlert

class AlertStatusIndicator:
    """Small status indicator widget for showing alert status."""
    
    def __init__(self, parent_frame):
        self.parent = parent_frame
        
        # Create status indicator frame
        self.status_frame = ttk.Frame(parent_frame)
        
        # Alert icon/text label
        self.status_label = ttk.Label(
            self.status_frame,
            text="🔔",
            cursor="hand2",
            font=("Arial", 12)
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
    
    def grid(self, **kwargs):
        """Allow grid positioning of the status frame."""
        self.status_frame.grid(**kwargs)
    
    def pack(self, **kwargs):
        """Allow pack positioning of the status frame.""" 
        self.status_frame.pack(**kwargs)
    
    def update_status(self, alerts: List[WeatherAlert]):
        """Update the alert status indicator based on active alerts."""
        if not alerts:
            self.status_label.configure(text="🔔", foreground="gray")
            self.tooltip_text = "No active alerts"
            return
        
        # Count by severity
        warnings = len([a for a in alerts if a.severity == 'warning'])
        cautions = len([a for a in alerts if a.severity == 'caution'])
        watches = len([a for a in alerts if a.severity == 'watch'])
        
        total_count = len(alerts)
        
        if warnings > 0:
            self.status_label.configure(text="⚠️", foreground="red")
            self.tooltip_text = f"{warnings} warning(s), {total_count} total alerts"
        elif cautions > 0:
            self.status_label.configure(text="🔶", foreground="orange")
            self.tooltip_text = f"{cautions} caution(s), {total_count} total alerts"
        elif watches > 0:
            self.status_label.configure(text="👁️", foreground="blue")
            self.tooltip_text = f"{watches} watch alert(s)"
        else:
            self.status_label.configure(text="🔔", foreground="blue")
            self.tooltip_text = f"{total_count} active alerts"
    
    def set_click_callback(self, callback: Callable):
        """Set callback function for when indicator is clicked."""
        self.on_click_callback = callback
    
    def _on_click(self, event):
        """Handle click on status indicator."""
        if self.on_click_callback:
            self.on_click_callback()
        else:
            # Default behavior - show simple message
            messagebox.showinfo("Alerts", f"Alert system active.\n{self.tooltip_text}")

class SimpleAlertPopup:
    """Simple popup window for displaying alerts."""
    
    def __init__(self, parent, alerts: List[WeatherAlert]):
        self.alerts = alerts
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Weather Alerts")
        self.window.geometry("400x300")
        
        if parent:
            self.window.transient(parent)
        
        self._create_display()
        self._center_window()
    
    def _create_display(self):
        """Create simple alert display."""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        alert_count = len(self.alerts)
        title_text = f"Weather Alerts ({alert_count} active)"
        
        title_label = ttk.Label(main_frame, text=title_text, font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Alert list
        if self.alerts:
            for alert in self.alerts:
                self._create_alert_item(main_frame, alert)
        else:
            no_alerts_label = ttk.Label(main_frame, text="No active alerts")
            no_alerts_label.pack()
        
        # Close button
        ttk.Button(main_frame, text="Close", command=self.window.destroy).pack(pady=(10, 0))
    
    def _create_alert_item(self, parent, alert: WeatherAlert):
        """Create display for individual alert."""
        # Alert frame
        alert_frame = ttk.LabelFrame(parent, text=f"{alert.icon} {alert.title}", padding="5")
        alert_frame.pack(fill=tk.X, pady=3)
        
        # Alert message
        message_label = ttk.Label(alert_frame, text=alert.message, wraplength=350)
        message_label.pack(anchor=tk.W)
        
        # Time and severity
        time_str = alert.timestamp.strftime("%H:%M:%S")
        info_text = f"Severity: {alert.severity.upper()} | Time: {time_str}"
        info_label = ttk.Label(alert_frame, text=info_text, foreground="gray")
        info_label.pack(anchor=tk.W)
    
    def _center_window(self):
        """Center the popup window."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')