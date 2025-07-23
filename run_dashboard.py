#!/usr/bin/env python3
"""
Weather Dashboard Application Launcher

Secure entry point that validates environment and launches the main application.

Usage:
    python run_dashboard.py
"""

import os
import sys


def validate_environment():
    """Validate Python version and module import requirements for application startup.
    
    Performs comprehensive environment validation to ensure the Weather Dashboard
    can run properly. Validates Python version compatibility and verifies that
    the main application module can be imported correctly.
    
    Validation Steps:
        1. Python version check: Requires Python 3.8 or higher
        2. WeatherDashboard module import test: Ensures package structure is valid
        3. Path resolution: Provides helpful error messages with current vs expected paths
    
    Side Effects:
        Prints warning messages to stdout for API key issues during import validation.
        Does not modify sys.path or perform any permanent system changes.
    """
    # Check Python version
    if sys.version_info < (3, 8):
        raise RuntimeError(
            f"Python 3.8 is required. Current version: {sys.version_info.major}.{sys.version_info.minor}"
        )
    
    # Verify we can import the main application module
    try:
        # Test import without adding to sys.path
        import WeatherDashboard
    except ImportError as e:
        # Provide helpful error message for common setup issues
        current_dir = os.getcwd()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        error_msg = (
            f"Cannot import WeatherDashboard module: {e}\n\n"
            f"Common solutions:\n"
            f"1. Run from project root containing WeatherDashboard/\n"
            f"   Current: {current_dir}\n"
            f"   Script: {script_dir}\n"
            f"2. Install in development mode: pip install -e .\n"
            f"3. Use module flag: python -m WeatherDashboard.main\n"
            f"4. Set PYTHONPATH: export PYTHONPATH=\"{script_dir}:$PYTHONPATH\"\n"
            f"5. Ensure WeatherDashboard/ contains __init__.py"
        )
        raise RuntimeError(error_msg) from e

def _handle_startup_error(error_type: str, error: Exception, exit_code: int) -> None:
    """Handle startup errors with consistent messaging and exit codes."""
    error_messages = {
        "environment": f"❌ Environment Error: {error}",
        "import": f"❌ Import Error: {error}\n💡 Tip: Make sure you're running from the correct directory or install the package with: pip install -e .",
        "unexpected": f"❌ Unexpected Error: {error}\n🐛 This might be a bug. Please check the logs for details."
    }
    
    print(error_messages.get(error_type, f"❌ Error: {error}"))
    sys.exit(exit_code)

def main():
    """Main entry point that validates environment and launches the application."""
    try:
        # Validate environment before proceeding
        validate_environment()
        
        # Import and run the main application
        # This is secure because we're not modifying sys.path
        from WeatherDashboard.main import main as app_main
        
        print("🌤️ Loading Weather Dashboard...")
        app_main()
        
    except KeyboardInterrupt:
        print("\n👋 Weather Dashboard stopped by user")
        sys.exit(0)
    except RuntimeError as e:
        _handle_startup_error("environment", e, 1)
    except ImportError as e:
        _handle_startup_error("import", e, 1)
    except Exception as e:
        _handle_startup_error("unexpected", e, 1)


if __name__ == "__main__":
    main()