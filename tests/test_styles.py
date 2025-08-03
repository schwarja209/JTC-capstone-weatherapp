"""
Test for WeatherDashboard.styles

Covers: Import only (style config module)
"""
def test_import_styles():
    import WeatherDashboard.styles
    assert hasattr(WeatherDashboard.styles, "__doc__")