"""
Widget interface for Weather Dashboard (ADR 030-compliant)

Defines the contract for all widget operations required by the controller.
This interface ensures a consistent, decoupled API for all widget managers
and composite widget managers in the Weather Dashboard application.

Classes:
    IWeatherDashboardWidgets: Interface for controller-widget communication

ADR Reference:
    - ADR 030: Documentation and docstring standards
"""

from typing import Any, Dict, List, Optional

class IWeatherDashboardWidgets:
    """Interface for all widget operations required by the controller."""
    def is_ready(self) -> bool:
        """Return True if all widgets are ready."""
        raise NotImplementedError

    def get_creation_error(self) -> Optional[str]:
        """Return error message if widget creation failed, else None."""
        raise NotImplementedError

    def update_metric_display(self, metrics: Dict[str, str]) -> None:
        """Update metric display widgets."""
        raise NotImplementedError

    def update_status_bar(self, city_name: str, error_exception: Optional[Exception], simulated: bool = False) -> None:
        """Update the status bar widgets with the current city, error status, and data source."""
        raise NotImplementedError

    def update_alerts(self, raw_data: Dict[str, Any]) -> None:
        """Update alert display widgets."""
        raise NotImplementedError

    def update_chart_display(self, x_vals: List[str], y_vals: List[Any], metric_key: str, city: str, unit_system: str, fallback: bool = False) -> None:
        """Update chart display widgets."""
        raise NotImplementedError

    def get_alert_popup_parent(self):
        """Return parent widget for alert popups."""
        raise NotImplementedError
    
    def clear_chart_with_error_message(self) -> None:
        """Clear the chart and show an error message."""
        raise NotImplementedError
