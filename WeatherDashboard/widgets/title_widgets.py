"""
Title widget for the dashboard header.
"""

from tkinter import ttk


class TitleWidget:
    """Simple title display widget for the dashboard."""
    
    def __init__(self, parent_frame: ttk.Frame, title: str = "Weather Dashboard") -> None:
        self.parent = parent_frame
        self.title = title
        self._create_title()

    def _create_title(self) -> None:
        """Creates the title label."""
        label = ttk.Label(self.parent, text=self.title, style="Title.TLabel")
        label.pack()
    
    def update_title(self, new_title: str) -> None:
        """Updates the title text (for future customization)."""
        self.title = new_title