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

import config

class SampleWeatherGenerator:
    '''Generates simulated metric weather data for a given city over a specified number of days.'''
    def generate(self, city, num_days=7):
        data = []
        base_temp = random.randint(5, 30)
        for i in range(num_days):
            date = datetime.now() - timedelta(days=num_days - 1 - i)
            data.append({
                'date': date,
                'temperature': base_temp + random.randint(-15, 15),
                'humidity': random.randint(30, 90),
                # 'precipitation': random.uniform(0, 2),  # All precipitation values and handling is on hold for now
                'conditions': random.choice(['Sunny', 'Cloudy', 'Rainy', 'Snowy']),
                'wind_speed': random.randint(0, 10),
                'pressure': random.uniform(990, 1035)
            })
        return data

class UnitConverter:
    '''Utility class for converting between explicit weather units.'''

    @staticmethod
    def convert_temperature(value, from_unit, to_unit):
        '''Converts temperature between Celsius and Fahrenheit.'''
        if from_unit == to_unit:
            return value
        if from_unit == "F" and to_unit == "C":
            return (value - 32) * 5 / 9
        if from_unit == "C" and to_unit == "F":
            return (value * 9 / 5) + 32
        raise ValueError(f"Unsupported temperature conversion: {from_unit} to {to_unit}")

    @staticmethod
    def convert_pressure(value, from_unit, to_unit):
        '''Converts pressure between hPa and inHg.'''
        if from_unit == to_unit:
            return value
        if from_unit == "hPa" and to_unit == "inHg":
            return value * 0.02953
        if from_unit == "inHg" and to_unit == "hPa":
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

class WeatherAPIService:
    '''Fetches current weather data from OpenWeatherMap API. Otherwise uses fallback data generator.'''
    def __init__(self):
        self.api = config.API_BASE_URL
        self.key = config.API_KEY
        self.fallback = SampleWeatherGenerator()

    def fetch_current(self, city):
        '''Fetches current weather data for a given city using OpenWeatherMap API.'''
        try:
            if not city.strip():
                raise Exception("No city provided") # No city error handling
            if not self.key:
                raise Exception("Missing API key") # No API key error handling
            url = f"{self.api}?q={city}&appid={self.key}&units=metric" # hardcoded units for API call because OpenWeatherMap API only supports metric for some metrics anyway
            response = requests.get(url)
            data = response.json()
            if str(data.get("cod")) != "200":
                raise Exception("City not found") # City not found error handling

            # rain = data.get("rain", {})
            # snow = data.get("snow", {})
            # precip_mm = rain.get("1h", 0) + snow.get("1h", 0)

            return {
                'temperature': data['main']['temp'], # May expand to additional values later
                'humidity': data['main']['humidity'],
                # 'precipitation': precip_mm,
                'conditions': data['weather'][0]['description'].title(),
                'wind_speed': data['wind']['speed'],
                'pressure': data['main']['pressure'],
                'date': datetime.now()
            }, False

        # Enumerate specific exceptions for clearer error handling
        except requests.exceptions.RequestException as e: 
            return self.use_fallback(city, f"Network/API issue: {e}")
        except (KeyError, TypeError, ValueError) as e:
            return self.use_fallback(city, f"Data parsing issue: {e}")
        except Exception as e:
            return self.use_fallback(city, f"General error: {e}")
    
    def use_fallback(self, city, error_message):
        '''Uses simulated data generator when API call fails.'''
        print(f"{error_message} - Using fallback data")
        fallback_data = self.fallback.generate(city)
        return fallback_data[-1], True

class WeatherDataManager:
    '''Manages weather data fetching and storage, including fallback handling.'''
    def __init__(self):
        self.api_service = WeatherAPIService()
        self.weather_data = {}
        self.fallback_used = False

    def fetch_current(self, city, unit_system):
        '''Fetches current weather data for a city, using fallback if API call fails.'''
        raw_data, fallback_used = self.api_service.fetch_current(city)

        # All API and fallback data is assumed to be in metric units and converted downstream.
        # If this changes in future (e.g., new fallback with imperial), update convert_units().
        converted_data = self.convert_units(raw_data, unit_system)

        self.weather_data.setdefault(city, []).append(converted_data) # Store the latest data for the city, for use in history tracking later
        return converted_data, fallback_used
    
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
        return self.api_service.fallback.generate(city, num_days)

    def get_recent_data(self, city, days):
        '''Returns recent weather data for a city, filtered by specified dates. Not currently used, but may support trend-based features like Tomorrow's Guess.'''
        return [entry for entry in self.weather_data.get(city, []) if entry['date'].date() in days]

    def format_data_for_logging(self, city, data, unit_system):
        '''Formats weather data for logging to a file with timestamp and unit system information.'''
        timestamp = data.get('date', datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            f"\n\nTime: {timestamp}",
            f"City: {city}",
            f"Temperature: {UnitConverter.format_value('temperature', data.get('temperature'), unit_system)}",
            f"Humidity: {UnitConverter.format_value('humidity', data.get('humidity'), unit_system)}",
            f"Pressure: {UnitConverter.format_value('pressure', data.get('pressure'), unit_system)}",
            f"Wind Speed: {UnitConverter.format_value('wind_speed', data.get('wind_speed'), unit_system)}",
            f"Conditions: {data.get('conditions', '--')}"
        ]
        return "\n".join(lines)

    def write_to_file(self, city, data, unit_system):
        '''Writes formatted weather data to a log file with timestamp and unit system information.'''
        log_entry = self.format_data_for_logging(city, data, unit_system)
        with open(config.OUTPUT["log"], "a") as f:
            f.write(log_entry)


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
            label = config.LABELS["key_to_display"].get(metric_key, metric_key.title())
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
        city_label = ttk.Label(metric, text="--", width=15, style="LabelValue.TLabel")
        city_label.grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(metric, text="Date:", style="LabelName.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5) # Date label
        date_label = ttk.Label(metric, text="--", width=15, style="LabelValue.TLabel")
        date_label.grid(row=1, column=1, sticky=tk.W, pady=5)

        for i, metric_key in enumerate(config.LABELS["key_to_display"]): # Create labels for each metric subject to visibility
            row = 0 + i
            name = ttk.Label(metric, text=f"{config.LABELS["key_to_display"][metric_key]}:", style="LabelName.TLabel")
            value = ttk.Label(metric, text="--", style="LabelValue.TLabel")
            name.grid(row=row, column=2, sticky=tk.W, pady=5)
            value.grid(row=row, column=3, sticky=tk.W, pady=5)
            self._metric_labels[metric_key] = {"label": name, "value": value}

        self.gui_vars['status_label'] = ttk.Label(metric, text="", foreground="red", style="LabelValue.TLabel") # Status label for API fallback or errors
        self.gui_vars['status_label'].grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=5)

        self._metric_labels['summary_city'] = {'value': city_label} # City value
        self._metric_labels['summary_date'] = {'value': date_label} # Date value

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

    def update_chart_display(self, x_vals, y_vals, metric_key, city, unit_system):
        '''Updates the chart display with new data for the specified metric and city.'''
        ax = self._chart_ax
        ax.clear()
        ax.plot(x_vals, y_vals, marker="o")

        label = config.LABELS["key_to_display"].get(metric_key, metric_key.title())
        unit = UnitConverter.get_unit_label(metric_key, unit_system)

        ax.set_title(f"{label} (Simulated) in {city}")
        ax.set_xlabel("Date")
        ax.set_ylabel(f"{label} ({unit})")

        self._chart_fig.autofmt_xdate(rotation=45)
        self._chart_fig.tight_layout()
        self._chart_canvas.draw()
    
    def bind_entry_events(self):
        '''Binds events for immediate updates'''
        self.city_entry.bind("<Return>", lambda e: self.update_cb()) # Pressing Enter in city entry triggers update

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


class WeatherDashboardLogic:
    '''Handles the logic for fetching and displaying weather data in the dashboard.'''
    def __init__(self, gui_vars, metric_labels, data_manager):
        self.vars = gui_vars
        self.labels = metric_labels
        self.data = data_manager
        self.widgets = None

    def fetch_city(self, city_name, unit_system):
        '''Fetches weather data for the specified city and updates the display.'''
        city = city_name.strip().title()
        
        current, fallback_used = self.data.fetch_current(city, unit_system)

        if fallback_used: # Error pop-ups for clear communication
            if not city:
                messagebox.showerror("Error", "Please enter a city name.")
            else:
                messagebox.showerror("Error", f"No data available for '{city}'.")

        self.update_display(city, current, fallback_used)
        self.data.write_to_file(city, current, unit_system)

    def update_display(self, city, data, fallback_used):
        '''Updates the display with current weather data.'''
        for metric, widgets in self.labels.items():
            if metric not in self.vars['visibility']: # skip metrics not set as visible
                continue  # skip entries that can't be toggled off like city and date
            visible = self.vars['visibility'][metric].get()
            if visible:
                widgets['label'].grid()
                widgets['value'].grid()
                unit = self.vars['unit'].get()
                widgets['value'].config(text=UnitConverter.format_value(metric, data.get(metric, "--"), unit))
            else:
                widgets['label'].grid_remove() # remove labels for hidden metrics
                widgets['value'].grid_remove()
            
        self.labels['summary_city']['value'].config(text=city) # Then update city and date
        date_str = data.get('date', datetime.now()).strftime("%Y-%m-%d")
        self.labels['summary_date']['value'].config(text=date_str)
        self.vars['status_label'].config(text="(Simulated)" if fallback_used else "") # Update status

    def update_chart(self):
        '''Updates the chart with historical weather data for the selected city and metric.'''
        city = self.vars['city'].get().strip().title()
        range_key = self.vars['range'].get()
        days = config.CHART["range_options"].get(range_key, 7)

        display_name = self.vars['chart'].get()
        metric_key = config.LABELS["display_to_key"].get(display_name)
        if not metric_key:
            messagebox.showerror("Error", "No chart metric available.")
            print("No chart metric available.")
            return         

        raw_data = self.data.get_historical(city, days)
        if not raw_data:
            return

        unit = self.vars['unit'].get()
        converted_data = [self.data.convert_units(entry, unit) for entry in raw_data]

        x_vals = [d['date'].strftime("%Y-%m-%d") for d in converted_data] # Dynamic axis values
        y_vals = [d[metric_key] for d in converted_data if metric_key in d]
        if not all(metric_key in d for d in converted_data):
            print(f"Warning: Some data entries are missing '{metric_key}'")

        self.widgets.update_chart_display(x_vals, y_vals, metric_key, city, unit)


class WeatherDashboardMain:
    '''Main application class for the Weather Dashboard.'''
    def __init__(self, root):
        self.root = root
        self.gui_vars = self.init_vars()
        self.frames = WeatherDashboardGUIFrames(root)
        self.data_manager = WeatherDataManager()

        self.widgets = WeatherDashboardWidgets(
            frames=self.frames.frames,
            gui_vars=self.gui_vars,
            update_cb=self.on_update_clicked,
            clear_cb=self.on_clear_clicked,
            dropdown_cb=self.update_chart_dropdown
        )

        self.gui_vars['metric_labels'] = self.widgets.metric_labels

        self.logic = WeatherDashboardLogic(
            self.gui_vars,
            metric_labels=self.widgets.metric_labels,
            data_manager=self.data_manager
        )

        self.logic.widgets = self.widgets
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
            config.LABELS["key_to_display"][k]
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