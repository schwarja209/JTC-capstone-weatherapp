"""
Main window and application initialization.

This module provides the primary application window and orchestrates the
initialization of all components including state management, UI widgets,
business logic, and async operations. Serves as the main entry point for
the GUI application.

Classes:
    WeatherDashboardMain: Primary application window and component coordinator
"""

from typing import Optional
import threading
import tkinter.messagebox as messagebox

from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.gui.state_manager import WeatherDashboardState
from WeatherDashboard.gui.frames import WeatherDashboardGUIFrames
from WeatherDashboard.gui.loading_states import LoadingStateManager, AsyncWeatherOperation
from WeatherDashboard.widgets.dashboard_widgets import WeatherDashboardWidgets
from WeatherDashboard.core.data_manager import WeatherDataManager
from WeatherDashboard.core.data_service import WeatherDataService
from WeatherDashboard.core.controller import WeatherDashboardController


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
    def __init__(self, root) -> None:
        """Initialize the main weather dashboard application.
        
        Sets up all application components including state management, UI widgets,
        business logic, data services, and async operations. Connects all systems
        and prepares the application for user interaction.
        
        Args:
            root: Main tkinter window instance
        """
        self.root = root
        self._operation_lock = threading.Lock()
        
        # Core components
        self.state = WeatherDashboardState() 
        self.data_manager = WeatherDataManager()
        
        # Single widget manager instead of separate frames + widgets
        self.widgets = self._create_widgets(root)
        
        # Business logic
        self.service = WeatherDataService(self.data_manager)
        self.controller = WeatherDashboardController(
            state=self.state,
            data_service=self.service,
            widgets=self.widgets,
            theme='neutral'
        )
        
        # Async components
        self.loading_manager = LoadingStateManager(self.state, self.widgets.status_bar_widgets)
        self.async_operations = AsyncWeatherOperation(self.controller, self.loading_manager)
        
        # Connect callbacks and initialize
        self._connect_callbacks()
        self.update_chart_dropdown()

    def _create_widgets(self, root):
        """Create and configure all widgets in a single, unified manager."""
        # Create frames
        frames = WeatherDashboardGUIFrames(root)
        
        # Create widget manager with direct frame access
        widgets = WeatherDashboardWidgets(
            frames=frames.frames,
            state=self.state,
            update_cb=self.on_update_clicked_async,
            cancel_cb=self.cancel_current_operation,
            clear_cb=self.on_clear_clicked,
            dropdown_cb=self.update_chart_dropdown
        )
        
        # Store frame references in widget manager for unified access
        widgets.frames = frames.frames
        
        return widgets
    
    def _connect_callbacks(self):
        """Connect all widget callbacks and alert system."""
        # Alert system connection
        if hasattr(self.widgets, 'metric_widgets') and self.widgets.metric_widgets:
            alert_widget = getattr(self.widgets.metric_widgets, 'alert_status_widget', None)
            if alert_widget:
                alert_widget.set_click_callback(self.show_alerts)

# ================================
# 2. EVENT HANDLERS
# ================================
    def on_update_clicked_async(self) -> None:
        """Handle the update button click event with async weather fetching.
        
        Initiates asynchronous weather data fetching for the currently selected
        city and unit system. Prevents concurrent operations and updates both
        weather display and chart upon completion.
        """
        # Prevent concurrent operations
        with self._operation_lock:
            if hasattr(self, '_operation_in_progress') and self._operation_in_progress:
                return
            self._operation_in_progress = True

        if self.widgets.control_widgets:
            self.widgets.control_widgets.set_loading_state(True, "Fetching weather...")
            
        # Fetch weather data asynchronously
        self.async_operations.fetch_weather_async(
            self.state.get_current_city(),
            self.state.get_current_unit_system(),
            on_complete=self._create_update_operation_callback()
        )

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
        messagebox.showinfo("Reset", "Dashboard reset to default values.")
        self.update_chart_dropdown()

        if self.widgets.control_widgets:
            self.widgets.control_widgets.set_loading_state(True, "Loading default city...")

        self.async_operations.fetch_weather_async(
            self.state.get_current_city(),
            self.state.get_current_unit_system(),
            on_complete=self._create_clear_operation_callback()
        )

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

    def show_alerts(self) -> None:
        """Show weather alerts popup."""
        if hasattr(self.controller, 'show_weather_alerts'):
            self.controller.show_weather_alerts()

# ================================
# 3. ASYNC OPERATION MANAGEMENT
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

        def operation_finished(success: bool):
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

# ================================
# 4. UI UPDATE METHODS
# ================================
    def update_chart_dropdown(self) -> None:
        """Update the chart dropdown based on the current visibility settings."""
        if self.widgets.control_widgets:
            self.widgets.control_widgets.update_chart_dropdown_options()