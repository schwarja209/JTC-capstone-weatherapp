"""
Status bar widget for system status, progress, and data information.

This module provides a comprehensive status bar widget for the Weather Dashboard
bottom panel. Manages three status sections: system status (left), progress
indicators (center), and data source information (right) with color-coded
status messages and real-time updates.

Classes:
    StatusBarWidgets: Multi-section status bar with system, progress, and data status
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Any, Dict
from datetime import datetime

from WeatherDashboard.utils.logger import Logger
from WeatherDashboard import styles

from WeatherDashboard.widgets.widget_interface import IWeatherDashboardWidgets
from WeatherDashboard.widgets.base_widgets import BaseWidgetManager, SafeWidgetCreator, widget_error_handler


class StatusBarWidgets(BaseWidgetManager, IWeatherDashboardWidgets):
    """Manages the status bar display at bottom of application.
    
    Creates and manages a three-section status bar with system status,
    progress indicators, and data source information. Provides color-coded
    status messages, progress updates during async operations, and real-time
    data source tracking.
    
    Attributes:
        parent: Parent frame container
        state: Application state manager
        system_status_label: Left section - system status messages
        progress_label: Center section - operation progress indicators  
        data_status_label: Right section - data source information
    """

    def __init__(self, parent_frame: ttk.Frame, state: Any) -> None:
        """Initialize the status bar with error handling.
        
        Creates left (system), center (progress), and right (data) status sections
        with appropriate styling, separators, and registers widgets with state manager.
        
        Args:
            parent_frame: Parent TTK frame to contain the status bar
            state: Application state manager for widget registration
        """
        # Direct imports for stable utilities
        self.styles = styles
        self.logger = Logger()
        self.datetime = datetime
        
        # Injected dependencies for testable components
        self.parent_frame = parent_frame
        self.state = state

        # Widget references
        self.system_status_label: Optional[ttk.Label] = None
        self.progress_label: Optional[ttk.Label] = None  
        self.progress_var = tk.StringVar(value="")
        self.data_status_label: Optional[ttk.Label] = None
        
        # Initialize base class with error handling
        super().__init__(parent_frame, state, "status bar widgets")
        
        # Create widgets with standardized error handling
        if not self.safe_create_widgets():
            self.logger.warn("Status bar widgets created with errors - some functionality may be limited")
    
    def _create_widgets(self) -> None:
        """Create the three-section status bar layout with base class error handling.
        
        Creates left section for system status, center section for progress
        indicators, and right section for data source information. Includes
        visual separators and appropriate styling for each section.
        """
        # Left section: System status using SafeWidgetCreator
        self.system_status_label = SafeWidgetCreator.create_label(self.parent, "Ready", "SystemStatus.TLabel")
        self.system_status_label.pack(side=tk.LEFT, padx=self.styles.STATUS_BAR_CONFIG['padding']['system'])

        # Separator
        ttk.Separator(self.parent, orient='vertical').pack(side=tk.LEFT, fill='y', padx=self.styles.STATUS_BAR_CONFIG['padding']['separator'])

        # Center section: Progress indicator using SafeWidgetCreator
        self.progress_label = SafeWidgetCreator.create_label(self.parent, "", "LabelValue.TLabel", textvariable=self.progress_var)
        self.progress_label.pack(side=tk.LEFT, padx=self.styles.STATUS_BAR_CONFIG['padding']['progress'])

        # Right section: Data source information using SafeWidgetCreator
        self.data_status_label = SafeWidgetCreator.create_label(self.parent, "No data", "DataStatus.TLabel")
        self.data_status_label.pack(side=tk.RIGHT, padx=self.styles.STATUS_BAR_CONFIG['padding']['data'])

        # Separator
        ttk.Separator(self.parent, orient='vertical').pack(side=tk.RIGHT, fill='y', padx=self.styles.STATUS_BAR_CONFIG['padding']['separator'])

        # Scheduler section: Auto-collection status
        self._create_scheduler_status()

    def update_status_bar(self, city_name: str, error_exception: Optional[Exception], simulated: bool = False) -> None:
        """Update all status bar sections: system, progress, and data status."""
        # Left section: system/city
        self.update_system_status(f"City: {city_name}", status_type="info")
        
        # Center section: progress/error
        if error_exception:
            self.update_progress(f"Error: {error_exception}", error=True)
        # Do NOT clear the progress message on success here.
        # Let LoadingStateManager handle clearing progress when appropriate.
        
        # Right section: data source
        if simulated:
            self.update_data_status("Simulated data", status_type="warning")
        else:
            self.update_data_status("Live data", status_type="info")

    def update_data_status(self, message: str, status_type: str = "info") -> None:
        """Updates data source information with dynamic styling.

        Args:
            message: Data source status message to display
            status_type: Type of status ("info", "warning", "none")
        """
        # color parameter is deprecated but kept for backward compatibility
        if self.data_status_label:
            self.data_status_label.configure(text=message)

            if status_type == "warning":
                self.data_status_label.configure(style="DataStatusSimulated.TLabel")
            elif status_type == "info":
                self.data_status_label.configure(style="DataStatusLive.TLabel")
            else:
                self.data_status_label.configure(style="DataStatusNone.TLabel")
    
    def update_system_status(self, message: str, status_type: str = "info") -> None:
        """Update main system status message with appropriate styling.

        Args:
            message: Status message to display
            status_type: Type of status ("error", "warning", "info")
        """
        if self.system_status_label:
            self.system_status_label.configure(text=message)
            
            # Switch style based on status type
            if status_type == "error":
                self.system_status_label.configure(style="SystemStatusError.TLabel")
            elif status_type == "warning":
                self.system_status_label.configure(style="SystemStatusWarning.TLabel")
            else:  # "info" or default
                self.system_status_label.configure(style="SystemStatusReady.TLabel")

    def update_progress(self, message: str = "", error: bool = False) -> None:
        """Updates progress indicator in center section."""
        if self.progress_var:
            self.progress_var.set(message)
        if self.progress_label:
            color = self.styles.STATUS_BAR_CONFIG['colors']['error'] if error else self.styles.STATUS_BAR_CONFIG['colors']['info']
            self.progress_label.configure(foreground=color)
     
    def clear_progress(self) -> None:
        """Clears progress indicator in center section."""
        if self.progress_var:
            self.progress_var.set("")

    def _create_scheduler_status(self) -> None:
        """Create scheduler status display."""        
        # Status indicator
        self.scheduler_status_label = SafeWidgetCreator.create_label(
            self.parent, 
            "⏸️ Auto: Off", 
            "StatusBar.TLabel"
        )
        self.scheduler_status_label.pack(side=tk.RIGHT, padx=(5,0))
        
        # Next fetch countdown
        self.scheduler_countdown_label = SafeWidgetCreator.create_label(
            self.parent, 
            "", 
            "StatusBar.TLabel"
        )
        self.scheduler_countdown_label.pack(side=tk.RIGHT, padx=(5, 0))

    def update_scheduler_status(self, status_info: Dict[str, Any]) -> None:
        """Update scheduler status display."""
        if not hasattr(self, 'scheduler_status_label'):
            return
     
        try:       
            # Update status indicator
            if status_info['enabled'] and status_info['is_running']:
                self.scheduler_status_label.config(text="🟢 On")
            elif status_info['enabled']:
                self.scheduler_status_label.config(text="🟡 Paused")
            else:
                self.scheduler_status_label.config(text="🔴 Off")
            
            # Update countdown
            if status_info['next_fetch_time']:
                try:
                    time_until = status_info['next_fetch_time'] - self.datetime.now()
                    if time_until.total_seconds() > 0:
                        minutes = int(time_until.total_seconds() // 60)
                        seconds = int(time_until.total_seconds() % 60)
                        self.scheduler_countdown_label.config(text=f"Next: {minutes:02d}:{seconds:02d}")
                    else:
                        self.scheduler_countdown_label.config(text="Fetching...")
                except (AttributeError, TypeError):
                    # Fallback if datetime is not available
                    self.scheduler_countdown_label.config(text="")
            else:
                self.scheduler_countdown_label.config(text="")
        
        except RuntimeError:
            # Handle tkinter thread safety issues
            pass
    
    def clear_all(self) -> None:
        """Resets all status bar sections to default states."""
        self.update_system_status("Ready", "info")
        self.clear_progress()
        self.update_data_status("No data")