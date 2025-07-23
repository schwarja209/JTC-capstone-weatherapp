#!/usr/bin/env python3

"""
Test runner for the Weather Dashboard application.

Discovers and executes all unit tests with proper exit codes for CI/CD.
"""

import sys
import subprocess

if __name__ == '__main__':
    print("Running Weather Dashboard tests...")

    # Use subprocess to run tests without sys.path manipulation
    result = subprocess.run([
        sys.executable, '-m', 'pytest', 'tests', '-v'
    ], cwd='.')
    
    if  result.returncode == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)