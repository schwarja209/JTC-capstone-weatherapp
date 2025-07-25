"""
GUI frame management for the Weather Dashboard application.

This module provides frame management and layout organization for the
Weather Dashboard UI. Creates and organizes the main window structure
with proper frame hierarchy and layout management.

Classes:
    WeatherDashboardGUIFrames: Main frame manager and layout coordinator
"""

from typing import Dict, Union
import tkinter as tk
from tkinter import ttk
from WeatherDashboard import styles


class WeatherDashboardGUIFrames:
    """Manage the main window frames and layout for the Weather Dashboard.
    
    Creates and organizes the main UI frame structure including title area,
    control panels, tabbed content area, chart display, and status bar.
    Provides proper layout management and frame hierarchy.
    
    Attributes:
        root: Main tkinter window
        frames: Dictionary containing all created frame widgets
    """
    def __init__(self, root: tk.Tk) -> None:
        """Create the main frames for the dashboard layout.
        
        Sets up the primary frame structure including title, controls, tabbed
        content area, and status bar with proper grid layout and weight configuration.
        """
        self.root = root
        self.frames: Dict[str, Union[ttk.Frame, ttk.LabelFrame]] = {}
        self.create_styles()
        self.create_frames()

    def create_styles(self) -> None:
        """Configure the styles for the GUI elements."""
        styles.configure_styles()

    def create_frames(self) -> None:
        """Create the main frames for the dashboard layout."""
        FRAME_TITLE = "title"
        FRAME_CONTROL = "control"
        FRAME_TABBED = "tabbed"
        FRAME_STATUS = "status_bar"

        self.frames[FRAME_TITLE] = ttk.Frame(self.root, padding="10")
        self.frames[FRAME_TITLE].grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.frames[FRAME_CONTROL] = ttk.LabelFrame(self.root, text="Controls", padding="10", style="FrameLabel.TLabelframe")
        self.frames[FRAME_CONTROL].grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W, tk.E), padx=10)

        self.frames[FRAME_TABBED] = ttk.LabelFrame(self.root, text="Weather Information", padding="10", style="FrameLabel.TLabelframe")
        self.frames[FRAME_TABBED].grid(row=1, column=1, sticky=(tk.N, tk.S, tk.W, tk.E), padx=10)

        self.frames[FRAME_STATUS] = ttk.Frame(self.root, padding="5")
        self.frames[FRAME_STATUS].grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=0)  # Status bar doesn't expand