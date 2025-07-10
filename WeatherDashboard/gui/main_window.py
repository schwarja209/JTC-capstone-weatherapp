"""
Main window and application initialization.
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
    '''Main application class for the Weather Dashboard.'''
    def __init__(self, root) -> None:
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

        # Initialize business logic
        self.service = WeatherDataService(self.data_manager)
        self.controller = WeatherDashboardController(
            state=self.state,
            data_service=self.service,
            widgets=self.ui_renderer
        )

        # Initialize async components
        self.loading_manager = LoadingStateManager(self.state)
        self.async_operations = AsyncWeatherOperation(self.controller, self.loading_manager)

        # Store button references for loading state management
        self._store_button_references()

        self.update_chart_dropdown()

    def load_initial_display(self) -> None:
        '''Fetches and displays the initial city's weather data on startup. (async)'''
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
        """Store button references for loading state management."""
        # Connect control widget buttons to state for loading manager access
        if hasattr(self.ui_renderer, 'control_widgets') and self.ui_renderer.control_widgets:
            control_widgets = self.ui_renderer.control_widgets
            
            # Store button references in state for LoadingStateManager access
            if hasattr(control_widgets, 'update_button'):
                self.state.update_button = control_widgets.update_button
            if hasattr(control_widgets, 'reset_button'):
                self.state.reset_button = control_widgets.reset_button
            if hasattr(control_widgets, 'progress_label'):
                self.state.progress_label = control_widgets.progress_label

    def on_update_clicked_async(self) -> None:
        '''Handles the update button click event with async weather fetching.'''
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
        '''Handles the reset button click event to reset input controls to default values (but does not clear display output).'''
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
        '''Updates the chart dropdown based on the current visibility settings.'''
        if hasattr(self.ui_renderer, 'control_widgets') and self.ui_renderer.control_widgets:
            self.ui_renderer.control_widgets.update_chart_dropdown_options()
    
    def _handle_async_complete(self, success: bool, next_callback: Optional[callable] = None) -> None:
        if hasattr(self.ui_renderer, 'control_widgets') and self.ui_renderer.control_widgets:
            self.ui_renderer.control_widgets.set_loading_state(False)
        
        if next_callback:
            next_callback(success)


    # LEGACY SYNC METHOD (for fallback/testing)   
    # def on_update_clicked(self) -> None:
    #     '''Handles the update button click event to fetch and display weather data.'''
    #     success = self.controller.update_weather_display(
    #         self.state.get_current_city(),
    #         self.state.get_current_unit_system()
    #     )

    #     if success:
    #         self.controller.update_chart()