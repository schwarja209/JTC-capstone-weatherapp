"""
Test for WeatherDashboard.widgets.status_bar_widgets

Covers: StatusBarWidgets
"""
import pytest

@pytest.mark.skip("GUI test: requires tkinter display")
def test_status_bar_widgets_instantiation_and_update():
    from WeatherDashboard.widgets.status_bar_widgets import StatusBarWidgets
    import tkinter as tk
    root = tk.Tk()
    class DummyManager: pass
    status = StatusBarWidgets(DummyManager())
    if hasattr(status, "update_status"):
        status.update_status("Test")
    root.destroy()