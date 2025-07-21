"""
Base widget classes with standardized error handling for the Weather Dashboard application.

This module provides foundational widget management classes and utilities for creating
robust GUI components with consistent error handling, lifecycle management, and safe
widget creation patterns. Eliminates duplicate error handling code across all widget
implementations.

Classes:
    BaseWidgetManager: Abstract base class for widget managers with error handling
    SafeWidgetCreator: Utility class for safe widget creation with error wrapping
    ExampleRefactoredWidgetManager: Example implementation showing migration patterns

Functions:
    widget_error_handler: Decorator for standardized widget method error handling
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, Tuple

from WeatherDashboard import styles
from WeatherDashboard.utils.logger import Logger

class WidgetUtils:
    """Centralized widget positioning and creation utilities."""
    
    @staticmethod
    def position_widget_pair(parent: ttk.Frame, 
                           label_widget: ttk.Widget, 
                           value_widget: ttk.Widget,
                           row: int, 
                           label_col: int, 
                           value_col: int,
                           label_text: str = "",
                           sticky: str = tk.W,
                           pady: int = 5,
                           padx_override: Optional[int] = None) -> None:
        """Position a label/value widget pair in grid layout.
        
        Consolidates the repeated grid positioning logic from multiple files.
        
        Args:
            parent: Parent frame container
            label_widget: Label widget to position
            value_widget: Value widget to position  
            row: Grid row position
            label_col: Grid column for label
            value_col: Grid column for value
            label_text: Text to set on label (optional)
            sticky: Grid sticky option (default tk.W)
            pady: Vertical padding (default 5)
            padx_override: Override automatic padding calculation
        """
        try:
            # Set label text if provided
            if label_text and hasattr(label_widget, 'configure'):
                label_widget.configure(text=label_text)
            
            # Calculate padding based on column position
            if padx_override is not None:
                padx = padx_override
            else:
                # Use style-based padding calculation
                padx = (styles.ALERT_DISPLAY_CONFIG['column_padding']['right_section'] 
                       if label_col >= 4 
                       else styles.ALERT_DISPLAY_CONFIG['column_padding']['left_section'])
            
            # Position widgets
            label_widget.grid(row=row, column=label_col, sticky=sticky, pady=pady, padx=padx)
            value_widget.grid(row=row, column=value_col, sticky=sticky, pady=pady)
            
        except Exception as e:
            Logger.error(f"Failed to position widget pair at row {row}: {e}")
    
    @staticmethod
    def create_label_value_pair(parent: ttk.Frame, 
                               label_text: str,
                               value_text: str = "--",
                               label_style: str = "LabelName.TLabel",
                               value_style: str = "LabelValue.TLabel") -> Tuple[ttk.Label, ttk.Label]:
        """Create a standardized label/value widget pair.
        
        Args:
            parent: Parent frame container
            label_text: Text for the label widget
            value_text: Initial text for value widget (default "--")
            label_style: TTK style for label (default "LabelName.TLabel")
            value_style: TTK style for value (default "LabelValue.TLabel")
            
        Returns:
            Tuple[ttk.Label, ttk.Label]: Label widget, value widget
        """
        try:
            label_widget = ttk.Label(parent, text=label_text, style=label_style)
            value_widget = ttk.Label(parent, text=value_text, style=value_style)
            return label_widget, value_widget
        except Exception as e:
            Logger.error(f"Failed to create label/value pair for '{label_text}': {e}")
            # Return minimal fallback widgets
            label_widget = ttk.Label(parent, text=label_text)
            value_widget = ttk.Label(parent, text=value_text)
            return label_widget, value_widget
    
    @staticmethod
    def create_and_position_metric(parent: ttk.Frame,
                                 metric_key: str,
                                 label_text: str,
                                 value_text: str,
                                 row: int,
                                 label_col: int,
                                 value_col: int,
                                 widget_storage: Optional[Dict[str, Dict[str, ttk.Label]]] = None) -> Tuple[ttk.Label, ttk.Label]:
        """Create and position a metric display in one step.
        
        Combines widget creation and positioning into a single utility function.
        
        Args:
            parent: Parent frame container
            metric_key: Metric identifier for storage
            label_text: Display text for label
            value_text: Display text for value
            row: Grid row position
            label_col: Grid column for label
            value_col: Grid column for value
            widget_storage: Optional dict to store widget references
            
        Returns:
            Tuple[ttk.Label, ttk.Label]: Created label and value widgets
        """
        # Create widgets
        label_widget, value_widget = WidgetUtils.create_label_value_pair(
            parent, label_text, value_text)
        
        # Position widgets
        WidgetUtils.position_widget_pair(
            parent, label_widget, value_widget, row, label_col, value_col)
        
        # Store in provided storage dict
        if widget_storage is not None:
            widget_storage[metric_key] = {
                'label': label_widget,
                'value': value_widget
            }
        
        return label_widget, value_widget
    
    @staticmethod
    def safe_grid_forget(widget: ttk.Widget) -> None:
        """Safely remove widget from grid layout.
        
        Args:
            widget: Widget to remove from grid
        """
        try:
            if widget and hasattr(widget, 'grid_forget'):
                widget.grid_forget()
        except Exception as e:
            Logger.warn(f"Failed to grid_forget widget: {e}")
    
    @staticmethod
    def configure_grid_weights(parent: ttk.Frame, columns: int = 3) -> None:
        """Configure grid column weights for proper layout.
        
        Args:
            parent: Parent frame to configure
            columns: Number of columns to configure (default 3)
        """
        try:
            for i in range(columns):
                parent.columnconfigure(i, weight=1)
        except Exception as e:
            Logger.error(f"Failed to configure grid weights: {e}")
            
    @staticmethod  
    def create_error_handling_wrapper(widget_creation_func):
        """Decorator to add consistent error handling to widget creation functions.
        
        Args:
            widget_creation_func: Function to wrap with error handling
            
        Returns:
            Wrapped function with error handling
        """
        def wrapper(*args, **kwargs):
            try:
                return widget_creation_func(*args, **kwargs)
            except Exception as e:
                function_name = getattr(widget_creation_func, '__name__', 'unknown_function')
                Logger.error(f"Failed to create widgets in {function_name}: {e}")
                raise
        return wrapper