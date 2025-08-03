"""
Unit tests for WeatherDashboard.utils.rate_limiter module.

Tests rate limiting functionality including:
- Request tracking and limiting
- Time-based rate limiting
- Error handling and edge cases
- Performance characteristics
"""

import unittest
import time
from unittest.mock import Mock, patch

# Add project root to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WeatherDashboard.utils.rate_limiter import RateLimiter


class TestRateLimiter(unittest.TestCase):
    """Test RateLimiter functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.rate_limiter = RateLimiter(min_interval_seconds=1)

    def test_initialization(self):
        """Test rate limiter initialization."""
        self.assertEqual(self.rate_limiter.min_interval, 1)
        self.assertIsNone(self.rate_limiter.last_request_time)

    def test_can_make_request_initial(self):
        """Test can_make_request when no requests have been made."""
        self.assertTrue(self.rate_limiter.can_make_request())
    
    def test_can_make_request_after_interval(self):
        """Test can_make_request after the minimum interval has passed."""
        # Record a request
        self.rate_limiter.record_request()
        
        # Should be blocked initially
        self.assertFalse(self.rate_limiter.can_make_request())
        
        # Wait for interval to pass
        time.sleep(1.1)
        
        # Should be allowed now
        self.assertTrue(self.rate_limiter.can_make_request())
    
    def test_can_make_request_before_interval(self):
        """Test can_make_request before the minimum interval has passed."""
        # Record a request
        self.rate_limiter.record_request()
        
        # Should be blocked
        self.assertFalse(self.rate_limiter.can_make_request())

    def test_record_request(self):
        """Test record_request functionality."""
        # Initially no request time
        self.assertIsNone(self.rate_limiter.last_request_time)
        
        # Record a request
        self.rate_limiter.record_request()
        
        # Should have recorded the time
        self.assertIsNotNone(self.rate_limiter.last_request_time)

    def test_get_wait_time(self):
        """Test get_wait_time functionality."""
        # Initially no wait time
        self.assertEqual(self.rate_limiter.get_wait_time(), 0.0)
        
        # Record a request
        self.rate_limiter.record_request()
        
        # Should have wait time
        wait_time = self.rate_limiter.get_wait_time()
        self.assertGreater(wait_time, 0.0)
        self.assertLessEqual(wait_time, 1.0)
        
        # Wait for interval to pass
        time.sleep(1.1)
        
        # Should have no wait time
        self.assertEqual(self.rate_limiter.get_wait_time(), 0.0)

    def test_different_intervals(self):
        """Test rate limiter with different intervals."""
        # Test with 2 second interval
        limiter_2sec = RateLimiter(min_interval_seconds=2)
        
        limiter_2sec.record_request()
        self.assertFalse(limiter_2sec.can_make_request())
        
        # Wait 1 second (not enough)
        time.sleep(1.0)
        self.assertFalse(limiter_2sec.can_make_request())
        
        # Wait another 1.1 seconds (total 2.1, should be enough)
        time.sleep(1.1)
        self.assertTrue(limiter_2sec.can_make_request())

    def test_zero_interval(self):
        """Test rate limiter with zero interval."""
        limiter_zero = RateLimiter(min_interval_seconds=0)
        
        limiter_zero.record_request()
        # Should always be able to make request with zero interval
        self.assertTrue(limiter_zero.can_make_request())

    def test_negative_interval(self):
        """Test rate limiter with negative interval."""
        limiter_negative = RateLimiter(min_interval_seconds=-1)
        
        limiter_negative.record_request()
        # Should always be able to make request with negative interval
        self.assertTrue(limiter_negative.can_make_request())

    def test_concurrent_access(self):
        """Test rate limiter with concurrent access."""
        import threading
        
        results = []
        errors = []
        
        def worker():
            try:
                for _ in range(10):
                    if self.rate_limiter.can_make_request():
                        self.rate_limiter.record_request()
                        results.append(True)
                    else:
                        results.append(False)
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify no errors occurred
        self.assertEqual(len(errors), 0)
        
        # Verify we got some results
        self.assertGreater(len(results), 0)

    def test_performance(self):
        """Test rate limiter performance."""
        import time
        
        start_time = time.time()
        
        # Perform many operations
        for _ in range(1000):
            self.rate_limiter.can_make_request()
            self.rate_limiter.record_request()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete 2000 operations in reasonable time
        self.assertLess(execution_time, 1.0)

    def test_memory_usage(self):
        """Test rate limiter memory usage."""
        import gc
        
        initial_objects = len(gc.get_objects())
        
        # Create many rate limiters
        limiters = []
        for _ in range(100):
            limiter = RateLimiter(min_interval_seconds=1)
            for _ in range(10):
                limiter.record_request()
            limiters.append(limiter)
        
        # Force garbage collection
        gc.collect()
        
        final_objects = len(gc.get_objects())
        
        # Memory usage should not increase significantly
        self.assertLess(abs(final_objects - initial_objects), 2000)

    def test_documentation(self):
        """Test that rate limiter has proper documentation."""
        # Test that class and methods exist
        self.assertTrue(hasattr(self.rate_limiter, 'can_make_request'))
        self.assertTrue(hasattr(self.rate_limiter, 'record_request'))
        self.assertTrue(hasattr(self.rate_limiter, 'get_wait_time'))
        
        # Test that methods are callable
        self.assertTrue(callable(self.rate_limiter.can_make_request))
        self.assertTrue(callable(self.rate_limiter.record_request))
        self.assertTrue(callable(self.rate_limiter.get_wait_time))
        
        # Test that class has docstring
        self.assertIsNotNone(RateLimiter.__doc__)


if __name__ == '__main__':
    unittest.main() 