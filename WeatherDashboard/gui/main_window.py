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
import tkinter.messagebox as messagebox

from WeatherDashboard.gui.state_manager import WeatherDashboardState
from WeatherDashboard.gui.frames import WeatherDashboardGUIFrames
from WeatherDashboard.gui.loading_states import LoadingStateManager, AsyncWeatherOperation
from WeatherDashboard.widgets.dashboard_widgets import WeatherDashboardWidgets
from WeatherDashboard.core.data_manager import WeatherDataManager
from WeatherDashboard.core.data_service import WeatherDataService
from WeatherDashboard.core.controller import WeatherDashboardController


class WeatherDashboardMain:
    """Main application class for the Weather Dashboard.
    
    Orchestrates the initialization and coordination of all application components
    including state management, UI widgets, business logic controllers, data
    services, and async operation handling.
    
    Attributes:
        root: Main tkinter window
        state: Application state manager
        frames: GUI frame manager
        data_manager: Weather data management service
        ui_renderer: UI widget coordinator
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
        self.state = WeatherDashboardState() 
        self.frames = WeatherDashboardGUIFrames(root)
        self.data_manager = WeatherDataManager()

        # Initialize UI components
        self.ui_renderer = WeatherDashboardWidgets(
            frames=self.frames.frames,
            state=self.state,
            update_cb=self.on_update_clicked_async,
            clear_cb=self.on_clear_clicked,
            dropdown_cb=self.update_chart_dropdown
        )

        # Connect alert system to UI
        self._connect_alert_system()

        # Initialize business logic
        self.service = WeatherDataService(self.data_manager)
        self.controller = WeatherDashboardController(
            state=self.state,
            data_service=self.service,
            widgets=self.ui_renderer,
            theme='neutral'
        )

        # Initialize async components
        self.loading_manager = LoadingStateManager(self.state)
        self.async_operations = AsyncWeatherOperation(self.controller, self.loading_manager)

        # Store button references for loading state management
        self._store_button_references()

        self.update_chart_dropdown()

    def _connect_alert_system(self) -> None:
        """Connect alert system to UI components.
        
        Links the alert status widget to the alert display callback for
        user interaction with weather alerts.
        """
        # Access through tabbed widgets property
        if (hasattr(self.ui_renderer, 'metric_widgets') and 
            self.ui_renderer.metric_widgets and
            hasattr(self.ui_renderer.metric_widgets, 'alert_status_widget')):
            
            alert_widget = self.ui_renderer.metric_widgets.alert_status_widget
            alert_widget.set_click_callback(self.show_alerts)

    def show_alerts(self) -> None:
        """Show weather alerts popup.
        
        Displays active weather alerts in a popup dialog. Called when
        user clicks on the alert status indicator.
        """
        if hasattr(self.controller, 'show_weather_alerts'):
            self.controller.show_weather_alerts()

    def load_initial_display(self) -> None:
        """Fetch and display the initial city's weather data on startup.
        
        Loads weather data for the default city asynchronously and updates
        the chart display. Prevents concurrent operations during startup.
        """
        # Prevent concurrent operations
        if hasattr(self, '_operation_in_progress') and self._operation_in_progress:
            return
        
        self._operation_in_progress = True
        
        def on_weather_complete(success: bool) -> None:
            if success:
                # Update chart after weather data loads (but don't reset operation flag yet)
                self.controller.update_chart()
        
        def operation_finished(success: bool):
            self._operation_in_progress = False
            on_weather_complete(success)
        
        # Load initial data asynchronously
        self.async_operations.fetch_weather_async(
            self.state.get_current_city(),
            self.state.get_current_unit_system(),
            on_complete=operation_finished
        )

    def _store_button_references(self) -> None:
        """Store button references for loading state management.
        
        Connects control widget buttons to the state manager so the loading
        manager can access and manage button states during async operations.
        """
        # Connect control widget buttons to state for loading manager access
        if hasattr(self.ui_renderer, 'control_widgets') and self.ui_renderer.control_widgets:
            control_widgets = self.ui_renderer.control_widgets
            
            # Store button references in state for LoadingStateManager access
            if hasattr(control_widgets, 'update_button'):
                self.state.update_button = control_widgets.update_button
            if hasattr(control_widgets, 'reset_button'):
                self.state.reset_button = control_widgets.reset_button

    def on_update_clicked_async(self) -> None:
        """Handle the update button click event with async weather fetching.
        
        Initiates asynchronous weather data fetching for the currently selected
        city and unit system. Prevents concurrent operations and updates both
        weather display and chart upon completion.
        """
        # Prevent concurrent operations
        if hasattr(self, '_operation_in_progress') and self._operation_in_progress:
            return
        
        self._operation_in_progress = True
        
        def on_weather_complete(success: bool) -> None:
            if success:
                # Update chart after weather data loads (but don't reset operation flag yet)
                self.controller.update_chart()
        
        def operation_finished(success: bool):
            self._operation_in_progress = False
            self._handle_async_complete(success, on_weather_complete)

        if hasattr(self.ui_renderer, 'control_widgets') and self.ui_renderer.control_widgets:
            self.ui_renderer.control_widgets.set_loading_state(True, "Fetching weather...")

        # Fetch weather data asynchronously
        self.async_operations.fetch_weather_async(
            self.state.get_current_city(),
            self.state.get_current_unit_system(),
            on_complete=operation_finished
        )

    def on_clear_clicked(self) -> None:
        """Handle the reset button click event to reset input controls to default values.
        
        Resets all user inputs to default values and loads weather data for the
        default city. Does not clear display output - updates with default city data.
        Prevents concurrent operations during reset process.
        """
        # Prevent concurrent operations
        if hasattr(self, '_operation_in_progress') and self._operation_in_progress:
            return
        
        self._operation_in_progress = True
        
        self.state.reset_to_defaults()
        messagebox.showinfo("Reset", "Dashboard reset to default values.")
        self.update_chart_dropdown()

        # Load default city data asynchronously after reset
        def on_weather_complete(success: bool) -> None:
            if success:
                # Update chart after weather data loads (but don't reset operation flag yet)
                self.controller.update_chart()
        
        def operation_finished(success: bool):
            self._operation_in_progress = False
            self._handle_async_complete(success, on_weather_complete)

        if hasattr(self.ui_renderer, 'control_widgets') and self.ui_renderer.control_widgets:
            self.ui_renderer.control_widgets.set_loading_state(True, "Loading default city...")

        self.async_operations.fetch_weather_async(
            self.state.get_current_city(),
            self.state.get_current_unit_system(),
            on_complete=operation_finished
        )

    def update_chart_dropdown(self) -> None:
        """Update the chart dropdown based on the current visibility settings.
        
        Refreshes the chart metric dropdown options to reflect currently visible
        metrics. Called when metric visibility settings change.
        """
        if hasattr(self.ui_renderer, 'control_widgets') and self.ui_renderer.control_widgets:
            self.ui_renderer.control_widgets.update_chart_dropdown_options()

    def cancel_current_operation(self) -> None:
        """Cancel any currently running async operation.
        
        Stops any active background weather fetching operation and resets
        the UI to normal state. Safe to call even when no operation is running.
        """
        if hasattr(self, 'async_operations'):
            self.async_operations.cancel_current_operation()
            
        # Reset operation flag
        if hasattr(self, '_operation_in_progress'):
            self._operation_in_progress = False
    
        # Reset UI state
        if hasattr(self.ui_renderer, 'control_widgets') and self.ui_renderer.control_widgets:
            self.ui_renderer.control_widgets.set_loading_state(False)
    
    def _handle_async_complete(self, success: bool, next_callback: Optional[callable] = None) -> None:
        """Handle completion of async operations.
        
        Resets UI loading state and calls optional completion callback.
        Used internally to clean up after async weather operations.
        
        Args:
            success: True if the async operation succeeded
            next_callback: Optional callback to execute after cleanup
        """
        if hasattr(self.ui_renderer, 'control_widgets') and self.ui_renderer.control_widgets:
            self.ui_renderer.control_widgets.set_loading_state(False)
        
        if next_callback:
            next_callback(success)