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

class StatusBarWidgets:
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
        """Initialize the status bar with three status sections.
        
        Creates left (system), center (progress), and right (data) status sections
        with appropriate styling, separators, and registers widgets with state manager.
        
        Args:
            parent_frame: Parent TTK frame to contain the status bar
            state: Application state manager for widget registration
        """
        self.parent = parent_frame
        self.state = state
        
        # Widget references
        self.system_status_label: Optional[ttk.Label] = None
        self.progress_label: Optional[ttk.Label] = None  
        self.data_status_label: Optional[ttk.Label] = None
        
        self._create_status_sections()
    
    def _create_status_sections(self) -> None:
        """Create the three-section status bar layout.
        
        Creates left section for system status, center section for progress
        indicators, and right section for data source information. Includes
        visual separators and appropriate styling for each section.
        """
        # Left section: System status
        self.system_status_label = ttk.Label(
            self.parent, 
            text="Ready", 
            style="LabelValue.TLabel",
            foreground="green"
        )
        self.system_status_label.pack(side=tk.LEFT, padx=styles.STATUS_BAR_CONFIG['padding']['system'])
        
        # Separator
        ttk.Separator(self.parent, orient='vertical').pack(side=tk.LEFT, fill='y', padx=styles.STATUS_BAR_CONFIG['padding']['separator'])
        
        # Center section: Progress indicator  
        self.progress_label = ttk.Label(
            self.parent,
            text="",
            style="LabelValue.TLabel", 
            foreground="blue"
        )
        self.progress_label.pack(side=tk.LEFT, padx=styles.STATUS_BAR_CONFIG['padding']['progress'])
        
        # Right section: Data source information
        self.data_status_label = ttk.Label(
            self.parent,
            text="No data",
            style="LabelValue.TLabel",
            foreground="gray"
        )
        self.data_status_label.pack(side=tk.RIGHT, padx=styles.STATUS_BAR_CONFIG['padding']['data'])
    
    def update_system_status(self, message: str, status_type: str = "info") -> None:
        """Updates main system status message."""
        colors = styles.STATUS_BAR_CONFIG['colors']
        
        if self.system_status_label:
            self.system_status_label.configure(
                text=message,
                foreground=colors.get(status_type, "green")
            )
    
    def update_progress(self, message: str) -> None:
        """Updates progress indicator."""
        if self.progress_label:
            self.progress_label.configure(text=message)
    
    def update_data_status(self, message: str, color: str = "gray") -> None:
        """Updates data source information with optional color coding."""
        if self.data_status_label:
            # Safety check for None values
            display_message = str(message) if message is not None else "No data"
            self.data_status_label.configure(text=display_message, foreground=color)
    
    def clear_progress(self) -> None:
        """Clears progress indicator."""
        if self.progress_label:
            self.progress_label.configure(text="")
    
    def clear_all(self) -> None:
        """Resets status bar to default state."""
        self.update_system_status("Ready", "info")
        self.clear_progress()
        self.update_data_status("No data")