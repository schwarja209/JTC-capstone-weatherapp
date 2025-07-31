"""
GUI frame management for the Weather Dashboard application.

This module provides frame management and layout organization for the
Weather Dashboard UI. Creates and organizes the main window structure
with proper frame hierarchy and layout management.

Classes:
    WeatherDashboardGUIFrames: Main frame manager and layout coordinator
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Union

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

        Args:
            root: Main tkinter window
        """
        # Direct imports for stable utilities
        self.styles = styles

        # Instance data
        self.root = root
        self.frames: Dict[str, Union[ttk.Frame, ttk.LabelFrame]] = {}

        # Initialize frames
        self.create_styles()
        self.create_frames()

    def create_styles(self) -> None:
        """Configure the styles for the GUI elements."""
        self.styles.configure_styles()

    def create_frames(self) -> None:
        """Create the main frames for the dashboard layout."""

        layout_config = self.styles.LAYOUT_CONFIG

        # Create frames using configuration
        for frame_name, frame_config in layout_config['frames'].items():
            if frame_config.get('text'):
                # LabelFrame with text
                self.frames[frame_name] = ttk.LabelFrame(
                    self.root, 
                    text=frame_config['text'],
                    padding=frame_config['padding'],
                    style=frame_config['style']
                )
            else:
                # Regular Frame
                self.frames[frame_name] = ttk.Frame(
                    self.root,
                    padding=frame_config['padding'],
                    style=frame_config['style']
                )
            
            # Apply grid configuration
            grid_config = frame_config['grid']
            self.frames[frame_name].grid(**grid_config)
        
            # IMPORTANT: Configure grid weights for each frame
            if 'sticky' in grid_config and 'ew' in grid_config['sticky']:
                # Frame spans columns, configure column weights
                col = grid_config.get('column', 0)
                self.root.columnconfigure(col, weight=1)
            if 'sticky' in grid_config and 'ns' in grid_config['sticky']:
                # Frame spans rows, configure row weights
                row = grid_config.get('row', 0)
                self.root.rowconfigure(row, weight=1)

        # Apply additional grid weights from config
        grid_weights = layout_config['grid_weights']
        for i, weight in enumerate(grid_weights['columns']):
            self.root.columnconfigure(i, weight=weight)
        for i, weight in enumerate(grid_weights['rows']):
            self.root.rowconfigure(i, weight=weight)