"""
Weather Data Collection Scheduler

Automatically collects weather data at configurable intervals to support
24/7 weather monitoring and historical data building. Integrates with
history service for data storage and memory management.
"""

from typing import Dict, Any
from datetime import datetime, timedelta
import threading
import time

from WeatherDashboard import config
from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.core.view_models import WeatherViewModel
from WeatherDashboard.services.weather_service import WeatherAPIService

from .history_service import WeatherHistoryService


class WeatherDataScheduler:
    """Manages automatic weather data collection for 24/7 monitoring.
    
    Provides scheduled data collection for both default and display cities,
    with error handling, status tracking, and UI integration.
    
    Attributes:
        history_service: Service for data storage and retrieval
        data_manager: Service for data fetching and processing
        state_manager: Application state manager
        ui_handler: UI update handler
        enabled: Whether scheduler is currently enabled
        is_running: Whether scheduler thread is active
        next_fetch_time: Timestamp of next scheduled fetch
        error_counts: Track consecutive errors per city
    """
    
    def __init__(self, history_service: WeatherHistoryService, data_manager: Any,
                 state_manager: Any, ui_handler: Any):
        """Initialize the weather data scheduler.
        
        Args:
            history_service: Service for data storage and retrieval
            data_manager: Service for data fetching and processing
            state_manager: Application state manager for current city/unit info
            ui_handler: UI update handler for display updates
        """
        # Direct imports for stable utilities
        self.logger = Logger()
        self.config = config
        self.datetime = datetime
        
        # Injected dependencies for testable components
        self.history_service = history_service
        self.data_manager = data_manager
        self.state_manager = state_manager
        self.ui_handler = ui_handler
        
        # Scheduler state
        self.enabled = self.config.SCHEDULER["enabled"]
        self.interval_minutes = self.config.SCHEDULER["default_interval_minutes"]
        self.default_city = self.config.DEFAULTS["city"]
        self.error_threshold = self.config.SCHEDULER["error_threshold"]
        self.retry_attempts = self.config.SCHEDULER["retry_attempts"]
        self.retry_delay_seconds = self.config.SCHEDULER["retry_delay_seconds"]
        self.quiet_hours = self.config.SCHEDULER["quiet_hours"]
        
        # Threading
        self.scheduler_thread = None
        self.stop_event = threading.Event()
        self.is_running = False
        
        # Status tracking
        self.next_fetch_time = None
        self.error_counts = {}
        self.last_fetch_time = None
        self.fetch_count = 0

    def start_scheduler(self) -> None:
        """Start the automatic data collection scheduler."""
        if self.is_running:
            return
            
        self.enabled = True
        self.stop_event.clear()
        self.is_running = True

        # Set initial next fetch time if not already set
        if not self.next_fetch_time:
            self.next_fetch_time = self.datetime.now() + timedelta(minutes=self.interval_minutes)
        
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        
        # Start countdown update timer
        self._start_countdown_timer()
        
        self.logger.info("Weather data scheduler started")
        self._update_status_display()

    def stop_scheduler(self) -> None:
        """Stop the automatic data collection scheduler."""
        self.enabled = False
        self.stop_event.set()
        self.is_running = False
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        # Stop countdown timer
        self._stop_countdown_timer()
        
        self.logger.info("Weather data scheduler stopped")
        self._update_status_display()

    def toggle_scheduler(self) -> None:
        """Toggle scheduler on/off."""
        if self.enabled:
            self.stop_scheduler()
        else:
            # Preserve the next fetch time when restarting
            if not self.next_fetch_time:
                self.next_fetch_time = self.datetime.now() + timedelta(minutes=self.interval_minutes)
            self.start_scheduler()

    def _start_countdown_timer(self) -> None:
        """Start a timer to update countdown every second."""
        def update_countdown():
            if self.enabled and self.is_running and hasattr(self.ui_handler, 'root'):
                self._update_status_display()
                # Schedule next update in 1 second
                self.ui_handler.root.after(1000, update_countdown)
        
        # Start the countdown updates
        if hasattr(self.ui_handler, 'root'):
            self.ui_handler.root.after(1000, update_countdown)

    def _stop_countdown_timer(self) -> None:
        """Stop the countdown update timer."""
        # No need to cancel anything - tkinter's after() will stop when window closes
        pass

    def _scheduler_loop(self) -> None:
        """Main scheduler loop - runs every interval."""
        # Wait for the first interval before starting data collection
        self.stop_event.wait(self.interval_minutes * 60)

        while not self.stop_event.is_set():
            try:
                self._collect_data_for_scheduled_cities()
                self.last_fetch_time = self.datetime.now()
                self.fetch_count += 1
                
                # Trigger memory cleanup after data collection
                self.history_service.cleanup_old_data()
                
                # Calculate next fetch time
                self.next_fetch_time = self.last_fetch_time + timedelta(minutes=self.interval_minutes)
                self._update_status_display()
                
                # Wait for next interval
                self.stop_event.wait(self.interval_minutes * 60)
                
            except Exception as e:
                self.logger.error(f"Scheduler error: {e}")
                # Wait shorter time on error, then retry
                self.stop_event.wait(60)  # 1 minute

    def _collect_data_for_scheduled_cities(self) -> None:
        """Collect data for both default and display cities."""
        cities_to_fetch = set()
        
        # Always fetch default city
        cities_to_fetch.add(self.default_city)
        
        # Add display city if different from default
        current_display_city = self.state_manager.city.get()

        if current_display_city != self.default_city:
            cities_to_fetch.add(current_display_city)
        
        # Fetch data sequentially
        for city in cities_to_fetch:
            self._fetch_city_data(city, update_display=(city == current_display_city))

    def _fetch_city_data(self, city: str, update_display: bool = False) -> None:
        """Fetch data for a single city."""
        try:
            # Use existing data_manager.fetch_current logic
            weather_data = self.data_manager.fetch_current(
                city, 
                self.state_manager.unit.get()
            )
            
            if update_display:
                # Update UI for display city
                view_model = WeatherViewModel(city, weather_data, self.state_manager.unit.get())
                self.ui_handler.update_display(view_model, None, False)
                
        except Exception as e:
            self._handle_fetch_error(city, e)

    def _handle_fetch_error(self, city: str, error: Exception) -> None:
        """Handle fetch errors with threshold-based notifications."""
        error_key = f"{city}_errors"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        
        # Log silently
        self.logger.warn(f"Auto-fetch failed for {city}: {error}")
        
        # Check threshold
        if self.error_counts[error_key] >= self.error_threshold:
            self._show_error_notification(city, error)
            self.error_counts[error_key] = 0  # Reset counter

    def _show_error_notification(self, city: str, error: Exception) -> None:
        """Show error notification when threshold is reached."""
        error_msg = f"Auto-fetch failed {self.error_threshold} times for {city}: {error}"
        self.logger.error(error_msg)
        # Could add UI notification here later

    def handle_manual_update(self, city: str) -> None:
        """Handle manual update button click - adds extra data point."""
        if not self.enabled:
            return  # Scheduler disabled, just do normal manual update
            
        # Fetch data for display city only
        self._fetch_city_data(city, update_display=True)
        # Don't interrupt the scheduler - it continues on its interval

    def _update_status_display(self) -> None:
        """Update scheduler status in UI."""
        if hasattr(self.ui_handler, 'update_scheduler_status'):
            status_info = {
                'enabled': self.enabled,
                'is_running': self.is_running,
                'next_fetch_time': self.next_fetch_time,
                'last_fetch_time': self.last_fetch_time,
                'fetch_count': self.fetch_count,
                'interval_minutes': self.interval_minutes
            }
            self.ui_handler.update_scheduler_status(status_info)

    def get_status_info(self) -> Dict[str, Any]:
        """Get current scheduler status for UI display."""
        return {
            'enabled': self.enabled,
            'is_running': self.is_running,
            'next_fetch_time': self.next_fetch_time,
            'last_fetch_time': self.last_fetch_time,
            'fetch_count': self.fetch_count,
            'interval_minutes': self.interval_minutes,
            'default_city': self.default_city,
            'current_display_city': self.state_manager.city.get()
        }