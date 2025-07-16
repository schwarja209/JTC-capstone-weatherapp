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
    config.validate_config()  # Validate configuration at startup
except ValueError as e:
    print(f"Configuration error: {e}")
    import sys
    sys.exit(1)

from WeatherDashboard.gui.main_window import WeatherDashboardMain
from WeatherDashboard.utils.logger import Logger

# Ensure required directories exist at app startup
for folder in {config.OUTPUT["data_dir"], config.OUTPUT["log_dir"]}:
    os.makedirs(folder, exist_ok=True)

# Test logging system health after directory creation
if not Logger.test_logging_health():
    print("Warning: Logging system health check failed")

def main():
    """Main entry point for the Weather Dashboard application."""
    root = tk.Tk()
    root.title("Weather Dashboard")
    app = WeatherDashboardMain(root)
    app.load_initial_display()
    root.mainloop()

if __name__ == "__main__":
    main()