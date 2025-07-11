"""
Title widget for the dashboard header.

This module provides a simple title display widget for the Weather Dashboard
application header. Creates a styled label widget for application branding
and title display with support for dynamic title updates.

Classes:
    TitleWidget: Simple title display widget with customizable text
"""

from tkinter import ttk


class TitleWidget:
    """Simple title display widget for the dashboard header.
    
    Creates and manages a styled title label for the application header.
    Provides a clean, prominent display of the application name with
    support for runtime title updates and consistent styling.
    
    Attributes:
        parent: Parent frame container
        title: Current title text string
    """
    def __init__(self, parent_frame: ttk.Frame, title: str = "Weather Dashboard") -> None:
        """Initialize the title widget with specified text.
        
        Args:
            parent_frame: Parent TTK frame to contain the title label
            title: Title text to display (default: "Weather Dashboard")
        """
        self.parent = parent_frame
        self.title = title
        self._create_title()

    def _create_title(self) -> None:
        """Create and display the title label widget.
        
        Creates a TTK label with the title text using the "Title.TLabel" style
        and packs it into the parent frame for display.
        """
        label = ttk.Label(self.parent, text=self.title, style="Title.TLabel")
        label.pack()
    
    def update_title(self, new_title: str) -> None:
        """Updates the title text (for future customization)."""
        self.title = new_title