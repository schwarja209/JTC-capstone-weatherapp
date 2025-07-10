if __name__ == "__main__":
    import sys
    import os

    # Ensure project root is in path (optional safety)
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))

    # Import and launch the app
    from WeatherDashboard.gui.main_window import WeatherDashboardMain
    import tkinter as tk

    root = tk.Tk()
    root.title("Weather Dashboard")
    app = WeatherDashboardMain(root)
    app.load_initial_display()
    root.mainloop()