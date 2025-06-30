"""
Weather Dashboard - Combining HW 8 and 10, and refactoring
- GUI from weather_dashboard_big.py
- Live data via OpenWeatherMap API (current only)
- Simulated past data via fallback generator
- Modular design with separate service and generator
- All API calls are user-triggered; chart is simulated
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import requests

import config

class SampleWeatherGenerator:
    """Generates simulated weather data for a given city over a specified number of days."""
    def generate(self, city, num_days=30):
        data = []
        base_temp = random.randint(40, 85)
        for i in range(num_days):
            date = datetime.now() - timedelta(days=num_days - 1 - i)
            data.append({
                'date': date,
                'temperature': base_temp + random.randint(-15, 15),
                'humidity': random.randint(30, 90),
                # 'precipitation': round(random.uniform(0, 2), 2),  # All precipitation values and handling is on hold for now
                'conditions': random.choice(['Sunny', 'Cloudy', 'Rainy', 'Snowy']),
                'wind_speed': random.randint(0, 25),
                'pressure': round(random.uniform(29.5, 30.5), 2)
            })
        return data

class WeatherAPIService:
    """Fetches current weather data from OpenWeatherMap API. Otherwise uses fallback data generator."""
    def __init__(self):
        self.api = config.API_BASE_URL
        self.key = config.API_KEY

    def fetch_current(self, city, unit="imperial"):
        """Fetches current weather data for a given city using OpenWeatherMap API."""
        try:
            if not city.strip():
                raise Exception("No city provided") # No city error handling
            if not self.key:
                raise Exception("Missing API key") # No API key error handling
            url = f"{self.api}?q={city}&appid={self.key}&units={unit}"
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
                # 'precipitation': round(precip_mm / 25.4, 2),
                'conditions': data['weather'][0]['description'].title(),
                'wind_speed': data['wind']['speed'],
                'pressure': round(data['main']['pressure'] * 0.02953, 2),
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
        """Uses simulated data generator when API call fails."""
        print(f"{error_message} - Using fallback data")
        fallback = SampleWeatherGenerator().generate(city)
        return fallback[-1], True

class WeatherDataManager:
    """Manages weather data fetching and storage, including fallback handling."""
    def __init__(self):
        self.api_service = WeatherAPIService()
        self.fallback_generator = SampleWeatherGenerator()
        self.weather_data = {}
        self.fallback_used = False

    def fetch_current(self, city, unit):
        """Fetches current weather data for a city, using fallback if API call fails."""
        data, fallback = self.api_service.fetch_current(city, unit)
        self.weather_data[city] = data if isinstance(data, list) else [data]
        self.fallback_used = fallback
        return data

    def get_historical(self, city, num_days):
        """Fetches historical weather data for a city. Currently always defaults to fallback."""
        return self.fallback_generator.generate(city, num_days)

    def get_recent_data(self, city, days):
        """Returns recent weather data for a city, filtered by specified dates. Not currently used, but may support trend-based features like Tomorrow's Guess."""
        return [entry for entry in self.weather_data.get(city, []) if entry['date'].date() in days]

    def is_fallback(self):
        """Checks if fallback data was used in the last fetch."""
        return self.fallback_used

    def write_to_file(self, city, data):
        """Appends last app data produced to a text file for use log."""
        # Get data
        timestamp = data.get('date', datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        temp = data.get('temperature', '--')
        humid = data.get('humidity', '--')
        # precip = data.get('precipitation', '--')
        cond = data.get('conditions', '--')
        pressure = data.get('pressure', '--')
        wind = data.get('wind_speed', '--')

        # Format data
        temp_display = f"{temp:.1f} °C" if isinstance(temp, (int, float)) else f"{temp} °F"
        humid_display = f"{humid}%"
        # precip_display = f"{precip} in"
        pressure_display = f"{pressure} inHg"
        wind_display = f"{wind} mph"

        # Append data to file
        with open(config.OUTPUT_FILE, "a") as f:
            f.write(f"\n\nTime: {timestamp}\n")
            f.write(f"City: {city}\n")
            f.write(f"Temperature: {temp_display}\n")
            f.write(f"Humidity: {humid_display}\n")
            # f.write(f"Precipitation: {precip_display}\n")
            f.write(f"Pressure: {pressure_display}\n")
            f.write(f"Wind Speed: {wind_display}\n")
            f.write(f"Conditions: {cond}\n")

class WeatherDashboardGUIFrames:
    """Creates and manages the main GUI frames for the weather dashboard."""
    def __init__(self, root):
        self.root = root
        self.frames = {}
        self.create_styles()
        self.create_frames()

    def create_styles(self):
        """Configures the styles for the GUI elements."""
        style = ttk.Style()
        style.configure("FrameLabel.TLabelframe.Label", font=('Arial', 15, 'bold'))
        style.configure("LabelName.TLabel", font=('Arial', 10, 'bold'))
        style.configure("LabelValue.TLabel", font=('Arial', 10))
        style.configure("MainButton.TButton", font=('Arial', 10, 'bold'), padding=5)
        style.configure("Title.TLabel", font=('Comic Sans MS', 20, 'bold'))

    def create_frames(self):
        """Creates the main frames for the dashboard layout."""
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
    """Creates and manages the widgets for the weather dashboard."""
    def __init__(self, frames, gui_vars, key_to_display, range_options, update_cb, clear_cb, dropdown_cb):
        self.frames = frames
        self.gui_vars = gui_vars
        self.KEY_TO_DISPLAY = key_to_display
        self.RANGE_OPTIONS = range_options
        self.update_cb = update_cb
        self.clear_cb = clear_cb
        self.dropdown_cb = dropdown_cb
        self.metric_labels = {}
        self.chart_canvas = None

        self.create_title_widgets()
        self.create_control_widgets()
        self.create_metric_widgets()
        self.create_chart_widgets()
        self.bind_entry_events()

    def create_title_widgets(self):
        """Creates the title label for the dashboard."""
        label = ttk.Label(self.frames["title"], text="Weather Dashboard", style="Title.TLabel")
        label.pack()

    def create_control_widgets(self):
        """Creates the control widgets for user input and actions."""
        control = self.frames["control"]

        ttk.Label(control, text="City:", style="LabelName.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5) # City label and entry
        self.city_entry = ttk.Entry(control, textvariable=self.gui_vars['city'])
        self.city_entry.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(control, text="Temp Unit:", style="LabelName.TLabel").grid(row=2, column=0, sticky=tk.W, pady=5) # Temp unit selector
        ttk.Radiobutton(control, text="Fahrenheit (°F)", variable=self.gui_vars['unit'], value="F").grid(row=2, column=1, sticky=tk.W)
        ttk.Radiobutton(control, text="Celsius (°C)", variable=self.gui_vars['unit'], value="C").grid(row=3, column=1, sticky=tk.W)

        ttk.Label(control, text="Show Metrics:", style="LabelName.TLabel").grid(row=4, column=0, sticky=tk.W, pady=5) # Metric visibility checkboxes
        for i, (metric_key, var) in enumerate(self.gui_vars['visibility'].items()):
            label = self.KEY_TO_DISPLAY.get(metric_key, metric_key.title())
            checkbox = ttk.Checkbutton(control, text=label, variable=var, command=self.dropdown_cb)
            checkbox.grid(row=5 + i // 2, column=i % 2, sticky=tk.W)

        ttk.Label(control, text="Chart Metric:", style="LabelName.TLabel").grid(row=4, column=2, sticky=tk.E, pady=5) # Chart metric selector
        chart_cb = ttk.Combobox(control, textvariable=self.gui_vars['chart'], state="readonly")
        chart_cb.grid(row=5, column=2, sticky=tk.E)
        self.gui_vars['chart_widget'] = chart_cb

        ttk.Label(control, text="Date Range:", style="LabelName.TLabel").grid(row=6, column=2, sticky=tk.E, pady=5) # Date range selector
        range_cb = ttk.Combobox(control, textvariable=self.gui_vars['range'], state="readonly")
        range_cb['values'] = list(self.RANGE_OPTIONS.keys())
        range_cb.current(0)
        range_cb.grid(row=7, column=2, sticky=tk.E)

        # Control buttons for updating and resetting display
        ttk.Button(control, text="Update Weather", command=self.update_cb, style="MainButton.TButton").grid(row=1, column=2, pady=10, sticky=tk.E)
        ttk.Button(control, text="Reset", command=self.clear_cb, style="MainButton.TButton").grid(row=2, column=2, pady=5, sticky=tk.E)
        
        # Configure grid weights so things aren't cramped
        for i in range(3):
            control.columnconfigure(i, weight=1)

    def create_metric_widgets(self):
        """Creates the metric display widgets for current weather data."""
        metric = self.frames["metric"]

        ttk.Label(metric, text="City:", style="LabelName.TLabel").grid(row=0, column=0, sticky=tk.W, pady=5) # City label
        city_label = ttk.Label(metric, text="--", width=15, style="LabelValue.TLabel")
        city_label.grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(metric, text="Date:", style="LabelName.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5) # Date label
        date_label = ttk.Label(metric, text="--", width=15, style="LabelValue.TLabel")
        date_label.grid(row=1, column=1, sticky=tk.W, pady=5)

        for i, metric_key in enumerate(self.KEY_TO_DISPLAY): # Create labels for each metric subject to visibility
            row = 0 + i
            name = ttk.Label(metric, text=f"{self.KEY_TO_DISPLAY[metric_key]}:", style="LabelName.TLabel")
            value = ttk.Label(metric, text="--", style="LabelValue.TLabel")
            name.grid(row=row, column=2, sticky=tk.W, pady=5)
            value.grid(row=row, column=3, sticky=tk.W, pady=5)
            self.metric_labels[metric_key] = {"name": name, "value": value}

        self.gui_vars['status_label'] = ttk.Label(metric, text="", foreground="red", style="LabelValue.TLabel") # Status label for API fallback or errors
        self.gui_vars['status_label'].grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=5)

        self.metric_labels['summary_city'] = {'value': city_label} # City value
        self.metric_labels['summary_date'] = {'value': date_label} # Date value

    def create_chart_widgets(self):
        """Creates the chart display for historical weather trends."""
        self.fig = Figure(figsize=(8, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("")
        self.ax.set_xlabel("")
        self.ax.set_ylabel("")

        self.chart_canvas = FigureCanvasTkAgg(self.fig, master=self.frames["chart"])
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.gui_vars['chart_fig'] = self.fig
        self.gui_vars['chart_ax'] = self.ax
        self.gui_vars['chart_canvas'] = self.chart_canvas
    
    def bind_entry_events(self):
        """Binds events for immediate updates"""
        self.city_entry.bind("<Return>", lambda e: self.update_cb()) # Pressing Enter in city entry triggers update

class WeatherDashboardLogic:
    """Handles the logic for fetching and displaying weather data in the dashboard."""
    def __init__(self, gui_vars, metric_labels, data_manager, key_to_display, range_options):
        self.vars = gui_vars
        self.labels = metric_labels
        self.data = data_manager
        self.KEY_TO_DISPLAY = key_to_display
        self.RANGE_OPTIONS = range_options

    def fetch_city(self, city_name):
        """Fetches weather data for the specified city and updates the display."""
        unit = "metric" if self.vars['unit'].get() == "C" else "imperial"
        city = city_name.strip().title()
        
        current = self.data.fetch_current(city, unit)

        if self.data.is_fallback(): # Error pop-ups for clear communication
            if not city:
                messagebox.showerror("Error", "Please enter a city name.")
            else:
                messagebox.showerror("Error", f"No data available for '{city}'.")

        self.update_display(city, current)
        self.data.write_to_file(city, current)

    def update_display(self, city, data):
        """Updates the display with current weather data."""
        for metric, widgets in self.labels.items():
            if metric not in self.vars['visibility']: # skip metrics not set as visible
                continue  # skip entries that can't be toggled off like city and date
            visible = self.vars['visibility'][metric].get()
            if visible:
                widgets['name'].grid()
                widgets['value'].grid()
                widgets['value'].config(text=self.format_metric_value(metric, data.get(metric, "--")))
            else:
                widgets['name'].grid_remove() # remove labels for hidden metrics
                widgets['value'].grid_remove()
            
        self.labels['summary_city']['value'].config(text=city) # Then update city and date
        date_str = data.get('date', datetime.now()).strftime("%Y-%m-%d")
        self.labels['summary_date']['value'].config(text=date_str)

        self.vars['status_label'].config( # Update status
            text="(Simulated)" if self.data.is_fallback() else ""
        )

    def update_chart(self):
        """Updates the chart with historical weather data for the selected city and metric."""
        city = self.vars['city'].get().strip().title()
        range_key = self.vars['range'].get()
        metric_key = self.inverse_lookup(self.vars['chart'].get())
        days = self.RANGE_OPTIONS.get(range_key, 7)

        data = self.data.get_historical(city, days)
        if not data:
            return

        x_vals = [d['date'].strftime("%Y-%m-%d") for d in data] # Dynamic axis values
        y_vals = [d[metric_key] for d in data if metric_key in d]

        ax = self.vars['chart_ax']
        fig = self.vars['chart_fig']
        ax.clear()
        ax.plot(x_vals, y_vals, marker="o")

        metric_label = self.KEY_TO_DISPLAY.get(metric_key, metric_key.title()) # Dynamic axis labels
        y_axis_label = f"{metric_label} ({self.y_axis_label(metric_key)})"

        ax.set_title(f"{metric_label} (Simulated) in {city}")
        ax.set_xlabel("Date")
        ax.set_ylabel(y_axis_label)
        fig.autofmt_xdate(rotation=45)
        fig.tight_layout()
        self.vars['chart_canvas'].draw()

    def inverse_lookup(self, display_name):
        """Finds the internal metric key from the display name."""
        for k, v in self.KEY_TO_DISPLAY.items():
            if v == display_name:
                return k
        return display_name.lower()

    def y_axis_label(self, metric):
        """Returns the appropriate y-axis label for the chart based on the metric."""
        return {
            'temperature': "°C" if self.vars['unit'].get() == "C" else "°F",
            'humidity': "%",
            'pressure': "inHg",
            'wind_speed': "mph",
            'conditions': "Category"
        }.get(metric, "Value")

    def format_metric_value(self, metric, val):
        """Formats the metric value for display based on its type and the selected unit."""
        if metric == "temperature":
            if isinstance(val, (int, float)):
                return f"{val:.1f} °{'C' if self.vars['unit'].get() == 'C' else 'F'}"
        elif metric == "humidity":
            return f"{val}%"
        elif metric == "pressure":
            return f"{val} inHg"
        elif metric == "wind_speed":
            return f"{val} mph"
        return val or "--"

class WeatherDashboardMain:
    """Main application class for the Weather Dashboard."""
    def __init__(self, root):
        self.root = root
        self.gui_vars = self.init_vars()
        self.frames = WeatherDashboardGUIFrames(root)
        self.data_manager = WeatherDataManager()

        self.logic = WeatherDashboardLogic(
            self.gui_vars,
            metric_labels={},  # temporary, will be replaced below
            data_manager=self.data_manager,
            key_to_display=self.get_display_keys(),
            range_options=self.get_range_options()
        )

        self.widgets = WeatherDashboardWidgets(
            frames=self.frames.frames,
            gui_vars=self.gui_vars,
            key_to_display=self.get_display_keys(),
            range_options=self.get_range_options(),
            update_cb=self.on_update_clicked,
            clear_cb=self.on_clear_clicked,
            dropdown_cb=self.update_chart_dropdown
        )

        self.gui_vars['metric_labels'] = self.widgets.metric_labels
        self.logic.labels = self.widgets.metric_labels
        self.update_chart_dropdown()
        self.logic.fetch_city(self.gui_vars['city'].get())

    def init_vars(self):
        """Initializes the GUI variables with default values from config."""
        return {
            'city': tk.StringVar(value=config.DEFAULT_CITY),
            'unit': tk.StringVar(value=config.DEFAULT_UNIT),
            'range': tk.StringVar(value=config.DEFAULT_RANGE),
            'chart': tk.StringVar(value=config.DEFAULT_CHART),
            'visibility': {
                key: tk.BooleanVar(value=val)
                for key, val in config.DEFAULT_VISIBILITY.items()
            }
        }

    def get_display_keys(self):
        """Returns a dictionary mapping internal metric keys to their display names."""
        return config.KEY_TO_DISPLAY

    def get_range_options(self):
        """Returns the date range options for the chart dropdown."""
        return config.RANGE_OPTIONS
    
    def on_update_clicked(self):
        """Handles the update button click event to fetch and display weather data."""
        self.logic.fetch_city(self.gui_vars['city'].get())
        self.logic.update_chart()

    def on_clear_clicked(self):
        """Handles the reset button click event to reset input controls to default values (but does not clear display output)."""
        self.gui_vars['city'].set(config.DEFAULT_CITY)
        self.gui_vars['unit'].set(config.DEFAULT_UNIT)
        self.gui_vars['range'].set(config.DEFAULT_RANGE)
        self.gui_vars['chart'].set(config.DEFAULT_CHART)

        for key, var in self.gui_vars['visibility'].items():
            var.set(config.DEFAULT_VISIBILITY.get(key, False))

        messagebox.showinfo("Reset", "Dashboard reset to default values.") # Pop-up confirmation
        self.update_chart_dropdown()

    def update_chart_dropdown(self):
        """Updates the chart dropdown based on the current visibility settings."""
        chart_widget = self.gui_vars.get('chart_widget')
        if not chart_widget:
            return
        visible = [ # Get display versions of visible metrics for chart dropdown
            self.get_display_keys()[k]
            for k, v in self.gui_vars['visibility'].items() if v.get()
        ]
        chart_widget['values'] = visible
        if visible:
            self.gui_vars['chart'].set(visible[0])
        else:
            self.gui_vars['chart'].set("")

if __name__ == "__main__":
    """Main entry point for the Weather Dashboard application."""
    root = tk.Tk()
    root.title("Weather Dashboard")
    app = WeatherDashboardMain(root)
    root.mainloop()
