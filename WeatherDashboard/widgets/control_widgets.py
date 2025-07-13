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

from WeatherDashboard import config, styles
from WeatherDashboard.utils.logger import Logger


# ================================
# 1. INITIALIZATION & SETUP
# ================================
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
    
    def _get_metric_visibility_var(self, metric_key: str) -> tk.BooleanVar:
        """Safely get metric visibility variable with fallback."""
        return self.state.visibility.get(metric_key, tk.BooleanVar())
    
    def _is_metric_visible(self, metric_key: str) -> bool:
        """Safely check if a metric is currently visible."""
        return self._get_metric_visibility_var(metric_key).get()

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

# ================================
# 2. BASIC INPUT CONTROLS
# ================================
    def _create_city_input(self) -> None:
        """Create city name input field with label.
        
        Creates a labeled text entry field for city name input, bound to the
        state city variable for automatic state synchronization.
        """
        ttk.Label(self.parent, text="City:", style="LabelName.TLabel").grid(row=1, column=0, sticky=tk.W, pady=styles.CONTROL_PANEL_CONFIG['padding']['standard'])
        self.city_entry = ttk.Entry(self.parent, textvariable=self.state.city)
        self.city_entry.grid(row=1, column=1, sticky=tk.W)

    def _create_unit_selection(self) -> None:
        """Create unit system selection radio buttons.
        
        Creates Imperial and Metric radio button options for temperature,
        wind speed, and pressure unit selection, bound to state unit variable.
        """
        ttk.Label(self.parent, text="Units:", style="LabelName.TLabel").grid(row=2, column=0, sticky=tk.W, pady=styles.CONTROL_PANEL_CONFIG['padding']['standard'])
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

# ================================
# 3. METRIC VISIBILITY CONTROLS  
# ================================
    def _create_metric_visibility(self):
        """Create metric visibility controls using existing two-column design."""
        
        # Main section header (unchanged)
        # Main section header with select/clear buttons
        header_frame = ttk.Frame(self.parent)
        header_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=styles.CONTROL_PANEL_CONFIG['padding']['header'])

        ttk.Label(header_frame, text="Metrics Visibility:", style="LabelName.TLabel").pack(side=tk.LEFT)

        # Add Select All / Clear All buttons
        ttk.Button(header_frame, text="Select All", command=self._select_all_metrics, 
                style="MainButton.TButton").pack(side=tk.LEFT, padx=styles.CONTROL_PANEL_CONFIG['padding']['button_group'])
        ttk.Button(header_frame, text="Clear All", command=self._clear_all_metrics, 
                style="MainButton.TButton").pack(side=tk.LEFT, padx=styles.CONTROL_PANEL_CONFIG['padding']['standard'])
        
        current_row = 5
        
        # Iterate through metric groups with cleaner logic
        for group_key, group_config in config.METRIC_GROUPS.items():
            current_row = self._add_metric_group_two_column(group_config, current_row)
            current_row += styles.CONTROL_PANEL_CONFIG['spacing']['section'] # Extra space between groups

    def _add_metric_group_two_column(self, group_config, start_row):
        """Add metric group with existing two-column layout, cleaner logic.
        
        Args:
            group_config: Group configuration from METRIC_GROUPS
            start_row: Starting row position
            
        Returns:
            int: Next available row after this group
        """
        current_row = start_row
        
        # Group header (unchanged design)
        ttk.Label(self.parent, text=f"{group_config['label']}:", style="LabelName.TLabel").grid(
            row=current_row, column=0, sticky=tk.W, pady=styles.CONTROL_PANEL_CONFIG['spacing']['group'])
        current_row += 1
        
        # Add metrics in two-column layout with cleaner logic
        metrics_to_add = [m for m in group_config['display_metrics'] if m in self.state.visibility]
        
        for i, metric_key in enumerate(metrics_to_add):
            row = current_row + (i // 2)  # Integer division for row calculation
            col = i % 2  # Modulo for column (0 or 1)
            
            self._add_single_checkbox(metric_key, row, col)
        
        # Calculate next available row
        rows_used = (len(metrics_to_add) + 1) // 2  # Ceiling division
        return current_row + rows_used

    def _add_single_checkbox(self, metric_key, row, col):
        """Add single checkbox at specified position with safe state access.
        
        Args:
            metric_key: Metric key
            row: Grid row
            col: Grid column (0 or 1)
        """
        display_label = config.ENHANCED_DISPLAY_LABELS.get(metric_key, config.METRICS[metric_key]['label'])
        
        checkbox = ttk.Checkbutton(
            self.parent, 
            text=display_label, 
            variable=self._get_metric_visibility_var(metric_key),
            command=self.callbacks.get('dropdown_update')
        )
        checkbox.grid(row=row, column=col, sticky=tk.W, padx=styles.CONTROL_PANEL_CONFIG['padding']['checkbox'])

    def _select_all_metrics(self) -> None:
        """Select all metric visibility checkboxes."""
        for metric_key, var in self.state.visibility.items():
            var.set(True)
        # Update chart dropdown after changing visibility
        if self.callbacks.get('dropdown_update'):
            self.callbacks['dropdown_update']()

    def _clear_all_metrics(self) -> None:
        """Clear all metric visibility checkboxes."""
        for metric_key, var in self.state.visibility.items():
            var.set(False)
        # Update chart dropdown after changing visibility
        if self.callbacks.get('dropdown_update'):
            self.callbacks['dropdown_update']()

# ================================
# 4. CHART & ACTION CONTROLS
# ================================
    def _create_chart_controls(self) -> None:
        """Create chart configuration controls.
        
        Creates dropdown selectors for chart metric selection and date range
        options, allowing users to customize the historical weather chart display.
        """
        # Chart metric selector
        ttk.Label(self.parent, text="Chart Metric:", style="LabelName.TLabel").grid(row=4, column=2, sticky=tk.E, pady=styles.CONTROL_PANEL_CONFIG['padding']['standard'])
        chart_cb = ttk.Combobox(self.parent, textvariable=self.state.chart, state="readonly")
        chart_cb.grid(row=5, column=2, sticky=tk.E)
        self.state.chart_widget = chart_cb

        # Date range selector
        ttk.Label(self.parent, text="Date Range:", style="LabelName.TLabel").grid(row=6, column=2, sticky=tk.E, pady=styles.CONTROL_PANEL_CONFIG['padding']['standard'])
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
        self.reset_button.grid(row=2, column=2, pady=styles.CONTROL_PANEL_CONFIG['padding']['standard'], sticky=tk.E)

        self.cancel_button = ttk.Button(
            self.parent, 
            text="Cancel", 
            command=self.callbacks.get('cancel'), 
            style="MainButton.TButton"
        )
        self.cancel_button.grid(row=3, column=2, pady=styles.CONTROL_PANEL_CONFIG['padding']['standard'], sticky=tk.E)

    def update_chart_dropdown_options(self):
        """Update chart dropdown using centralized metric configuration with error handling."""
        try:
            if not hasattr(self.state, 'chart_widget') or not self.state.chart_widget:
                Logger.warn("Chart widget not available for dropdown update")
                return
            
            chart_metrics = set()  # Use set to automatically handle duplicates
            
            # Collect unique chartable metrics from visible groups
            for group_key, group_config in config.METRIC_GROUPS.items():
                if self._is_group_visible(group_config):
                    for chart_metric in group_config['chart_metrics']:
                        if self._is_metric_chartable(chart_metric):
                            chart_metrics.add(chart_metric)
            
            # Convert to display names and sort for consistent order
            chart_display_names = sorted([
                config.METRICS[metric]['label'] for metric in chart_metrics
            ])
            
            # Update dropdown
            if not chart_display_names:
                self.state.chart_widget['values'] = ["No metrics selected"]
                self.state.chart.set("No metrics selected")
                self.state.chart_widget.configure(state="disabled")
            else:
                self.state.chart_widget['values'] = chart_display_names
                current_selection = self.state.chart.get()
                if current_selection not in chart_display_names:
                    self.state.chart.set(chart_display_names[0])
                self.state.chart_widget.configure(state="readonly")
                
        except Exception as e:
            Logger.error(f"Failed to update chart dropdown options: {e}")
            # Graceful degradation - set to disabled state
            try:
                if hasattr(self.state, 'chart_widget') and self.state.chart_widget:
                    self.state.chart_widget['values'] = ["Error updating options"]
                    self.state.chart.set("Error updating options")
                    self.state.chart_widget.configure(state="disabled")
            except Exception:
                pass  # If even the fallback fails, just continue

# ================================
# 5. LAYOUT & EVENT HANDLING
# ================================
    def _configure_grid_weights(self) -> None:
        """Configure grid column weights for proper layout."""
        for i in range(3):
            self.parent.columnconfigure(i, weight=1)
    
    def _bind_events(self) -> None:
        """Bind keyboard events for better UX."""
        if self.city_entry and self.callbacks.get('update'):
            # Enter key in city field triggers update
            self.city_entry.bind("<Return>", lambda e: self.callbacks['update']())

# ================================
# 6. LOADING STATE MANAGEMENT
# ================================
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
        pass

    def _hide_progress(self) -> None:
        """Hides progress message in status bar."""
        # Delegate to status bar instead of local progress label
        pass

# ================================
# 7. CHART UTILITY METHODS
# ================================
    def _is_group_visible(self, group_config):
        """Check if any display metrics in this group are visible using standardized access."""
        return any(
            self._is_metric_visible(display_metric)
            for display_metric in group_config['display_metrics']
        )

    def _is_metric_chartable(self, metric_key: str) -> bool:
        """Check if a metric makes sense to chart based on user requirements.
        
        Excludes:
        - Non-numeric metrics (conditions, weather_main, weather_id, weather_icon)
        - Wind direction and gusts (not meaningful for trend charts)
        - Individual precipitation metrics (use combined precipitation instead)
        """
        # Non-numeric metrics that can't be charted
        non_chartable = {
            'conditions', 'weather_main', 'weather_id', 'weather_icon'
        }
        
        # Wind metrics that don't make sense for trending
        non_trending_wind = {
            'wind_direction', 'wind_gust'
        }
        
        # Raw precipitation details (simplified rain/snow are chartable)
        raw_precipitation_details = {
            'rain_1h', 'rain_3h', 'snow_1h', 'snow_3h'
        }
        
        excluded_metrics = non_chartable | non_trending_wind | raw_precipitation_details
        
        return metric_key not in excluded_metrics