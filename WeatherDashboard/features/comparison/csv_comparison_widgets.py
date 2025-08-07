"""
CSV comparison widgets for the Weather Dashboard.

This module provides UI widgets for the CSV comparison tab, including
line toggle controls, chart integration, and status displays.
Handles user interaction and coordinates with the CSV data manager.

Classes:
    CSVComparisonWidgets: Main widget manager for CSV comparison tab
    CSVLineToggleWidgets: Widgets for toggling individual CSV lines
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Any, Callable

from WeatherDashboard import styles, config
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.features.comparison.csv_data_manager import CSVDataManager
from WeatherDashboard.widgets.base_widgets import BaseWidgetManager, SafeWidgetCreator, widget_error_handler
from WeatherDashboard.widgets.chart_widgets import ChartWidgets


class CSVLineToggleWidgets:
    """Widgets for toggling individual CSV lines on/off.
    
    Provides checkboxes and controls for enabling/disabling
    individual CSV data series in the comparison chart.
    
    Attributes:
        parent: Parent frame container
        toggle_vars: Dictionary mapping CSV filenames to toggle variables
        toggle_callbacks: Dictionary mapping CSV filenames to callback functions
        logger: Application logger instance
    """
    
    def __init__(self, parent_frame: ttk.Frame) -> None:
        """Initialize the CSV line toggle widgets.
        
        Sets up the toggle controls and callback management
        for individual CSV line visibility.
        
        Args:
            parent_frame: Parent TTK frame to contain the toggle controls
        """
        self.logger = Logger()
        self.parent = parent_frame
        
        # Toggle state management
        self.toggle_vars: Dict[str, tk.BooleanVar] = {}
        self.toggle_callbacks: Dict[str, Callable[[str, bool], None]] = {}
        
        # Create the toggle frame
        self.toggle_frame = SafeWidgetCreator.create_frame(parent_frame)
        self.toggle_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create scrollable frame for toggles
        self._create_scrollable_toggles()
    
    def _create_scrollable_toggles(self) -> None:
        """Create simple frame for CSV line toggles."""
        # Create simple frame
        self.main_frame = SafeWidgetCreator.create_frame(self.parent)
        self.main_frame.pack(fill='x', padx=5, pady=2)
        
        # Create toggle frame
        self.toggle_frame = SafeWidgetCreator.create_frame(self.main_frame)
        self.toggle_frame.pack(fill='x')
    
    def update_csv_toggles(self, csv_files: List[str], available_files: List[str]) -> None:
        """Update CSV line toggle checkboxes.
        
        Args:
            csv_files: List of all CSV filenames
            available_files: List of CSV files that have the current metric
        """
        try:
            # Clear existing toggles
            for widget in self.toggle_frame.winfo_children():
                widget.destroy()
            
            # Create toggles for each CSV file
            for filename in csv_files:
                # Create checkbox
                enabled = filename in available_files
                var = tk.BooleanVar(value=enabled)
                
                checkbox = SafeWidgetCreator.create_checkbutton(
                    self.toggle_frame, 
                    filename, 
                    var,
                    command=lambda f=filename, v=var: self._on_toggle_changed(f, v.get())
                )
                checkbox.pack(side='left', padx=(0, 10))
                
                # Store reference
                self.toggle_vars[filename] = var
                
        except Exception as e:
            self.logger.error(f"Error updating CSV toggles: {e}")
    
    def _on_toggle_changed(self, filename: str, enabled: bool) -> None:
        """Handle toggle state changes.
        
        Calls the registered callback when a toggle state changes.
        
        Args:
            filename: Name of the CSV file
            enabled: Whether the toggle is enabled
        """
        if 'update_chart' in self.toggle_callbacks:
            try:
                self.toggle_callbacks['update_chart'](filename, enabled)
            except Exception as e:
                self.logger.error(f"Error in toggle callback for {filename}: {e}")
    
    def get_enabled_files(self) -> List[str]:
        """Get list of CSV files that are currently enabled.
        
        Returns:
            List of enabled CSV filenames
        """
        enabled_files = []
        for filename, var in self.toggle_vars.items():
            if var.get():
                enabled_files.append(filename)
        return enabled_files


class CSVComparisonWidgets(BaseWidgetManager):
    """Main widget manager for the CSV comparison tab.
    
    Manages all UI components for the CSV comparison feature,
    including line toggles, status displays, and chart integration.
    Coordinates with the CSV data manager and provides user interface
    for CSV data visualization.
    
    Attributes:
        parent: Parent frame container
        state: Application state manager
        data_manager: CSV data manager for data operations
        toggle_widgets: Widgets for line toggle controls
        status_label: Status display label
        chart_widgets: Reference to chart widgets for updates
        logger: Application logger instance
    """
    
    def __init__(self, parent_frame: ttk.Frame, state: Any, 
                 data_manager: Optional[CSVDataManager] = None,
                 chart_widgets: Optional[Any] = None) -> None:
        """Initialize the CSV comparison widgets.
        
        Sets up the UI components for the CSV comparison tab,
        including toggle controls, status displays, and chart integration.
        
        Args:
            parent_frame: Parent TTK frame to contain the comparison widgets
            state: Application state manager
            data_manager: CSV data manager (injected for testability)
            chart_widgets: Chart widgets for data display (injected for testability)
        """
        # Direct imports for stable utilities
        self.logger = Logger()
        self.styles = styles
        self.config = config

        # Injected dependencies for testable components
        self.parent_frame = parent_frame
        self.state = state
        self.data_manager = data_manager or CSVDataManager()
        self.chart_widgets = chart_widgets

        # Widget references
        self.toggle_widgets: Optional[CSVLineToggleWidgets] = None
        self.status_label: Optional[ttk.Label] = None
        self.control_frame: Optional[ttk.Frame] = None
        
        # Initialize base class with error handling
        super().__init__(parent_frame, state, "CSV comparison widgets")
        
        # Create widgets with standardized error handling
        if not self.safe_create_widgets():
            self.logger.warn("CSV comparison widgets created with errors - some functionality may be limited")
    
    def _create_widgets(self) -> None:
        """Create the CSV comparison tab widgets.
        
        Sets up the main layout with toggle controls, status display,
        and chart integration area.
        """
        # Create main layout frame
        self.main_frame = SafeWidgetCreator.create_frame(self.parent)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create chart area - top
        self.chart_frame = SafeWidgetCreator.create_frame(self.main_frame)
        self.chart_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Create legend area - between chart and controls
        self.legend_frame = SafeWidgetCreator.create_frame(self.main_frame)
        self.legend_frame.pack(expand=True, padx=10, pady=(0, 0))

        # Create control panel - bottom
        self.control_frame = SafeWidgetCreator.create_frame(
            self.main_frame
        )
        self.control_frame.pack(side='bottom', fill='y', padx=(0, 0))
        
        # Create toggle widgets
        self.toggle_widgets = CSVLineToggleWidgets(self.control_frame)

        # Register callback for toggle changes
        self.toggle_widgets.toggle_callbacks['update_chart'] = self._on_csv_toggle_changed
        
        # Create status label
        self.status_label = SafeWidgetCreator.create_label(
            self.control_frame,
            text="Ready to load CSV data",
            style="Info.TLabel"
        )
        self.status_label.pack(pady=(0, 0))
        
        # Create chart widget for CSV comparison
        self.chart_widgets = ChartWidgets(self.chart_frame, self.state)

    def _on_csv_toggle_changed(self, filename: str, enabled: bool) -> None:
        """Handle CSV toggle changes and update chart accordingly.
        
        Args:
            filename: Name of the CSV file that was toggled
            enabled: Whether the file is now enabled
        """
        try:
            self.logger.debug(f"CSV toggle changed: {filename} = {enabled}")
            # Update chart with current enabled files
            self.update_csv_chart()
        except Exception as e:
            self.logger.error(f"Error updating chart after toggle change: {e}")

    def update_status(self, message: str) -> None:
        """Update the status display message.
        
        Args:
            message: Status message to display
        """
        if self.status_label:
            self.status_label.config(text=message)
            self.logger.debug(f"CSV comparison status: {message}")
    
    def load_csv_data(self) -> Dict[str, Any]:
        """Load and process all CSV data.
        
        Loads all available CSV files, processes them, and updates
        the UI components accordingly.
        
        Returns:
            Dictionary containing loaded CSV data information
        """
        try:
            self.update_status("Loading CSV data...")
            
            # Load data from CSV data manager
            result = self.data_manager.load_all_csv_data()
            
            if result['files']:
                self.update_status(f"Loaded {len(result['files'])} CSV files")
                
                # Update toggle widgets with only files that have the target city
                target_city = self.state.get_current_city()
                if target_city and self.toggle_widgets:
                    # Get city availability
                    city_availability = self.data_manager.get_city_availability(target_city)
                    available_files = [f for f in result['files'] if city_availability.get(f, False)]
                    
                    self.toggle_widgets.update_csv_toggles(
                        result['files'], 
                        available_files  # Only files with the target city
                    )
                
                # Update chart with loaded data
                self.update_csv_chart()
            else:
                self.update_status("No CSV files found")
            
            return result
            
        except Exception as e:
            error_msg = f"Error loading CSV data: {e}"
            self.update_status(error_msg)
            self.logger.error(error_msg)
            return {'files': [], 'available_metrics': [], 'data': {}}
    
    def get_chart_data(self, metric: str, target_city: str) -> tuple:
        """Get chart-ready data for the specified metric.
        
        Args:
            metric: Standard metric name to chart
            
        Returns:
            Tuple of (dates, values_list, colors, labels, available_files, missing_files) for charting
        """
        try:
            return self.data_manager.get_chart_data(metric, target_city)
        except Exception as e:
            self.logger.error(f"Error getting chart data for metric {metric}: {e}")
            return [], [], [], [], [], []
    
    def get_enabled_files(self) -> List[str]:
        """Get list of currently enabled CSV files.
        
        Returns:
            List of enabled CSV filenames
        """
        if self.toggle_widgets:
            return self.toggle_widgets.get_enabled_files()
        return []
    
    def clear_cache(self) -> None:
        """Clear all cached CSV data.
        
        Clears the data manager cache and updates the status.
        """
        self.data_manager.clear_cache()
        self.update_status("Cache cleared")
    
    def get_available_metrics(self) -> List[str]:
        """Get list of available metrics across all CSV files.
        
        Returns:
            List of available standard metric names
        """
        return self.data_manager.get_available_metrics() 
    
    def update_csv_chart(self, metric: str = None) -> None:
        """Update the CSV comparison chart with data for the specified metric."""
        try:
            if not self.chart_widgets:
                return
                
            # Get metric from state if not provided
            if not metric:
                metric = self.state.get_current_chart_metric()
                if not metric:
                    # Get first available metric
                    available_metrics = self.get_available_metrics()
                    if available_metrics:
                        metric = available_metrics[0]
                    else:
                        self.update_status("No metrics available for charting")
                        return
            
            # Convert display metric name to lowercase key
            # The chart dropdown shows labels like "Temperature" but we need keys like "temperature"
            metric = metric.lower()
                    
            # Get date range from state and convert to integer
            date_range_str = self.state.get_current_range()
            try:
                # Look up the days value from the config using the range string
                date_range_days = self.config.CHART["range_options"].get(date_range_str, 30)
            except (ValueError, TypeError, KeyError):
                date_range_days = 30  # Default to 30 days if conversion fails

            date_range_months = date_range_days  # Direct conversion: days = months

            # Set the date range in the data manager
            self.data_manager.set_date_range(date_range_months)
            
            # Force reload of CSV data with new date range
            self.data_manager.clear_cache()
            self.data_manager.load_all_csv_data(date_range_months)

            # Get current city from state
            target_city = self.state.get_current_city()
            if not target_city:
                self.update_status("Please enter a city name")
                return
            
            # Get enabled files from toggle widgets
            enabled_files = self.toggle_widgets.get_enabled_files() if self.toggle_widgets else None

            # Get chart data filtered by city
            dates, values_list, colors, labels, available_files, missing_files = self.data_manager.get_chart_data(
                metric, target_city, enabled_files, date_range_months
            )
            
            # Debug logging
            self.logger.debug(f"Chart data summary:")
            self.logger.debug(f"  - Available files: {available_files}")
            self.logger.debug(f"  - Missing files: {missing_files}")
            self.logger.debug(f"  - Number of data series: {len(values_list)}")
            self.logger.debug(f"  - Colors: {colors}")
            self.logger.debug(f"  - Labels: {labels}")

            if dates and values_list:
                # Update chart with CSV data
                self.chart_widgets.update_chart_display(
                    dates, values_list, metric, f"{target_city} CSV Comparison", "metric", labels, colors
                )
                # Create legend widget with CSV filenames
                self._create_legend_widget(labels, colors)
                
                # Update status with missing files info
                if missing_files:
                    missing_msg = f"CSVs without {target_city} data: {', '.join(missing_files)}"
                    self.update_status(f"Chart updated with {metric} data ({date_range_months} months). {missing_msg}")
                else:
                    self.update_status(f"Chart updated with {metric} data ({date_range_months} months)")
            else:
                self.update_status(f"No data available for {target_city} in any CSV files")
                
        except Exception as e:
            self.logger.error(f"Error updating CSV chart: {e}")
            self.update_status(f"Error updating chart: {e}")

    def _create_legend_widget(self, labels: List[str], colors: List[str]) -> None:
        """Create a legend widget with city names and colors.
        
        Args:
            labels: List of city names
            colors: List of corresponding colors
        """
        # Clear existing legend
        for widget in self.legend_frame.winfo_children():
            widget.destroy()
        
        if not labels:
            return
        
        # Create legend container - centered
        legend_container = SafeWidgetCreator.create_frame(self.legend_frame)
        legend_container.pack(expand=True, pady=2)
        
        # Create legend items in rows
        items_per_row = 5
        for i in range(0, len(labels), items_per_row):
            row_frame = SafeWidgetCreator.create_frame(legend_container)
            row_frame.pack(expand=True, pady=1)
            
            for j in range(items_per_row):
                if i + j < len(labels):
                    # Create color indicator using a label with background color
                    color_label = SafeWidgetCreator.create_label(
                        row_frame, 
                        text="  ",  # Two spaces for width
                        font=('Arial', 8)
                    )
                    color_label.pack(side='left', padx=(0, 5))
                    color_label.configure(background=colors[i + j])
                    
                    # Create CSV filename label (not city name)
                    csv_label = SafeWidgetCreator.create_label(
                        row_frame, 
                        text=labels[i + j],  # This now shows CSV filenames
                        font=('Arial', 8)
                    )
                    csv_label.pack(side='left', padx=(0, 15))