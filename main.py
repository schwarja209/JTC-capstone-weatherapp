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
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: 'dotenv' not found. Skipping .env loading.")

class SampleWeatherGenerator:
    def generate(self, city, num_days=30):
        data = []
        base_temp = random.randint(40, 85)
        for i in range(num_days):
            date = datetime.now() - timedelta(days=num_days - 1 - i)
            data.append({
                'date': date,
                'temperature': base_temp + random.randint(-15, 15),
                'humidity': random.randint(30, 90),
                # 'precipitation': round(random.uniform(0, 2), 2),
                'conditions': random.choice(['Sunny', 'Cloudy', 'Rainy', 'Snowy']),
                'wind_speed': random.randint(0, 25),
                'pressure': round(random.uniform(29.5, 30.5), 2)
            })
        return data

class WeatherAPIService:
    def __init__(self):
        self.api = "https://api.openweathermap.org/data/2.5/weather"
        self.key = os.getenv("OPENWEATHER_API_KEY")

    def fetch_current(self, city, unit="imperial"):
        try:
            if not city.strip():
                raise Exception("No city provided")
            if not self.key:
                raise Exception("Missing API key")
            url = f"{self.api}?q={city}&appid={self.key}&units={unit}"
            response = requests.get(url)
            data = response.json()
            if str(data.get("cod")) != "200":
                raise Exception("City not found")

            # rain = data.get("rain", {})
            # snow = data.get("snow", {})
            # precip_mm = rain.get("1h", 0) + snow.get("1h", 0)

            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                # 'precipitation': round(precip_mm / 25.4, 2),
                'conditions': data['weather'][0]['description'].title(),
                'wind_speed': data['wind']['speed'],
                'pressure': round(data['main']['pressure'] * 0.02953, 2),
                'date': datetime.now()
            }, False

        except requests.exceptions.RequestException as e:
            return self.use_fallback(city, f"Network/API issue: {e}")
        except (KeyError, TypeError, ValueError) as e:
            return self.use_fallback(city, f"Data parsing issue: {e}")
        except Exception as e:
            return self.use_fallback(city, f"General error: {e}")
    
    def use_fallback(self, city, error_message):
        print(f"{error_message} - Using fallback data")
        fallback = SampleWeatherGenerator().generate(city)
        return fallback[-1], True

class WeatherDataManager:
    def __init__(self):
        self.api_service = WeatherAPIService()
        self.fallback_generator = SampleWeatherGenerator()
        self.weather_data = {}
        self.fallback_used = False

    def fetch_current(self, city, unit):
        data, fallback = self.api_service.fetch_current(city, unit)
        self.weather_data[city] = data if isinstance(data, list) else [data]
        self.fallback_used = fallback
        return data

    def get_historical(self, city, num_days):
        return self.fallback_generator.generate(city, num_days)

    def get_recent_data(self, city, days):
        return [entry for entry in self.weather_data.get(city, []) if entry['date'].date() in days]

    def is_fallback(self):
        return self.fallback_used

    def write_to_file(self, city, data):
        timestamp = data.get('date', datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        temp = data.get('temperature', '--')
        humid = data.get('humidity', '--')
        # precip = data.get('precipitation', '--')
        cond = data.get('conditions', '--')
        pressure = data.get('pressure', '--')
        wind = data.get('wind_speed', '--')

        temp_display = f"{temp:.1f} °C" if isinstance(temp, (int, float)) else f"{temp} °F"
        humid_display = f"{humid}%"
        # precip_display = f"{precip} in"
        pressure_display = f"{pressure} inHg"
        wind_display = f"{wind} mph"

        with open("data_big.txt", "a") as f:
            f.write(f"\n\nTime: {timestamp}\n")
            f.write(f"City: {city}\n")
            f.write(f"Temperature: {temp_display}\n")
            f.write(f"Humidity: {humid_display}\n")
            # f.write(f"Precipitation: {precip_display}\n")
            f.write(f"Pressure: {pressure_display}\n")
            f.write(f"Wind Speed: {wind_display}\n")
            f.write(f"Conditions: {cond}\n")

class WeatherDashboardGUIFrames:
    def __init__(self, root):
        self.root = root
        self.frames = {}
        self.create_styles()
        self.create_frames()

    def create_styles(self):
        style = ttk.Style()
        style.configure("FrameLabel.TLabelframe.Label", font=('Arial', 15, 'bold'))
        style.configure("LabelName.TLabel", font=('Arial', 10, 'bold'))
        style.configure("LabelValue.TLabel", font=('Arial', 10))
        style.configure("MainButton.TButton", font=('Arial', 10, 'bold'), padding=5)
        style.configure("Title.TLabel", font=('Comic Sans MS', 20, 'bold'))

    def create_frames(self):
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
        label = ttk.Label(self.frames["title"], text="Weather Dashboard", style="Title.TLabel")
        label.pack()

    def create_control_widgets(self):
        control = self.frames["control"]

        ttk.Label(control, text="City:", style="LabelName.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.city_entry = ttk.Entry(control, textvariable=self.gui_vars['city'])
        self.city_entry.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(control, text="Temp Unit:", style="LabelName.TLabel").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(control, text="Fahrenheit (°F)", variable=self.gui_vars['unit'], value="F").grid(row=2, column=1, sticky=tk.W)
        ttk.Radiobutton(control, text="Celsius (°C)", variable=self.gui_vars['unit'], value="C").grid(row=3, column=1, sticky=tk.W)

        ttk.Label(control, text="Show Metrics:", style="LabelName.TLabel").grid(row=4, column=0, sticky=tk.W, pady=5)
        for i, (metric_key, var) in enumerate(self.gui_vars['visibility'].items()):
            label = self.KEY_TO_DISPLAY.get(metric_key, metric_key.title())
            checkbox = ttk.Checkbutton(control, text=label, variable=var, command=self.dropdown_cb)
            checkbox.grid(row=5 + i // 2, column=i % 2, sticky=tk.W)

        ttk.Label(control, text="Chart Metric:", style="LabelName.TLabel").grid(row=4, column=2, sticky=tk.E, pady=5)
        chart_cb = ttk.Combobox(control, textvariable=self.gui_vars['chart'], state="readonly")
        chart_cb.grid(row=5, column=2, sticky=tk.E)
        self.gui_vars['chart_widget'] = chart_cb

        ttk.Label(control, text="Date Range:", style="LabelName.TLabel").grid(row=6, column=2, sticky=tk.E, pady=5)
        range_cb = ttk.Combobox(control, textvariable=self.gui_vars['range'], state="readonly")
        range_cb['values'] = list(self.RANGE_OPTIONS.keys())
        range_cb.current(0)
        range_cb.grid(row=7, column=2, sticky=tk.E)

        ttk.Button(control, text="Update Weather", command=self.update_cb, style="MainButton.TButton").grid(row=1, column=2, pady=10, sticky=tk.E)
        ttk.Button(control, text="Reset", command=self.clear_cb, style="MainButton.TButton").grid(row=2, column=2, pady=5, sticky=tk.E)
        for i in range(3):
            control.columnconfigure(i, weight=1)

    def create_metric_widgets(self):
        metric = self.frames["metric"]

        ttk.Label(metric, text="City:", style="LabelName.TLabel").grid(row=0, column=0, sticky=tk.W, pady=5)
        city_label = ttk.Label(metric, text="--", width=15, style="LabelValue.TLabel")
        city_label.grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(metric, text="Date:", style="LabelName.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
        date_label = ttk.Label(metric, text="--", width=15, style="LabelValue.TLabel")
        date_label.grid(row=1, column=1, sticky=tk.W, pady=5)

        for i, metric_key in enumerate(self.KEY_TO_DISPLAY):
            row = 0 + i
            name = ttk.Label(metric, text=f"{self.KEY_TO_DISPLAY[metric_key]}:", style="LabelName.TLabel")
            value = ttk.Label(metric, text="--", style="LabelValue.TLabel")
            name.grid(row=row, column=2, sticky=tk.W, pady=5)
            value.grid(row=row, column=3, sticky=tk.W, pady=5)
            self.metric_labels[metric_key] = {"name": name, "value": value}

        self.gui_vars['status_label'] = ttk.Label(metric, text="", foreground="red", style="LabelValue.TLabel")
        self.gui_vars['status_label'].grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=5)

        self.metric_labels['summary_city'] = {'value': city_label}
        self.metric_labels['summary_date'] = {'value': date_label}

    def create_chart_widgets(self):
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
        self.city_entry.bind("<Return>", lambda e: self.update_cb())

class WeatherDashboardLogic:
    def __init__(self, gui_vars, metric_labels, data_manager, key_to_display, range_options):
        self.vars = gui_vars
        self.labels = metric_labels
        self.data = data_manager
        self.KEY_TO_DISPLAY = key_to_display
        self.RANGE_OPTIONS = range_options

    def fetch_city(self, city_name):
        unit = "metric" if self.vars['unit'].get() == "C" else "imperial"
        city = city_name.strip().title()
        
        current = self.data.fetch_current(city, unit)

        if self.data.is_fallback():
            if not city:
                messagebox.showerror("Error", "Please enter a city name.")
            else:
                messagebox.showerror("Error", f"No data available for '{city}'.")

        self.update_display(city, current)
        self.data.write_to_file(city, current)

    def update_display(self, city, data):
        for metric, widgets in self.labels.items():
            if metric not in self.vars['visibility']:
                continue  # skip non-metric entries like 'summary_city'
            visible = self.vars['visibility'][metric].get()
            if visible:
                widgets['name'].grid()
                widgets['value'].grid()
                widgets['value'].config(text=self.format_metric_value(metric, data.get(metric, "--")))
            else:
                widgets['name'].grid_remove()
                widgets['value'].grid_remove()
            
        self.labels['summary_city']['value'].config(text=city)
        date_str = data.get('date', datetime.now()).strftime("%Y-%m-%d")
        self.labels['summary_date']['value'].config(text=date_str)

        self.vars['status_label'].config(
            text="(Simulated)" if self.data.is_fallback() else ""
        )

    def update_chart(self):
        city = self.vars['city'].get().strip().title()
        range_key = self.vars['range'].get()
        metric_key = self.inverse_lookup(self.vars['chart'].get())
        days = self.RANGE_OPTIONS.get(range_key, 7)

        data = self.data.get_historical(city, days)
        if not data:
            return

        x_vals = [d['date'].strftime("%Y-%m-%d") for d in data]
        y_vals = [d[metric_key] for d in data if metric_key in d]

        ax = self.vars['chart_ax']
        fig = self.vars['chart_fig']
        ax.clear()
        ax.plot(x_vals, y_vals, marker="o")

        metric_label = self.KEY_TO_DISPLAY.get(metric_key, metric_key.title())
        y_axis_label = f"{metric_label} ({self.y_axis_label(metric_key)})"

        ax.set_title(f"{metric_label} (Simulated) in {city}")
        ax.set_xlabel("Date")
        ax.set_ylabel(y_axis_label)
        fig.autofmt_xdate(rotation=45)
        fig.tight_layout()
        self.vars['chart_canvas'].draw()

    def inverse_lookup(self, display_name):
        for k, v in self.KEY_TO_DISPLAY.items():
            if v == display_name:
                return k
        return display_name.lower()

    def y_axis_label(self, metric):
        return {
            'temperature': "°C" if self.vars['unit'].get() == "C" else "°F",
            'humidity': "%",
            'pressure': "inHg",
            'wind_speed': "mph",
            'conditions': "Category"
        }.get(metric, "Value")

    def format_metric_value(self, metric, val):
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
        return {
            'city': tk.StringVar(value="New York"),
            'unit': tk.StringVar(value="F"),
            'range': tk.StringVar(value="Last 7 Days"),
            'chart': tk.StringVar(value="Temperature"),
            'visibility': {
                'temperature': tk.BooleanVar(value=True),
                'humidity': tk.BooleanVar(value=True),
                'wind_speed': tk.BooleanVar(value=False),
                'pressure': tk.BooleanVar(value=False),
                'conditions': tk.BooleanVar(value=False),
            }
        }

    def get_display_keys(self):
        return {
            'temperature': 'Temperature',
            'humidity': 'Humidity',
            'wind_speed': 'Wind Speed',
            'pressure': 'Pressure',
            'conditions': 'Conditions'
        }

    def get_range_options(self):
        return {
            'Last 7 Days': 7,
            'Last 14 Days': 14,
            'Last 30 Days': 30
        }

    def on_update_clicked(self):
        self.logic.fetch_city(self.gui_vars['city'].get())
        self.logic.update_chart()

    def on_clear_clicked(self):
        self.gui_vars['city'].set("New York")
        self.gui_vars['unit'].set("F")
        self.gui_vars['range'].set("Last 7 Days")
        self.gui_vars['chart'].set("Temperature")
        
        self.gui_vars['visibility']['temperature'].set(True)
        self.gui_vars['visibility']['humidity'].set(True)
        self.gui_vars['visibility']['wind_speed'].set(False)
        self.gui_vars['visibility']['pressure'].set(False)
        self.gui_vars['visibility']['conditions'].set(False)

        messagebox.showinfo("Reset", "Dashboard reset to default values.")  # confirm that everything was reset
        self.update_chart_dropdown()

    def update_chart_dropdown(self):
        chart_widget = self.gui_vars.get('chart_widget')
        if not chart_widget:
            return
        visible = [
            self.get_display_keys()[k]
            for k, v in self.gui_vars['visibility'].items() if v.get()
        ]
        chart_widget['values'] = visible
        if visible:
            self.gui_vars['chart'].set(visible[0])
        else:
            self.gui_vars['chart'].set("")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Weather Dashboard")
    app = WeatherDashboardMain(root)
    root.mainloop()
