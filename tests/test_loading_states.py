"""
Test for WeatherDashboard.gui.loading_states

Covers: LoadingStateManager, AsyncWeatherOperation
"""
import pytest

@pytest.mark.skip("GUI test: requires tkinter display")
def test_loading_state_manager_and_async_op():
    from WeatherDashboard.gui.loading_states import LoadingStateManager, AsyncWeatherOperation
    import tkinter as tk
    root = tk.Tk()
    class DummyState: pass
    class DummyStatusBar:
        def update_progress(self, *a, **kw): pass
        def clear_progress(self): pass
    manager = LoadingStateManager(DummyState(), DummyStatusBar())
    manager.start_loading("TestOp")
    manager.stop_loading()
    op = AsyncWeatherOperation(None, manager)
    assert hasattr(op, "fetch_weather_async")
    root.destroy()