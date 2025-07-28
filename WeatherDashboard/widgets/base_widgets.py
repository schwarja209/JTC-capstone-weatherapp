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

from typing import Any, Optional, Callable, Dict
from tkinter import ttk
import functools

from WeatherDashboard.utils.logger import Logger
from WeatherDashboard import config


class BaseWidgetManager:
    """Abstract base class for widget managers with standardized error handling.

    Provides foundational error handling and lifecycle management for widget
    creation. Eliminates duplicate error handling code across widget implementations.

    Attributes:
        parent: Parent frame container
        state: Application state manager
        widget_type: Widget type description for error messages
        _widgets_created: Boolean flag indicating successful widget creation
        _creation_error: Error message if widget creation failed
    """  

    def __init__(self, parent_frame: ttk.Frame, state: Any, widget_type: str = "widgets"):
        """Initialize base widget manager.
        
        Args:
            parent_frame: Parent TTK frame container
            state: Application state manager
            widget_type: Type of widgets for error messages
        """
        # Direct imports for stable utilities
        self.config = config
        self.logger = Logger()

        # Instance data
        self.parent = parent_frame
        self.state = state
        self.widget_type = widget_type
        self._widgets_created = False
        self._creation_error = None
    
    def safe_create_widgets(self) -> bool:
        """Create widgets with standardized error handling.
        
        Returns:
            bool: True if widgets created successfully, False otherwise
        """
        try:
            self._create_widgets()
            self._widgets_created = True
            self._creation_error = None
            self.logger.info(f"{self.widget_type} created successfully")
            return True
            
        except Exception as e:
            self._widgets_created = False
            self._creation_error = str(e)
            self.logger.error(self.config.ERROR_MESSAGES['config_error'].format(
                section=f"{self.widget_type} creation", reason=str(e)))
            return False
    
    def _create_widgets(self) -> None:
        """Override this method to implement widget creation logic."""
        raise NotImplementedError("Subclasses must implement _create_widgets()")
    
    def is_ready(self) -> bool:
        """Check if widgets are ready for use."""
        return self._widgets_created and self._creation_error is None
    
    def get_creation_error(self) -> Optional[str]:
        """Get widget creation error if any."""
        return self._creation_error
    
    def get_alert_popup_parent(self) -> Any:
        """Return the parent widget to be used for alert popups.

        Returns:
            The widget to use as the parent for alert popups, or None if not available.

        Side Effects:
            None.
        """
        if hasattr(self, 'frames') and isinstance(self.frames, dict) and 'title' in self.frames:
            return self.frames['title']
        return None
    
    def update_metric_display(self, metrics: Dict[str, str]) -> None:
        """Update the metric display widgets with the provided metrics.

        Args:
            metrics: Dictionary or data structure containing metric values to display.

        Side Effects:
            Updates the UI to reflect new metric values.
            Logs a warning if widgets are not ready.
        """
        if not self.is_ready():
            self.logger.warn("Cannot update metrics: widgets not ready")
            return

    def update_status_bar(self, city_name: str, error_exception: Optional[Exception]) -> None:
        """Update the status bar widgets with the current city and error status.

        Args:
            city_name: Name of the city to display in the status bar.
            error_exception: Exception object if an error occurred, otherwise None.

        Side Effects:
            Updates the status bar UI elements.
            Logs a warning if widgets are not ready.
        """
        if not self.is_ready():
            self.logger.warn("Cannot update status bar: widgets not ready")
            return

    def update_alerts(self, raw_data: Dict[str, Any]) -> None:
        """Update the alert display widgets with the provided raw weather data.

        Args:
            raw_data: Dictionary or data structure containing raw weather data for alert processing.

        Side Effects:
            Updates the alert UI elements.
            Logs a warning if widgets are not ready.
        """
        if not self.is_ready():
            self.logger.warn("Cannot update alerts: widgets not ready")
            return

def widget_error_handler(widget_type: str = "widget"):
    """Decorator for standardized widget method error handling.
    
    Args:
        widget_type: Type of widget for error messages
        
    Returns:
        Decorator function
    """
    logger = Logger() # create instance

    def decorator(func: Callable) -> Callable:
        """Decorator implementation with error handling wrapper.
    
        Wraps the target function with standardized error logging and re-raising
        to maintain proper exception propagation while ensuring consistent error
        reporting across all widget operations.
        
        Args:
            func: Function to wrap with error handling
            
        Returns:
            Callable: Wrapped function with error handling
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Import config here since it's not available in decorator scope
                from WeatherDashboard import config
                logger.error(config.ERROR_MESSAGES['config_error'].format(section=f"{widget_type} {func.__name__}", reason=str(e)))
                # Re-raise for calling code to handle
                raise
        return wrapper
    return decorator

class SafeWidgetCreator:
    """Utility class for safe widget creation with consistent error handling."""
    
    @staticmethod
    @widget_error_handler("label")
    def create_label(parent: ttk.Frame, text: str, style: str = "TLabel", **kwargs) -> ttk.Label:
        """Create label with error handling."""
        return ttk.Label(parent, text=text, style=style, **kwargs) # kwargs = Additional label options
    
    @staticmethod
    @widget_error_handler("button")
    def create_button(parent: ttk.Frame, text: str, command: Callable, style: str = "TButton", **kwargs) -> ttk.Button:
        """Create button with error handling."""
        return ttk.Button(parent, text=text, command=command, style=style, **kwargs)
    
    @staticmethod
    @widget_error_handler("entry")
    def create_entry(parent: ttk.Frame, textvariable: Any = None, **kwargs) -> ttk.Entry:
        """Create entry with error handling."""
        return ttk.Entry(parent, textvariable=textvariable, **kwargs)
    
    @staticmethod
    @widget_error_handler("combobox")
    def create_combobox(parent: ttk.Frame, textvariable: Any = None, state: str = "readonly", **kwargs) -> ttk.Combobox:
        """Create combobox with error handling."""
        return ttk.Combobox(parent, textvariable=textvariable, state=state, **kwargs)
    
    @staticmethod
    @widget_error_handler("checkbutton")
    def create_checkbutton(parent: ttk.Frame, text: str, variable: Any, command: Optional[Callable] = None, **kwargs) -> ttk.Checkbutton:
        """Create checkbutton with error handling."""
        return ttk.Checkbutton(parent, text=text, variable=variable, command=command, **kwargs)
    
    @staticmethod
    @widget_error_handler("radiobutton")
    def create_radiobutton(parent: ttk.Frame, text: str, variable: Any, value: Any, **kwargs) -> ttk.Radiobutton:
        """Create radiobutton with error handling."""
        return ttk.Radiobutton(parent, text=text, variable=variable, value=value, **kwargs)
    
    @staticmethod
    @widget_error_handler("frame")
    def create_frame(parent: ttk.Frame, **kwargs) -> ttk.Frame:
        """Create frame with error handling."""
        return ttk.Frame(parent, **kwargs)

# Example usage for existing widget classes:
# class ExampleRefactoredWidgetManager(BaseWidgetManager):
#     """Example of how to refactor existing widget managers."""
    
#     def __init__(self, parent_frame: ttk.Frame, state: Any):
#         super().__init__(parent_frame, state, "example widgets")
        
#         # Widget references
#         self.label1 = None
#         self.button1 = None
        
#         # Create widgets with error handling
#         if not self.safe_create_widgets():
#             Logger.warn("Example widgets created with errors - some functionality may be limited")
    
#     def _create_widgets(self) -> None:
#         """Implementation of widget creation - will be called with error handling."""
#         # This method is automatically wrapped with error handling by BaseWidgetManager
#         self.label1 = SafeWidgetCreator.create_label(self.parent, "Example Label")
#         self.button1 = SafeWidgetCreator.create_button(self.parent, "Example Button", self._button_clicked)
        
#         # Position widgets
#         self.label1.grid(row=0, column=0, pady=5)
#         self.button1.grid(row=1, column=0, pady=5)
    
#     @widget_error_handler("button callback")
#     def _button_clicked(self) -> None:
#         """Example button callback with error handling."""
#         Logger.info("Example button clicked")