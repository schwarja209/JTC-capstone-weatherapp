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
import random
import requests
import os
import json

import config
# Ensure required directories exist at app startup
for folder in {config.OUTPUT["data_dir"], config.OUTPUT["log_dir"]}:
    os.makedirs(folder, exist_ok=True)

class Logger:
    '''Centralized logger with timestamp, level, optional file + JSON output.'''

    LOG_FOLDER = config.OUTPUT.get("log_dir", "data")  # default fallback
    PLAIN_LOG = os.path.join(LOG_FOLDER, "weather.log")
    JSON_LOG = os.path.join(LOG_FOLDER, "weather.jsonl")

    @staticmethod
    def _timestamp():
        '''Returns current timestamp in YYYY-MM-DD HH:MM:SS format.'''
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def info(msg): Logger._log("INFO", msg)
    @staticmethod
    def warn(msg): Logger._log("WARN", msg)
    @staticmethod
    def error(msg): Logger._log("ERROR", msg)


    @staticmethod
    def _log(level, msg):
        '''Logs a message with the specified level, timestamp, and writes to files.'''
        ts = Logger._timestamp()
        formatted = f"[{level}] {ts} {msg}"
        print(formatted)
        Logger._write_to_files(level, ts, msg)

    @staticmethod
    def _write_to_files(level, ts, msg):
        '''Writes log entry to both plain text and JSON files.'''
        with open(Logger.PLAIN_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{level}] {ts} {msg}\n")

        log_entry = {
            "timestamp": ts,
            "level": level,
            "message": msg
        }
        with open(Logger.JSON_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")


class SampleWeatherGenerator:
    '''Generates simulated metric weather data.'''
    def __init__(self):
        ''' Initializes the generator with default units. '''
        self.source_unit = "metric"
    
    def generate(self, city, num_days=7):
        '''Generates simulated weather data for a given city over a specified number of days.'''
        data = []
        base_temp = random.randint(5, 30)               # Celsius
        for i in range(num_days):
            date = datetime.now() - timedelta(days=num_days - 1 - i)
            data.append({
                'date': date,
                'temperature': base_temp + random.randint(-15, 15),
                'humidity': random.randint(30, 90),     # %
                # TODO: 'precipitation': random.uniform(0, 2),  # All precipitation values and handling is on hold for now
                'conditions': random.choice(['Sunny', 'Cloudy', 'Rainy', 'Snowy']),
                'wind_speed': random.randint(0, 10),    # m/s
                'pressure': random.uniform(990, 1035)   # hPa
            })
        return data

class UnitConverter:
    '''Utility class for converting between explicit weather units.'''

    TEMP_UNITS = ("C", "F")
    PRESSURE_UNITS = ("hPa", "inHg")
    WIND_UNITS = ("m/s", "mph")

    @staticmethod
    def convert_temperature(value, from_unit, to_unit):
        '''Converts temperature between Celsius and Fahrenheit.'''
        C, F = UnitConverter.TEMP_UNITS
        if from_unit == to_unit:
            return value
        if from_unit == F and to_unit == C:
            return (value - 32) * 5 / 9
        if from_unit == C and to_unit == F:
            return (value * 9 / 5) + 32
        raise ValueError(f"Unsupported temperature conversion: {from_unit} to {to_unit}")

    @staticmethod
    def convert_pressure(value, from_unit, to_unit):
        '''Converts pressure between hPa and inHg.'''
        HPA, INHG = UnitConverter.PRESSURE_UNITS
        if from_unit == to_unit:
            return value
        if from_unit == HPA and to_unit == INHG:
            return value * 0.02953
        if from_unit == INHG and to_unit == HPA:
            return value / 0.02953
        raise ValueError(f"Unsupported pressure conversion: {from_unit} to {to_unit}")

    @staticmethod
    def convert_wind_speed(value, from_unit, to_unit):
        '''Converts wind speed between m/s and mph.'''
        if from_unit == to_unit:
            return value
        if from_unit == "m/s" and to_unit == "mph":
            return value * 2.23694
        if from_unit == "mph" and to_unit == "m/s":
            return value / 2.23694
        raise ValueError(f"Unsupported wind speed conversion: {from_unit} to {to_unit}")
    
    @staticmethod
    def get_unit_label(metric, unit_system):
        '''Returns the unit label for a given metric based on the unit system (imperial or metric).'''
        return config.UNITS["metric_units"].get(metric, {}).get(unit_system, "")

    @staticmethod
    def format_value(metric, val, unit_system):
        '''Formats the metric value for display based on the unit system and metric type.'''
        if val is None:
            return "--"
        
        unit = UnitConverter.get_unit_label(metric, unit_system)
            
        if metric == "temperature":
            return f"{val:.1f} {unit}"
        elif metric == "humidity":
            return f"{val} {unit}"
        elif metric in ["pressure", "wind_speed"]:
            return f"{val:.2f} {unit}"
        return f"{val} {unit}" if unit else str(val)

def display_fallback_status(fallback_used):
    '''Returns fallback status label for display based on boolean.'''
    return "(Simulated)" if fallback_used else ""

def describe_fallback_status(fallback_used):
    '''Returns descriptive fallback status for logging based on boolean.'''
    return "(Simulated)" if fallback_used else "Live"

def is_fallback(data):
    '''Returns True if the data was generated as a fallback.'''
    return data.get('source') == 'simulated'

def normalize_city_name(name):
    '''Strips whitespace and capitalizes each word of the city name.'''
    return name.strip().title()

def city_key(name):
    '''Generates a normalized key for city name to ensure consistent API calls and logging.'''
    return normalize_city_name(name).lower().replace(" ", "_")
    

class WeatherAPIService:
    '''Handles fetching current weather data from OpenWeatherMap API with fallback to simulated data.'''
    def __init__(self):
        self.api = config.API_BASE_URL
        self.key = config.API_KEY
        self.fallback = SampleWeatherGenerator()

    def fetch_current(self, city):
        '''Fetches current weather data for a given city using OpenWeatherMap API.'''
        try:
            self._validate_city(city)
            data = self._get_api_data(city)
            parsed = self._parse_weather_data(data)
            parsed['source'] = 'live'
            self._validate_weather_data(parsed)
            self._status_weather_data(parsed)

            return parsed, ""

        # Enumerate specific exceptions for clearer error handling
        except requests.exceptions.RequestException as e:
            data, used, msg = self.use_fallback(city, "Network/API issue", e)
            return data, used, msg
        except (KeyError, TypeError, ValueError, LookupError, EnvironmentError, RuntimeError) as e:
            data, used, msg = self.use_fallback(city, type(e).__name__, e)
            return data, used, msg
        except Exception as e:
            data, used, msg = self.use_fallback(city, "General error", e)
            return data, used, msg

    def _validate_city(self, city):
        '''Validates the city input for non-empty and API key presence.'''
        if not city.strip():
            raise ValueError("City is empty") # No city error handling
        if not self.key:
            raise EnvironmentError("Missing API key") # No API key error handling

    def _get_api_data(self, city):
        '''Fetches raw weather data from OpenWeatherMap API for the specified city.'''
        city = normalize_city_name(city)  # Normalize city name for consistency
        url = f"{self.api}?q={city}&appid={self.key}&units=metric" # hardcoded always in metric, for consistency
        response = requests.get(url)

        if response.status_code == 429:
            raise RuntimeError("Rate limit exceeded (Too Many Requests)") # Rate limit error handling
        
        data = response.json()

        if str(data.get("cod")) != "200":
            raise LookupError(f"City '{city_key(city)}' not found") # City not found error handling
        return data

    def _parse_weather_data(self, data):
        '''Parses the raw weather data from the API response into a structured format.'''
        # TODO:
        # rain = data.get("rain", {})
        # snow = data.get("snow", {})
        # precip_mm = rain.get("1h", 0) + snow.get("1h", 0)

        return {
            'temperature': data.get("main", {}).get("temp"),
            'humidity': data.get("main", {}).get("humidity"),
            # TODO: 'precipitation': precip_mm,
            'pressure': data.get("main", {}).get("pressure"),
            'wind_speed': data.get("wind", {}).get("speed"),
            'conditions': data.get("weather", [{}])[0].get("description", "--").title(),
            'date': datetime.now()
        }

    def _validate_weather_data(self, d):
        '''Performs basic sanity checks on the parsed weather data.'''
        if not all(isinstance(val, (int, float)) for val in [d['temperature'], d['humidity'], d['wind_speed'], d['pressure']]):
            raise ValueError("One or more values in the API response are not numeric")
        if not (0 <= d['humidity'] <= 100):
            raise ValueError("Humidity outside of expected range")
        if not (-100 <= d['temperature'] <= 70):
            raise ValueError("Temperature outside of expected range")
        if not (900 <= d['pressure'] <= 1100):
            raise ValueError("Pressure outside of expected range")

    def _status_weather_data(self, d):
        '''Prints status message for fetched weather data.'''
        Logger.info("Fetched current weather for city")
        return d
    
    def use_fallback(self, city, msg, exc):
        '''Uses simulated data generator when API call fails.'''
        error_msg = f"{msg}: {exc}"
        Logger.error(f"{msg}: {exc} - Using fallback data for {city_key(city)}")

        fallback_data = self.fallback.generate(city)
        fallback_data[-1]['source'] = 'simulated'
        return fallback_data[-1], error_msg

class WeatherDataManager:
    '''Manages weather data fetching and storage, including fallback handling.'''
    def __init__(self):
        self.api_service = WeatherAPIService()
        self.weather_data = {}

    def fetch_current(self, city, unit_system):
        '''Fetches current weather data for a city, using fallback if API call fails.'''
        raw_data, error_msg = self.api_service.fetch_current(city)

        # All API and fallback data is assumed to be in metric units and converted downstream.
        # If this changes in future (e.g., new fallback with imperial), update convert_units().
        converted_data = self.convert_units(raw_data, unit_system)

        key = city_key(city)
        existing_data = self.weather_data.setdefault(key, []) # Store the latest data for the city with a timestamp, for use in history tracking later
        if not existing_data or existing_data[-1].get("date") != converted_data.get("date"):
            existing_data.append(converted_data)
        return converted_data, error_msg
    
    def convert_units(self, data, unit_system):
        '''Converts weather data units based on the selected UI unit system (metric or imperial).'''
        converted = data.copy()
        if 'temperature' in data:
            converted['temperature'] = UnitConverter.convert_temperature(data['temperature'], "C", "F" if unit_system == "imperial" else "C")
        if 'pressure' in data:
            converted['pressure'] = UnitConverter.convert_pressure(data['pressure'], "hPa", "inHg" if unit_system == "imperial" else "hPa")
        if 'wind_speed' in data:
            converted['wind_speed'] = UnitConverter.convert_wind_speed(data['wind_speed'], "m/s", "mph" if unit_system == "imperial" else "m/s")
        return converted

    def get_historical(self, city, num_days):
        '''Fetches historical weather data for a city. Currently always defaults to fallback.'''
        return self.api_service.fallback.generate(normalize_city_name(city), num_days)

    def get_recent_data(self, city, days):
        '''Returns recent weather data for a city, filtered by specified dates. Not currently used, but may support trend-based features like Tomorrow's Guess.'''
        return [entry for entry in self.weather_data.get(city_key(city), []) if entry['date'].date() in days]

    def write_to_file(self, city, data, unit_system):
        '''Writes formatted weather data to a log file with timestamp and unit system information.'''
        log_entry = self.format_data_for_logging(city, data, unit_system)
        with open(config.OUTPUT["log"], "a", encoding="utf-8") as f:
            f.write(log_entry)

        status = describe_fallback_status(is_fallback(data))
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

        self._metric_labels = {}
        self._chart_canvas = None
        self._chart_fig = None
        self._chart_ax = None

        self.create_title_widgets()
        self.create_control_widgets()
        self.create_metric_widgets()
        self.create_chart_widgets()
        self.bind_entry_events()

    def create_title_widgets(self):
        '''Creates the title label for the dashboard.'''
        label = ttk.Label(self.frames["title"], text="Weather Dashboard", style="Title.TLabel")
        label.pack()

    def create_control_widgets(self):
        '''Creates the control widgets for user input and actions.'''
        control = self.frames["control"]

        ttk.Label(control, text="City:", style="LabelName.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5) # City label and entry
        self.city_entry = ttk.Entry(control, textvariable=self.gui_vars['city'])
        self.city_entry.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(control, text="Units:", style="LabelName.TLabel").grid(row=2, column=0, sticky=tk.W, pady=5) # Unit selection radio buttons
        ttk.Radiobutton(control, text="Imperial (°F, mph, inHg)", variable=self.gui_vars['unit'], value="imperial").grid(row=2, column=1, sticky=tk.W)
        ttk.Radiobutton(control, text="Metric (°C, m/s, hPa)", variable=self.gui_vars['unit'], value="metric").grid(row=3, column=1, sticky=tk.W)

        ttk.Label(control, text="Show Metrics:", style="LabelName.TLabel").grid(row=4, column=0, sticky=tk.W, pady=5) # Metric visibility checkboxes
        for i, (metric_key, var) in enumerate(self.gui_vars['visibility'].items()):
            label = config.KEY_TO_DISPLAY.get(metric_key, metric_key.title())
            checkbox = ttk.Checkbutton(control, text=label, variable=var, command=self.dropdown_cb)
            checkbox.grid(row=5 + i // 2, column=i % 2, sticky=tk.W)

        ttk.Label(control, text="Chart Metric:", style="LabelName.TLabel").grid(row=4, column=2, sticky=tk.E, pady=5) # Chart metric selector
        chart_cb = ttk.Combobox(control, textvariable=self.gui_vars['chart'], state="readonly")
        chart_cb.grid(row=5, column=2, sticky=tk.E)
        self.gui_vars['chart_widget'] = chart_cb

        ttk.Label(control, text="Date Range:", style="LabelName.TLabel").grid(row=6, column=2, sticky=tk.E, pady=5) # Date range selector
        range_cb = ttk.Combobox(control, textvariable=self.gui_vars['range'], state="readonly")
        range_cb['values'] = list(config.CHART["range_options"].keys())
        range_cb.current(0)
        range_cb.grid(row=7, column=2, sticky=tk.E)

        # Control buttons for updating and resetting display
        ttk.Button(control, text="Update Weather", command=self.update_cb, style="MainButton.TButton").grid(row=1, column=2, pady=10, sticky=tk.E)
        ttk.Button(control, text="Reset", command=self.clear_cb, style="MainButton.TButton").grid(row=2, column=2, pady=5, sticky=tk.E)
        
        # Configure grid weights so things aren't cramped
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
            self._metric_labels[metric_key] = {"label": name, "value": value}

        self.status_label = ttk.Label(metric, text="", foreground="red", style="LabelValue.TLabel") # Status label for API fallback or errors
        self.status_label.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=5)

    def create_chart_widgets(self):
        '''Creates the chart display for historical weather trends.'''
        fig = Figure(figsize=(8, 3), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=self.frames["chart"])

        self._chart_fig = fig
        self._chart_ax = ax
        self._chart_canvas = canvas

        ax.set_title("")
        ax.set_xlabel("")
        ax.set_ylabel("")

        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_chart_display(self, x_vals, y_vals, metric_key, city, unit_system, fallback=False):
        '''Updates the chart display with new data for the specified metric and city.'''
        ax = self._chart_ax
        ax.clear()
        ax.plot(x_vals, y_vals, marker="o")

        label = config.KEY_TO_DISPLAY.get(metric_key, metric_key.title())
        unit = UnitConverter.get_unit_label(metric_key, unit_system)

        ax.set_title(f"{label} {display_fallback_status(fallback)} in {city_key(city)}")
        ax.set_xlabel("Date")
        ax.set_ylabel(f"{label} ({unit})")

        self._chart_fig.autofmt_xdate(rotation=45)
        self._chart_fig.tight_layout()
        self._chart_canvas.draw()
    
    def bind_entry_events(self):
        '''Binds events for immediate updates'''
        self.city_entry.bind("<Return>", lambda e: self.update_cb()) # Pressing Enter in city entry triggers update

    @property
    def city_label_widget(self):
        '''Returns the city label widget for current weather data.'''
        return self.city_label

    @property
    def date_label_widget(self):
        '''Returns the date label widget for current weather data.'''
        return self.date_label

    @property
    def status_label_widget(self):
        '''Returns the error status label widget for current weather data.'''
        return self.status_label

    @property
    def metric_labels(self):
        '''Returns the dictionary of metric labels for current weather data.'''
        return self._metric_labels

    @property
    def chart_canvas(self):
        '''Returns the canvas for the chart display.'''
        return self._chart_canvas

    @property
    def chart_fig(self):
        '''Returns the figure for the chart display.'''
        return self._chart_fig

    @property
    def chart_ax(self):
        '''Returns the axes for the chart display.'''
        return self._chart_ax


class WeatherDataController:
    '''Handles fetching and returning weather data without interacting with GUI.'''
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def get_city_data(self, city_name, unit_system):
        '''Fetches weather data for a city. Handles fallback. Returns (city, data, fallback_flag).'''
        city = normalize_city_name(city_name)
        data, error_msg = self.data_manager.fetch_current(city, unit_system)
        return city, data, error_msg

    def get_historical_data(self, city_name, num_days, unit_system):
        '''Fetches historical data and applies unit conversion.'''
        city = normalize_city_name(city_name)
        raw = self.data_manager.get_historical(city, num_days)

        source_unit = "metric"  # Same as generator’s output
        if unit_system == source_unit:
            return raw
        return [self.data_manager.convert_units(d, unit_system) for d in raw]

    def write_to_log(self, city, data, unit, fallback_used):
        '''Writes weather data to log file with timestamp and unit system information.'''
        self.data_manager.write_to_file(city, data, unit)


class WeatherViewModel:
    '''Prepares sanitized, display-ready data from raw weather data.'''

    def __init__(self, city, data, unit):
        self.city_name = city_key(city)
        self.date_str = data['date'].strftime("%Y-%m-%d") if 'date' in data else "--"
        self.status = " (Simulated)" if is_fallback(data) else ""
        self.unit = unit

        self.metrics = {}
        for key in KEY_TO_DISPLAY:
            raw_value = data.get(key, "--")
            display_val = UnitConverter.format_value(key, raw_value, unit)
            self.metrics[key] = display_val
            

class WeatherDashboardLogic:
    '''Handles the rendering logic for the dashboard.'''
    def __init__(self, gui_vars, metric_labels, data_controller):
        self.vars = gui_vars
        self.labels = metric_labels
        self.controller = data_controller
        self.widgets = None

    def fetch_city(self, city_name, unit_system):
        '''Fetches weather data and updates display using the ViewModel.'''      
        try:
            city, raw_data, error_msg = self.controller.get_city_data(city_name, unit_system)
            vm = WeatherViewModel(city, raw_data, unit_system)

            if vm.status:
                Logger.warn(f"Using fallback for {vm.city_name}: {error_msg}")
                messagebox.showerror("Notice", f"No live data for '{vm.city_name}'. Simulated data is shown.")

            self.update_display(vm)

            self.controller.write_to_log(city, raw_data, unit_system, is_fallback(raw_data))

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            Logger.warn(f"Input error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")
            Logger.error(f"Unexpected error: {e}")

    def update_display(self, vm: WeatherViewModel):
        '''Updates the display with current weather data.'''
        self._render_metric_labels(vm)
        self._update_metadata_labels(vm)
        self._update_status_label(vm.status)

    def _render_metric_labels(self, vm):
        '''Renders the metric labels based on visibility settings and updates their values.'''
        row_counter = 0  # Fresh stacking for metric labels in column 2/3 only
        for metric_key in config.KEY_TO_DISPLAY:
            if metric_key not in self.labels: # skip metrics not set as visible
                continue
            widgets = self.labels[metric_key]
            is_visible = self.vars['visibility'].get(metric_key, tk.BooleanVar()).get()

            # Always remove whole grid before potentially re-adding
            widgets['label'].grid_forget()
            widgets['value'].grid_forget()

            if is_visible:
                widgets['label'].grid(row=row_counter, column=2, sticky=tk.W, pady=5)
                widgets['value'].grid(row=row_counter, column=3, sticky=tk.W, pady=5)
                widgets['value'].config(text=vm.metrics.get(metric_key, "--"))
                row_counter += 1 # Only increment when visible

    def _update_metadata_labels(self, vm):
        '''Updates the city and date labels in the display.'''
        self.vars['city_label'].config(text=vm.city_name)
        self.vars['date_label'].config(text=vm.date_str)

    def _update_status_label(self, status_text):
        '''Updates the status label to indicate if fallback data was used.'''
        label = self.vars.get('status_label')
        if label:
            label.config(text=status_text)

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
        raw_city = self.vars["city"].get()
        city = normalize_city_name(raw_city)
        days = config.CHART["range_options"].get(self.vars['range'].get(), 7)
        metric_key = self._get_chart_metric_key()
        unit = self.vars['unit'].get()
        return city, days, metric_key, unit
    
    def _build_chart_series(self, city, days, metric_key, unit):
        '''Builds the x and y axis values for the chart based on historical data.'''
        data = self.controller.get_historical_data(city, days, unit)

        if not data:
            raise ValueError(f"No historical data available for {city_key(city)}.")

        if not all(metric_key in d for d in data):
            print(f"Warning: Some data entries are missing '{metric_key}'")

        x_vals = [d['date'].strftime("%Y-%m-%d") for d in data] # Dynamic axis values
        y_vals = [d[metric_key] for d in data if metric_key in d]
        return x_vals, y_vals
    
    def _render_chart(self, x_vals, y_vals, metric_key, city, unit):
        '''Renders the chart with the provided x and y values for the specified metric and city.'''
        self.widgets.update_chart_display(x_vals, y_vals, metric_key, city, unit, fallback=False)

    def _get_chart_metric_key(self):
        '''Determines the metric key for the chart based on user selection.'''
        display_name = self.vars['chart'].get()
        metric_key = config.DISPLAY_TO_KEY.get(display_name)
        if not metric_key:
            raise KeyError("No valid chart metric available.")
        return metric_key
    

class WeatherDashboardMain:
    '''Main application class for the Weather Dashboard.'''
    def __init__(self, root):
        self.root = root
        self.gui_vars = self.init_vars()
        self.frames = WeatherDashboardGUIFrames(root)
        self.data_manager = WeatherDataManager()

        self.ui_renderer = WeatherDashboardWidgets(
            frames=self.frames.frames,
            gui_vars=self.gui_vars,
            update_cb=self.on_update_clicked,
            clear_cb=self.on_clear_clicked,
            dropdown_cb=self.update_chart_dropdown
        )

        self.gui_vars['metric_labels'] = self.ui_renderer.metric_labels
        self.gui_vars['city_label'] = self.ui_renderer.city_label_widget
        self.gui_vars['date_label'] = self.ui_renderer.date_label_widget
        self.gui_vars['status_label'] = self.ui_renderer.status_label_widget

        self.controller = WeatherDataController(self.data_manager)

        self.logic = WeatherDashboardLogic(
            self.gui_vars,
            metric_labels=self.ui_renderer.metric_labels,
            data_controller=self.controller
        )

        self.logic.widgets = self.ui_renderer
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
        '''Fetches and displays the initial city’s weather data on startup.'''
        self.logic.fetch_city(
            self.gui_vars['city'].get(),
            self.gui_vars['unit'].get()
        )

    def on_update_clicked(self):
        '''Handles the update button click event to fetch and display weather data.'''
        self.logic.fetch_city(
            self.gui_vars['city'].get(),
            self.gui_vars['unit'].get()
        )
        self.logic.update_chart()

    def on_clear_clicked(self):
        '''Handles the reset button click event to reset input controls to default values (but does not clear display output).'''
        self.gui_vars['city'].set(config.DEFAULTS["city"])
        self.gui_vars['unit'].set(config.DEFAULTS["unit"])
        self.gui_vars['range'].set(config.DEFAULTS["range"])
        self.gui_vars['chart'].set(config.DEFAULTS["chart"])

        for key, var in self.gui_vars['visibility'].items():
            var.set(config.DEFAULTS["visibility"].get(key, False))

        messagebox.showinfo("Reset", "Dashboard reset to default values.") # Pop-up confirmation
        self.update_chart_dropdown()

    def update_chart_dropdown(self):
        '''Updates the chart dropdown based on the current visibility settings.'''
        chart_widget = self.gui_vars.get('chart_widget')
        if not chart_widget:
            return
        visible = [ # Get display versions of visible metrics for chart dropdown
            config.KEY_TO_DISPLAY[k]
            for k, v in self.gui_vars['visibility'].items() if v.get()
        ]
        chart_widget['values'] = visible
        self.gui_vars['chart'].set(visible[0] if visible else "")

if __name__ == "__main__":
    '''Main entry point for the Weather Dashboard application.'''
    root = tk.Tk()
    root.title("Weather Dashboard")
    app = WeatherDashboardMain(root)
    app.load_initial_display()
    root.mainloop()