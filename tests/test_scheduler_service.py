"""
Test for WeatherDashboard.features.history.scheduler_service

Covers: WeatherDataScheduler
"""
from WeatherDashboard.features.history.scheduler_service import WeatherDataScheduler

def test_scheduler_methods_and_status():
    class DummyHistoryService:
        def cleanup_old_data(self): pass
    class DummyDataManager:
        def fetch_current(self, *a, **kw): return {}
    class DummyStateManager:
        city = type("C", (), {"get": lambda self: "Testville"})()
        unit = type("U", (), {"get": lambda self: "metric"})()
    class DummyUIHandler:
        root = None
        def update_display(self, *a, **kw): pass
        def update_scheduler_status(self, *a, **kw): pass
    scheduler = WeatherDataScheduler(DummyHistoryService(), DummyDataManager(), DummyStateManager(), DummyUIHandler())
    status = scheduler.get_status_info()
    assert "enabled" in status
    assert "default_city" in status