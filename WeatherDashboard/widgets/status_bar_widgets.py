"""
Status bar widget for system status, progress, and data information.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Any

class StatusBarWidgets:
    """Manages the status bar display at bottom of application."""
    
    def __init__(self, parent_frame: ttk.Frame, state: Any) -> None:
        self.parent = parent_frame
        self.state = state
        
        # Widget references
        self.system_status_label: Optional[ttk.Label] = None
        self.progress_label: Optional[ttk.Label] = None  
        self.data_status_label: Optional[ttk.Label] = None
        
        self._create_status_sections()
        self._register_with_state()
    
    def _create_status_sections(self) -> None:
        """Creates left, center, and right status sections."""
        
        # Left section: System status
        self.system_status_label = ttk.Label(
            self.parent, 
            text="Ready", 
            style="LabelValue.TLabel",
            foreground="green"
        )
        self.system_status_label.pack(side=tk.LEFT, padx=5)
        
        # Separator
        ttk.Separator(self.parent, orient='vertical').pack(side=tk.LEFT, fill='y', padx=5)
        
        # Center section: Progress indicator  
        self.progress_label = ttk.Label(
            self.parent,
            text="",
            style="LabelValue.TLabel", 
            foreground="blue"
        )
        self.progress_label.pack(side=tk.LEFT, padx=10)
        
        # Right section: Data source information
        self.data_status_label = ttk.Label(
            self.parent,
            text="No data",
            style="LabelValue.TLabel",
            foreground="gray"
        )
        self.data_status_label.pack(side=tk.RIGHT, padx=5)
    
    def _register_with_state(self) -> None:
        """Registers status bar widgets with state manager."""
        self.state.system_status_label = self.system_status_label
        self.state.progress_label = self.progress_label
        self.state.data_status_label = self.data_status_label
    
    def update_system_status(self, message: str, status_type: str = "info") -> None:
        """Updates main system status message."""
        colors = {
            "info": "green",
            "warning": "orange", 
            "error": "red",
            "loading": "blue"
        }
        
        if self.system_status_label:
            self.system_status_label.configure(
                text=message,
                foreground=colors.get(status_type, "green")
            )
    
    def update_progress(self, message: str) -> None:
        """Updates progress indicator."""
        if self.progress_label:
            self.progress_label.configure(text=message)
    
    def update_data_status(self, message: str) -> None:
        """Updates data source information."""
        if self.data_status_label:
            # Safety check for None values
            display_message = str(message) if message is not None else "No data"
            self.data_status_label.configure(text=display_message)
    
    def clear_progress(self) -> None:
        """Clears progress indicator."""
        if self.progress_label:
            self.progress_label.configure(text="")
    
    def clear_all(self) -> None:
        """Resets status bar to default state."""
        self.update_system_status("Ready", "info")
        self.clear_progress()
        self.update_data_status("No data")