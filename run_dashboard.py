#!/usr/bin/env python3
"""
Weather Dashboard Application Launcher

Secure entry point for the Weather Dashboard application.
This launcher properly imports the main application without manipulating sys.path.

Usage:
    python run_dashboard.py
    
    or from project root:
    python -m WeatherDashboard.run_dashboard
    
    or if installed:
    weather-dashboard

Security Note:
    This launcher does not modify sys.path to avoid potential import hijacking
    vulnerabilities. Instead, it relies on proper Python package structure.
"""

import os
import sys


def validate_environment():
    """
    Validate that the application can run in the current environment.
    
    Raises:
        ImportError: If required modules cannot be imported
        RuntimeError: If environment is not suitable
    """
    # Check Python version
    if sys.version_info < (3, 8):
        raise RuntimeError(
            f"Python 3.8+ is required. Current version: {sys.version_info.major}.{sys.version_info.minor}"
        )
    
    # Verify we can import the main application module
    try:
        # Test import without adding to sys.path
        import WeatherDashboard
    except ImportError as e:
        # Provide helpful error message for common setup issues
        current_dir = os.getcwd()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        error_msg = f"""
Cannot import WeatherDashboard module: {e}

Common solutions:
1. Run from the project root directory containing WeatherDashboard/
   Current directory: {current_dir}
   Script directory: {script_dir}

2. Install in development mode:
   pip install -e .

3. Use the module flag:
   python -m WeatherDashboard.main

4. Set PYTHONPATH:
   export PYTHONPATH="{script_dir}:$PYTHONPATH"
   python run_dashboard.py

5. Ensure WeatherDashboard/ contains __init__.py
"""
        raise RuntimeError(error_msg) from e


def main():
    """
    Main entry point for the Weather Dashboard application.
    
    This function validates the environment and launches the application
    using secure import practices.
    """
    try:
        # Validate environment before proceeding
        validate_environment()
        
        # Import and run the main application
        # This is secure because we're not modifying sys.path
        from WeatherDashboard.main import main as app_main
        
        print("🌤️  Starting Weather Dashboard...")
        app_main()
        
    except KeyboardInterrupt:
        print("\n👋 Weather Dashboard stopped by user")
        sys.exit(0)
        
    except RuntimeError as e:
        print(f"❌ Environment Error: {e}")
        sys.exit(1)
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\n💡 Tip: Make sure you're running from the correct directory")
        print("   or install the package with: pip install -e .")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print("\n🐛 This might be a bug. Please check the logs for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()