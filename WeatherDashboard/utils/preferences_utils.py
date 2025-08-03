"""
User Preferences Service

Manages user preferences persistence between application sessions.
Handles saving and loading of user settings including visible metrics,
unit system, chart configuration, scheduler state, and recent city.

This module provides a centralized preferences system that integrates
with the state manager and scheduler to maintain user settings across
application restarts.
"""

import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, Any, Optional

from WeatherDashboard import config

from .logger import Logger


@dataclass
class UserPreferences:
    """Type-safe container for user preferences.
    
    Encapsulates all user-configurable settings that should persist
    between application sessions. Provides validation and default
    value handling for preference management.
    
    Attributes:
        city: Most recently used city name
        unit_system: User's preferred unit system (metric/imperial)
        chart_days: Number of days for chart display
        visible_metrics: Dictionary of metric visibility settings
        scheduler_enabled: Whether automatic data collection is enabled
        last_updated: Timestamp of last preferences update
    """
    city: str
    unit_system: str
    chart_days: int
    visible_metrics: Dict[str, bool]
    scheduler_enabled: bool
    last_updated: datetime = datetime.now()
    # LIGHT METADATA FIELDS
    preferences_version: str = "1.0"  # For future schema migrations
    total_metrics_visible: Optional[int] = None  # Count of visible metrics
    last_session_duration: Optional[int] = None  # Session duration in seconds
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert preferences to dictionary for JSON serialization.
        
        Returns:
            Dict[str, Any]: Dictionary representation of preferences
        """
        return {
            'city': self.city,
            'unit_system': self.unit_system,
            'chart_days': self.chart_days,
            'visible_metrics': self.visible_metrics,
            'scheduler_enabled': self.scheduler_enabled,
            'last_updated': self.last_updated.isoformat(),
            # LIGHT METADATA FIELDS
            'preferences_version': self.preferences_version,
            'total_metrics_visible': self.total_metrics_visible,
            'last_session_duration': self.last_session_duration
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserPreferences':
        """Create preferences from dictionary.
        
        Args:
            data: Dictionary containing preference data
            
        Returns:
            UserPreferences: Preferences object created from data
            
        Raises:
            ValueError: If required fields are missing or invalid
        """
        try:
            return cls(
                city=data.get('city', config.DEFAULTS['city']),
                unit_system=data.get('unit_system', config.DEFAULTS['unit']),
                chart_days=data.get('chart_days', 7),
                visible_metrics=data.get('visible_metrics', {}),
                scheduler_enabled=data.get('scheduler_enabled', config.SCHEDULER['enabled']),
                last_updated=datetime.fromisoformat(data.get('last_updated', datetime.now().isoformat())),
                # LIGHT METADATA FIELDS
                preferences_version=data.get('preferences_version', '1.0'),
                total_metrics_visible=data.get('total_metrics_visible'),
                last_session_duration=data.get('last_session_duration')
            )
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid preferences data: {e}")


class PreferencesService:
    """Service for managing user preferences persistence.
    
    Handles saving and loading of user preferences to/from JSON files.
    Provides validation, default value handling, and error recovery
    for preference management operations.
    
    Attributes:
        logger: Logger instance for operation logging
        config: Configuration instance for default values
        preferences_file: Path to preferences JSON file
    """
    
    def __init__(self, preferences_file: Optional[str] = None) -> None:
        """Initialize the preferences service.
        
        Args:
            preferences_file: Optional custom path for preferences file.
                           Defaults to data/user_preferences.json
        """
        # Direct imports for stable utilities
        self.logger = Logger()
        self.config = config
        
        # Set preferences file path
        if preferences_file:
            self.preferences_file = Path(preferences_file)
        else:
            self.preferences_file = Path(config.OUTPUT['data_dir']) / 'user_preferences.json'
        
        # Ensure data directory exists
        self.preferences_file.parent.mkdir(parents=True, exist_ok=True)
    
    def save_preferences(self, preferences: UserPreferences) -> bool:
        """Save user preferences to JSON file.
        
        Args:
            preferences: UserPreferences object to save
            
        Returns:
            bool: True if save was successful, False otherwise
            
        Side Effects:
            Creates or overwrites preferences JSON file
        """
        try:
            # Convert to dictionary and save as JSON
            preferences_data = preferences.to_dict()
            
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(preferences_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Preferences saved")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save preferences: {e}")
            return False
    
    def load_preferences(self) -> UserPreferences:
        """Load user preferences from JSON file.
        
        Returns:
            UserPreferences: Loaded preferences object
            
        Raises:
            FileNotFoundError: If preferences file doesn't exist
            ValueError: If preferences file is invalid
            
        Side Effects:
            Creates default preferences file if none exists
        """
        try:
            # Check if preferences file exists
            if not self.preferences_file.exists():
                self.logger.info("No preferences file found, creating default preferences")
                default_preferences = self._create_default_preferences()
                self.save_preferences(default_preferences)
                return default_preferences
            
            # Load preferences from file
            with open(self.preferences_file, 'r', encoding='utf-8') as f:
                preferences_data = json.load(f)
            
            preferences = UserPreferences.from_dict(preferences_data)
            self.logger.info(f"Preferences loaded from {self.preferences_file}")
            return preferences
            
        except (json.JSONDecodeError, ValueError) as e:
            self.logger.error(f"Invalid preferences file: {e}")
            # Create backup of corrupted file
            backup_file = self.preferences_file.with_suffix('.json.bak')
            if self.preferences_file.exists():
                self.preferences_file.rename(backup_file)
                self.logger.info(f"Corrupted preferences backed up to {backup_file}")
            
            # Return default preferences
            default_preferences = self._create_default_preferences()
            self.save_preferences(default_preferences)
            return default_preferences
            
        except Exception as e:
            self.logger.error(f"Failed to load preferences: {e}")
            return self._create_default_preferences()
    
    def _create_default_preferences(self) -> UserPreferences:
        """Create default preferences based on configuration.
        
        Returns:
            UserPreferences: Default preferences object
        """
        # Create default visibility settings from config
        default_visibility = {}
        for metric_key, metric_data in self.config.METRICS.items():
            default_visibility[metric_key] = metric_data.get('visible', False)

        # Calculate total visible metrics
        total_visible = sum(1 for is_visible in default_visibility.values() if is_visible)
        
        return UserPreferences(
            city=self.config.DEFAULTS['city'],
            unit_system=self.config.DEFAULTS['unit'],
            chart_days=7,  # Default to 7 days
            visible_metrics=default_visibility,
            scheduler_enabled=self.config.SCHEDULER['enabled'],
            # LIGHT METADATA FIELDS
            preferences_version="1.0",
            total_metrics_visible=total_visible,
            last_session_duration=None
        )
    
    def update_preferences_from_state(self, state: Any, scheduler_enabled: bool) -> UserPreferences:
        """Create preferences object from current application state.
        
        Args:
            state: Application state manager
            scheduler_enabled: Current scheduler enabled state
            
        Returns:
            UserPreferences: Preferences object created from current state
        """
        # Get current visibility settings
        visible_metrics = {}
        for metric_key in self.config.METRICS.keys():
            visible_metrics[metric_key] = state.is_metric_visible(metric_key)
        
        # Get chart days from range setting
        chart_range = state.get_current_range()
        chart_days = self.config.CHART['range_options'].get(chart_range, 7)

        # Calculate total visible metrics
        total_visible = sum(1 for is_visible in visible_metrics.values() if is_visible)
        
        return UserPreferences(
            city=state.get_current_city(),
            unit_system=state.get_current_unit_system(),
            chart_days=chart_days,
            visible_metrics=visible_metrics,
            scheduler_enabled=scheduler_enabled,
            # LIGHT METADATA FIELDS
            preferences_version="1.0",
            total_metrics_visible=total_visible,
            last_session_duration=None  # Could be calculated from session start time
        )
    
    def apply_preferences_to_state(self, preferences: UserPreferences, state: Any) -> None:
        """Apply loaded preferences to application state.
        
        Args:
            preferences: UserPreferences object to apply
            state: Application state manager to update
            
        Side Effects:
            Updates state manager with loaded preferences
        """
        try:
            # Apply city and unit system
            state.city.set(preferences.city)
            state.unit.set(preferences.unit_system)
            
            # Apply chart range (convert days back to range string)
            chart_days = preferences.chart_days
            chart_range = "Last 7 Days"  # Default
            for range_name, days in self.config.CHART['range_options'].items():
                if days == chart_days:
                    chart_range = range_name
                    break
            state.range.set(chart_range)
            
            # Apply visibility settings
            for metric_key, is_visible in preferences.visible_metrics.items():
                if metric_key in state.visibility:
                    state.visibility[metric_key].set(is_visible)
            
            self.logger.info("Preferences applied to application state")
            
        except Exception as e:
            self.logger.error(f"Failed to apply preferences to state: {e}")
    
    def get_preferences_file_path(self) -> Path:
        """Get the path to the preferences file.
        
        Returns:
            Path: Path to preferences JSON file
        """
        return self.preferences_file