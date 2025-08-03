"""
Test for WeatherDashboard.features.alerts.alert_display

Covers: AlertStatusIndicator, SimpleAlertPopup
"""
import pytest

@pytest.mark.skip("GUI test: requires tkinter display")
def test_alert_display_indicator_and_popup():
    from WeatherDashboard.features.alerts.alert_display import AlertStatusIndicator, SimpleAlertPopup
    import tkinter as tk
    root = tk.Tk()
    indicator = AlertStatusIndicator(root)
    indicator.update_status([])
    assert hasattr(indicator, "set_click_callback")
    popup = SimpleAlertPopup(root, [])
    assert hasattr(popup, "_create_display")
    root.destroy()