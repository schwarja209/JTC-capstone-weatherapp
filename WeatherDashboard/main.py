'''
Weather Dashboard - Entry Point
- Live data via OpenWeatherMap API (current only)
- Simulated past data via fallback generator
- Modular design with separate service and generator
- All API calls are user-triggered; chart is simulated
- Centralized state management for better scalability
'''

import os
import tkinter as tk

try:
    from WeatherDashboard import config
except ValueError as e:
    print(f"Configuration error: {e}")
    import sys
    sys.exit(1)

from WeatherDashboard.gui.main_window import WeatherDashboardMain

# Ensure required directories exist at app startup
for folder in {config.OUTPUT["data_dir"], config.OUTPUT["log_dir"]}:
    os.makedirs(folder, exist_ok=True)

if __name__ == "__main__":
    '''Main entry point for the Weather Dashboard application.'''
    root = tk.Tk()
    root.title("Weather Dashboard")
    app = WeatherDashboardMain(root)
    app.load_initial_display()
    root.mainloop()