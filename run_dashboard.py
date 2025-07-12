"""
Convenience runner for the Weather Dashboard application.

Simple entry point script that sets up the Python path and launches
the Weather Dashboard from the project root directory. Provides an
easy way to run the application without navigating to the package directory.
"""

if __name__ == "__main__":
    import sys
    import os

    # Ensure project root is in path
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))

    # Import and launch the app
    from WeatherDashboard.gui.main_window import WeatherDashboardMain
    import tkinter as tk

    root = tk.Tk()
    root.title("Weather Dashboard")
    app = WeatherDashboardMain(root)
    app.load_initial_display()
    root.mainloop()