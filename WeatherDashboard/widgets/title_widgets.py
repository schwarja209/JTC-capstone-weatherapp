"""
Title widget for the dashboard header.

This module provides a simple title display widget for the Weather Dashboard
application header. Creates a styled label widget for application branding
and title display with support for dynamic title updates.

Classes:
    TitleWidget: Simple title display widget with customizable text
"""

from typing import Optional
from tkinter import ttk

from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.widgets.base_widgets import BaseWidgetManager, SafeWidgetCreator, widget_error_handler


class TitleWidget(BaseWidgetManager):
    """Simple title display widget for the dashboard header.

    Attributes:
        parent: Parent frame container
        title: Current title text string
        title_label: Title display label widget
    """
    def __init__(self, parent_frame: ttk.Frame, title: str = "Weather Dashboard") -> None:
        """Initialize the title widget with specified text."""
        # Add version to default title
        if title == "Weather Dashboard":
            try:
                from WeatherDashboard import get_version
                version = get_version()
                title = f"Weather Dashboard (v{version})"
            except (ImportError, AttributeError) as e:
                Logger.warn(f"Could not get version info: {e}")
                title = "Weather Dashboard"

        self.title = title
        self.title_label: Optional[ttk.Label] = None
        
        # Initialize base class with error handling
        super().__init__(parent_frame, None, "title widget")
        
        # Create widgets with standardized error handling
        if not self.safe_create_widgets():
            Logger.warn("Title widget created with errors - title may not display")

    def _create_widgets(self) -> None:
        """Create and display the title label widget."""
        self.title_label = SafeWidgetCreator.create_label(self.parent, self.title, "Title.TLabel")
        self.title_label.pack()
    
    @widget_error_handler("title update")
    def update_title(self, new_title: str) -> None:
        """Updates the title text (for future customization)."""
        self.title = new_title

        if self.title_label:
            self.title_label.configure(text=new_title)