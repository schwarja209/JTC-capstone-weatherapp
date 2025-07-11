"""
Style configuration for GUI elements.

This module provides centralized styling configuration for all tkinter
GUI components in the Weather Dashboard. Defines fonts, colors, padding,
and visual appearance settings for consistent UI theming.

Functions:
    configure_styles: Apply comprehensive styling to all GUI components
"""

from tkinter import ttk


def configure_styles() -> None:
    """Configure comprehensive styles for all GUI elements.
    
    Applies consistent styling including fonts, colors, padding, and
    visual effects to labels, buttons, frames, notebooks, and other
    tkinter components throughout the application.
    """
    style = ttk.Style()
    style.configure("FrameLabel.TLabelframe.Label", font=('Arial', 15, 'bold'))
    style.configure("LabelName.TLabel", font=('Arial', 10, 'bold'))
    style.configure("LabelValue.TLabel", font=('Arial', 10))
    style.configure("MainButton.TButton", font=('Arial', 10, 'bold'), padding=5)
    style.configure("Title.TLabel", font=('Comic Sans MS', 20, 'bold'))
    
    style.configure("TNotebook", background="lightgray")
    style.configure("TNotebook.Tab", padding=[12, 8], font=("Arial", 10, "bold"))
    style.map("TNotebook.Tab",
             background=[("selected", "lightblue"), ("active", "lightgreen")],
             foreground=[("selected", "darkblue"), ("active", "darkgreen")])