"""
GUI frame creation and management.
"""

import tkinter as tk
from tkinter import ttk
from WeatherDashboard.gui.styles import configure_styles


class WeatherDashboardGUIFrames:
    '''Creates and manages the main GUI frames for the weather dashboard.'''
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.frames = {}
        self.create_styles()
        self.create_frames()

    def create_styles(self) -> None:
        '''Configures the styles for the GUI elements.'''
        configure_styles()

    def create_frames(self) -> None:
        '''Creates the main frames for the dashboard layout.'''
        self.frames["title"] = ttk.Frame(self.root, padding="10")
        self.frames["title"].grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.frames["control"] = ttk.LabelFrame(self.root, text="Controls", padding="10", style="FrameLabel.TLabelframe")
        self.frames["control"].grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W, tk.E), padx=10)

        self.frames["metric"] = ttk.LabelFrame(self.root, text="Current Weather", padding="10", style="FrameLabel.TLabelframe")
        self.frames["metric"].grid(row=1, column=1, sticky=(tk.N, tk.S, tk.W, tk.E), padx=10)

        self.frames["chart"] = ttk.LabelFrame(self.root, text="Weather Trends", padding="10", style="FrameLabel.TLabelframe")
        self.frames["chart"].grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=0)