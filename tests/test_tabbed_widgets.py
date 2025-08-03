"""
Test for WeatherDashboard.widgets.tabbed_widgets

Covers: TabbedDisplayWidgets
"""
import pytest

@pytest.mark.skip("GUI test: requires tkinter display")
def test_tabbed_widgets_instantiation_and_update():
    from WeatherDashboard.widgets.tabbed_widgets import TabbedDisplayWidgets
    import tkinter as tk
    root = tk.Tk()
    class DummyManager: pass
    tabbed = TabbedDisplayWidgets(DummyManager())
    if hasattr(tabbed, "update_tabs"):
        tabbed.update_tabs({})
    root.destroy()