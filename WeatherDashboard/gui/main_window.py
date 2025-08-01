"""
Main window and application initialization.

This module provides the primary application window and orchestrates the
initialization of all components including state management, UI widgets,
business logic, and async operations. Serves as the main entry point for
the GUI application.

Classes:
    WeatherDashboardMain: Primary application window and component coordinator
"""

from typing import Optional, List, Any, Dict
import threading
import tkinter.messagebox as messagebox

from WeatherDashboard.utils.logger import Logger

from .state_manager import WeatherDashboardState
from .frames import WeatherDashboardGUIFrames
from .loading_states import LoadingStateManager, AsyncWeatherOperation
from WeatherDashboard.widgets.dashboard_widgets import WeatherDashboardWidgets
from WeatherDashboard.core.data_manager import WeatherDataManager
from WeatherDashboard.core.data_service import WeatherDataService
from WeatherDashboard.core.controller import WeatherDashboardController
from WeatherDashboard.features.alerts.alert_display import SimpleAlertPopup
from WeatherDashboard.features.history.scheduler_service import WeatherDataScheduler
from WeatherDashboard.features.themes.theme_manager import Theme, theme_manager


# ================================
# 1. APPLICATION INITIALIZATION
# ================================
class WeatherDashboardMain:
    """Main application class for the Weather Dashboard.

    Orchestrates the initialization and coordination of all application components
    including state management, UI widgets, business logic controllers, data
    services, and async operation handling.

    Attributes:
        root: Main tkinter window
        _operation_lock: Threading lock for operation state protection
        state: Application state manager
        widgets: Unified widget manager
        data_manager: Weather data management service
        service: Weather data service layer
        controller: Main business logic controller
        loading_manager: Async loading state manager
        async_operations: Async weather operation handler
    """
    
    def __init__(self, root, data_manager: Optional[WeatherDataManager] = None, data_service: Optional[WeatherDataService] = None,
                 loading_manager: Optional[LoadingStateManager] = None, async_operations: Optional[AsyncWeatherOperation] = None,
                 state_manager: Optional[WeatherDashboardState] = None, frames: Optional[WeatherDashboardGUIFrames] = None,
                 widgets: Optional[WeatherDashboardWidgets] = None, controller: Optional[WeatherDashboardController] = None) -> None:
        """Initialize the main weather dashboard application.
        
        Sets up all application components including state management, UI widgets,
        business logic, data services, and async operations. Connects all systems
        and prepares the application for user interaction.
        
        Args:
            root: Main tkinter window instance
            data_manager: Weather data manager (injected for testability)
            data_service: Weather data service (injected for testability)
            loading_manager: Loading state manager (injected for testability)
            async_operations: Async operation handler (injected for testability)
            state_manager: Application state manager (injected for testability)
            frames: GUI frames manager (injected for testability)
            widgets: Widget manager (injected for testability)
            controller: Business logic controller (injected for testability)
        """
        # Direct imports for stable utilities
        self.logger = Logger()

        # Instance data
        self.root = root
        self._operation_lock = threading.Lock()
        self._setup_window_constraints()
        
        # Injected dependencies for testable core components
        self.state = state_manager or WeatherDashboardState()
        self.data_manager = data_manager or WeatherDataManager()
        
        # Create scheduler
        self.scheduler_service = WeatherDataScheduler(
            self.data_manager.history_service,
            self.data_manager,
            self.state,
            self
        )

        # Create or inject single widget manager instead of separate frames + widgets
        if widgets:
            self.widgets = widgets
        else:
            self.widgets = self._create_widgets(root, frames)

        # Business logic
        self.service = data_service or WeatherDataService(self.data_manager)
        self.controller = controller or WeatherDashboardController(
            state=self.state,
            data_service=self.service,
            widgets=self.widgets,
            ui_handler=self,
            theme='neutral'
        )

        # Async components
        self.loading_manager = loading_manager or LoadingStateManager(self.state, self.widgets.status_bar_widgets)
        self.async_operations = async_operations or AsyncWeatherOperation(self.controller, self.loading_manager)
        
        # Connect callbacks and initialize
        self._connect_callbacks()
        self.update_chart_components()

        # Start scheduler after everything is ready
        if self.scheduler_service.enabled:
            self.scheduler_service.start_scheduler()

    def _create_widgets(self, root: Any, frames: Optional[WeatherDashboardGUIFrames] = None) -> None:
        """Create and configure all widgets in a single, unified manager."""
        # Create or use injected frames
        if frames is None:
            frames = WeatherDashboardGUIFrames(root)
        
        # Create widget manager with direct frame access
        widgets = WeatherDashboardWidgets(
            frames=frames.frames,
            state=self.state,
            update_cb=self.on_update_clicked_async,
            cancel_cb=self.cancel_current_operation,
            clear_cb=self.on_clear_clicked,
            dropdown_cb=lambda: self.update_chart_components(),
            scheduler_cb=self.scheduler_service.toggle_scheduler,
            theme_cb=self._on_theme_change
        )
        
        # Store frame references in widget manager for unified access
        widgets.frames = frames.frames
        
        return widgets
    
    def _connect_callbacks(self) -> None:
        """Connect all widget callbacks and alert system."""
        # Alert system connection
        if hasattr(self.widgets, 'metric_widgets') and self.widgets.metric_widgets:
            alert_widget = getattr(self.widgets.metric_widgets, 'alert_status_widget', None)
            if alert_widget:
                alert_widget.set_click_callback(self.show_alerts)
        elif hasattr(self.widgets, 'tabbed_widgets') and self.widgets.tabbed_widgets:
            # Try to get alert widget through tabbed interface
            metric_widgets = self.widgets.tabbed_widgets.get_metric_widgets()
            if metric_widgets:
                alert_widget = getattr(metric_widgets, 'alert_status_widget', None)
                if alert_widget:
                    alert_widget.set_click_callback(self.show_alerts)

    def _setup_window_constraints(self) -> None:
        """Set up window size constraints and positioning."""
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate adaptive window size (80% of screen size, but with limits)
        window_width = min(max(800, int(screen_width * 0.8)), 1400)
        window_height = min(max(600, int(screen_height * 0.8)), 1000)
        
        # Set minimum and maximum window size
        self.root.minsize(600, 400)  # Smaller minimum size
        self.root.maxsize(screen_width - 50, screen_height - 50)  # Leave some margin
        
        # Set initial window size
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Calculate center position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Ensure window doesn't go off-screen
        x = max(0, min(x, screen_width - window_width))
        y = max(0, min(y, screen_height - window_height))
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Configure grid weights for responsive layout - match the 2-column layout
        self.root.grid_rowconfigure(0, weight=0)  # Title row
        self.root.grid_rowconfigure(1, weight=1)  # Main content row  
        self.root.grid_rowconfigure(2, weight=0)  # Status row
        self.root.grid_columnconfigure(0, weight=1)  # Control column
        self.root.grid_columnconfigure(1, weight=2)  # Main content column
        
        # Set window background from theme
        backgrounds = theme_manager.get_backgrounds()
        self.root.configure(bg=backgrounds['main_window'])

        # Prevent window from resizing beyond screen bounds
        def on_configure(event):
            """Handle window resize events to keep window on screen."""
            if event.widget == self.root:
                # Get current window position and size
                x = self.root.winfo_x()
                y = self.root.winfo_y()
                width = self.root.winfo_width()
                height = self.root.winfo_height()
                
                # Get screen dimensions
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                
                # Adjust if window goes off-screen
                if x + width > screen_width:
                    x = screen_width - width
                if y + height > screen_height:
                    y = screen_height - height
                if x < 0:
                    x = 0
                if y < 0:
                    y = 0
                
                # Only move if significantly off-screen (more than 10 pixels)
                if abs(x - self.root.winfo_x()) > 10 or abs(y - self.root.winfo_y()) > 10:
                    self.root.geometry(f"+{x}+{y}")
                
        self.root.bind('<Configure>', on_configure)

# ================================
# 2. UI HANDLERS
# ================================
    def show_info(self, title: str, message: str) -> None:
        """Display information message to user."""
        messagebox.showinfo(title, message)

    def show_warning(self, title: str, message: str) -> None:
        """Display warning message to user."""
        messagebox.showwarning(title, message)

    def show_error(self, title: str, message: str) -> None:
        """Display error message to user."""
        messagebox.showerror(title, message)
    
    def show_alert_popup(self, alerts: List[Dict[str, Any]]) -> None:
        """Display weather alerts popup."""
        parent = self.get_alert_popup_parent()
        SimpleAlertPopup(parent, alerts)
    
    def are_widgets_ready(self) -> bool:
        """Check if all widgets are properly initialized."""
        if not self.widgets.is_ready():
            self.logger.warn(f"Widget manager not ready: {self.widgets.get_creation_error()}")
            return False
        return True
    
    def get_alert_popup_parent(self) -> Any:
        """Get parent window for alert popups."""
        return self.widgets.get_alert_popup_parent()

    def update_display(self, view_model: Any, error_exception: Optional[Exception] = None, simulated: bool = False) -> None:
        """Update main display components with weather data.
        
        Args:
            view_model: Weather data view model containing metrics and metadata
            error_exception: Optional exception that occurred during data fetching
            simulated: Whether the displayed data is simulated/fallback data
        """
        self.widgets.update_metric_display({
            **view_model.metrics,
            "city": view_model.city_name,
            "date": view_model.date_str
        })
        self.widgets.update_status_bar(view_model.city_name, error_exception, simulated)
        self.widgets.update_alerts(view_model.raw_data)

    def update_scheduler_status(self, status_info: Dict[str, Any]) -> None:
        """Update scheduler status in status bar."""
        if self.widgets.status_bar_widgets:
            self.widgets.status_bar_widgets.update_scheduler_status(status_info)

    def update_chart_components(self, x_vals: Optional[List[str]] = None, y_vals: Optional[List[Any]] = None, metric_key: Optional[str] = None, city: Optional[str] = None, unit: Optional[str] = None, fallback: bool = True, clear: bool = False) -> None:
        """Update chart-related components.
        
        Args:
            x_vals: X-axis values for chart (typically dates)
            y_vals: Y-axis values for chart (metric data)
            metric_key: Weather metric being charted
            city: City name for chart title
            unit: Unit system for labeling
            fallback: Whether to use fallback chart rendering
            clear: Whether to clear the chart instead of updating it
        """
        if clear:
            self.widgets.clear_chart_with_error_message()
        elif x_vals is not None and y_vals is not None:
            self.widgets.update_chart_display(x_vals, y_vals, metric_key, city, unit, fallback)
        
        # Always update dropdown options unless explicitly clearing
        if not clear and self.widgets.control_widgets:
            self.widgets.control_widgets.update_chart_dropdown_options()
            
# ================================
# 3. EVENT HANDLERS
# ================================
    def _on_theme_change(self, theme_name: str) -> None:
        """Handle theme change events.
        
        Args:
            theme_name: New theme name ('neutral', 'optimistic', 'pessimistic')
        """
        try:
            # Update theme in controller
            self.controller.set_theme(theme_name)
            
            # IMPORTANT: Reconfigure styles for the new theme
            from WeatherDashboard import styles
            styles.configure_styles(theme_name)
            
            # Update window background from theme on main thread
            from WeatherDashboard.features.themes.theme_manager import theme_manager, Theme

            # Map theme name to Theme enum
            theme_mapping = {
                "neutral": Theme.NEUTRAL,
                "optimistic": Theme.OPTIMISTIC,
                "pessimistic": Theme.PESSIMISTIC
            }
            
            theme_enum = theme_mapping.get(theme_name, Theme.NEUTRAL)
            theme_manager.change_theme(theme_enum)
            
            # Update window background
            backgrounds = theme_manager.get_backgrounds()
            self.root.configure(bg=backgrounds['main_window'])

            # Force window to stay within bounds
            self.root.update_idletasks()
            
            self.logger.info(f"Theme changed to {theme_name}")
            
        except Exception as e:
            self.logger.error(f"Error handling theme change: {e}")

    def on_update_clicked_async(self) -> None:
        """Handle the update button click event with async weather fetching.
        
        Initiates asynchronous weather data fetching for the currently selected
        city and unit system. Prevents concurrent operations and updates both
        weather display and chart upon completion.
        """
        try:
            # Prevent concurrent operations
            with self._operation_lock:
                if hasattr(self, '_operation_in_progress') and self._operation_in_progress:
                    return
                self._operation_in_progress = True

            # Save preferences when user manually updates
            self.state.save_preferences()

            # Check if scheduler might interfere with manual updates
            if hasattr(self, 'scheduler_service') and self.scheduler_service.is_running:
                # Log that manual update is taking precedence over scheduler
                self.logger.info("Manual update requested - scheduler will continue in background")

            if self.widgets.control_widgets:
                self.widgets.control_widgets.set_loading_state(True, "Fetching weather...")
                
            # Fetch weather data asynchronously
            self.async_operations.fetch_weather_async(
                self.state.get_current_city(),
                self.state.get_current_unit_system(),
                on_complete=self._create_update_operation_callback()
            )
            
        except Exception as e:
            # Ensure buttons are unlocked on any error
            self.logger.error(f"Async update error: {e}")
            with self._operation_lock:
                self._operation_in_progress = False
            if self.widgets.control_widgets:
                self.widgets.control_widgets.set_loading_state(False)
            self.show_error("Update Error", f"Failed to start weather update: {e}")

    def on_clear_clicked(self) -> None:
        """Handle the reset button click event to reset input controls to default values.
        
        Resets all user inputs to default values and loads weather data for the
        default city. Does not clear display output - updates with default city data.
        Prevents concurrent operations during reset process.
        """
        # Prevent concurrent operations
        with self._operation_lock:
            if hasattr(self, '_operation_in_progress') and self._operation_in_progress:
                return
            self._operation_in_progress = True
        
        self.state.reset_to_defaults()

        # Save preferences after reset
        self.state.save_preferences()

        self.show_info("Reset", "Dashboard reset to default values.")
        self.update_chart_components()

        if self.widgets.control_widgets:
            self.widgets.control_widgets.set_loading_state(True, "Loading default city...")

        self.async_operations.fetch_weather_async(
            self.state.get_current_city(),
            self.state.get_current_unit_system(),
            on_complete=self._create_clear_operation_callback()
        )

    def _on_closing(self) -> None:
        """Handle application shutdown and save preferences."""
        try:
            self.logger.info("Application shutting down")
            
            # Save preferences before closing
            if hasattr(self.state, 'save_preferences'):
                # Pass scheduler state to state manager
                self.state._scheduler_enabled = self.scheduler_service.enabled
                self.state.save_preferences()
            
            # Stop scheduler
            if hasattr(self, 'scheduler_service'):
                self.scheduler_service.stop_scheduler()
                
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
        finally:
            # Always close the window
            try:
                self.root.destroy()
            except:
                pass

    def show_alerts(self) -> None:
        """Show weather alerts popup."""
        if hasattr(self.controller, 'show_weather_alerts'):
            self.controller.show_weather_alerts()

    def _create_update_operation_callback(self) -> callable:
        """Create callback function for update operation completion."""
        def operation_finished(success: bool):
            with self._operation_lock:
                self._operation_in_progress = False
            self._handle_async_complete(success, self._update_chart_on_success)
        return operation_finished

    def _create_clear_operation_callback(self) -> callable:
        """Create callback function for clear operation completion."""
        def operation_finished(success: bool):
            self._operation_in_progress = False
            self._handle_async_complete(success, self._update_chart_on_success)
        return operation_finished
    
    def _update_chart_on_success(self, success: bool) -> None:
        """Update chart after successful weather data load."""
        if success:
            self.controller.update_chart()

# ================================
# 4. ASYNC OPERATION MANAGEMENT
# ================================
    def load_initial_display(self) -> None:
        """Fetch and display the initial city's weather data on startup.
        
        Loads weather data for the default city asynchronously and updates
        the chart display. Prevents concurrent operations during startup.
        """
        # Prevent concurrent operations
        with self._operation_lock:
            if hasattr(self, '_operation_in_progress') and self._operation_in_progress:
                return
            self._operation_in_progress = True
        
        # Set loading state for initial load
        if self.widgets.control_widgets:
            self.widgets.control_widgets.set_loading_state(True, "Loading...")

        def operation_finished(success: bool) -> None:
            with self._operation_lock:
                self._operation_in_progress = False
            
            # Clear loading state
            if self.widgets.control_widgets:
                self.widgets.control_widgets.set_loading_state(False)
            
            if success:
                self.controller.update_chart()
        
        # Load initial data asynchronously
        self.async_operations.fetch_weather_async(
            self.state.get_current_city(),
            self.state.get_current_unit_system(),
            on_complete=operation_finished,
            enable_cancellation=True  # Use long timeout for startup
        )

    def cancel_current_operation(self) -> None:
        """Cancel any currently running async operation.
    
        Stops any active background weather fetching operation and resets
        the UI to normal state. Uses thread-safe locking to prevent race
        conditions with completion handlers. Safe to call even when no 
        operation is running.
        """
        with self._operation_lock:
            if hasattr(self, 'async_operations'):
                self.async_operations.cancel_current_operation()
            
            # Reset operation flag when cancelling
            if hasattr(self, '_operation_in_progress'):
                self._operation_in_progress = False
    
        # UI reset can happen immediately
        if self.widgets.control_widgets:
            self.widgets.control_widgets.set_loading_state(False)
    
    def _handle_async_complete(self, success: bool, next_callback: Optional[callable] = None) -> None:
        """Handle completion of async operations."""
        if self.widgets.control_widgets:
            self.widgets.control_widgets.set_loading_state(False)
        
        if next_callback: # Optional callback to execute after cleanup
            next_callback(success)