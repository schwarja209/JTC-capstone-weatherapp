"""
Metric display widgets for current weather data.
"""

from typing import Dict, Any
import tkinter as tk
from tkinter import ttk

from WeatherDashboard import config


class MetricDisplayWidgets:
    """Manages the display of current weather metrics."""
    
    def __init__(self, parent_frame: ttk.Frame, state: Any) -> None:
        self.parent = parent_frame
        self.state = state
        
        # Widget references
        self.metric_labels: Dict[str, Dict[str, ttk.Label]] = {}
        self.city_label: Optional[ttk.Label] = None
        self.date_label: Optional[ttk.Label] = None
        self.status_label: Optional[ttk.Label] = None
        
        self._create_all_metrics()
    
    def _create_all_metrics(self) -> None:
        """Creates all metric display widgets."""
        self._create_header_info()
        self._create_weather_metrics()
        self._create_status_display()
        self._register_with_state()
    
    def _create_header_info(self) -> None:
        """Creates city and date display labels."""
        # City label
        ttk.Label(self.parent, text="City:", style="LabelName.TLabel").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.city_label = ttk.Label(self.parent, text="--", width=15, style="LabelValue.TLabel")
        self.city_label.grid(row=0, column=1, sticky=tk.W, pady=5)

        # Date label
        ttk.Label(self.parent, text="Date:", style="LabelName.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.date_label = ttk.Label(self.parent, text="--", width=15, style="LabelValue.TLabel")
        self.date_label.grid(row=1, column=1, sticky=tk.W, pady=5)
    
    def _create_weather_metrics(self) -> None:
        """Creates labels for each weather metric subject to visibility."""
        for i, metric_key in enumerate(config.KEY_TO_DISPLAY):
            row = 0 + i
            
            # Create label and value widgets
            name_label = ttk.Label(self.parent, text=f"{config.KEY_TO_DISPLAY[metric_key]}:", style="LabelName.TLabel")
            value_label = ttk.Label(self.parent, text="--", style="LabelValue.TLabel")
            
            # Position them (initially visible, will be managed by state)
            name_label.grid(row=row, column=2, sticky=tk.W, pady=5)
            value_label.grid(row=row, column=3, sticky=tk.W, pady=5)
            
            # Store references
            self.metric_labels[metric_key] = {
                "label": name_label, 
                "value": value_label
            }
    
    def _create_status_display(self) -> None:
        """Creates status label for API fallback or error messages."""
        self.status_label = ttk.Label(
            self.parent, 
            text="", 
            foreground="red", 
            style="LabelValue.TLabel"
        )
        self.status_label.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=5)
    
    def _register_with_state(self) -> None:
        """Registers widget references with the state manager."""
        self.state.metric_labels = self.metric_labels
        self.state.city_label = self.city_label
        self.state.date_label = self.date_label
        self.state.status_label = self.status_label