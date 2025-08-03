"""
Title widget for the dashboard header.

This module provides a simple title display widget for the Weather Dashboard
application header. Creates a styled label widget for application branding
and title display with support for dynamic title updates.

Classes:
    TitleWidget: Simple title display widget with customizable text
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable

from WeatherDashboard import config, styles
from WeatherDashboard.utils.logger import Logger

from .base_widgets import BaseWidgetManager, SafeWidgetCreator, widget_error_handler


class TitleWidget(BaseWidgetManager):
    """Simple title display widget for the dashboard header.

    Attributes:
        parent: Parent frame container
        title: Current title text string
        title_label: Title display label widget
        scheduler_callback: Callback for scheduler toggle
    """

    def __init__(self, parent_frame: ttk.Frame, title: str = "Weather Dashboard", scheduler_callback: Optional[Callable] = None, theme_callback: Optional[Callable] = None) -> None:
        """Initialize the title widget with specified text."""
        # Direct imports for stable utilities
        self.logger = Logger()
        self.config = config
        self.styles = styles
        
        # Injected dependencies for testable components
        self.parent_frame = parent_frame
        self.scheduler_callback = scheduler_callback
        self.theme_callback = theme_callback

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

        # Theme switcher components
        self.theme_var: Optional[tk.StringVar] = None
        self.theme_combobox: Optional[ttk.Combobox] = None
        
        # Initialize base class with error handling
        super().__init__(parent_frame, None, "title widget")
        
        # Create widgets with standardized error handling
        if not self.safe_create_widgets():
            self.logger.warn("Title widget created with errors - title may not display")

    def _create_widgets(self) -> None:
        """Create and display the title label widget."""
        # Create main container frame
        theme_config = self.styles.get_theme_config()
        title_padding = theme_config['title_padding']  # New configuration needed

        main_frame = SafeWidgetCreator.create_frame(self.parent)
        main_frame.pack(fill=tk.X, padx=title_padding['horizontal'], pady=title_padding['vertical'])

        self.title_label = SafeWidgetCreator.create_label(main_frame, self.title, "Title.TLabel")
        self.title_label.pack(anchor=tk.CENTER)

        # System controls on the right
        if self.scheduler_callback or self.theme_callback:
            self._create_system_controls(main_frame)

    def _create_system_controls(self, parent_frame: ttk.Frame) -> None:
        """Create system control widgets (scheduler and theme switcher)."""
        layout_config = self.styles.LAYOUT_CONFIG()
        title_config = layout_config['widget_positions'].get('title_controls', {})

        # Create controls frame on the right
        controls_frame = SafeWidgetCreator.create_frame(parent_frame)
        controls_pack_config = title_config.get('controls_frame_pack', {'side': 'RIGHT', 'padx': (10, 0)})
        controls_frame.pack(**controls_pack_config)

        # Theme switcher
        if self.theme_callback:
            self._create_theme_control(controls_frame)

        # Scheduler toggle
        if self.scheduler_callback:
            self._create_scheduler_control(controls_frame)

    def _create_theme_control(self, parent_frame: ttk.Frame) -> None:
        """Create theme switcher dropdown."""
        layout_config = self.styles.LAYOUT_CONFIG()
        theme_config = layout_config['widget_positions'].get('title_controls', {}).get('theme_control', {})

        # Theme label
        theme_label = SafeWidgetCreator.create_label(parent_frame, "Theme:", "GrayLabel.TLabel")
        label_pack_config = theme_config.get('label_pack', {'side': 'LEFT', 'padx': (0, 5)})
        theme_label.pack(**label_pack_config)

        # Initialize theme variable
        self.theme_var = tk.StringVar(value="Neutral")

        # Get parent dimensions for ratio-based sizing
        parent_width = parent_frame.winfo_width()
        if parent_width <= 0:  # Handle case where parent hasn't been sized yet
            parent_width = 200  # Default fallback

        # Calculate width using ratio (e.g., 6% of parent width)
        theme_width = max(8, int(0.06 * parent_width))  # Minimum 8 characters

        # Theme dropdown
        self.theme_combobox = SafeWidgetCreator.create_combobox(
            parent_frame,
            textvariable=self.theme_var,
            values=["Neutral", "Optimistic", "Pessimistic"],
            state="readonly",
            width=theme_width
        )
        combobox_pack_config = theme_config.get('combobox_pack', {'side': 'LEFT', 'padx': (0, 10)})
        self.theme_combobox.pack(**combobox_pack_config)
    
        # Bind theme change event
        self.theme_combobox.bind('<<ComboboxSelected>>', self._on_theme_change)

    def _create_scheduler_control(self, parent_frame: ttk.Frame) -> None:
        """Create scheduler toggle control."""        
        # Scheduler toggle
        layout_config = self.styles.LAYOUT_CONFIG()
        scheduler_config = layout_config['widget_positions'].get('title_controls', {}).get('scheduler_control', {})
        
        # Scheduler toggle
        self.scheduler_var = tk.BooleanVar(value=self.config.SCHEDULER["enabled"])
        self.scheduler_checkbox = SafeWidgetCreator.create_checkbutton(
            parent_frame,
            text="Live Updates",
            variable=self.scheduler_var,
            command=self._on_scheduler_toggle
        )
        checkbox_pack_config = scheduler_config.get('checkbox_pack', {'side': 'RIGHT'})
        self.scheduler_checkbox.pack(**checkbox_pack_config)
    
    def _on_theme_change(self, event=None) -> None:
        """Handle theme selection change."""
        try:
            self.logger.info("Theme change event triggered")  # Debug log
            
            selected_theme = self.theme_var.get()
            self.logger.info(f"Selected theme: {selected_theme}")  # Debug log
            
            theme_mapping = {
                "Neutral": "neutral",
                "Optimistic": "optimistic", 
                "Pessimistic": "pessimistic"
            }
            
            theme_name = theme_mapping.get(selected_theme, "neutral")
            self.logger.info(f"Mapped theme name: {theme_name}")  # Debug log
            
            self.logger.info(f"Theme callback exists: {self.theme_callback is not None}")  # Debug log
            
            if self.theme_callback:
                self.theme_callback(theme_name)
                self.logger.info(f"Theme changed to {theme_name}")
            else:
                self.logger.error("Theme callback is None!")
            
        except Exception as e:
            self.logger.error(f"Error handling theme change: {e}")

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

    def set_theme(self, theme_name: str) -> None:
        """Update theme dropdown to reflect current theme.
        
        Args:
            theme_name: Theme name ('neutral', 'optimistic', 'pessimistic')
        """
        if self.theme_var:
            theme_mapping = {
                "neutral": "Neutral",
                "optimistic": "Optimistic",
                "pessimistic": "Pessimistic"
            }
            display_name = theme_mapping.get(theme_name, "Neutral")
            self.theme_var.set(display_name)
    
    @widget_error_handler("title update")
    def update_title(self, new_title: str) -> None:
        """Updates the title text (for future customization)."""
        self.title = new_title

        if self.title_label:
            self.title_label.configure(text=new_title)