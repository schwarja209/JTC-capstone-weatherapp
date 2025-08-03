"""
Widget registry for centralized widget management and runtime manipulation.

This module provides a centralized registry system for managing all widgets
in the Weather Dashboard application. Enables runtime style changes, widget
movement, and dynamic layout management.

Classes:
    WidgetRegistry: Centralized widget management and runtime manipulation
    WidgetInfo: Container for widget metadata and state
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, List

from WeatherDashboard import styles
from WeatherDashboard.utils.logger import Logger


class WidgetInfo:
    """Container for widget metadata and state information.
    
    Stores widget reference, type, parent frame, current position,
    and style information for runtime manipulation.
    
    Attributes:
        widget: The actual widget object
        widget_type: Type/category of the widget
        parent_frame: Parent frame containing the widget
        current_position: Current grid/pack position
        current_style: Current style applied to widget
        is_visible: Whether widget is currently visible
        metadata: Additional widget-specific information
    """
    
    def __init__(self, widget: Any, widget_type: str, parent_frame: ttk.Frame, 
                 position: Dict[str, Any], style: str = None):
        """Initialize widget information container.
        
        Args:
            widget: The actual widget object
            widget_type: Type/category of the widget
            parent_frame: Parent frame containing the widget
            position: Current position (grid or pack info)
            style: Current style applied to widget
        """
        self.widget = widget
        self.widget_type = widget_type
        self.parent_frame = parent_frame
        self.current_position = position
        self.current_style = style
        self.is_visible = True
        self.metadata = {}


class WidgetRegistry:
    """Centralized widget management and runtime manipulation system.
    
    Provides a unified interface for registering, accessing, and manipulating
    widgets at runtime. Enables dynamic style changes, widget movement,
    and responsive layout management.
    
    Attributes:
        widgets: Dictionary of registered widgets by ID
        widget_types: Dictionary of widgets grouped by type
        frames: Dictionary of frame containers
        styles: Application styles configuration
        logger: Application logger
    """
    
    def __init__(self):
        """Initialize the widget registry."""
        self.widgets: Dict[str, WidgetInfo] = {}
        self.widget_types: Dict[str, List[str]] = {}
        self.frames: Dict[str, ttk.Frame] = {}
        self.styles = styles
        self.logger = Logger()
    
    def register_widget(self, widget_id: str, widget: Any, widget_type: str, 
                       parent_frame: ttk.Frame, position: Dict[str, Any], 
                       style: str = None) -> None:
        """Register a widget with the registry.
        
        Args:
            widget_id: Unique identifier for the widget
            widget: The widget object to register
            widget_type: Type/category of the widget
            parent_frame: Parent frame containing the widget
            position: Current position (grid or pack info)
            style: Current style applied to widget
        """
        widget_info = WidgetInfo(widget, widget_type, parent_frame, position, style)
        self.widgets[widget_id] = widget_info
        
        # Group by type for easy access
        if widget_type not in self.widget_types:
            self.widget_types[widget_type] = []
        self.widget_types[widget_type].append(widget_id)
        
        self.logger.info(f"Registered widget: {widget_id} (type: {widget_type})")
    
    def register_frame(self, frame_id: str, frame: ttk.Frame) -> None:
        """Register a frame with the registry.
        
        Args:
            frame_id: Unique identifier for the frame
            frame: The frame object to register
        """
        self.frames[frame_id] = frame
        self.logger.info(f"Registered frame: {frame_id}")
    
    def get_widget(self, widget_id: str) -> Optional[Any]:
        """Get a widget by ID.
        
        Args:
            widget_id: Unique identifier for the widget
            
        Returns:
            The widget object or None if not found
        """
        widget_info = self.widgets.get(widget_id)
        return widget_info.widget if widget_info else None
    
    def get_widget_info(self, widget_id: str) -> Optional[WidgetInfo]:
        """Get widget information by ID.
        
        Args:
            widget_id: Unique identifier for the widget
            
        Returns:
            WidgetInfo object or None if not found
        """
        return self.widgets.get(widget_id)
    
    def get_widgets_by_type(self, widget_type: str) -> List[Any]:
        """Get all widgets of a specific type.
        
        Args:
            widget_type: Type of widgets to retrieve
            
        Returns:
            List of widget objects of the specified type
        """
        widget_ids = self.widget_types.get(widget_type, [])
        return [self.widgets[widget_id].widget for widget_id in widget_ids 
                if widget_id in self.widgets]
    
    def get_all_widgets(self) -> Dict[str, Any]:
        """Get all registered widgets.
        
        Returns:
            Dictionary mapping widget IDs to widget objects
        """
        return {widget_id: info.widget for widget_id, info in self.widgets.items()}
    
    # STYLE MANAGEMENT
    def apply_style_to_widget(self, widget_id: str, style: str) -> bool:
        """Apply a style to a specific widget.
        
        Args:
            widget_id: Unique identifier for the widget
            style: Style to apply
            
        Returns:
            True if style applied successfully, False otherwise
        """
        widget_info = self.widgets.get(widget_id)
        if not widget_info:
            self.logger.warn(f"Widget not found: {widget_id}")
            return False
        
        try:
            widget_info.widget.configure(style=style)
            widget_info.current_style = style
            self.logger.info(f"Applied style '{style}' to widget '{widget_id}'")
            return True
        except Exception as e:
            self.logger.error(f"Failed to apply style '{style}' to widget '{widget_id}': {e}")
            return False
    
    def apply_style_to_type(self, widget_type: str, style: str) -> int:
        """Apply a style to all widgets of a specific type.
        
        Args:
            widget_type: Type of widgets to style
            style: Style to apply
            
        Returns:
            Number of widgets successfully styled
        """
        widget_ids = self.widget_types.get(widget_type, [])
        success_count = 0
        
        for widget_id in widget_ids:
            if self.apply_style_to_widget(widget_id, style):
                success_count += 1
        
        self.logger.info(f"Applied style '{style}' to {success_count} widgets of type '{widget_type}'")
        return success_count
    
    def apply_style_to_all(self, style: str) -> int:
        """Apply a style to all registered widgets.
        
        Args:
            style: Style to apply
            
        Returns:
            Number of widgets successfully styled
        """
        success_count = 0
        for widget_id in self.widgets:
            if self.apply_style_to_widget(widget_id, style):
                success_count += 1
        
        self.logger.info(f"Applied style '{style}' to {success_count} widgets")
        return success_count
    
    # WIDGET MOVEMENT
    def move_widget(self, widget_id: str, new_frame_id: str, 
                   new_position: Dict[str, Any]) -> bool:
        """Move a widget to a different frame and position.
        
        Args:
            widget_id: Unique identifier for the widget
            new_frame_id: ID of the frame to move widget to
            new_position: New position (grid or pack info)
            
        Returns:
            True if widget moved successfully, False otherwise
        """
        widget_info = self.widgets.get(widget_id)
        new_frame = self.frames.get(new_frame_id)
        
        if not widget_info or not new_frame:
            self.logger.warn(f"Widget or frame not found: {widget_id}, {new_frame_id}")
            return False
        
        try:
            # Remove from current parent
            widget_info.widget.pack_forget()
            widget_info.widget.grid_forget()
            
            # Add to new parent
            if 'pack' in new_position:
                widget_info.widget.pack(**new_position['pack'])
            elif 'grid' in new_position:
                widget_info.widget.grid(**new_position['grid'])
            
            # Update widget info
            widget_info.parent_frame = new_frame
            widget_info.current_position = new_position
            
            self.logger.info(f"Moved widget '{widget_id}' to frame '{new_frame_id}'")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to move widget '{widget_id}': {e}")
            return False
    
    def reposition_widget(self, widget_id: str, new_position: Dict[str, Any]) -> bool:
        """Reposition a widget within its current frame.
        
        Args:
            widget_id: Unique identifier for the widget
            new_position: New position (grid or pack info)
            
        Returns:
            True if widget repositioned successfully, False otherwise
        """
        widget_info = self.widgets.get(widget_id)
        if not widget_info:
            self.logger.warn(f"Widget not found: {widget_id}")
            return False
        
        try:
            # Remove current positioning
            widget_info.widget.pack_forget()
            widget_info.widget.grid_forget()
            
            # Apply new positioning
            if 'pack' in new_position:
                widget_info.widget.pack(**new_position['pack'])
            elif 'grid' in new_position:
                widget_info.widget.grid(**new_position['grid'])
            
            widget_info.current_position = new_position
            self.logger.info(f"Repositioned widget '{widget_id}'")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to reposition widget '{widget_id}': {e}")
            return False
    
    # VISIBILITY CONTROL
    def show_widget(self, widget_id: str) -> bool:
        """Show a widget.
        
        Args:
            widget_id: Unique identifier for the widget
            
        Returns:
            True if widget shown successfully, False otherwise
        """
        widget_info = self.widgets.get(widget_id)
        if not widget_info:
            self.logger.warn(f"Widget not found: {widget_id}")
            return False
        
        try:
            widget_info.widget.pack()
            widget_info.is_visible = True
            self.logger.info(f"Showed widget '{widget_id}'")
            return True
        except Exception as e:
            self.logger.error(f"Failed to show widget '{widget_id}': {e}")
            return False
    
    def hide_widget(self, widget_id: str) -> bool:
        """Hide a widget.
        
        Args:
            widget_id: Unique identifier for the widget
            
        Returns:
            True if widget hidden successfully, False otherwise
        """
        widget_info = self.widgets.get(widget_id)
        if not widget_info:
            self.logger.warn(f"Widget not found: {widget_id}")
            return False
        
        try:
            widget_info.widget.pack_forget()
            widget_info.is_visible = False
            self.logger.info(f"Hidden widget '{widget_id}'")
            return True
        except Exception as e:
            self.logger.error(f"Failed to hide widget '{widget_id}': {e}")
            return False
    
    # THEME SWITCHING
    def switch_theme(self, theme_name: str) -> int:
        """Switch the application theme.
        
        Args:
            theme_name: Name of the theme to switch to
            
        Returns:
            Number of widgets successfully updated
        """
        # This would integrate with your existing theme system
        # For now, just apply a style to all widgets
        return self.apply_style_to_all(theme_name)
    
    # RESPONSIVE LAYOUT
    def adapt_to_window_size(self, width: int, height: int) -> None:
        """Adapt layout to window size changes.
        
        Args:
            width: New window width
            height: New window height
        """
        # This would implement responsive layout logic
        # For now, just log the size change
        self.logger.info(f"Window resized to {width}x{height}")
    
    def enable_responsive_mode(self) -> None:
        """Enable responsive layout mode."""
        self.logger.info("Responsive mode enabled")
    
    def disable_responsive_mode(self) -> None:
        """Disable responsive layout mode."""
        self.logger.info("Responsive mode disabled")