"""
Title widget for the dashboard header.

This module provides a simple title display widget for the Weather Dashboard
application header. Creates a styled label widget for application branding
and title display with support for dynamic title updates.

Classes:
    TitleWidget: Simple title display widget with customizable text
"""

from typing import Optional, Callable
from tkinter import ttk
import tkinter as tk

from WeatherDashboard.utils.logger import Logger
from WeatherDashboard import config

from .base_widgets import BaseWidgetManager, SafeWidgetCreator, widget_error_handler


class TitleWidget(BaseWidgetManager):
    """Simple title display widget for the dashboard header.

    Attributes:
        parent: Parent frame container
        title: Current title text string
        title_label: Title display label widget
        scheduler_callback: Callback for scheduler toggle
    """

    def __init__(self, parent_frame: ttk.Frame, title: str = "Weather Dashboard", scheduler_callback: Optional[Callable] = None) -> None:
        """Initialize the title widget with specified text."""
        # Direct imports for stable utilities
        self.logger = Logger()
        self.config = config
        
        # Injected dependencies for testable components
        self.parent_frame = parent_frame
        self.scheduler_callback = scheduler_callback

        # Add version to default title
        if title == "Weather Dashboard":
            try:
                from WeatherDashboard import get_version
                version = get_version()
                title = f"Weather Dashboard (v{version})"
            except (ImportError, AttributeError) as e:
                self.logger.warn(f"Could not get version info: {e}")
                title = "Weather Dashboard"

        self.title = title
        self.title_label: Optional[ttk.Label] = None

        self.scheduler_var: Optional[tk.BooleanVar] = None
        self.scheduler_checkbox: Optional[ttk.Checkbutton] = None
        
        # Initialize base class with error handling
        super().__init__(parent_frame, None, "title widget")
        
        # Create widgets with standardized error handling
        if not self.safe_create_widgets():
            self.logger.warn("Title widget created with errors - title may not display")

    def _create_widgets(self) -> None:
        """Create and display the title label widget."""
        # Create main container frame
        main_frame = SafeWidgetCreator.create_frame(self.parent)
        main_frame.pack(fill=tk.X, padx=10, pady=5)

        self.title_label = SafeWidgetCreator.create_label(main_frame, self.title, "Title.TLabel")
        self.title_label.pack(side=tk.LEFT)

        # System controls on the right
        if self.scheduler_callback:
            self._create_scheduler_control(main_frame)

    def _create_scheduler_control(self, parent_frame: ttk.Frame) -> None:
        """Create scheduler toggle control."""        
        # Scheduler toggle
        self.scheduler_var = tk.BooleanVar(value=self.config.SCHEDULER["enabled"])
        self.scheduler_checkbox = SafeWidgetCreator.create_checkbutton(
            parent_frame,
            text="Live Updates",
            variable=self.scheduler_var,
            command=self._on_scheduler_toggle
        )
        self.scheduler_checkbox.pack(side=tk.RIGHT)
    
    def _on_scheduler_toggle(self) -> None:
        """Handle scheduler toggle."""
        if self.scheduler_callback:
            self.scheduler_callback()
            # Save preferences when scheduler state changes
            if hasattr(self, 'state') and self.state:
                self.state.save_preferences()
    
    def set_scheduler_state(self, enabled: bool) -> None:
        """Update scheduler checkbox state."""
        if self.scheduler_var:
            self.scheduler_var.set(enabled)
    
    @widget_error_handler("title update")
    def update_title(self, new_title: str) -> None:
        """Updates the title text (for future customization)."""
        self.title = new_title

        if self.title_label:
            self.title_label.configure(text=new_title)