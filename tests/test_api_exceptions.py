"""
Test for WeatherDashboard.services.api_exceptions

Covers: All custom exception classes.
"""
import pytest
import WeatherDashboard.services.api_exceptions as exc

def test_exception_hierarchy_and_raising():
    # Test inheritance and raising/catching
    for cls in [
        exc.WeatherDashboardError, exc.WeatherAPIError, exc.CityNotFoundError,
        exc.RateLimitError, exc.NetworkError, exc.ValidationError,
        exc.UIError, exc.LoadingError, exc.ThemeError
    ]:
        with pytest.raises(cls):
            raise cls("test")
    # Test catching by base class
    try:
        raise exc.CityNotFoundError("city")
    except exc.WeatherAPIError:
        pass