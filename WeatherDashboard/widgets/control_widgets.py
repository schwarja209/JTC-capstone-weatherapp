"""
Control widgets for user input and actions.

This module provides comprehensive control panel widgets for user interaction
including city input, unit selection, metric visibility controls, chart settings,
and action buttons. Manages loading states, event handling, and coordinates
with callbacks for application control flow.

Classes:
    ControlWidgets: Main control panel manager with inputs, selections, and actions
"""

from typing import Dict, Any, Callable, Optional
import tkinter as tk
from tkinter import ttk

from WeatherDashboard import config
from WeatherDashboard.utils.logger import Logger


class ControlWidgets:
    """Manages all control panel widgets including inputs, selections, and buttons.
    
    Creates and manages the complete control panel interface including city input
    field, unit system radio buttons, metric visibility checkboxes, chart controls,
    and action buttons. Handles loading states, keyboard events, and coordinates
    with application callbacks for user interactions.
    
    Attributes:
        parent: Parent frame container
        state: Application state manager
        callbacks: Dictionary of callback functions for user actions
        city_entry: City name input field
        update_button: Weather update action button
        reset_button: Settings reset action button
        cancel_button: Operation cancel button
    """
    def __init__(self, parent_frame: ttk.Frame, state: Any, callbacks: Dict[str, Callable]) -> None:
        """Initialize the control widgets with complete control panel.
        
        Creates all control panel sections including city input, unit selection,
        metric visibility controls, chart settings, and action buttons. Configures
        grid layout, binds events, and registers widgets with state manager.
        
        Args:
            parent_frame: Parent TTK frame to contain the control panel
            state: Application state manager for widget coordination
            callbacks: Dictionary of callback functions for user actions
        """
        self.parent = parent_frame
        self.state = state
        self.callbacks = callbacks
        
        # Widget references
        self.city_entry: Optional[ttk.Entry] = None
        self.update_button: Optional[ttk.Button] = None
        self.reset_button: Optional[ttk.Button] = None
        self.cancel_button: Optional[ttk.Button] = None
        
        self._create_all_controls()
        self._register_widgets_with_state()
    
    def _create_all_controls(self) -> None:
        """Create all control widgets in organized sections with error handling.
        
        Orchestrates the creation of city input, unit selection, metric visibility
        controls, chart settings, and action buttons. Configures layout and events,
        with comprehensive error handling and logging for debugging failures.
        """
        try:
            self._create_city_input()
            self._create_unit_selection()
            self._create_metric_visibility()
            self._create_chart_controls()
            self._create_action_buttons()
            self._configure_grid_weights()
            self._bind_events()
        except Exception as e:
            Logger.error(f"Failed to create control widgets: {e}")
            raise

    def _create_city_input(self) -> None:
        """Create city name input field with label.
        
        Creates a labeled text entry field for city name input, bound to the
        state city variable for automatic state synchronization.
        """
        ttk.Label(self.parent, text="City:", style="LabelName.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.city_entry = ttk.Entry(self.parent, textvariable=self.state.city)
        self.city_entry.grid(row=1, column=1, sticky=tk.W)

    def _create_unit_selection(self) -> None:
        """Create unit system selection radio buttons.
        
        Creates Imperial and Metric radio button options for temperature,
        wind speed, and pressure unit selection, bound to state unit variable.
        """
        ttk.Label(self.parent, text="Units:", style="LabelName.TLabel").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(
            self.parent, 
            text="Imperial (°F, mph, inHg)", 
            variable=self.state.unit, 
            value="imperial"
        ).grid(row=2, column=1, sticky=tk.W)
        
        ttk.Radiobutton(
            self.parent, 
            text="Metric (°C, m/s, hPa)", 
            variable=self.state.unit, 
            value="metric"
        ).grid(row=3, column=1, sticky=tk.W)

    def _create_metric_visibility(self) -> None:
        """Create metric visibility control checkboxes.
        
        Creates checkboxes for each weather metric allowing users to control
        which metrics are displayed. Updates chart dropdown when changed.
        """
        ttk.Label(self.parent, text="Show Metrics:", style="LabelName.TLabel").grid(row=4, column=0, sticky=tk.W, pady=5)
        
        for i, (metric_key, var) in enumerate(self.state.visibility.items()):
            label = config.KEY_TO_DISPLAY.get(metric_key, metric_key.title())
            checkbox = ttk.Checkbutton(
                self.parent, 
                text=label, 
                variable=var, 
                command=self.callbacks.get('dropdown_update')
            )
            checkbox.grid(row=5 + i // 2, column=i % 2, sticky=tk.W)

    def _create_chart_controls(self) -> None:
        """Create chart configuration controls.
        
        Creates dropdown selectors for chart metric selection and date range
        options, allowing users to customize the historical weather chart display.
        """
        # Chart metric selector
        ttk.Label(self.parent, text="Chart Metric:", style="LabelName.TLabel").grid(row=4, column=2, sticky=tk.E, pady=5)
        chart_cb = ttk.Combobox(self.parent, textvariable=self.state.chart, state="readonly")
        chart_cb.grid(row=5, column=2, sticky=tk.E)
        self.state.chart_widget = chart_cb

        # Date range selector
        ttk.Label(self.parent, text="Date Range:", style="LabelName.TLabel").grid(row=6, column=2, sticky=tk.E, pady=5)
        range_cb = ttk.Combobox(self.parent, textvariable=self.state.range, state="readonly")
        range_cb['values'] = list(config.CHART["range_options"].keys())
        range_cb.current(0)
        range_cb.grid(row=7, column=2, sticky=tk.E)

    def _create_action_buttons(self) -> None:
        """Create main action buttons for user operations.
        
        Creates Update Weather, Reset, and Cancel buttons with appropriate
        styling and callback connections for primary user actions.
        """
        self.update_button = ttk.Button(
            self.parent, 
            text="Update Weather", 
            command=self.callbacks.get('update'), 
            style="MainButton.TButton"
        )
        self.update_button.grid(row=1, column=2, pady=10, sticky=tk.E)
        
        self.reset_button = ttk.Button(
            self.parent, 
            text="Reset", 
            command=self.callbacks.get('reset'), 
            style="MainButton.TButton"
        )
        self.reset_button.grid(row=2, column=2, pady=5, sticky=tk.E)

        self.cancel_button = ttk.Button(
            self.parent, 
            text="Cancel", 
            command=self.callbacks.get('cancel'), 
            style="MainButton.TButton"
        )
        self.cancel_button.grid(row=3, column=2, pady=5, sticky=tk.E)

    def _configure_grid_weights(self) -> None:
        """Configure grid column weights for proper layout."""
        for i in range(3):
            self.parent.columnconfigure(i, weight=1)
    
    def _bind_events(self) -> None:
        """Bind keyboard events for better UX."""
        if self.city_entry and self.callbacks.get('update'):
            # Enter key in city field triggers update
            self.city_entry.bind("<Return>", lambda e: self.callbacks['update']())

    def _register_widgets_with_state(self) -> None:
        """Register widget references with state for loading management."""
        # Register buttons for loading state management
        self.state.update_button = self.update_button
        self.state.reset_button = self.reset_button
        self.state.cancel_button = self.cancel_button
    
    def update_chart_dropdown_options(self) -> None:
        """Update chart dropdown based on visible metrics."""
        if not hasattr(self.state, 'chart_widget') or not self.state.chart_widget:
            return
        
        # Get data from state (UI-agnostic)
        visible_display_names, has_metrics = self.state.get_current_chart_dropdown_data()
        
        if not visible_display_names:
            self.state.chart_widget['values'] = ["No metrics selected"]
            self.state.chart.set("No metrics selected")
            self.state.chart_widget.configure(state="disabled")
        else:
            self.state.chart_widget['values'] = visible_display_names
            self.state.chart.set(visible_display_names[0])
            self.state.chart_widget.configure(state="readonly")
    
    # LOADING STATE METHODS
    def set_loading_state(self, is_loading: bool, message: str = "") -> None:
        """Sets the loading state of the controls."""
        if is_loading:
            self._disable_controls()
            self._show_progress(message)
        else:
            self._enable_controls()
            self._hide_progress()
    
    def _disable_controls(self) -> None:
        """Disables controls during loading."""
        if self.update_button:
            self.update_button.configure(state='disabled', text="Loading...")
        if self.reset_button:
            self.reset_button.configure(state='disabled')
        if self.cancel_button:
            self.cancel_button.configure(state='normal')
        if self.city_entry:
            self.city_entry.configure(state='disabled')
    
    def _enable_controls(self) -> None:
        """Re-enables controls after loading."""
        if self.update_button:
            self.update_button.configure(state='normal', text="Update Weather")
        if self.reset_button:
            self.reset_button.configure(state='normal')
        if self.cancel_button:
            self.cancel_button.configure(state='disabled') 
        if self.city_entry:
            self.city_entry.configure(state='normal')
    
    def _show_progress(self, message: str) -> None:
        """Shows progress message in status bar."""
        # Delegate to status bar instead of local progress label
        if hasattr(self.state, 'progress_label') and self.state.progress_label:
            self.state.progress_label.configure(text=f"🔄 {message}", foreground="blue")

    def _hide_progress(self) -> None:
        """Hides progress message in status bar."""
        # Delegate to status bar instead of local progress label
        if hasattr(self.state, 'progress_label') and self.state.progress_label:
            self.state.progress_label.configure(text="", foreground="blue")