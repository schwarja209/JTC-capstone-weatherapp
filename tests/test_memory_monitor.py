"""
Memory leak detection system for WeatherDashboard test suite.

This module provides utilities for monitoring memory usage during tests
and detecting potential memory leaks in GUI components and long-running operations.
"""

import gc
import psutil
import time
import threading
from typing import Dict, List, Optional, Callable, Any
from contextlib import contextmanager
from dataclasses import dataclass, field
from unittest import TestCase
import unittest


@dataclass
class MemorySnapshot:
    """Snapshot of memory usage at a specific point in time."""
    timestamp: float
    memory_mb: float
    cpu_percent: float
    object_count: int
    gc_stats: Dict[str, Any] = field(default_factory=dict)


class MemoryMonitor:
    """Monitors memory usage and detects potential memory leaks."""
    
    def __init__(self, process_id: Optional[int] = None):
        """Initialize the memory monitor."""
        self.process_id = process_id or psutil.Process().pid
        self.process = psutil.Process(self.process_id)
        self.snapshots: List[MemorySnapshot] = []
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
    
    def take_snapshot(self) -> MemorySnapshot:
        """Take a snapshot of current memory usage."""
        try:
            memory_info = self.process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024  # Convert to MB
            cpu_percent = self.process.cpu_percent()
            
            # Get garbage collector statistics
            gc_stats = {
                'collections': gc.get_stats(),
                'counts': gc.get_count(),
                'thresholds': gc.get_threshold()
            }
            
            # Count objects (approximate)
            object_count = len(gc.get_objects())
            
            snapshot = MemorySnapshot(
                timestamp=time.time(),
                memory_mb=memory_mb,
                cpu_percent=cpu_percent,
                object_count=object_count,
                gc_stats=gc_stats
            )
            
            self.snapshots.append(snapshot)
            return snapshot
            
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Process may have ended or we don't have access
            return MemorySnapshot(
                timestamp=time.time(),
                memory_mb=0.0,
                cpu_percent=0.0,
                object_count=0
            )
    
    def start_monitoring(self, interval: float = 1.0):
        """Start continuous memory monitoring."""
        if self._monitoring:
            return
        
        self._monitoring = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self._monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous memory monitoring."""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5.0)
    
    def _monitor_loop(self, interval: float):
        """Internal monitoring loop."""
        while self._monitoring:
            self.take_snapshot()
            time.sleep(interval)
    
    def get_memory_growth(self, window_seconds: float = 60.0) -> Dict[str, float]:
        """Calculate memory growth over a time window."""
        if len(self.snapshots) < 2:
            return {'memory_growth_mb': 0.0, 'object_growth': 0}
        
        current_time = time.time()
        recent_snapshots = [
            s for s in self.snapshots 
            if current_time - s.timestamp <= window_seconds
        ]
        
        if len(recent_snapshots) < 2:
            return {'memory_growth_mb': 0.0, 'object_growth': 0}
        
        # Calculate growth rates
        memory_growth = recent_snapshots[-1].memory_mb - recent_snapshots[0].memory_mb
        object_growth = recent_snapshots[-1].object_count - recent_snapshots[0].object_count
        
        time_span = recent_snapshots[-1].timestamp - recent_snapshots[0].timestamp
        if time_span > 0:
            memory_growth_rate = memory_growth / time_span  # MB per second
            object_growth_rate = object_growth / time_span  # objects per second
        else:
            memory_growth_rate = 0.0
            object_growth_rate = 0.0
        
        return {
            'memory_growth_mb': memory_growth,
            'memory_growth_rate_mb_per_sec': memory_growth_rate,
            'object_growth': object_growth,
            'object_growth_rate_per_sec': object_growth_rate,
            'snapshots_analyzed': len(recent_snapshots)
        }
    
    def detect_memory_leak(self, threshold_mb: float = 10.0, 
                          window_seconds: float = 30.0) -> bool:
        """Detect if there's a memory leak based on growth threshold."""
        growth_data = self.get_memory_growth(window_seconds)
        return growth_data['memory_growth_mb'] > threshold_mb
    
    def force_garbage_collection(self):
        """Force garbage collection and take a snapshot."""
        gc.collect()
        return self.take_snapshot()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of memory monitoring data."""
        if not self.snapshots:
            return {'error': 'No snapshots available'}
        
        latest = self.snapshots[-1]
        growth_data = self.get_memory_growth()
        
        return {
            'current_memory_mb': latest.memory_mb,
            'current_cpu_percent': latest.cpu_percent,
            'current_object_count': latest.object_count,
            'total_snapshots': len(self.snapshots),
            'monitoring_duration_seconds': latest.timestamp - self.snapshots[0].timestamp,
            'memory_growth': growth_data,
            'peak_memory_mb': max(s.memory_mb for s in self.snapshots),
            'average_memory_mb': sum(s.memory_mb for s in self.snapshots) / len(self.snapshots)
        }


class MemoryTestMixin:
    """Mixin for test classes that need memory leak detection."""
    
    def setUp(self):
        """Set up memory monitoring for the test."""
        self.memory_monitor = MemoryMonitor()
        self.memory_monitor.take_snapshot()  # Baseline snapshot
    
    def tearDown(self):
        """Clean up memory monitoring."""
        if hasattr(self, 'memory_monitor'):
            self.memory_monitor.take_snapshot()  # Final snapshot
            self.memory_monitor.stop_monitoring()
    
    def assert_no_memory_leak(self, threshold_mb: float = 5.0, 
                             window_seconds: float = 30.0):
        """Assert that no significant memory leak occurred during the test."""
        if hasattr(self, 'memory_monitor'):
            leak_detected = self.memory_monitor.detect_memory_leak(threshold_mb, window_seconds)
            self.assertFalse(leak_detected, 
                           f"Memory leak detected: {self.memory_monitor.get_memory_growth()}")
    
    def assert_memory_usage_acceptable(self, max_memory_mb: float = 100.0):
        """Assert that memory usage is within acceptable limits."""
        if hasattr(self, 'memory_monitor') and self.memory_monitor.snapshots:
            current_memory = self.memory_monitor.snapshots[-1].memory_mb
            self.assertLess(current_memory, max_memory_mb,
                          f"Memory usage {current_memory:.1f}MB exceeds limit {max_memory_mb}MB")
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get memory usage summary for the test."""
        if hasattr(self, 'memory_monitor'):
            return self.memory_monitor.get_summary()
        return {'error': 'No memory monitor available'}


@contextmanager
def memory_monitoring(threshold_mb: float = 5.0, window_seconds: float = 30.0):
    """Context manager for memory monitoring during operations."""
    monitor = MemoryMonitor()
    try:
        monitor.take_snapshot()  # Baseline
        yield monitor
    finally:
        monitor.take_snapshot()  # Final
        if monitor.detect_memory_leak(threshold_mb, window_seconds):
            growth_data = monitor.get_memory_growth()
            raise AssertionError(f"Memory leak detected: {growth_data}")


def create_memory_intensive_operation(operation_count: int = 1000) -> Callable:
    """Create a memory-intensive operation for testing."""
    def memory_intensive_operation():
        """Create and destroy many objects to test memory management."""
        objects = []
        for i in range(operation_count):
            # Create various types of objects
            objects.append([i] * 100)  # Lists
            objects.append({f'key_{i}': f'value_{i}'} for _ in range(10))  # Dicts
            objects.append(f'string_{i}' * 10)  # Strings
            objects.append(bytearray(i * 100))  # Byte arrays
            
            # Periodically clear some objects to simulate real usage
            if i % 100 == 0:
                objects = objects[::2]  # Keep every other object
        
        return len(objects)
    
    return memory_intensive_operation


class TestMemoryMonitor(unittest.TestCase):
    """Test the memory monitoring system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.monitor = MemoryMonitor()
    
    def test_memory_cleanup(self):
        """Test that memory is properly cleaned up after operations."""
        def cleanup_function():
            """Test cleanup function."""
            objects = []
            for i in range(100):
                objects.append([i] * 10)
            return len(objects)
        
        # Test memory cleanup
        monitor = MemoryMonitor()
        
        for i in range(5):
            monitor.take_snapshot()
            
            # Perform the operation
            cleanup_function()
            
            # Force garbage collection
            gc.collect()
            
            monitor.take_snapshot()
        
        # Check for memory growth
        growth_data = monitor.get_memory_growth()
        self.assertLess(growth_data['memory_growth_mb'], 2.0,
                       f"Memory growth {growth_data['memory_growth_mb']:.1f}MB exceeds limit 2.0MB")
    
    def test_memory_monitoring_basic(self):
        """Test basic memory monitoring functionality."""
        # Take initial snapshot
        snapshot1 = self.monitor.take_snapshot()
        self.assertIsInstance(snapshot1, MemorySnapshot)
        self.assertGreater(snapshot1.memory_mb, 0)
        
        # Create some objects
        test_objects = []
        for i in range(1000):
            test_objects.append([i] * 100)
        
        # Take second snapshot
        snapshot2 = self.monitor.take_snapshot()
        self.assertGreater(snapshot2.memory_mb, snapshot1.memory_mb)
        
        # Clean up
        del test_objects
        import gc
        gc.collect()
        
        # Take final snapshot
        snapshot3 = self.monitor.take_snapshot()
        
        # Memory should either decrease or stay roughly the same after cleanup
        # Allow for some variance in memory measurement
        memory_change = snapshot3.memory_mb - snapshot2.memory_mb
        self.assertLess(memory_change, 5.0,  # Allow up to 5MB increase
                       f"Memory increased by {memory_change:.2f}MB after cleanup")
    
    def test_memory_leak_detection(self):
        """Test memory leak detection."""
        # Should not detect leak initially
        self.assertFalse(self.monitor.detect_memory_leak(threshold_mb=1.0))
        
        # Create objects that won't be cleaned up (simulate leak)
        self.monitor._leak_objects = []
        for i in range(1000):
            self.monitor._leak_objects.append([i] * 100)
        
        # Take snapshots to simulate growth
        self.monitor.take_snapshot()
        time.sleep(0.1)  # Add some time between snapshots
        
        # Create more objects to ensure growth
        for i in range(1000):
            self.monitor._leak_objects.append([i] * 200)
        
        self.monitor.take_snapshot()
        
        # Force garbage collection to make the leak more apparent
        gc.collect()
        
        # Should detect leak - use a very low threshold
        self.assertTrue(self.monitor.detect_memory_leak(threshold_mb=0.01))
    
    def test_memory_growth_calculation(self):
        """Test memory growth calculation."""
        # Take multiple snapshots
        for i in range(5):
            self.monitor.take_snapshot()
        
        growth_data = self.monitor.get_memory_growth()
        self.assertIn('memory_growth_mb', growth_data)
        self.assertIn('object_growth', growth_data)
        self.assertIn('snapshots_analyzed', growth_data)


class TestMemoryTestMixin(unittest.TestCase, MemoryTestMixin):
    """Test the MemoryTestMixin functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        MemoryTestMixin.setUp(self)
    
    def tearDown(self):
        """Clean up test fixtures."""
        MemoryTestMixin.tearDown(self)
        super().tearDown()
    
    def test_memory_assertions(self):
        """Test memory assertion methods."""
        # Test no memory leak assertion
        self.assert_no_memory_leak(threshold_mb=5.0)
        
        # Test memory usage assertion
        self.assert_memory_usage_acceptable(max_memory_mb=100.0)
        
        # Test memory summary
        summary = self.get_memory_summary()
        self.assertIsInstance(summary, dict)
        self.assertIn('current_memory_mb', summary)


if __name__ == '__main__':
    # Test the memory monitoring system
    unittest.main() 