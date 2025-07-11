"""
Rate limiting utility for API requests.

This module provides rate limiting functionality to prevent excessive API
requests and ensure compliance with service rate limits. Implements
time-based request tracking and configurable rate limiting thresholds.

Classes:
    RateLimiter: Time-based rate limiting for API requests
"""

from datetime import datetime

class RateLimiter:
    """Handle rate limiting for API requests.
    
    Implements time-based rate limiting to prevent excessive API calls.
    Tracks the last request time and enforces minimum intervals between requests.
    
    Attributes:
        min_interval: Minimum seconds required between requests
        last_request_time: Timestamp of the last recorded request
    """
    def __init__(self, min_interval_seconds: int = 3) -> None:
        """Initialize the rate limiter.
        
        Args:
            min_interval_seconds: Minimum seconds required between requests (default 3)
        """
        self.min_interval = min_interval_seconds
        self.last_request_time = None
    
    def can_make_request(self) -> bool:
        """Check if enough time has passed since the last request."""
        if not self.last_request_time:
            return True
        return (datetime.now() - self.last_request_time).total_seconds() > self.min_interval
    
    def record_request(self) -> None:
        """Record that a request was made at this time."""
        self.last_request_time = datetime.now()
    
    def get_wait_time(self) -> float:
        """Get seconds to wait before next request, or 0 if ready.
        
        Returns:
            float: Number of seconds to wait before making next request,
                   or 0 if request can be made immediately
        """
        if not self.last_request_time:
            return 0
        elapsed = (datetime.now() - self.last_request_time).total_seconds()
        return max(0, self.min_interval - elapsed)