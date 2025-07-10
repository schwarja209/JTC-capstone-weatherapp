'''
Weather Dashboard - Combining HW 8 and 10, and refactoring
- GUI from weather_dashboard_big.py
- Live data via OpenWeatherMap API (current only)
- Simulated past data via fallback generator
- Modular design with separate service and generator
- All API calls are user-triggered; chart is simulated
'''

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os

try:
    from WeatherDashboard import config
except ValueError as e:
    print(f"Configuration error: {e}")
    import sys
    sys.exit(1)

from WeatherDashboard.utils.utils import (
    normalize_city_name,
    city_key,
    is_fallback,
    format_fallback_status,
    validate_unit_system
)
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.utils.unit_converter import UnitConverter

from WeatherDashboard.services.weather_service import WeatherAPIService
from WeatherDashboard.services.api_exceptions import (
    WeatherDashboardError,
    WeatherAPIError,
    CityNotFoundError,
    ValidationError,
    RateLimitError,
    NetworkError
)

# Ensure required directories exist at app startup
for folder in {config.OUTPUT["data_dir"], config.OUTPUT["log_dir"]}:
    os.makedirs(folder, exist_ok=True)


class WeatherDataManager:
    '''Manages weather data fetching and storage, including fallback handling.'''
    def __init__(self):
        self.api_service = WeatherAPIService()
        self.weather_data = {}

    def fetch_current(self, city, unit_system):
        '''Fetches current weather data for a city, using fallback if API call fails.
        
        Args:
            city (str): Normalized city name (expected to already be processed)
            unit_system (str): Target unit system for the data
        '''
        raw_data, use_fallback, error_exception = self.api_service.fetch_current(city)

        # All API and fallback data is assumed to be in metric units and converted downstream.
        # If this changes in future (e.g., new fallback with imperial), update convert_units().
        converted_data = self.convert_units(raw_data, unit_system)

        key = city_key(city)
        existing_data = self.weather_data.setdefault(key, [])
        last_date = existing_data[-1].get("date") if existing_data else None
        current_date = converted_data.get("date")
        if not existing_data or (last_date and current_date and last_date.date() != current_date.date()):
            existing_data.append(converted_data)
            # Limit stored data to prevent memory issues (keep last 30 entries per city)
            max_entries = 30
            if len(existing_data) > max_entries:
                existing_data[:] = existing_data[-max_entries:]  # Keep only the most recent entries

        return converted_data, use_fallback, error_exception
    
    def convert_units(self, data, unit_system):
        '''Converts weather data units based on the selected UI unit system (metric or imperial).'''
        validate_unit_system(unit_system)

        # Skip conversion if already in target system
        if unit_system == "metric":
            return data.copy()
        
        converted = data.copy()
        
        # Get unit mappings from config
        unit_config = config.UNITS.get("metric_units", {})
        
        # Define converter functions mapping
        converters = {
            'temperature': UnitConverter.convert_temperature,
            'pressure': UnitConverter.convert_pressure,
            'wind_speed': UnitConverter.convert_wind_speed
        }
        
        conversion_errors = []  # Track conversion failures

        # Apply conversions using config-defined units
        for field, converter_func in converters.items():
            if field in data and data[field] is not None and field in unit_config:
                try:
                    from_unit = unit_config[field]["metric"]  # Always convert from metric
                    to_unit = unit_config[field]["imperial"]  # To imperial
                    converted[field] = converter_func(data[field], from_unit, to_unit)
                except (ValueError, TypeError, KeyError) as e:
                    Logger.warn(f"Failed to convert {field}: {e}")
                    conversion_errors.append(field)
                    # Keep original value if conversion fails
        
        
        if conversion_errors: # Track which fields failed conversion
            converted['_conversion_warnings'] = f"Some units could not be converted: {', '.join(conversion_errors)}"

        return converted

    def get_historical(self, city, num_days):
        '''Fetches historical weather data for a city. Currently always defaults to fallback.'''
        return self.api_service.fallback.generate(city, num_days)

    def get_recent_data(self, city, days_back=7):
        '''Returns recent weather data for a city from the last N days.
        
        Args:
            city: City name
            days_back: Number of days to look back (default 7)
        
        Returns:
            List of weather data entries from the specified time period
        
        Note: Reserved for future features like trend analysis or prediction.
        '''
        city_data = self.weather_data.get(city_key(city), [])
        cutoff_date = datetime.now().date() - timedelta(days=days_back)
        
        return [
            entry for entry in city_data 
            if entry.get('date', datetime.now()).date() >= cutoff_date
        ]

    def write_to_file(self, city, data, unit_system):
        '''Writes formatted weather data to a log file with timestamp and unit system information.'''
        log_entry = self.format_data_for_logging(city, data, unit_system)
        with open(config.OUTPUT["log"], "a", encoding="utf-8") as f:
            f.write(log_entry)

        status = format_fallback_status(is_fallback(data), "log")
        Logger.info(f"Weather data written for {city_key(city)} - {status}")

    def format_data_for_logging(self, city, data, unit_system):
        '''Formats weather data for logging to a file with timestamp and unit system information.'''
        timestamp = data.get('date', datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            f"\n\nTime: {timestamp}",
            f"City: {city_key(city)}",
            f"Temperature: {UnitConverter.format_value('temperature', data.get('temperature'), unit_system)}",
            f"Humidity: {UnitConverter.format_value('humidity', data.get('humidity'), unit_system)}",
            f"Pressure: {UnitConverter.format_value('pressure', data.get('pressure'), unit_system)}",
            f"Wind Speed: {UnitConverter.format_value('wind_speed', data.get('wind_speed'), unit_system)}",
            f"Conditions: {data.get('conditions', '--')}"
        ]
        return "\n".join(lines)
    
    def cleanup_old_data(self, days_to_keep=30):
        '''Removes weather data older than specified days to free memory.'''
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        for city_key, data_list in self.weather_data.items():
            # Filter out entries older than cutoff date
            self.weather_data[city_key] = [
                entry for entry in data_list 
                if entry.get('date', datetime.now()) >= cutoff_date
            ]


class WeatherDashboardGUIFrames:
    '''Creates and manages the main GUI frames for the weather dashboard.'''
    def __init__(self, root):
        self.root = root
        self.frames = {}
        self.create_styles()
        self.create_frames()

    def create_styles(self):
        '''Configures the styles for the GUI elements.'''
        style = ttk.Style()
        style.configure("FrameLabel.TLabelframe.Label", font=('Arial', 15, 'bold'))
        style.configure("LabelName.TLabel", font=('Arial', 10, 'bold'))
        style.configure("LabelValue.TLabel", font=('Arial', 10))
        style.configure("MainButton.TButton", font=('Arial', 10, 'bold'), padding=5)
        style.configure("Title.TLabel", font=('Comic Sans MS', 20, 'bold'))

    def create_frames(self):
        '''Creates the main frames for the dashboard layout.'''
        self.frames["title"] = ttk.Frame(self.root, padding="10")
        self.frames["title"].grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.frames["control"] = ttk.LabelFrame(self.root, text="Controls", padding="10", style="FrameLabel.TLabelframe")
        self.frames["control"].grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W, tk.E), padx=10)

        self.frames["metric"] = ttk.LabelFrame(self.root, text="Current Weather", padding="10", style="FrameLabel.TLabelframe")
        self.frames["metric"].grid(row=1, column=1, sticky=(tk.N, tk.S, tk.W, tk.E), padx=10)

        self.frames["chart"] = ttk.LabelFrame(self.root, text="Weather Trends", padding="10", style="FrameLabel.TLabelframe")
        self.frames["chart"].grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=0)


class WeatherDashboardWidgets:
    '''Creates and manages the widgets for the weather dashboard.'''
    def __init__(self, frames, gui_vars, update_cb, clear_cb, dropdown_cb):
        self.frames = frames
        self.gui_vars = gui_vars
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
        self.city_entry = ttk.Entry(control, textvariable=self.gui_vars['city'])
        self.city_entry.grid(row=1, column=1, sticky=tk.W)

    def _create_unit_selection(self, control):
        '''Creates unit selection radio buttons.'''
        ttk.Label(control, text="Units:", style="LabelName.TLabel").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(control, text="Imperial (°F, mph, inHg)", variable=self.gui_vars['unit'], value="imperial").grid(row=2, column=1, sticky=tk.W)
        ttk.Radiobutton(control, text="Metric (°C, m/s, hPa)", variable=self.gui_vars['unit'], value="metric").grid(row=3, column=1, sticky=tk.W)

    def _create_metric_visibility(self, control):
        '''Creates metric visibility checkboxes.'''
        ttk.Label(control, text="Show Metrics:", style="LabelName.TLabel").grid(row=4, column=0, sticky=tk.W, pady=5)
        for i, (metric_key, var) in enumerate(self.gui_vars['visibility'].items()):
            label = config.KEY_TO_DISPLAY.get(metric_key, metric_key.title())
            checkbox = ttk.Checkbutton(control, text=label, variable=var, command=self.dropdown_cb)
            checkbox.grid(row=5 + i // 2, column=i % 2, sticky=tk.W)

    def _create_chart_controls(self, control):
        '''Creates chart metric and date range selectors.'''
        ttk.Label(control, text="Chart Metric:", style="LabelName.TLabel").grid(row=4, column=2, sticky=tk.E, pady=5)
        chart_cb = ttk.Combobox(control, textvariable=self.gui_vars['chart'], state="readonly")
        chart_cb.grid(row=5, column=2, sticky=tk.E)
        self.gui_vars['chart_widget'] = chart_cb

        ttk.Label(control, text="Date Range:", style="LabelName.TLabel").grid(row=6, column=2, sticky=tk.E, pady=5)
        range_cb = ttk.Combobox(control, textvariable=self.gui_vars['range'], state="readonly")
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

        ttk.Label(metric, text="Date:", style="LabelName.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5) # Date label
        self.date_label = ttk.Label(metric, text="--", width=15, style="LabelValue.TLabel")
        self.date_label.grid(row=1, column=1, sticky=tk.W, pady=5)

        for i, metric_key in enumerate(config.KEY_TO_DISPLAY): # Create labels for each metric subject to visibility
            row = 0 + i
            name = ttk.Label(metric, text=f"{config.KEY_TO_DISPLAY[metric_key]}:", style="LabelName.TLabel")
            value = ttk.Label(metric, text="--", style="LabelValue.TLabel")
            name.grid(row=row, column=2, sticky=tk.W, pady=5)
            value.grid(row=row, column=3, sticky=tk.W, pady=5)
            self.metric_labels[metric_key] = {"label": name, "value": value}

        self.status_label = ttk.Label(metric, text="", foreground="red", style="LabelValue.TLabel") # Status label for API fallback or errors
        self.status_label.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=5)

    def create_chart_widgets(self):
        '''Creates the chart display for historical weather trends.'''
        try:
            fig = Figure(figsize=(8, 3), dpi=100)
            ax = fig.add_subplot(111)
            canvas = FigureCanvasTkAgg(fig, master=self.frames["chart"])

            self.chart_fig = fig
            self.chart_ax = ax
            self.chart_canvas = canvas

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

    def update_chart_display(self, x_vals, y_vals, metric_key, city, unit_system, fallback=False):
        '''Updates the chart display with new data for the specified metric and city.'''
        if self.chart_ax is None:
            Logger.warn("Chart display unavailable - matplotlib setup failed")
            return

        ax = self.chart_ax
        ax.clear()
        ax.plot(x_vals, y_vals, marker="o")

        label = config.KEY_TO_DISPLAY.get(metric_key, metric_key.title())
        unit = UnitConverter.get_unit_label(metric_key, unit_system)

        ax.set_title(f"{label} {format_fallback_status(fallback, 'display')} in {city}")
        ax.set_xlabel("Date")
        ax.set_ylabel(f"{label} ({unit})")

        self.chart_fig.autofmt_xdate(rotation=45)
        self.chart_fig.tight_layout()
        self.chart_canvas.draw()
    
    def bind_entry_events(self):
        '''Binds events for immediate updates'''
        self.city_entry.bind("<Return>", lambda e: self.update_cb()) # Pressing Enter in city entry triggers update


class WeatherDataController:
    '''Handles fetching and returning weather data without interacting with GUI.'''
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def get_city_data(self, city_name, unit_system):
        '''Fetches weather data for a city. Handles fallback. Returns (city, data, fallback_flag).'''
        # Normalize once at the entry point
        try:
            city = normalize_city_name(city_name)
            validate_unit_system(unit_system) 
        except ValueError as e:
            # Convert to our custom exception for consistent error handling
            raise ValidationError(str(e))
        
        data, use_fallback, error_exception = self.data_manager.fetch_current(city, unit_system)
        
        return city, data, error_exception

    def get_historical_data(self, city_name, num_days, unit_system):
        '''Fetches historical data and applies unit conversion.'''
        # Normalize once at the entry point
        try:
            city = normalize_city_name(city_name)
            validate_unit_system(unit_system) 
        except ValueError as e:
            raise ValidationError(str(e))
        
        raw = self.data_manager.get_historical(city, num_days)

        source_unit = "metric"  # Same as generator’s output
        if unit_system == source_unit:
            return raw
        return [self.data_manager.convert_units(d, unit_system) for d in raw]

    def write_to_log(self, city, data, unit):
        '''Writes weather data to log file with timestamp and unit system information.'''
        validate_unit_system(unit)
        self.data_manager.write_to_file(city, data, unit)


class WeatherViewModel:
    '''Prepares sanitized, display-ready data from raw weather data.
    
    This class encapsulates all display formatting logic, making it easy to:
    - Test formatting logic in isolation
    - Move to a separate views module later
    - Extend with additional display features
    '''

    def __init__(self, city, data, unit_system):
        self.city_name = city
        self.unit_system = unit_system
        self.raw_data = data
        
        # Process all display data on initialization
        self.date_str = self._format_date()
        self.status = self._format_status()
        self.metrics = self._format_metrics()

    def _format_date(self):
        '''Formats the date for display.'''
        if 'date' in self.raw_data and self.raw_data['date']:
            return self.raw_data['date'].strftime("%Y-%m-%d")
        return "--"

    def _format_status(self):
        '''Formats the status text including fallback and warning info.'''
        status = f" {format_fallback_status(is_fallback(self.raw_data), 'display')}"
        
        # Check for conversion warnings
        if '_conversion_warnings' in self.raw_data:
            status += f" (Warning: {self.raw_data['_conversion_warnings']})"
        
        return status

    def _format_metrics(self):
        '''Formats all weather metrics for display.'''
        metrics = {}
        for key in config.KEY_TO_DISPLAY:
            raw_value = self.raw_data.get(key, "--")
            display_val = UnitConverter.format_value(key, raw_value, self.unit_system)
            metrics[key] = display_val
        return metrics

    def get_display_data(self):
        '''Returns all formatted data as a dictionary.
        
        This method makes it easy to pass data around without exposing
        internal ViewModel structure.
        '''
        return {
            'city_name': self.city_name,
            'date_str': self.date_str,
            'status': self.status,
            'metrics': self.metrics
        }

    def has_warnings(self):
        '''Returns True if there are any warnings to display.'''
        return '_conversion_warnings' in self.raw_data

    def get_metric_value(self, metric_key):
        '''Gets a specific formatted metric value.'''
        return self.metrics.get(metric_key, "--")

# Create separate classes for different concerns:

class RateLimiter:
    '''Handles rate limiting for API requests.'''
    
    def __init__(self, min_interval_seconds=3):
        self.min_interval = min_interval_seconds
        self.last_request_time = None
    
    def can_make_request(self):
        '''Returns True if enough time has passed since the last request.'''
        if not self.last_request_time:
            return True
        return (datetime.now() - self.last_request_time).total_seconds() > self.min_interval
    
    def record_request(self):
        '''Records that a request was made at this time.'''
        self.last_request_time = datetime.now()
    
    def get_wait_time(self):
        '''Returns seconds to wait before next request, or 0 if ready.'''
        if not self.last_request_time:
            return 0
        elapsed = (datetime.now() - self.last_request_time).total_seconds()
        return max(0, self.min_interval - elapsed)


class WeatherDashboardGUIState:
    '''Internal helper class to organize GUI variables better while preserving existing interface.'''
    
    def __init__(self, gui_vars_dict):
        self._vars = gui_vars_dict
    
    def get_current_city(self):
        return self._vars['city'].get()
    
    def get_current_unit_system(self):
        return self._vars['unit'].get()
    
    def get_current_range(self):
        return self._vars['range'].get()
    
    def get_current_chart_metric(self):
        return self._vars['chart'].get()
    
    def is_metric_visible(self, metric_key):
        return self._vars['visibility'].get(metric_key, tk.BooleanVar()).get()
    
    def get_visible_metrics(self):
        return [key for key, var in self._vars['visibility'].items() if var.get()]
    
    def reset_to_defaults(self):
        self._vars['city'].set(config.DEFAULTS["city"])
        self._vars['unit'].set(config.DEFAULTS["unit"])
        self._vars['range'].set(config.DEFAULTS["range"])
        self._vars['chart'].set(config.DEFAULTS["chart"])
        
        for key, var in self._vars['visibility'].items():
            var.set(config.DEFAULTS["visibility"].get(key, False))
            

class WeatherDisplayUpdater:
    '''Handles updating the GUI display with weather data.'''
    
    def __init__(self, gui_vars, metric_labels):
        self.vars = gui_vars
        self.labels = metric_labels
        # Optional internal helper
        self._state_helper = WeatherDashboardGUIState(gui_vars)
    
    def update_display(self, view_model):
        '''Updates the display with weather data from ViewModel.'''
        self._render_metric_labels(view_model)
        self._update_metadata_labels(view_model)
        self._update_status_label(view_model.status)
    
    def _render_metric_labels(self, view_model):
        '''Renders the metric labels based on visibility settings.'''
        row_counter = 0
        for metric_key in config.KEY_TO_DISPLAY:
            if metric_key not in self.labels:
                continue
            widgets = self.labels[metric_key]
            is_visible = self._state_helper.is_metric_visible(metric_key)

            widgets['label'].grid_forget()
            widgets['value'].grid_forget()

            if is_visible:
                widgets['label'].grid(row=row_counter, column=2, sticky=tk.W, pady=5)
                widgets['value'].grid(row=row_counter, column=3, sticky=tk.W, pady=5)
                widgets['value'].config(text=view_model.get_metric_value(metric_key))
                row_counter += 1

    def _update_metadata_labels(self, view_model):
        '''Updates the city and date labels in the display.'''
        self.vars['city_label'].config(text=view_model.city_name)
        self.vars['date_label'].config(text=view_model.date_str)

    def _update_status_label(self, status_text):
        '''Updates the status label to indicate if fallback data was used.'''
        label = self.vars.get('status_label')
        if label:
            label.config(text=status_text)


class WeatherErrorHandler:
    '''Handles error presentation and user messaging for weather data operations.'''
    
    @staticmethod
    def handle_weather_error(error_exception, city_name):
        '''Handles weather-related errors and shows appropriate user messages.
        
        Returns:
            bool: True if the error was handled and operation should continue,
                  False if the operation should be aborted.
        '''
        if not error_exception:
            return True
            
        if isinstance(error_exception, ValidationError):
            # Critical errors - don't show fallback data
            messagebox.showerror("Input Error", str(error_exception))
            return False
        elif isinstance(error_exception, CityNotFoundError):
            # City not found - show error but continue with fallback
            messagebox.showerror("City Not Found", str(error_exception))
            return True
        elif isinstance(error_exception, RateLimitError):
            # Rate limit - show specific message
            messagebox.showerror("Rate Limit", f"API rate limit exceeded. Using simulated data for '{city_name}'.")
            return True
        elif isinstance(error_exception, NetworkError):
            # Network issues - show network-specific message
            messagebox.showwarning("Network Issue", f"Network problem detected. Using simulated data for '{city_name}'.")
            return True
        else:
            # Other API errors - show general fallback notice
            Logger.warn(f"Using fallback for {city_name}: {error_exception}")
            messagebox.showinfo("Notice", f"No live data available for '{city_name}'. Simulated data is shown.")
            return True

    @staticmethod
    def handle_input_validation_error(error):
        '''Handles input validation errors.'''
        Logger.error(f"Input validation error: {error}")
        messagebox.showerror("Input Error", str(error))

    @staticmethod
    def handle_unexpected_error(error):
        '''Handles unexpected errors.'''
        Logger.error(f"Unexpected error: {error}")
        messagebox.showerror("Error", f"Unexpected error: {error}")


class WeatherDashboardCoordinator:
    '''Coordinates weather data operations without mixing concerns.
    
    This class replaces WeatherDashboardLogic with a cleaner separation of responsibilities.
    '''
    
    def __init__(self, gui_vars, metric_labels, data_controller, widgets):
        self.controller = data_controller
        self.widgets = widgets
        self.vars = gui_vars
        # Optional internal helper
        self._state_helper = WeatherDashboardGUIState(gui_vars)
        
        # Initialize helper classes
        self.rate_limiter = RateLimiter()
        self.display_updater = WeatherDisplayUpdater(gui_vars, metric_labels)
        self.error_handler = WeatherErrorHandler()
    
    def update_weather_display(self, city_name, unit_system):
        '''Coordinates fetching and displaying weather data.'''
        # Input validation
        if not isinstance(city_name, str):
            self.error_handler.handle_input_validation_error("City name must be text")
            return False
        
        try:
            validate_unit_system(unit_system)
        except ValueError as e:
            self.error_handler.handle_input_validation_error(str(e))
            return False
        
        # Rate limiting
        if not self.rate_limiter.can_make_request():
            wait_time = self.rate_limiter.get_wait_time()
            Logger.warn("Fetch blocked due to rate limiting.")
            messagebox.showinfo("Rate Limit", f"Please wait {wait_time:.0f} more seconds before making another request.")
            return False

        self.rate_limiter.record_request()

        try:
            # Fetch data
            city, raw_data, error_exception = self.controller.get_city_data(city_name, unit_system)
            
            # Create view model
            view_model = WeatherViewModel(city, raw_data, unit_system)
            
            # Handle any errors
            should_continue = self.error_handler.handle_weather_error(error_exception, view_model.city_name)
            if not should_continue:
                return False
            
            # Update display
            self.display_updater.update_display(view_model)
            
            # Log the data
            self.controller.write_to_log(city, raw_data, unit_system)
            return True

        except ValidationError as e:
            self.error_handler.handle_input_validation_error(str(e))
            return False
        except Exception as e:
            self.error_handler.handle_unexpected_error(str(e))
            return False

    def update_chart(self):
        '''Updates the chart with historical weather data for the selected city and metric.'''
        try:
            city, days, metric_key, unit = self._get_chart_settings()
            x_vals, y_vals = self._build_chart_series(city, days, metric_key, unit)
            self._render_chart(x_vals, y_vals, metric_key, city, unit)

        except KeyError as e:
            messagebox.showerror("Chart Error", str(e))
            Logger.warn(f"Chart error: {e}")
        except ValueError as e:
            messagebox.showerror("Chart Data Error", str(e))
            Logger.warn(f"Chart data error: {e}")
        except Exception as e:
            messagebox.showerror("Chart Error", f"Unexpected error: {e}")
            Logger.error(f"Unexpected chart error: {e}")

    def _get_chart_settings(self):
        '''Retrieves the current settings for chart display: city, date range, metric key, and unit.'''
        raw_city = self._state_helper.get_current_city()
        if not raw_city or not raw_city.strip():
            raise ValueError("City name is required for chart display")
        
        city = normalize_city_name(raw_city)
        days = config.CHART["range_options"].get(self._state_helper.get_current_range(), 7)
        
        if days <= 0:
            raise ValueError(f"Invalid date range: {days} days")
        
        metric_key = self._get_chart_metric_key()
        unit = self._state_helper.get_current_unit_system()
        
        validate_unit_system(unit)  # Ensure unit system is valid
        
        return city, days, metric_key, unit
    
    def _build_chart_series(self, city, days, metric_key, unit):
        '''Builds the x and y axis values for the chart based on historical data.'''
        data = self.controller.get_historical_data(city, days, unit)

        if not data:
            raise ValueError(f"No historical data available for {city}.")

        if not all(metric_key in d for d in data):
            print(f"Warning: Some data entries are missing '{metric_key}'")

        x_vals = [d['date'].strftime("%Y-%m-%d") for d in data]  # Dynamic axis values
        y_vals = [d[metric_key] for d in data if metric_key in d]
        return x_vals, y_vals
    
    def _render_chart(self, x_vals, y_vals, metric_key, city, unit):
        '''Renders the chart with the provided x and y values for the specified metric and city.'''
        self.widgets.update_chart_display(x_vals, y_vals, metric_key, city, unit, fallback=True)

    def _get_chart_metric_key(self):
        '''Determines the metric key for the chart based on user selection.'''
        display_name = self._state_helper.get_current_chart_metric()
        
        # Handle special case when no metrics are selected
        if display_name == "No metrics selected":
            raise ValueError("Please select at least one metric to display in the chart.")
        
        metric_key = config.DISPLAY_TO_KEY.get(display_name)
        if not metric_key:
            raise KeyError(f"Invalid chart metric: '{display_name}'. Please select a valid metric.")
        return metric_key
    

class WeatherDashboardMain:
    '''Main application class for the Weather Dashboard.'''
    def __init__(self, root):
        self.root = root
        self.gui_vars = self.init_vars()
        self.frames = WeatherDashboardGUIFrames(root)
        self.data_manager = WeatherDataManager()
        
        # Optional internal helper (doesn't change external interface)
        self._state_helper = WeatherDashboardGUIState(self.gui_vars)

        self.ui_renderer = WeatherDashboardWidgets(
            frames=self.frames.frames,
            gui_vars=self.gui_vars,
            update_cb=self.on_update_clicked,
            clear_cb=self.on_clear_clicked,
            dropdown_cb=self.update_chart_dropdown
        )

        # Direct attribute access instead of property methods
        self.gui_vars['metric_labels'] = self.ui_renderer.metric_labels
        self.gui_vars['city_label'] = self.ui_renderer.city_label
        self.gui_vars['date_label'] = self.ui_renderer.date_label
        self.gui_vars['status_label'] = self.ui_renderer.status_label

        self.controller = WeatherDataController(self.data_manager)

        self.coordinator = WeatherDashboardCoordinator(
            self.gui_vars,
            metric_labels=self.ui_renderer.metric_labels,
            data_controller=self.controller,
            widgets=self.ui_renderer
        )

        self.update_chart_dropdown()

    def init_vars(self):
        '''Initializes the GUI variables with default values from config.'''
        return {
            'city': tk.StringVar(value=config.DEFAULTS["city"]),
            'unit': tk.StringVar(value=config.DEFAULTS["unit"]),
            'range': tk.StringVar(value=config.DEFAULTS["range"]),
            'chart': tk.StringVar(value=config.DEFAULTS["chart"]),
            'visibility': {
                key: tk.BooleanVar(value=val)
                for key, val in config.DEFAULTS["visibility"].items()
            }
        }

    def load_initial_display(self):
        '''Fetches and displays the initial city's weather data on startup.'''
        success = self.coordinator.update_weather_display(
            self.gui_vars['city'].get(),
            self.gui_vars['unit'].get()
        )
        
        # Also update the chart on initial load
        if success:
            self.coordinator.update_chart()

    def on_update_clicked(self):
        '''Handles the update button click event to fetch and display weather data.'''
        success = self.coordinator.update_weather_display(
            self.gui_vars['city'].get(),
            self.gui_vars['unit'].get()
        )

        if success:
            self.coordinator.update_chart()

    def on_clear_clicked(self):
        '''Handles the reset button click event to reset input controls to default values (but does not clear display output).'''
        self._state_helper.reset_to_defaults()
        messagebox.showinfo("Reset", "Dashboard reset to default values.")  # Pop-up confirmation
        self.update_chart_dropdown()

        # Also update the display to show the default city's data
        success = self.coordinator.update_weather_display(
            self.gui_vars['city'].get(),
            self.gui_vars['unit'].get()
        )
        
        if success:
            self.coordinator.update_chart()

    def update_chart_dropdown(self):
        '''Updates the chart dropdown based on the current visibility settings.'''
        chart_widget = self.gui_vars.get('chart_widget')
        if not chart_widget:
            return
        
        # Get display versions of visible metrics for chart dropdown
        visible = [
            config.KEY_TO_DISPLAY[k]
            for k in self._state_helper.get_visible_metrics()
        ]
        
        # Handle case where no metrics are visible
        if not visible:
            chart_widget['values'] = ["No metrics selected"]
            self.gui_vars['chart'].set("No metrics selected")
            chart_widget.configure(state="disabled")
        else:
            chart_widget['values'] = visible
            self.gui_vars['chart'].set(visible[0])
            chart_widget.configure(state="readonly")


if __name__ == "__main__":
    '''Main entry point for the Weather Dashboard application.'''
    root = tk.Tk()
    root.title("Weather Dashboard")
    app = WeatherDashboardMain(root)
    app.load_initial_display()
    root.mainloop()