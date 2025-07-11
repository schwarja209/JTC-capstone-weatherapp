"""
Test runner for all Weather Dashboard tests.

Discovers and executes all test files in the tests directory.
Provides a unified way to run the entire test suite with proper
reporting and exit codes for CI/CD integration.
"""
import unittest
import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

def run_all_tests():
    """Discover and run all tests."""
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)