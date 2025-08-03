"""
Test for WeatherDashboard.services.fallback_generator

Covers: SampleWeatherGenerator
"""
from WeatherDashboard.services.fallback_generator import SampleWeatherGenerator

def test_generate_weather_data_content():
    gen = SampleWeatherGenerator()
    data = gen.generate("Testville", num_days=5)
    assert isinstance(data, list)
    assert len(data) == 5
    for entry in data:
        assert "temperature" in entry
        assert "humidity" in entry
        assert "date" in entry
        assert entry["temperature"] is not None