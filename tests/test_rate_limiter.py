"""
Comprehensive test suite for WeatherDashboard.utils.rate_limiter module.

Tests the RateLimiter class functionality, time-based rate limiting,
request tracking, and edge cases for API request rate limiting.
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import time
import datetime
from datetime import datetime, timedelta

# Import the module to test
from WeatherDashboard.utils.rate_limiter import RateLimiter


class TestRateLimiterInitialization(unittest.TestCase):
    """Test RateLimiter class initialization and basic properties."""
    
    def test_rate_limiter_initialization_default(self):
        """Test RateLimiter initialization with default parameters."""
        limiter = RateLimiter()
        
        self.assertEqual(limiter.min_interval, 3)
        self.assertIsNone(limiter.last_request_time)
        self.assertIsInstance(limiter.datetime, type(datetime))
    
    def test_rate_limiter_initialization_custom_interval(self):
        """Test RateLimiter initialization with custom interval."""
        limiter = RateLimiter(min_interval_seconds=5)
        
        self.assertEqual(limiter.min_interval, 5)
        self.assertIsNone(limiter.last_request_time)
    
    def test_rate_limiter_initialization_zero_interval(self):
        """Test RateLimiter initialization with zero interval."""
        limiter = RateLimiter(min_interval_seconds=0)
        
        self.assertEqual(limiter.min_interval, 0)
        self.assertIsNone(limiter.last_request_time)
    
    def test_rate_limiter_initialization_negative_interval(self):
        """Test RateLimiter initialization with negative interval."""
        limiter = RateLimiter(min_interval_seconds=-1)
        
        self.assertEqual(limiter.min_interval, -1)
        self.assertIsNone(limiter.last_request_time)
    
    def test_rate_limiter_attributes_exist(self):
        """Test that RateLimiter has required attributes."""
        limiter = RateLimiter()
        
        self.assertTrue(hasattr(limiter, 'min_interval'))
        self.assertTrue(hasattr(limiter, 'last_request_time'))
        self.assertTrue(hasattr(limiter, 'datetime'))
    
    def test_rate_limiter_methods_exist(self):
        """Test that RateLimiter has required methods."""
        limiter = RateLimiter()
        
        self.assertTrue(hasattr(limiter, 'can_make_request'))
        self.assertTrue(hasattr(limiter, 'record_request'))
        self.assertTrue(hasattr(limiter, 'get_wait_time'))
        
        self.assertTrue(callable(limiter.can_make_request))
        self.assertTrue(callable(limiter.record_request))
        self.assertTrue(callable(limiter.get_wait_time))


class TestRateLimiterCanMakeRequest(unittest.TestCase):
    """Test the can_make_request method functionality."""
    
    def test_can_make_request_first_request(self):
        """Test can_make_request when no previous request has been made."""
        limiter = RateLimiter(min_interval_seconds=3)
        
        self.assertTrue(limiter.can_make_request())
    
    def test_can_make_request_after_interval(self):
        """Test can_make_request after the minimum interval has passed."""
        limiter = RateLimiter(min_interval_seconds=1)
        
        # Record a request
        limiter.record_request()
        
        # Wait for interval to pass
        time.sleep(1.1)
        
        self.assertTrue(limiter.can_make_request())
    
    def test_can_make_request_before_interval(self):
        """Test can_make_request before the minimum interval has passed."""
        limiter = RateLimiter(min_interval_seconds=2)
        
        # Record a request
        limiter.record_request()
        
        # Try immediately after
        self.assertFalse(limiter.can_make_request())
    
    def test_can_make_request_exactly_at_interval(self):
        """Test can_make_request exactly at the minimum interval."""
        limiter = RateLimiter(min_interval_seconds=1)
        
        # Record a request
        limiter.record_request()
        
        # Wait exactly the interval
        time.sleep(1.0)
        
        # Should be able to make request at exactly the interval
        self.assertTrue(limiter.can_make_request())
    
    def test_can_make_request_zero_interval(self):
        """Test can_make_request with zero interval."""
        limiter = RateLimiter(min_interval_seconds=0)
        
        # Record a request
        limiter.record_request()
        
        # Should always be able to make request with zero interval
        self.assertTrue(limiter.can_make_request())
    
    def test_can_make_request_negative_interval(self):
        """Test can_make_request with negative interval."""
        limiter = RateLimiter(min_interval_seconds=-1)
        
        # Record a request
        limiter.record_request()
        
        # Should always be able to make request with negative interval
        self.assertTrue(limiter.can_make_request())


class TestRateLimiterRecordRequest(unittest.TestCase):
    """Test the record_request method functionality."""
    
    def test_record_request_sets_timestamp(self):
        """Test that record_request sets the last_request_time."""
        limiter = RateLimiter()
        
        # Before recording
        self.assertIsNone(limiter.last_request_time)
        
        # Record request
        limiter.record_request()
        
        # After recording
        self.assertIsNotNone(limiter.last_request_time)
        self.assertIsInstance(limiter.last_request_time, datetime)
    
    def test_record_request_updates_timestamp(self):
        """Test that record_request updates the last_request_time."""
        limiter = RateLimiter()
        
        # Record first request
        limiter.record_request()
        first_time = limiter.last_request_time
        
        # Wait a bit
        time.sleep(0.1)
        
        # Record second request
        limiter.record_request()
        second_time = limiter.last_request_time
        
        # Should be different timestamps
        self.assertNotEqual(first_time, second_time)
        self.assertGreater(second_time, first_time)
    
    def test_record_request_multiple_calls(self):
        """Test multiple calls to record_request."""
        limiter = RateLimiter()
        
        # Record multiple requests
        for i in range(5):
            limiter.record_request()
            time.sleep(0.01)  # Small delay
        
        # Should have recorded the last request
        self.assertIsNotNone(limiter.last_request_time)
    
    @patch('WeatherDashboard.utils.rate_limiter.datetime')
    def test_record_request_uses_mocked_datetime(self, mock_datetime):
        """Test that record_request uses the mocked datetime."""
        mock_now = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        
        limiter = RateLimiter()
        limiter.record_request()
        
        self.assertEqual(limiter.last_request_time, mock_now)
        mock_datetime.now.assert_called_once()


class TestRateLimiterGetWaitTime(unittest.TestCase):
    """Test the get_wait_time method functionality."""
    
    def test_get_wait_time_no_previous_request(self):
        """Test get_wait_time when no previous request has been made."""
        limiter = RateLimiter(min_interval_seconds=3)
        
        wait_time = limiter.get_wait_time()
        
        self.assertEqual(wait_time, 0.0)
    
    def test_get_wait_time_after_interval(self):
        """Test get_wait_time after the minimum interval has passed."""
        limiter = RateLimiter(min_interval_seconds=1)
        
        # Record a request
        limiter.record_request()
        
        # Wait for interval to pass
        time.sleep(1.1)
        
        wait_time = limiter.get_wait_time()
        
        self.assertEqual(wait_time, 0.0)
    
    def test_get_wait_time_before_interval(self):
        """Test get_wait_time before the minimum interval has passed."""
        limiter = RateLimiter(min_interval_seconds=2)
        
        # Record a request
        limiter.record_request()
        
        # Try immediately after
        wait_time = limiter.get_wait_time()
        
        self.assertGreater(wait_time, 0.0)
        self.assertLessEqual(wait_time, 2.0)
    
    def test_get_wait_time_exactly_at_interval(self):
        """Test get_wait_time exactly at the minimum interval."""
        limiter = RateLimiter(min_interval_seconds=1)
        
        # Record a request
        limiter.record_request()
        
        # Wait exactly the interval
        time.sleep(1.0)
        
        wait_time = limiter.get_wait_time()
        
        # Should be 0 or very close to 0
        self.assertLessEqual(wait_time, 0.1)
    
    def test_get_wait_time_zero_interval(self):
        """Test get_wait_time with zero interval."""
        limiter = RateLimiter(min_interval_seconds=0)
        
        # Record a request
        limiter.record_request()
        
        wait_time = limiter.get_wait_time()
        
        self.assertEqual(wait_time, 0.0)
    
    def test_get_wait_time_negative_interval(self):
        """Test get_wait_time with negative interval."""
        limiter = RateLimiter(min_interval_seconds=-1)
        
        # Record a request
        limiter.record_request()
        
        wait_time = limiter.get_wait_time()
        
        self.assertEqual(wait_time, 0.0)
    
    def test_get_wait_time_decreasing_over_time(self):
        """Test that get_wait_time decreases over time."""
        limiter = RateLimiter(min_interval_seconds=2)
        
        # Record a request
        limiter.record_request()
        
        # Check wait time immediately
        initial_wait = limiter.get_wait_time()
        self.assertGreater(initial_wait, 0.0)
        
        # Wait a bit and check again
        time.sleep(0.5)
        later_wait = limiter.get_wait_time()
        
        self.assertLess(later_wait, initial_wait)
        self.assertGreater(later_wait, 0.0)


class TestRateLimiterIntegration(unittest.TestCase):
    """Test integration between RateLimiter methods."""
    
    def test_full_request_cycle(self):
        """Test a complete request cycle with rate limiting."""
        limiter = RateLimiter(min_interval_seconds=1)
        
        # First request should be allowed
        self.assertTrue(limiter.can_make_request())
        limiter.record_request()
        
        # Second request should be blocked
        self.assertFalse(limiter.can_make_request())
        wait_time = limiter.get_wait_time()
        self.assertGreater(wait_time, 0.0)
        
        # Wait for interval to pass
        time.sleep(1.1)
        
        # Third request should be allowed again
        self.assertTrue(limiter.can_make_request())
        wait_time = limiter.get_wait_time()
        self.assertEqual(wait_time, 0.0)
    
    def test_multiple_request_cycles(self):
        """Test multiple request cycles."""
        limiter = RateLimiter(min_interval_seconds=0.5)
        
        for cycle in range(3):
            # Request should be allowed
            self.assertTrue(limiter.can_make_request())
            limiter.record_request()
            
            # Request should be blocked
            self.assertFalse(limiter.can_make_request())
            
            # Wait for interval
            time.sleep(0.6)
    
    def test_concurrent_access_simulation(self):
        """Test rate limiter behavior under simulated concurrent access."""
        limiter = RateLimiter(min_interval_seconds=1)
        
        # Simulate rapid requests
        for i in range(10):
            can_request = limiter.can_make_request()
            if can_request:
                limiter.record_request()
            
            # Small delay between checks
            time.sleep(0.1)
        
        # Should have recorded some requests
        self.assertIsNotNone(limiter.last_request_time)


class TestRateLimiterEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def test_rate_limiter_with_very_large_interval(self):
        """Test rate limiter with very large interval."""
        limiter = RateLimiter(min_interval_seconds=3600)  # 1 hour
        
        # First request should be allowed
        self.assertTrue(limiter.can_make_request())
        limiter.record_request()
        
        # Second request should be blocked
        self.assertFalse(limiter.can_make_request())
        
        wait_time = limiter.get_wait_time()
        self.assertGreater(wait_time, 3500)  # Should be close to 1 hour
    
    def test_rate_limiter_with_very_small_interval(self):
        """Test rate limiter with very small interval."""
        limiter = RateLimiter(min_interval_seconds=0.001)  # 1 millisecond
        
        # First request should be allowed
        self.assertTrue(limiter.can_make_request())
        limiter.record_request()
        
        # Wait a bit longer than the interval
        time.sleep(0.002)
        
        # Should be able to make request again
        self.assertTrue(limiter.can_make_request())
    
    def test_rate_limiter_time_precision(self):
        """Test rate limiter time precision."""
        limiter = RateLimiter(min_interval_seconds=0.1)
        
        # Record request
        limiter.record_request()
        
        # Wait slightly less than interval
        time.sleep(0.09)
        
        # Should still be blocked
        self.assertFalse(limiter.can_make_request())
        
        # Wait slightly more than interval
        time.sleep(0.02)
        
        # Should be allowed
        self.assertTrue(limiter.can_make_request())
    
    def test_rate_limiter_consistent_behavior(self):
        """Test that rate limiter behavior is consistent."""
        limiter = RateLimiter(min_interval_seconds=1)
        
        # Record a request
        limiter.record_request()
        
        # Multiple calls should return same result
        can_request_1 = limiter.can_make_request()
        can_request_2 = limiter.can_make_request()
        can_request_3 = limiter.can_make_request()
        
        self.assertEqual(can_request_1, can_request_2)
        self.assertEqual(can_request_2, can_request_3)
        
        # Wait for interval
        time.sleep(1.1)
        
        # Should all be True now
        can_request_4 = limiter.can_make_request()
        can_request_5 = limiter.can_make_request()
        
        self.assertTrue(can_request_4)
        self.assertTrue(can_request_5)


class TestRateLimiterMockedTime(unittest.TestCase):
    """Test RateLimiter with mocked time for precise control."""
    
    @patch('WeatherDashboard.utils.rate_limiter.datetime')
    def test_rate_limiter_with_mocked_time(self, mock_datetime):
        """Test rate limiter with mocked datetime for precise control."""
        # Set up mock datetime
        base_time = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.now.side_effect = [
            base_time,  # First call
            base_time + timedelta(seconds=2)  # Second call
        ]
        
        limiter = RateLimiter(min_interval_seconds=1)
        
        # Apply the mock to the instance's datetime attribute
        limiter.datetime = mock_datetime
        
        # Record first request
        limiter.record_request()
        
        # Should be blocked initially
        self.assertFalse(limiter.can_make_request())
        
        # Wait time should be calculated correctly
        wait_time = limiter.get_wait_time()
        self.assertEqual(wait_time, 0.0)  # 2 seconds have passed, 1 second interval
    
    @patch('WeatherDashboard.utils.rate_limiter.datetime')
    def test_rate_limiter_precise_timing(self, mock_datetime):
        """Test rate limiter with precise timing control."""
        base_time = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.now.side_effect = [
            base_time,  # First call
            base_time + timedelta(seconds=0.5),  # Second call
            base_time + timedelta(seconds=1.0),  # Third call
            base_time + timedelta(seconds=1.5)   # Fourth call
        ]
        
        limiter = RateLimiter(min_interval_seconds=1)
        
        # Apply the mock to the instance's datetime attribute
        limiter.datetime = mock_datetime
        
        # Record request
        limiter.record_request()
        
        # Check at 0.5 seconds (should be blocked)
        self.assertFalse(limiter.can_make_request())
        
        # Check at 1.0 seconds (should be allowed)
        self.assertTrue(limiter.can_make_request())
        
        # Check at 1.5 seconds (should be allowed)
        self.assertTrue(limiter.can_make_request())


if __name__ == '__main__':
    unittest.main() 