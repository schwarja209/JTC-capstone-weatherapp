"""
Test for WeatherDashboard.core.data_service

Covers: CityDataResult, HistoricalDataResult, LoggingResult, WeatherDataService
"""
import pytest
from WeatherDashboard.core import data_service
from datetime import datetime

def test_city_data_result_validation():
    # Valid instantiation
    result = data_service.CityDataResult(
        city_name="Testville",
        weather_data={},
        error=None,
        is_simulated=False,
        unit_system="metric",
        timestamp=datetime.now()
    )
    assert result.city_name == "Testville"
    # Invalid unit_system
    with pytest.raises(ValueError):
        data_service.CityDataResult(
            city_name="Testville",
            weather_data={},
            error=None,
            is_simulated=False,
            unit_system="kelvin",
            timestamp=datetime.now()
        )

def test_historical_data_result_validation():
    # Valid
    result = data_service.HistoricalDataResult(
        city_name="Testville",
        data_entries=[],
        num_days=1,
        unit_system="metric",
        source_unit="metric",
        conversion_applied=False,
        timestamp=datetime.now()
    )
    assert result.num_days == 1
    # Invalid num_days
    with pytest.raises(ValueError):
        data_service.HistoricalDataResult(
            city_name="Testville",
            data_entries=[],
            num_days=0,
            unit_system="metric",
            source_unit="metric",
            conversion_applied=False,
            timestamp=datetime.now()
        )

def test_logging_result_validation():
    # Valid
    result = data_service.LoggingResult(
        city_name="Testville",
        unit_system="metric",
        success=True,
        error_message=None,
        timestamp=datetime.now()
    )
    assert result.success is True
    # Invalid file_size_bytes
    with pytest.raises(ValueError):
        data_service.LoggingResult(
            city_name="Testville",
            unit_system="metric",
            success=True,
            error_message=None,
            timestamp=datetime.now(),
            file_size_bytes=-1
        )

def test_weather_data_service_methods():
    class DummyDataManager:
        def fetch_current(self, *a, **kw): return {"temp": 20}
        def get_historical(self, *a, **kw): return [{"temp": 20}]
        def convert_units(self, d, u): return d
        def write_to_file(self, *a, **kw): pass
    service = data_service.WeatherDataService(DummyDataManager())
    # get_city_data
    data = service.get_city_data("Testville", "metric")
    assert "temp" in data
    # get_historical_data
    hist = service.get_historical_data("Testville", 1, "metric")
    assert hasattr(hist, "data_entries")
    # write_to_log
    log = service.write_to_log("Testville", {"temp": 20}, "metric")
    assert log.success is True