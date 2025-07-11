#!/usr/bin/env python3
"""
Quick test runner for development.
"""
from tests.test_runner import run_all_tests

if __name__ == '__main__':
    print("Running Weather Dashboard tests...")
    success = run_all_tests()
    
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        exit(1)