"""
Test for WeatherDashboard.widgets.title_widgets

Covers: TitleWidget
"""
import pytest

@pytest.mark.skip("GUI test: requires tkinter display")
def test_title_widgets_instantiation_and_update():
    from WeatherDashboard.widgets.title_widgets import TitleWidget
    import tkinter as tk
    root = tk.Tk()
    class DummyManager: pass
    title = TitleWidget(DummyManager())
    if hasattr(title, "update_title"):
        title.update_title("Test")
    root.destroy()