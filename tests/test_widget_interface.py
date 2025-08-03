"""
Test for WeatherDashboard.widgets.widget_interface

Covers: IWeatherDashboardWidgets
"""
def test_import_widget_interface():
    from WeatherDashboard.widgets.widget_interface import IWeatherDashboardWidgets
    assert IWeatherDashboardWidgets is not None