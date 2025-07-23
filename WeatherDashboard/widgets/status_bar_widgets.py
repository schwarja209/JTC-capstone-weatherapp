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
from typing import Optional, Any

from WeatherDashboard import styles
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.widgets.base_widgets import BaseWidgetManager, SafeWidgetCreator, widget_error_handler


class StatusBarWidgets(BaseWidgetManager):
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
        # Widget references
        self.system_status_label: Optional[ttk.Label] = None
        self.progress_label: Optional[ttk.Label] = None  
        self.data_status_label: Optional[ttk.Label] = None
        
        # Initialize base class with error handling
        super().__init__(parent_frame, state, "status bar widgets")
        
        # Create widgets with standardized error handling
        if not self.safe_create_widgets():
            Logger.warn("Status bar widgets created with errors - some functionality may be limited")
    
    def _create_widgets(self) -> None:
        """Create the three-section status bar layout with base class error handling.
        
        Creates left section for system status, center section for progress
        indicators, and right section for data source information. Includes
        visual separators and appropriate styling for each section.
        """
        # Left section: System status using SafeWidgetCreator
        self.system_status_label = SafeWidgetCreator.create_label(self.parent, "Ready", "SystemStatus.TLabel")
        self.system_status_label.pack(side=tk.LEFT, padx=styles.STATUS_BAR_CONFIG['padding']['system'])

        # Separator
        ttk.Separator(self.parent, orient='vertical').pack(side=tk.LEFT, fill='y', padx=styles.STATUS_BAR_CONFIG['padding']['separator'])

        # Center section: Progress indicator using SafeWidgetCreator
        self.progress_label = SafeWidgetCreator.create_label(self.parent, "", "ProgressStatus.TLabel")
        self.progress_label.pack(side=tk.LEFT, padx=styles.STATUS_BAR_CONFIG['padding']['progress'])

        # Right section: Data source information using SafeWidgetCreator
        self.data_status_label = SafeWidgetCreator.create_label(self.parent, "No data", "DataStatus.TLabel")
        self.data_status_label.pack(side=tk.RIGHT, padx=styles.STATUS_BAR_CONFIG['padding']['data'])
    
    def update_data_status(self, message: str, color: str = "gray") -> None:
        """Updates data source information with dynamic styling.
        
        Updates the right section of the status bar with data source information
        and applies appropriate styling based on whether data is live, simulated,
        or unavailable.
        
        Args:
            message: Data source status message to display
            color: Color for message display (DEPRECATED - styling handled by message content)
        """
        # color parameter is deprecated but kept for backward compatibility
        if self.data_status_label:
            display_message = str(message) if message is not None else "No data"
            self.data_status_label.configure(text=display_message)
            
            # Switch style based on data source type
            if "simulated" in display_message.lower() or "fallback" in display_message.lower():
                self.data_status_label.configure(style="DataStatusSimulated.TLabel")
            elif "live" in display_message.lower() or display_message == "Live data":
                self.data_status_label.configure(style="DataStatusLive.TLabel")
            else:
                self.data_status_label.configure(style="DataStatusNone.TLabel")
    
    def update_system_status(self, message: str, status_type: str = "info") -> None:
        """Update main system status message with appropriate styling.

        Updates the left section with system status and applies color-coded
        styling based on status type (error, warning, info).

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

    def update_progress(self, message: str) -> None:
        """Updates progress indicator in center section."""
        if self.progress_label:
            self.progress_label.configure(text=message)
     
    def clear_progress(self) -> None:
        """Clears progress indicator in center section."""
        if self.progress_label:
            self.progress_label.configure(text="")
    
    def clear_all(self) -> None:
        """Resets all three status bar sections to default states."""
        self.update_system_status("Ready", "info")
        self.clear_progress()
        self.update_data_status("No data")