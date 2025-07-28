"""
Loading state management for async operations.

This module provides classes for managing UI loading states during background
operations, including button state management, progress indicators, and
thread-safe UI updates for async weather data fetching.

Classes:
    LoadingStateManager: Manages UI loading indicators and button states
    AsyncWeatherOperation: Handles async weather operations with threading
"""

from typing import Optional, Callable, Dict, Any
import tkinter as tk
import threading

from WeatherDashboard import styles
from WeatherDashboard.utils.logger import Logger

from WeatherDashboard.services.api_exceptions import ValidationError, NetworkError, RateLimitError
from WeatherDashboard.widgets.status_bar_widgets import StatusBarWidgets


class LoadingStateManager:
    """Manages loading indicators and button states during async operations.
    
    Provides methods to show/hide loading indicators, disable/enable UI controls,
    and manage progress messages during background operations.
    
    Attributes:
        state: Application state manager containing UI widget references
        is_loading: Boolean flag indicating if currently in loading state
        original_button_states: Dictionary storing original button states for restoration
    """

    BUTTONS_TO_DISABLE = ['update_button', 'reset_button'] # for later use during loading
    
    def __init__(self, state: Any, status_bar_widgets: StatusBarWidgets) -> None:
        """Initialize the loading state manager.

        Args:
            state: Application state manager containing UI widget references (injected for testability)
            status_bar_widgets: Status bar widgets for UI updates (injected for testability)
        """
        # Direct imports for stable utilities
        self.logger = Logger()
        self.styles = styles

        # Injected dependencies for testable components
        self.state = state
        self.status_bar_widgets = status_bar_widgets

        # Internal state
        self.is_loading = False
        self.original_button_states: Dict[str, str] = {}
    
    def start_loading(self, operation_name: str = "Loading...") -> None:
        """Start loading state - disables buttons, shows spinner."""
        self._last_error = False  # Reset error flag at the start of a new operation

        if self.is_loading:
            return  # Already loading
        
        self.is_loading = True
        self._disable_buttons()
        self._show_loading_status(operation_name)
        self._start_progress_indicator()
    
    def stop_loading(self) -> None:
        """Stop loading state - re-enables buttons, hides spinner."""
        if not self.is_loading:
            return
        
        self.is_loading = False
        self._enable_buttons()
        
        # Only clear progress if there was no error
        if not getattr(self, "_last_error", False):
            self._hide_loading_status()
            self._stop_progress_indicator()
    
    def update_progress(self, message: str) -> None:
        """Update progress message during ongoing operation."""
        if not self.is_loading:
            return  # Don't update if not in loading state
        
        self._show_loading_status(message)
    
    def show_error(self, message: str) -> None:
        """Display an error message in the status bar and set error flag."""
        self.logger.info(f"show_error called with: {message}")
        self.status_bar_widgets.update_progress(message, error=True)
        self._last_error = True
    
    def _disable_buttons(self) -> None:
        """Disable interactive buttons during loading.
        
        Stores original button states and sets buttons to disabled state.
        Handles UI errors gracefully if buttons are not available.
        """        
        for button_name in self.BUTTONS_TO_DISABLE:
            try:
                button = getattr(self.state, button_name, None)
                if button and hasattr(button, 'cget') and hasattr(button, 'configure'):
                    self.original_button_states[button_name] = str(button.cget('state'))
                    button.configure(state='disabled')
            except (tk.TclError, AttributeError) as e:
                self.logger.warn(f"Failed to disable button {button_name}: {e}")
    
    def _enable_buttons(self) -> None:
        """Re-enable buttons after loading.
        
        Restores buttons to their original states and clears the state cache.
        Handles UI errors gracefully if buttons are not available.
        """
        for button_name in self.BUTTONS_TO_DISABLE:
            try:
                button = getattr(self.state, button_name, None)
                if button and hasattr(button, 'configure'):
                    original_state = self.original_button_states.get(button_name, 'normal')
                    button.configure(state=original_state)
            except (tk.TclError, AttributeError) as e:
                self.logger.warn(f"Failed to re-enable button {button_name}: {e}")
        
        self.original_button_states.clear()
    
    def _show_loading_status(self, message: str) -> None:
        """Show loading message in status label."""
        try:
            icon = self.styles.LOADING_CONFIG['icons']['progress']
            #color = self.styles.LOADING_CONFIG['colors']['loading']
            self.status_bar_widgets.update_progress(f"{icon} {message}")
        except tk.TclError as e:
            self.logger.warn(f"Failed to show loading status: {e}")
    
    def _hide_loading_status(self) -> None:
        """Hide loading message from status label."""
        try:
            self.status_bar_widgets.clear_progress()
        except tk.TclError as e:
            self.logger.warn(f"Failed to hide loading status: {e}")
    
    def _start_progress_indicator(self) -> None:
        """Start a simple progress animation indicator."""
        try:
            wait_icon = self.styles.LOADING_CONFIG['icons']['waiting']
            default_msg = self.styles.LOADING_CONFIG['messages']['default']
            self.status_bar_widgets.update_progress(f"{wait_icon} {default_msg}")
        except tk.TclError as e:
            self.logger.warn(f"Failed to start progress indicator: {e}")
    
    def _stop_progress_indicator(self) -> None:
        """Stop progress animation indicator."""
        if not getattr(self, "_last_error", False):
            try:
                self.status_bar_widgets.clear_progress()
            except tk.TclError as e:
                self.logger.warn(f"Failed to stop progress indicator: {e}")


class AsyncWeatherOperation:
    """Handle async weather operations with proper threading and cancellation support.
    
    Manages background weather data fetching with thread-safe UI updates,
    cancellation support, and comprehensive error handling.
    
    Attributes:
        controller: Weather dashboard controller for data operations
        loading_manager: Loading state manager for UI updates
        current_thread: Reference to current background thread
        cancel_event: Threading event for operation cancellation
    """    
    def __init__(self, controller: Any, loading_manager: LoadingStateManager) -> None:
        """Initialize async weather operation manager."""
        # Direct imports for stable utilities
        self.logger = Logger()

        # Injected dependencies for testable components
        self.controller = controller # Weather dashboard controller for data operations
        self.loading_manager = loading_manager # Loading state manager for UI updates
        
        # Internal state
        self.current_thread: Optional[threading.Thread] = None
        self.cancel_event = threading.Event()
    
    def cancel_current_operation(self) -> None:
        """Cancel the currently running operation.
        
        Sets the cancellation event and stops the loading UI state.
        Safe to call even if no operation is currently running.
        """
        if self.current_thread and self.current_thread.is_alive():
            self.cancel_event.set()
            self.logger.info("Cancelling current weather operation")
            # Stop loading UI state
            self._schedule_ui_update(self.loading_manager.stop_loading)
    
    def fetch_weather_async(self, city_name: str, unit_system: str, on_complete: Optional[Callable] = None, enable_cancellation: bool = True) -> None:
        """Fetch weather data in background thread with cancellation support.
        
        Starts a background thread to fetch weather data while providing
        progress updates and proper error handling. Cancels any existing
        operation before starting a new one.
        
        Args:
            city_name: Name of the city to fetch weather for
            unit_system: Unit system for the weather data ('metric' or 'imperial')
            on_complete: Optional callback function called when operation completes
            enable_cancellation: Whether to enable cancellation support
        """
        # Setup cancellation
        cancel_event_to_pass = self.cancel_event if enable_cancellation else None
        if enable_cancellation:
            # Cancel any existing operation first
            self.cancel_current_operation()
            self.cancel_event.clear()

        def background_task():
            """Execute weather data fetching in background thread.
            
            Performs the actual weather data fetching with progress updates,
            cancellation checking, and comprehensive error handling. Runs
            in a separate thread to avoid blocking the UI.
            """
            try:
                # Check for cancellation before starting
                if self._is_cancelled():
                    return
                
                # Step 1: Start loading
                self._schedule_ui_update(self.loading_manager.start_loading, "Initializing...")
                
                # Step 2: Input validation (simulated delay for demonstration)
                if self._is_cancelled():
                    return
                self._schedule_ui_update(self.loading_manager.update_progress, "Validating input...")
                
                # Step 3: API call
                if self._is_cancelled():
                    return
                self._schedule_ui_update(self.loading_manager.update_progress, "Fetching weather data...")
                
                # Do the actual work in background
                result = self.controller.update_weather_display(city_name, unit_system, cancel_event_to_pass)

                # Check for cancellation before completion
                if self._is_cancelled():
                    self._schedule_ui_update(self.loading_manager.stop_loading)
                    return

                # Handle completion in main thread
                def complete_task():
                    """Complete the async operation and call completion callback."""
                    # Show error message if there is one
                    if result.error_message:
                        self.loading_manager.show_error(result.error_message)
                    
                    self.loading_manager.stop_loading()
                    if on_complete:
                        on_complete(result.success)
                
                self._schedule_ui_update(complete_task)
                
            except (ConnectionError, TimeoutError, RateLimitError) as e:
                if self._is_cancelled():
                    return  # Don't show error if operation was cancelled
                
                def handle_network_error():
                    """Handle network errors by stopping loading and showing error message."""
                    self.loading_manager.show_error(f"Network error: {e}")
                    self.loading_manager.stop_loading()
                    if hasattr(self.controller, 'error_handler') and self.controller.error_handler:
                        if isinstance(e, RateLimitError):
                            self.controller.error_handler.handle_weather_error(e, city_name)
                        else:
                            network_error = NetworkError(f"Network error during async operation: {e}")
                            self.controller.error_handler.handle_weather_error(network_error, city_name)
                
                self._schedule_ui_update(handle_network_error)
                return

            except ValidationError as e:
                if self._is_cancelled():
                    return
                
                def handle_validation_error():
                    """Handle validation errors by stopping loading and showing error message."""
                    self.loading_manager.show_error(f"Validation error: {e}")
                    self.loading_manager.stop_loading()
                    if hasattr(self.controller, 'error_handler') and self.controller.error_handler:
                        self.controller.error_handler.handle_input_validation_error(str(e))
                
                self._schedule_ui_update(handle_validation_error)
                return

            except Exception as e:
                if self._is_cancelled():
                    return
                
                def handle_unexpected_error():
                    """Handle unexpected errors by stopping loading and showing error message."""
                    error_message = f"Async operation failed: {str(e)}"
                    self.loading_manager.show_error(error_message)
                    self.loading_manager.stop_loading()
                    if hasattr(self.controller, 'error_handler'):
                        self.controller.error_handler.handle_unexpected_error(error_message)
                
                self._schedule_ui_update(handle_unexpected_error)
                return
        
        # Start background thread and store reference
        self.current_thread = threading.Thread(target=background_task, daemon=True)
        self.current_thread.start()
    
    def _is_cancelled(self) -> bool:
        """Check if the current operation has been cancelled."""
        return (hasattr(self, 'cancel_event') and self.cancel_event and self.cancel_event.is_set())
    
    def _schedule_ui_update(self, func: Callable, *args) -> None:
        """Safely schedule UI updates from background thread.
    
        Ensures thread-safe UI updates by using tkinter's after_idle method
        when possible, with fallback to direct execution. Handles widget
        destruction gracefully and prevents UI crashes from background threads.
        Critical for async operations that need to update the UI.
        
        Args:
            func: Function to execute in the main thread
            *args: Arguments to pass to the function
        """
        try:
            # Try to get the root window for thread-safe UI updates
            root = None
            if (hasattr(self.controller, 'state') and hasattr(self.controller.state, 'city_label') and self.controller.state.city_label):
                try:
                    root = self.controller.state.city_label.winfo_toplevel()
                except tk.TclError:
                    self.logger.warn("Widget was destroyed, falling back to direct call")
            
            if root:
                root.after_idle(lambda: self._safe_ui_call(func, *args))
            else:
                # Fallback: execute directly (not thread-safe but won't crash)
                self._safe_ui_call(func, *args)
                
        except Exception as e:
            self.logger.error(f"Error scheduling UI update: {e}")

    def _safe_ui_call(self, func: Callable, *args) -> None:
        """Safely execute UI function call with error handling.
        
        Wraps UI function calls with appropriate exception handling
        to prevent crashes from UI errors.
        
        Args:
            func: Function to execute
            *args: Arguments to pass to the function
        """
        try:
            func(*args)
        except tk.TclError as e:
            self.logger.error(f"UI error during scheduled update: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error during UI update: {e}")