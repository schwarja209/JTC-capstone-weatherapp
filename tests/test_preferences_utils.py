"""
Test for WeatherDashboard.utils.preferences_utils

Covers: UserPreferences, PreferencesService
"""
from WeatherDashboard.utils.preferences_utils import UserPreferences, PreferencesService
from datetime import datetime

def test_user_preferences_to_from_dict():
    prefs = UserPreferences(
        city="Testville",
        unit_system="metric",
        chart_days=7,
        visible_metrics={"temp": True},
        scheduler_enabled=True,
        last_updated=datetime.now()
    )
    d = prefs.to_dict()
    loaded = UserPreferences.from_dict(d)
    assert loaded.city == "Testville"

def test_preferences_service_save_and_load(tmp_path):
    service = PreferencesService(preferences_file=str(tmp_path / "prefs.json"))
    prefs = UserPreferences(
        city="Testville",
        unit_system="metric",
        chart_days=7,
        visible_metrics={"temp": True},
        scheduler_enabled=True,
        last_updated=datetime.now()
    )
    assert service.save_preferences(prefs)
    loaded = service.load_preferences()
    assert loaded.city == "Testville"