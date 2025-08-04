"""
Centralized dialog management surface module.

This module provides a unified interface for all dialog/message display
throughout the application, ensuring consistent theming and behavior.
"""

import tkinter.messagebox as messagebox
from typing import Optional, Dict, Any

from WeatherDashboard import styles
from WeatherDashboard.services.error_handler import WeatherErrorHandler


class DialogManager:
    """Centralized dialog management with theme-aware styling."""
    
    def __init__(self):
        """Initialize dialog manager with theme-aware configuration."""
        self.styles = styles
        self.error_handler = WeatherErrorHandler()
    
    def show_theme_aware_dialog(self, dialog_type: str, title_key: str, message: str, **kwargs) -> None:
        """Show dialog using theme-aware configuration with template support."""
        try:
            dialog_config = self.styles.DIALOG_CONFIG()
            dialog_method = dialog_config['dialog_types'][dialog_type]
            dialog_title = dialog_config['dialog_titles'][title_key]
            
            # Format message with template if kwargs provided
            if kwargs:
                template = dialog_config.get('error_templates', {}).get(title_key, message)
                formatted_message = template.format(**kwargs)
            else:
                formatted_message = message
                
            getattr(messagebox, dialog_method)(dialog_title, formatted_message)
        except (KeyError, AttributeError):
            # Fallback to standard dialog
            fallback_method = getattr(messagebox, f"show{dialog_type}")
            fallback_method(title_key, message)

    def show_info(self, title: str, message: str) -> None:
        """Show info dialog with theme-aware styling."""
        self.show_theme_aware_dialog('info', 'notice', message)

    def show_warning(self, title: str, message: str) -> None:
        """Show warning dialog with theme-aware styling."""
        self.show_theme_aware_dialog('warning', 'notice', message)

    def show_error(self, title: str, message: str) -> None:
        """Show error dialog with theme-aware styling."""
        self.show_theme_aware_dialog('error', 'general_error', message)


# Global instance
dialog_manager = DialogManager()