"""
Test for WeatherDashboard.widgets.chart_widgets

Covers: ChartWidgets
"""
import pytest

@pytest.mark.skip("GUI test: requires tkinter display")
def test_chart_widgets_instantiation_and_update():
    from WeatherDashboard.widgets.chart_widgets import ChartWidgets
    import tkinter as tk
    root = tk.Tk()
    class DummyManager: pass
    chart = ChartWidgets(DummyManager())
    if hasattr(chart, "update_chart"):
        chart.update_chart({})
    root.destroy()