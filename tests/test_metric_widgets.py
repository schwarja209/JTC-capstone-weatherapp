"""
Test for WeatherDashboard.widgets.metric_widgets

Covers: MetricDisplayWidgets
"""
import pytest

@pytest.mark.skip("GUI test: requires tkinter display")
def test_metric_widgets_instantiation_and_update():
    from WeatherDashboard.widgets.metric_widgets import MetricDisplayWidgets
    import tkinter as tk
    root = tk.Tk()
    class DummyManager: pass
    metric = MetricDisplayWidgets(DummyManager())
    if hasattr(metric, "update_metrics"):
        metric.update_metrics({})
    root.destroy()