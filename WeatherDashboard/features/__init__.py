"""
Feature modules for the Weather Dashboard application.

This package contains specialized feature implementations including
alert systems, theme management, and future extensibility modules
for enhanced functionality.

Modules:
    alerts: Weather alert processing and notification system
    history: Weather history data gathering, organizing, storage and access
    theme_switcher: Theme management and UI appearance control
    tomorrows_guess: Weather prediction and forecasting features
"""

__all__ = [
    "theme_switcher",
    "tomorrows_guess", 
    "alerts",
    "history"
]