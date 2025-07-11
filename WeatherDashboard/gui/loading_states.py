"""
Loading state management for async operations.
"""

from typing import Optional, Callable, Dict, Any
import tkinter as tk
from tkinter import ttk
import threading

from WeatherDashboard.services.api_exceptions import ValidationError
from WeatherDashboard.utils.logger import Logger


class LoadingStateManager:
    """Manages loading indicators and button states during async operations."""
    
    def __init__(self, state: Any) -> None:
        self.state = state
        self.is_loading = False
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
    
    def update_progress(self, message: str) -> None:
        """Updates progress message during ongoing operation."""
        if not self.is_loading:
            return  # Don't update if not in loading state
        
        self._show_loading_status(message)
    
    def _disable_buttons(self) -> None:
        """Disables interactive buttons during loading."""
        # Store original states and disable buttons
        buttons_to_disable = ['update_button', 'reset_button']
        
        for button_name in buttons_to_disable:
            button = getattr(self.state, button_name, None)
            if button:
                self.original_button_states[button_name] = str(button.cget('state'))
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
    """Handles async weather operations with proper threading and cancellation support."""
    
    def __init__(self, controller: Any, loading_manager: LoadingStateManager) -> None:
        self.controller = controller
        self.loading_manager = loading_manager
        self.current_thread: Optional[threading.Thread] = None
        self.cancel_event = threading.Event()
    
    def cancel_current_operation(self) -> None:
        """Cancel the currently running operation."""
        if self.current_thread and self.current_thread.is_alive():
            self.cancel_event.set()
            Logger.info("Cancelling current weather operation")
            # Stop loading UI state
            self._schedule_ui_update(self.loading_manager.stop_loading)
    
    def fetch_weather_async(self, city_name: str, unit_system: str, on_complete: Optional[Callable] = None) -> None:
        """Fetches weather data in background thread with cancellation support."""
        
        # Cancel any existing operation first
        self.cancel_current_operation()
        self.cancel_event.clear()
        
        def background_task():
            try:
                # Check for cancellation before starting
                if self.cancel_event.is_set():
                    return
                
                # Step 1: Start loading
                self._schedule_ui_update(self.loading_manager.start_loading, "Initializing...")
                
                # Step 2: Input validation (simulated delay for demonstration)
                if self.cancel_event.is_set():
                    return
                self._schedule_ui_update(self.loading_manager.update_progress, "Validating input...")
                
                # Step 3: API call
                if self.cancel_event.is_set():
                    return
                self._schedule_ui_update(self.loading_manager.update_progress, "Fetching weather data...")
                
                # Do the actual work in background
                success = self.controller.update_weather_display(city_name, unit_system)
                
                # Step 4: Processing data
                if self.cancel_event.is_set():
                    return
                self._schedule_ui_update(self.loading_manager.update_progress, "Processing weather data...")
                
                # Check for cancellation before completion
                if self.cancel_event.is_set():
                    self._schedule_ui_update(self.loading_manager.stop_loading)
                    return
                
                # Handle completion in main thread
                def complete_task():
                    self.loading_manager.stop_loading()
                    if on_complete:
                        on_complete(success)
                
                self._schedule_ui_update(complete_task)
                
            except (ConnectionError, TimeoutError) as e:
                if self.cancel_event.is_set():
                    return  # Don't show error if operation was cancelled
                
                def handle_network_error():
                    self.loading_manager.stop_loading()
                    if hasattr(self.controller, 'error_handler') and self.controller.error_handler:
                        from WeatherDashboard.services.api_exceptions import NetworkError
                        network_error = NetworkError(f"Network error during async operation: {e}")
                        self.controller.error_handler.handle_weather_error(network_error, city_name)
                
                self._schedule_ui_update(handle_network_error)

            except ValidationError as e:
                if self.cancel_event.is_set():
                    return
                
                def handle_validation_error():
                    self.loading_manager.stop_loading()
                    if hasattr(self.controller, 'error_handler') and self.controller.error_handler:
                        self.controller.error_handler.handle_input_validation_error(str(e))
                
                self._schedule_ui_update(handle_validation_error)

            except Exception as e:
                if self.cancel_event.is_set():
                    return
                
                def handle_unexpected_error():
                    self.loading_manager.stop_loading()
                    if hasattr(self.controller, 'error_handler') and self.controller.error_handler:
                        self.controller.error_handler.handle_unexpected_error(str(e))
                
                self._schedule_ui_update(handle_unexpected_error)
        
        # Start background thread and store reference
        self.current_thread = threading.Thread(target=background_task, daemon=True)
        self.current_thread.start()
    
    def _schedule_ui_update(self, func: Callable, *args) -> None:
        """Safely schedules UI updates from background thread."""
        try:
            if hasattr(self, 'controller') and self.controller and hasattr(self.controller, 'state'):
                state = self.controller.state
                if hasattr(state, 'city_label') and state.city_label:
                    try:
                        root = state.city_label.winfo_toplevel()
                        root.after_idle(lambda: func(*args))
                        return
                    except tk.TclError:
                        # Widget was destroyed, fall back to direct call
                        pass
            # Fallback: execute directly (not thread-safe but won't crash)
            func(*args)
        except Exception as e:
            print(f"Error scheduling UI update: {e}")