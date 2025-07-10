"""
Widget creation and management for the weather dashboard.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from WeatherDashboard import config
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.unit_converter import UnitConverter
from WeatherDashboard.utils.utils import format_fallback_status


class WeatherDashboardWidgets:
    '''Creates and manages the widgets for the weather dashboard.'''
    def __init__(self, frames, state, update_cb, clear_cb, dropdown_cb):
        self.frames = frames
        self.state = state
        self.update_cb = update_cb
        self.clear_cb = clear_cb
        self.dropdown_cb = dropdown_cb

        self.metric_labels = {}
        self.chart_canvas = None
        self.chart_fig = None
        self.chart_ax = None

        try:
            self.create_title_widgets()
            self.create_control_widgets()
            self.create_metric_widgets()
            self.create_chart_widgets()
            self.bind_entry_events()
        except tk.TclError as e:
            Logger.error(f"GUI widget creation failed: {e}")
            messagebox.showerror("GUI Error", f"Failed to create interface: {e}")
            raise
        except Exception as e:
            Logger.error(f"Unexpected error during GUI setup: {e}")
            messagebox.showerror("Setup Error", f"Failed to initialize dashboard: {e}")
            raise

    def create_title_widgets(self):
        '''Creates the title label for the dashboard.'''
        label = ttk.Label(self.frames["title"], text="Weather Dashboard", style="Title.TLabel")
        label.pack()

    def create_control_widgets(self):
        '''Creates the control widgets for user input and actions.'''
        control = self.frames["control"]
        
        try:
            self._create_city_input(control)
            self._create_unit_selection(control)
            self._create_metric_visibility(control)
            self._create_chart_controls(control)
            self._create_action_buttons(control)
            self._configure_grid_weights(control)
        except Exception as e:
            Logger.error(f"Failed to create control widgets: {e}")
            raise

    def _create_city_input(self, control):
        '''Creates city input field.'''
        ttk.Label(control, text="City:", style="LabelName.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.city_entry = ttk.Entry(control, textvariable=self.state.city)
        self.city_entry.grid(row=1, column=1, sticky=tk.W)

    def _create_unit_selection(self, control):
        '''Creates unit selection radio buttons.'''
        ttk.Label(control, text="Units:", style="LabelName.TLabel").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(control, text="Imperial (°F, mph, inHg)", variable=self.state.unit, value="imperial").grid(row=2, column=1, sticky=tk.W)
        ttk.Radiobutton(control, text="Metric (°C, m/s, hPa)", variable=self.state.unit, value="metric").grid(row=3, column=1, sticky=tk.W)

    def _create_metric_visibility(self, control):
        '''Creates metric visibility checkboxes.'''
        ttk.Label(control, text="Show Metrics:", style="LabelName.TLabel").grid(row=4, column=0, sticky=tk.W, pady=5)
        for i, (metric_key, var) in enumerate(self.state.visibility.items()):
            label = config.KEY_TO_DISPLAY.get(metric_key, metric_key.title())
            checkbox = ttk.Checkbutton(control, text=label, variable=var, command=self.dropdown_cb)
            checkbox.grid(row=5 + i // 2, column=i % 2, sticky=tk.W)

    def _create_chart_controls(self, control):
        '''Creates chart metric and date range selectors.'''
        ttk.Label(control, text="Chart Metric:", style="LabelName.TLabel").grid(row=4, column=2, sticky=tk.E, pady=5)
        chart_cb = ttk.Combobox(control, textvariable=self.state.chart, state="readonly")
        chart_cb.grid(row=5, column=2, sticky=tk.E)
        self.state.chart_widget = chart_cb

        ttk.Label(control, text="Date Range:", style="LabelName.TLabel").grid(row=6, column=2, sticky=tk.E, pady=5)
        range_cb = ttk.Combobox(control, textvariable=self.state.range, state="readonly")
        range_cb['values'] = list(config.CHART["range_options"].keys())
        range_cb.current(0)
        range_cb.grid(row=7, column=2, sticky=tk.E)

    def _create_action_buttons(self, control):
        '''Creates update and reset buttons.'''
        ttk.Button(control, text="Update Weather", command=self.update_cb, style="MainButton.TButton").grid(row=1, column=2, pady=10, sticky=tk.E)
        ttk.Button(control, text="Reset", command=self.clear_cb, style="MainButton.TButton").grid(row=2, column=2, pady=5, sticky=tk.E)

    def _configure_grid_weights(self, control):
        '''Configures grid column weights for proper layout.'''
        for i in range(3):
            control.columnconfigure(i, weight=1)

    def create_metric_widgets(self):
        '''Creates the metric display widgets for current weather data.'''
        metric = self.frames["metric"]

        ttk.Label(metric, text="City:", style="LabelName.TLabel").grid(row=0, column=0, sticky=tk.W, pady=5) # City label
        self.city_label = ttk.Label(metric, text="--", width=15, style="LabelValue.TLabel")
        self.city_label.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.state.city_label = self.city_label

        ttk.Label(metric, text="Date:", style="LabelName.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5) # Date label
        self.date_label = ttk.Label(metric, text="--", width=15, style="LabelValue.TLabel")
        self.date_label.grid(row=1, column=1, sticky=tk.W, pady=5)
        self.state.date_label = self.date_label

        for i, metric_key in enumerate(config.KEY_TO_DISPLAY): # Create labels for each metric subject to visibility
            row = 0 + i
            name = ttk.Label(metric, text=f"{config.KEY_TO_DISPLAY[metric_key]}:", style="LabelName.TLabel")
            value = ttk.Label(metric, text="--", style="LabelValue.TLabel")
            name.grid(row=row, column=2, sticky=tk.W, pady=5)
            value.grid(row=row, column=3, sticky=tk.W, pady=5)
            self.metric_labels[metric_key] = {"label": name, "value": value}
        self.state.metric_labels = self.metric_labels

        self.status_label = ttk.Label(metric, text="", foreground="red", style="LabelValue.TLabel") # Status label for API fallback or errors
        self.status_label.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=5)
        self.state.status_label = self.status_label

    def create_chart_widgets(self):
        '''Creates the chart display for historical weather trends.'''
        try:
            fig = Figure(figsize=(8, 3), dpi=100)
            ax = fig.add_subplot(111)
            canvas = FigureCanvasTkAgg(fig, master=self.frames["chart"])

            self.chart_fig = fig
            self.chart_ax = ax
            self.chart_canvas = canvas

            self.state.register_chart_widgets(canvas, fig, ax)

            ax.set_title("")
            ax.set_xlabel("")
            ax.set_ylabel("")

            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        except Exception as e:
            Logger.error(f"Failed to create chart widgets: {e}")
            # Create a simple label as fallback
            fallback_label = ttk.Label(self.frames["chart"], text="Chart unavailable")
            fallback_label.pack()
            self.chart_fig = None
            self.chart_ax = None
            self.chart_canvas = None
            self.state.register_chart_widgets(None, None, None)

    def update_chart_display(self, x_vals, y_vals, metric_key, city, unit_system, fallback=False):
        '''Updates the chart display with new data for the specified metric and city.'''
        if not self.state.is_chart_available():
            Logger.warn("Chart display unavailable - matplotlib setup failed")
            return

        ax = self.state.chart_ax
        ax.clear()
        ax.plot(x_vals, y_vals, marker="o")

        label = config.KEY_TO_DISPLAY.get(metric_key, metric_key.title())
        unit = UnitConverter.get_unit_label(metric_key, unit_system)

        ax.set_title(f"{label} {format_fallback_status(fallback, 'display')} in {city}")
        ax.set_xlabel("Date")
        ax.set_ylabel(f"{label} ({unit})")

        self.state.chart_fig.autofmt_xdate(rotation=45)
        self.state.chart_fig.tight_layout()
        self.state.chart_canvas.draw()
    
    def bind_entry_events(self):
        '''Binds events for immediate updates'''
        self.city_entry.bind("<Return>", lambda e: self.update_cb()) # Pressing Enter in city entry triggers update