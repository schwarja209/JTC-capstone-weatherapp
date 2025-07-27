"""
Centralized state access utilities for the Weather Dashboard application.

This module provides unified state management utilities to eliminate code duplication
across widget components. Consolidates metric visibility checking, state variable access,
and bulk state operations into a single utility class with consistent error handling.

Eliminates approximately 45 lines of duplicate visibility logic that was previously
scattered across control widgets, metric widgets, and alert management components.

Classes:
    StateUtils: Static utility class for centralized state access operations
"""

from typing import List, Any
import tkinter as tk

from WeatherDashboard.utils.logger import Logger
from WeatherDashboard import config

class StateUtils:
    """Centralized state access utilities to eliminate duplication."""

    def __init__(self) -> None:
        """Initialize state utils with optional dependencies."""
        # Direct imports for stable utilities
        self.config = config
        self.logger = Logger()

    def is_metric_visible(self, state_manager: Any, metric_key: str) -> bool:
        """Safely check if a metric is currently visible.
        
        Consolidates the 3 different implementations into one reliable method.
        
        Args:
            state_manager: Application state manager instance
            metric_key: Metric key to check visibility for
            
        Returns:
            bool: True if metric is visible, False otherwise
        """
        try:
            # Check if state manager has visibility attribute
            if not hasattr(state_manager, 'visibility') or not isinstance(state_manager.visibility, dict):
                self.logger.warn(self.config.ERROR_MESSAGES['state_error'].format(reason=f"state manager missing visibility for metric '{metric_key}'"))
                return False
            
            # Get visibility variable for metric
            visibility_var = state_manager.visibility.get(metric_key)
            if visibility_var is None:
                self.logger.warn(self.config.ERROR_MESSAGES['not_found'].format(resource="Visibility variable", name=metric_key))
                return False
            
            # Check if it's a proper tkinter variable
            if not hasattr(visibility_var, 'get'):
                self.logger.warn(self.config.ERROR_MESSAGES['state_error'].format(reason=f"visibility variable for '{metric_key}' is not a tkinter variable"))
                return False
            
            try:
                return visibility_var.get()
            except Exception as e:
                self.logger.warn(self.config.ERROR_MESSAGES['state_error'].format(reason=f"failed to check visibility for metric '{metric_key}': {e}"))
                return False
            
        except (AttributeError, KeyError, TypeError) as e:
            self.logger.warn(self.config.ERROR_MESSAGES['state_error'].format(reason=f"failed to check visibility for metric '{metric_key}': {e}"))
            return False
    
    def get_metric_visibility_var(self, state_manager: Any, metric_key: str) -> tk.BooleanVar:
        """Safely get metric visibility variable with fallback.
        
        Args:
            state_manager: Application state manager instance
            metric_key: Metric key to get variable for
            
        Returns:
            tk.BooleanVar: Visibility variable (may be default if not found)
        """
        try:
            if hasattr(state_manager, 'visibility') and isinstance(state_manager.visibility, dict) and metric_key in state_manager.visibility:
                return state_manager.visibility[metric_key]
        except (AttributeError, KeyError):
            pass
        
        # Return default BooleanVar if not found
        self.logger.warn(self.config.ERROR_MESSAGES['not_found'].format(resource="Visibility variable", name=metric_key))
        return tk.BooleanVar()
    
    def get_visible_metrics(self, state_manager: Any) -> List[str]:
        """Get list of currently visible metric keys.
        
        Consolidates the different implementations into one reliable method.
        
        Args:
            state_manager: Application state manager instance
            
        Returns:
            List[str]: List of metric keys that are currently visible
        """
        visible_metrics = []
        
        try:
            if not hasattr(state_manager, 'visibility') or not isinstance(state_manager.visibility, dict):
                self.logger.warn(self.config.ERROR_MESSAGES['state_error'].format(reason="state manager missing visibility attribute"))
                return visible_metrics
            
            for metric_key, visibility_var in state_manager.visibility.items():
                if self.is_metric_visible(state_manager, metric_key):
                    visible_metrics.append(metric_key)
            
        except Exception as e:
            self.logger.warn(self.config.ERROR_MESSAGES['state_error'].format(reason=f"failed to get visible metrics: {e}"))
        
        return visible_metrics
    
    def set_metric_visibility(self, state_manager: Any, metric_key: str, visible: bool) -> bool:
        """Safely set metric visibility.
        
        Args:
            state_manager: Application state manager instance
            metric_key: Metric key to set visibility for
            visible: Visibility state to set
            
        Returns:
            bool: True if successfully set, False otherwise
        """
        if not hasattr(state_manager, 'visibility') or not isinstance(state_manager.visibility, dict):
            self.logger.warn(self.config.ERROR_MESSAGES['state_error'].format(reason=f"state manager missing visibility for metric '{metric_key}'"))
            return False

        try:
            visibility_var = self.get_metric_visibility_var(state_manager, metric_key)
            visibility_var.set(visible)
            return True
        except Exception as e:
            self.logger.warn(self.config.ERROR_MESSAGES['state_error'].format(reason=f"failed to set visibility for metric '{metric_key}': {e}"))
            return False
    
    def set_all_metrics_visibility(self, state_manager: Any, visible: bool) -> int:
        """Set visibility for all metrics.
        
        Args:
            state_manager: Application state manager instance
            visible: Visibility state to set for all metrics
            
        Returns:
            int: Number of metrics successfully updated
        """
        updated_count = 0
        
        try:
            if not hasattr(state_manager, 'visibility') or not isinstance(state_manager.visibility, dict):
                self.logger.warn(self.config.ERROR_MESSAGES['state_error'].format(reason="state manager missing visibility attribute"))
                return updated_count
            
            for metric_key in state_manager.visibility.keys():
                if self.set_metric_visibility(state_manager, metric_key, visible):
                    updated_count += 1
            
        except Exception as e:
            self.logger.warn(self.config.ERROR_MESSAGES['state_error'].format(reason=f"failed to set all metrics visibility: {e}"))
        
        return updated_count