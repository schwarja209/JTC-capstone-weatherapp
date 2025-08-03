"""
Test for WeatherDashboard.widgets.control_widgets

Covers: ControlWidgets
"""
import pytest

@pytest.mark.skip("GUI test: requires tkinter display")
def test_control_widgets_instantiation_and_update():
    from WeatherDashboard.widgets.control_widgets import ControlWidgets
    import tkinter as tk
    root = tk.Tk()
    class DummyManager: pass
    control = ControlWidgets(DummyManager())
    if hasattr(control, "update_controls"):
        control.update_controls({})
    root.destroy()