"""
Test for WeatherDashboard.features.alerts.alert_config

Covers: ALERT_THRESHOLDS, ALERT_DEFINITIONS, validate_alert_config
"""
from WeatherDashboard.features.alerts import alert_config

def test_alert_config_validation_and_keys():
    assert isinstance(alert_config.ALERT_THRESHOLDS, dict)
    assert "temperature_high" in alert_config.ALERT_THRESHOLDS
    assert isinstance(alert_config.ALERT_DEFINITIONS, dict)
    assert "temperature_high" in alert_config.ALERT_DEFINITIONS
    assert alert_config.validate_alert_config() is True