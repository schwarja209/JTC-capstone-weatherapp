"""
Rate limiting utility for API requests.
"""

from datetime import datetime

class RateLimiter:
    '''Handles rate limiting for API requests.'''
    
    def __init__(self, min_interval_seconds=3):
        self.min_interval = min_interval_seconds
        self.last_request_time = None
    
    def can_make_request(self):
        '''Returns True if enough time has passed since the last request.'''
        if not self.last_request_time:
            return True
        return (datetime.now() - self.last_request_time).total_seconds() > self.min_interval
    
    def record_request(self):
        '''Records that a request was made at this time.'''
        self.last_request_time = datetime.now()
    
    def get_wait_time(self):
        '''Returns seconds to wait before next request, or 0 if ready.'''
        if not self.last_request_time:
            return 0
        elapsed = (datetime.now() - self.last_request_time).total_seconds()
        return max(0, self.min_interval - elapsed)