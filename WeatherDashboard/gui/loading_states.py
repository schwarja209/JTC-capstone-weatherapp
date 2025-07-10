"""
Loading state management for async operations.
"""

from typing import Optional, Callable, Dict, Any
import tkinter as tk
from tkinter import ttk
import threading
import time


class LoadingStateManager:
    """Manages loading indicators and button states during async operations."""
    
    def __init__(self, state: Any) -> None:
        self.state = state
        self.is_loading = False
        self.loading_widgets: Dict[str, ttk.Widget] = {}
        self.original_button_states: Dict[str, str] = {}
    
    def start_loading(self, operation_name: str = "Loading...") -> None:
        """Starts loading state - disables buttons, shows spinner."""
        if self.is_loading:
            return  # Already loading
        
        self.is_loading = True
        self._disable_buttons()
        self._show_loading_status(operation_name)
        self._start_progress_indicator()
    
    def stop_loading(self) -> None:
        """Stops loading state - re-enables buttons, hides spinner."""
        if not self.is_loading:
            return
        
        self.is_loading = False
        self._enable_buttons()
        self._hide_loading_status()
        self._stop_progress_indicator()
    
    def _disable_buttons(self) -> None:
        """Disables interactive buttons during loading."""
        # Store original states and disable buttons
        buttons_to_disable = ['update_button', 'reset_button']
        
        for button_name in buttons_to_disable:
            button = getattr(self.state, button_name, None)
            if button:
                self.original_button_states[button_name] = str(button['state'])
                button.configure(state='disabled')
    
    def _enable_buttons(self) -> None:
        """Re-enables buttons after loading."""
        for button_name, original_state in self.original_button_states.items():
            button = getattr(self.state, button_name, None)
            if button:
                button.configure(state=original_state)
        
        self.original_button_states.clear()
    
    def _show_loading_status(self, message: str) -> None:
        """Shows loading message in status label."""
        if self.state.status_label:
            self.state.status_label.configure(
                text=f"🔄 {message}", 
                foreground="blue"
            )
    
    def _hide_loading_status(self) -> None:
        """Hides loading message."""
        if self.state.status_label:
            self.state.status_label.configure(text="", foreground="red")
    
    def _start_progress_indicator(self) -> None:
        """Starts a simple progress animation."""
        if hasattr(self.state, 'progress_var'):
            self.state.progress_var.set("⏳ Fetching weather data...")
    
    def _stop_progress_indicator(self) -> None:
        """Stops progress animation."""
        if hasattr(self.state, 'progress_var'):
            self.state.progress_var.set("")


class AsyncWeatherOperation:
    """Handles async weather operations with proper threading."""
    
    def __init__(self, controller: Any, loading_manager: LoadingStateManager) -> None:
        self.controller = controller
        self.loading_manager = loading_manager
    
    def fetch_weather_async(self, city_name: str, unit_system: str, on_complete: Optional[Callable] = None) -> None:
        """Fetches weather data in background thread."""
        
        def background_task():
            try:
                # Start loading in main thread
                self._schedule_ui_update(self.loading_manager.start_loading, "Fetching weather...")
                
                # Do the actual work in background
                success = self.controller.update_weather_display(city_name, unit_system)
                
                # Handle completion in main thread
                def complete_task():
                    self.loading_manager.stop_loading()
                    if on_complete:
                        on_complete(success)
                
                self._schedule_ui_update(complete_task)
                
            except Exception as e:
                # Handle errors in main thread
                def handle_error():
                    self.loading_manager.stop_loading()
                    if self.controller.error_handler:
                        self.controller.error_handler.handle_unexpected_error(str(e))
                
                self._schedule_ui_update(handle_error)
        
        # Start background thread
        thread = threading.Thread(target=background_task, daemon=True)
        thread.start()
    
    def fetch_chart_async(self, on_complete: Optional[Callable] = None) -> None:
        """Updates chart in background thread."""
        
        def background_task():
            try:
                self._schedule_ui_update(self.loading_manager.start_loading, "Updating chart...")
                
                # Update chart in background
                self.controller.update_chart()
                
                def complete_task():
                    self.loading_manager.stop_loading()
                    if on_complete:
                        on_complete(True)
                
                self._schedule_ui_update(complete_task)
                
            except Exception as e:
                def handle_error():
                    self.loading_manager.stop_loading()
                    if on_complete:
                        on_complete(False)
                
                self._schedule_ui_update(handle_error)
        
        thread = threading.Thread(target=background_task, daemon=True)
        thread.start()
    
    def _schedule_ui_update(self, func: Callable, *args) -> None:
        """Safely schedules UI updates from background thread."""
        # Use tkinter's thread-safe method to update UI
        if hasattr(self.controller.state, 'city_label') and self.controller.state.city_label:
            root = self.controller.state.city_label.winfo_toplevel()
            root.after_idle(lambda: func(*args))


# Progress widget
class ProgressWidget:
    """A simple progress indicator widget."""
    def __init__(self, parent: ttk.Frame) -> None:
        self.parent = parent
        self.progress_var = tk.StringVar()
        self.progress_label = ttk.Label(parent, textvariable=self.progress_var)
        self.progress_label.pack(pady=5)
    
    def show_progress(self, message: str) -> None:
        """Shows progress message."""
        self.progress_var.set(message)
        self.progress_label.configure(foreground="blue")
    
    def hide_progress(self) -> None:
        """Hides progress message."""
        self.progress_var.set("")