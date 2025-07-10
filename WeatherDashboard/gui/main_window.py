"""
Main window and application initialization.
"""

import tkinter.messagebox as messagebox

from WeatherDashboard.gui.state_manager import WeatherDashboardState
from WeatherDashboard.gui.frames import WeatherDashboardGUIFrames
from WeatherDashboard.widgets.dashboard_widgets import WeatherDashboardWidgets
from WeatherDashboard.core.data_manager import WeatherDataManager
from WeatherDashboard.core.data_service import WeatherDataService
from WeatherDashboard.core.controller import WeatherDashboardController


class WeatherDashboardMain:
    '''Main application class for the Weather Dashboard.'''
    def __init__(self, root):
        self.root = root
        self.state = WeatherDashboardState() 
        self.frames = WeatherDashboardGUIFrames(root)
        self.data_manager = WeatherDataManager()

        self.ui_renderer = WeatherDashboardWidgets(
            frames=self.frames.frames,
            state=self.state,
            update_cb=self.on_update_clicked,
            clear_cb=self.on_clear_clicked,
            dropdown_cb=self.update_chart_dropdown
        )

        self.service = WeatherDataService(self.data_manager)

        self.controller = WeatherDashboardController(
            state=self.state,
            data_service=self.service,
            widgets=self.ui_renderer
        )

        self.update_chart_dropdown()

    def load_initial_display(self):
        '''Fetches and displays the initial city's weather data on startup.'''
        success = self.controller.update_weather_display(
            self.state.get_current_city(),
            self.state.get_current_unit_system()
        )
        
        # Also update the chart on initial load
        if success:
            self.controller.update_chart()

    def on_update_clicked(self):
        '''Handles the update button click event to fetch and display weather data.'''
        success = self.controller.update_weather_display(
            self.state.get_current_city(),
            self.state.get_current_unit_system()
        )

        if success:
            self.controller.update_chart()

    def on_clear_clicked(self):
        '''Handles the reset button click event to reset input controls to default values (but does not clear display output).'''
        self.state.reset_to_defaults()
        messagebox.showinfo("Reset", "Dashboard reset to default values.")  # Pop-up confirmation
        self.update_chart_dropdown()

        # Also update the display to show the default city's data
        success = self.controller.update_weather_display(
            self.state.get_current_city(),
            self.state.get_current_unit_system()
        )
        
        if success:
            self.controller.update_chart()

    def update_chart_dropdown(self):
        '''Updates the chart dropdown based on the current visibility settings.'''
        self.state.update_chart_dropdown_options()