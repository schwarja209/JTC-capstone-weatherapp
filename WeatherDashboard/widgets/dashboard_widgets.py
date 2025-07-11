"""
Main widget coordinator for the weather dashboard.
"""

from typing import Dict, Any, Callable, List, Optional
import tkinter as tk
from tkinter import ttk, messagebox

from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.widgets.title_widgets import TitleWidget
from WeatherDashboard.widgets.control_widgets import ControlWidgets
from WeatherDashboard.widgets.metric_widgets import MetricDisplayWidgets
from WeatherDashboard.widgets.chart_widgets import ChartWidgets
from WeatherDashboard.widgets.tabbed_widgets import TabbedDisplayWidgets
from WeatherDashboard.widgets.status_bar_widgets import StatusBarWidgets

class WeatherDashboardWidgets:
    """Coordinates all widget components for the weather dashboard."""
    
    def __init__(self, frames: Dict[str, ttk.Frame], state: Any, update_cb: Callable, clear_cb: Callable, dropdown_cb: Callable) -> None:
        self.frames = frames
        self.state = state
        
        # Callback mapping for cleaner organization
        self.callbacks = {
            'update': update_cb,
            'reset': clear_cb,
            'dropdown_update': dropdown_cb
        }
        
        # Widget component references
        self.title_widget: Optional[TitleWidget] = None
        self.control_widgets: Optional[ControlWidgets] = None
        self.tabbed_widgets: Optional[TabbedDisplayWidgets] = None
        self.status_bar_widgets: Optional[StatusBarWidgets] = None
        
        self._initialize_all_widgets()
    
    def _initialize_all_widgets(self) -> None:
        """Initializes all widget components with proper error handling."""
        try:
            self._create_title_section()
            self._create_control_section()
            self._create_tabbed_section()
            self._create_status_bar_section()
            
        except tk.TclError as e:
            Logger.error(f"GUI widget creation failed: {e}")
            messagebox.showerror("GUI Error", f"Failed to create interface: {e}")
            raise
        except Exception as e:
            Logger.error(f"Unexpected error during GUI setup: {e}")
            messagebox.showerror("Setup Error", f"Failed to initialize dashboard: {e}")
            raise
    
    def _create_title_section(self) -> None:
        """Creates the title widget."""
        self.title_widget = TitleWidget(self.frames["title"])
    
    def _create_control_section(self) -> None:
        """Creates the control widgets."""
        self.control_widgets = ControlWidgets(
            self.frames["control"], 
            self.state, 
            self.callbacks
        )
    
    def _create_tabbed_section(self) -> None:
        """Creates the tabbed interface for metrics and charts."""
        self.tabbed_widgets = TabbedDisplayWidgets(
            self.frames["tabbed"], 
            self.state
        )

    def _create_status_bar_section(self) -> None:
        """Creates the status bar widgets."""
        self.status_bar_widgets = StatusBarWidgets(
            self.frames["status_bar"],
            self.state
        )
    
    # DELEGATION METHODS    
    def update_chart_display(self, x_vals: List[str], y_vals: List[Any], metric_key: str, city: str, unit_system: str, fallback: bool = False) -> None:
        """Delegates chart updates to the tabbed chart widget component."""
        if self.chart_widgets:  # Uses the property accessor
            self.chart_widgets.update_chart_display(
                x_vals, y_vals, metric_key, city, unit_system, fallback
            )
    
    # For backward compatibility
    @property
    def metric_widgets(self):
        """Access to metric widgets through tabbed interface."""
        if self.tabbed_widgets:
            return self.tabbed_widgets.get_metric_widgets()
        return None

    @property
    def chart_widgets(self):
        """Access to chart widgets through tabbed interface."""
        if self.tabbed_widgets:
            return self.tabbed_widgets.get_chart_widgets()
        return None