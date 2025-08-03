"""
Test for WeatherDashboard.widgets.widget_registry

Covers: WidgetRegistry
"""
def test_widget_registry_register_and_get():
    from WeatherDashboard.widgets.widget_registry import WidgetRegistry, WidgetInfo
    import pytest
    registry = WidgetRegistry()
    class DummyWidget: pass
    class DummyFrame: pass
    widget = DummyWidget()
    frame = DummyFrame()
    registry.register_widget("test_id", widget, "test_type", frame, {"grid": {}})
    assert registry.get_widget("test_id") is widget
    assert isinstance(registry.get_widget_info("test_id"), WidgetInfo)
    assert "test_id" in registry.get_all_widgets()