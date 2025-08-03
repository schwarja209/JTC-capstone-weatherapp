"""
Test for WeatherDashboard.gui.frames

Covers: WeatherDashboardGUIFrames
"""
import pytest

@pytest.mark.skip("GUI test: requires tkinter display")
def test_frames_instantiation_and_layout():
    from WeatherDashboard.gui.frames import WeatherDashboardGUIFrames
    import tkinter as tk
    root = tk.Tk()
    frames = WeatherDashboardGUIFrames(root)
    assert isinstance(frames.frames, dict)
    assert "root" in dir(frames)
    root.destroy()