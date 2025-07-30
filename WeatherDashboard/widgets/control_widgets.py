"""
Control widgets for user input and actions.

This module provides comprehensive control panel widgets for user interaction
including city input, unit selection, metric visibility controls with two-column
layout, chart settings, and action buttons. Manages loading states during async
operations, event handling, and coordinates with callbacks for application control flow.

Features include dynamic chart dropdown updates based on metric visibility,
bulk selection controls (Select All/Clear All), and loading state management
for responsive user experience during background operations.

Classes:
    ControlWidgets: Main control panel manager with inputs, selections, and actions
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Callable, Optional

from WeatherDashboard import config, styles
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.state_utils import StateUtils
from WeatherDashboard.utils.widget_utils import WidgetUtils

from .base_widgets import BaseWidgetManager, SafeWidgetCreator, widget_error_handler


# ================================
# 1. INITIALIZATION & SETUP
# ================================
class ControlWidgets(BaseWidgetManager):
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
        """Initialize the control widgets with error handling.
        
        Creates all control panel sections including city input, unit selection,
        metric visibility controls, chart settings, and action buttons. Configures
        grid layout, binds events, and registers widgets with state manager.
        
        Args:
            parent_frame: Parent TTK frame to contain the control panel
            state: Application state manager for widget coordination
            callbacks: Dictionary of callback functions for user actions
        """
        # Direct imports for stable utilities
        self.logger = Logger()
        self.config = config
        self.styles = styles
        self.state_utils = StateUtils()
        self.widget_utils = WidgetUtils()

        # Injected dependencies for testable components
        self.parent_frame = parent_frame
        self.state = state
        self.callbacks = callbacks
        
        # Widget references
        self.city_entry: Optional[ttk.Entry] = None
        self.update_button: Optional[ttk.Button] = None
        self.reset_button: Optional[ttk.Button] = None
        self.cancel_button: Optional[ttk.Button] = None
        
        # Initialize base class with error handling
        super().__init__(parent_frame, state, "control widgets")
        
        # Create widgets with standardized error handling
        if not self.safe_create_widgets():
            self.logger.warn("Control widgets created with errors - some functionality may be limited")

    def _create_widgets(self) -> None:
        """Create all control widgets in organized sections with error handling.
        
        Orchestrates the creation of city input, unit selection, metric visibility
        controls, chart settings, and action buttons. Configures layout and events,
        with comprehensive error handling and logging for debugging failures.
        """
        self._create_city_input()
        self._create_unit_selection()
        self._create_metric_visibility()
        self._create_chart_controls()
        self._create_action_buttons()
        self._configure_grid_weights()
        self._bind_events()

# ================================
# 2. BASIC INPUT CONTROLS
# ================================
    @widget_error_handler("city input")
    def _create_city_input(self) -> None:
        """Create city name input field with label using centralized utilities with error handling."""
        layout_config = self.styles.LAYOUT_CONFIG
        city_config = layout_config['widget_positions']['control_panel']['city_input']
        
        city_label = SafeWidgetCreator.create_label(self.parent, text="City:", style="LabelName.TLabel")
        self.city_entry = SafeWidgetCreator.create_entry(self.parent, textvariable=self.state.city)
        
        # Use centralized positioning
        self.widget_utils.position_widget_pair(
            self.parent, city_label, self.city_entry, 
            city_config['row'], city_config['column'], city_config['column']+1, 
            pady=self.styles.CONTROL_PANEL_CONFIG['padding']['standard']
        )

    @widget_error_handler("unit selection")
    def _create_unit_selection(self) -> None:
        """Create unit system selection radio buttons using centralized utilities with error handling."""
        layout_config = self.styles.LAYOUT_CONFIG
        unit_config = layout_config['widget_positions']['control_panel']['unit_selection']
        
        units_label = SafeWidgetCreator.create_label(self.parent, text="Units:", style="LabelName.TLabel")
        units_label.grid(**unit_config, pady=self.styles.CONTROL_PANEL_CONFIG['padding']['standard'])
        
        imperial_radio = SafeWidgetCreator.create_radiobutton(self.parent, "Imperial (°F, mph, inHg)", self.state.unit, "imperial")
        imperial_radio.grid(row=unit_config['row'], column=unit_config['column']+1, sticky=unit_config['sticky'])
        
        metric_radio = SafeWidgetCreator.create_radiobutton(self.parent, "Metric (°C, m/s, hPa)", self.state.unit, "metric")
        metric_radio.grid(row=unit_config['row']+1, column=unit_config['column']+1, sticky=unit_config['sticky'])

# ================================
# 3. METRIC VISIBILITY CONTROLS  
# ================================
    @widget_error_handler("metric visibility")
    def _create_metric_visibility(self) -> None:
        """Create metric visibility controls with two-column checkbox layout.

        Creates visibility control section with header, bulk selection buttons
        (Select All/Clear All), and organized metric checkboxes arranged in
        two-column layout by metric groups.
        """
        # Main section header
        header_frame = SafeWidgetCreator.create_frame(self.parent)
        header_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=self.styles.CONTROL_PANEL_CONFIG['padding']['header'])

        visibility_label = SafeWidgetCreator.create_label(header_frame, "Metrics Visibility:", "LabelName.TLabel")
        visibility_label.pack(side=tk.LEFT)

        # Add Select All / Clear All buttons
        select_all_btn = SafeWidgetCreator.create_button(header_frame, "Select All", self._select_all_metrics, "MainButton.TButton")
        select_all_btn.pack(side=tk.LEFT, padx=self.styles.CONTROL_PANEL_CONFIG['padding']['button_group'])

        clear_all_btn = SafeWidgetCreator.create_button(header_frame, "Clear All", self._clear_all_metrics, "MainButton.TButton")
        clear_all_btn.pack(side=tk.LEFT, padx=self.styles.CONTROL_PANEL_CONFIG['padding']['standard'])
        
        current_row = 5
        
        # Iterate through metric groups with cleaner logic
        for group_key, group_config in self.config.METRIC_GROUPS.items():
            current_row = self._add_metric_group_two_column(group_config, current_row)
            current_row += self.styles.CONTROL_PANEL_CONFIG['spacing']['section'] # Extra space between groups

    def _add_metric_group_two_column(self, group_config: Dict[str, Any], start_row: int) -> int:
        """Add metric group with two-column checkbox layout and error handling.

        Creates group header and arranges visible metrics in two-column grid layout
        with proper row calculations and positioning. Uses SafeWidgetCreator for
        consistent widget creation and handles layout calculations automatically.
        
        Args:
            group_config: Group configuration dictionary from METRIC_GROUPS containing
                        label, display_metrics, and chart_metrics definitions
            start_row: Starting row position for grid layout positioning
            
        Returns:
            int: Next available row position after this group for subsequent widgets
        """
        current_row = start_row
        
        # Group header using SafeWidgetCreator
        group_label = SafeWidgetCreator.create_label(self.parent, f"{group_config['label']}:", "LabelName.TLabel")
        group_label.grid(row=current_row, column=0, sticky=tk.W, pady=self.styles.CONTROL_PANEL_CONFIG['spacing']['group'])
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

    def _add_single_checkbox(self, metric_key: str, row: int, col: int) -> None:
        """Add single checkbox at specified grid position with safe state access."""
        display_label = self.config.ENHANCED_DISPLAY_LABELS.get(metric_key, self.config.METRICS[metric_key]['label'])
        
        checkbox = SafeWidgetCreator.create_checkbutton(self.parent, display_label, self.state_utils.get_metric_visibility_var(self.state, metric_key), self.callbacks.get('dropdown_update'))
        checkbox.grid(row=row, column=col, sticky=tk.W, padx=self.styles.CONTROL_PANEL_CONFIG['padding']['checkbox'])

    def _select_all_metrics(self) -> None:
        """Select all metric visibility checkboxes and update chart dropdown."""
        count = self.state_utils.set_all_metrics_visibility(self.state, True)
        # Update chart dropdown after changing visibility
        if count > 0 and self.callbacks.get('dropdown_update'):
            self.callbacks['dropdown_update']()

    def _clear_all_metrics(self) -> None:
        """Clear all metric visibility checkboxes and update chart dropdown."""
        count = self.state_utils.set_all_metrics_visibility(self.state, False)
        # Update chart dropdown after changing visibility
        if count > 0 and self.callbacks.get('dropdown_update'):
            self.callbacks['dropdown_update']()

# ================================
# 4. CHART & ACTION CONTROLS
# ================================
    @widget_error_handler("chart controls")
    def _create_chart_controls(self) -> None:
        """Create chart configuration controls with error handling."""
        layout_config = self.styles.LAYOUT_CONFIG
        chart_config = layout_config['widget_positions']['control_panel']['chart_controls']
        
        # Chart metric selector
        chart_label = SafeWidgetCreator.create_label(self.parent, "Chart Metric:", "LabelName.TLabel")
        chart_label.grid(**chart_config, pady=self.styles.CONTROL_PANEL_CONFIG['padding']['standard'])

        chart_cb = SafeWidgetCreator.create_combobox(self.parent, textvariable=self.state.chart)
        chart_cb.grid(row=chart_config['row']+1, column=chart_config['column'], sticky=chart_config['sticky'])
        self.state.chart_widget = chart_cb
        
        # Date range selector
        range_label = SafeWidgetCreator.create_label(self.parent, "Date Range:", "LabelName.TLabel")
        range_label.grid(row=chart_config['row']+2, column=chart_config['column'], sticky=chart_config['sticky'], pady=self.styles.CONTROL_PANEL_CONFIG['padding']['standard'])
        
        range_cb = SafeWidgetCreator.create_combobox(self.parent, textvariable=self.state.range)
        range_cb['values'] = list(self.config.CHART["range_options"].keys())
        range_cb.current(0)
        range_cb.grid(row=chart_config['row']+3, column=chart_config['column'], sticky=chart_config['sticky'])

    @widget_error_handler("action buttons")
    def _create_action_buttons(self) -> None:
        """Create main action buttons for user operations with error handling."""
        layout_config = styles.LAYOUT_CONFIG
        action_config = layout_config['widget_positions']['control_panel']['action_buttons']
        
        self.update_button = SafeWidgetCreator.create_button(self.parent, "Update Weather", self.callbacks.get('update'), "MainButton.TButton")
        self.update_button.grid(**action_config, pady=10)
        
        self.reset_button = SafeWidgetCreator.create_button(self.parent, "Reset", self.callbacks.get('reset'), "MainButton.TButton")
        self.reset_button.grid(row=action_config['row']+1, column=action_config['column'], pady=self.styles.CONTROL_PANEL_CONFIG['padding']['standard'], sticky=action_config['sticky'])
        
        self.cancel_button = SafeWidgetCreator.create_button(self.parent, "Cancel", self.callbacks.get('cancel'), "MainButton.TButton")
        self.cancel_button.grid(row=action_config['row']+2, column=action_config['column'], pady=self.styles.CONTROL_PANEL_CONFIG['padding']['standard'], sticky=action_config['sticky'])

    def update_chart_dropdown_options(self) -> None:
        """Update chart dropdown options based on metric visibility and chartability configuration.
        
        Performs comprehensive filtering of available metrics for chart display by evaluating
        both user visibility preferences and intrinsic metric chartability. Updates the chart
        dropdown with filtered options and maintains current selection when possible.
        
        Filtering Process:
            1. Retrieves all metrics from centralized METRICS configuration
            2. Filters by user visibility settings (checkbox states)
            3. Filters by chartable property (metrics suitable for time-series display)
            4. Preserves current dropdown selection if still valid after filtering
            5. Falls back to first available option if current selection invalids
            
        Side Effects:
            - Modifies chart_metric_dropdown values list
            - May change current dropdown selection
            - Triggers dropdown widget refresh
        """
        try:
            if (not hasattr(self.state, 'chart_widget') or not self.state.chart_widget or not hasattr(self.state, 'chart')):
                self.logger.warn("Chart widget not available for dropdown update")
                return
            
            chart_metrics = set()  # Use set to automatically handle duplicates
            
            # Collect unique chartable metrics from visible groups
            for group_key, group_config in self.config.METRIC_GROUPS.items():
                for chart_metric in group_config['chart_metrics']:
                    if self._is_metric_chartable(chart_metric) and self.state_utils.is_metric_visible(self.state, chart_metric):
                        chart_metrics.add(chart_metric)
            
            # Convert to display names and sort for consistent order
            chart_display_names = sorted([
                self.config.METRICS[metric]['label'] for metric in chart_metrics
            ])
            
            # Update dropdown
            if not chart_display_names:
                self.state.chart_widget['values'] = ["No metrics selected"]
                self.state.chart.set("No metrics selected")
                self.state.chart_widget.configure(state="disabled")
            else:
                self.state.chart_widget['values'] = chart_display_names
                current_selection = self.state.chart.get()
                if hasattr(self.state, 'chart') and current_selection not in chart_display_names:
                    self.state.chart.set(chart_display_names[0])
                self.state.chart_widget.configure(state="readonly")
                
        except Exception as e:
            self.logger.error(self.config.ERROR_MESSAGES['config_error'].format(section="chart dropdown", reason=str(e)))
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
        """Configure grid column weights for proper layout using centralized utility."""
        self.widget_utils.configure_grid_weights(self.parent, columns=3)
    
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
    def _is_group_visible(self, group_config: Dict[str, Any]) -> bool:
        """Check if any display metrics in this group are visible using standardized access."""
        return any(
            self.state_utils.is_metric_visible(self.state, display_metric)
            for display_metric in group_config['display_metrics']
        )

    def _is_metric_chartable(self, metric_key: str) -> bool:
        """Check if a metric makes sense to chart based on user requirements.
        
        Excludes:
        - Non-numeric metrics (conditions, weather_main, weather_id, weather_icon)
        - Wind direction and gusts (not meaningful for trend charts)
        - Individual precipitation metrics (use combined precipitation instead)
        """
        return self.config.METRICS.get(metric_key, {}).get('chartable', False)