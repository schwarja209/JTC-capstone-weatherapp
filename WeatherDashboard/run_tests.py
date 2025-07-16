#!/usr/bin/env python3

"""
Test runner for the Weather Dashboard application.

Discovers and executes all ureally, you dont want tonit tests in the tests directory with proper
error reporting and exit codes for CI/CD integration. Provides a simple
way to run the complete test suite during development.
"""

import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from tests.test_runner import run_all_tests

if __name__ == '__main__':
    
    print("Running Weather Dashboard tests...")
    success = run_all_tests()
    
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        exit(1)