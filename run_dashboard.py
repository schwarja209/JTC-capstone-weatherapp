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
    
    Performs comprehensive environment validation including Python version checking,
    module import verification, and setup guidance for common configuration issues.
    Provides detailed error messages with specific remediation steps.
    
    Raises:
        RuntimeError: If Python version < 3.8 or WeatherDashboard module cannot be imported
        
    Side Effects:
        Prints warning messages for import issues
        Provides detailed troubleshooting information on failure
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
    
    Orchestrates application startup by validating the environment, handling
    import security, and launching the GUI application. Provides comprehensive
    error handling for common startup failures with user-friendly guidance.
    
    Handles keyboard interrupts gracefully and provides appropriate exit codes
    for different failure scenarios (environment, import, or unexpected errors).
    
    Exit Codes:
        0: Successful execution or user interruption
        1: Environment or import errors
    """
    def _handle_startup_error(error_type: str, error: Exception, exit_code: int) -> None:
        """Handle startup errors with consistent messaging and exit codes."""
        error_messages = {
            "environment": f"❌ Environment Error: {error}",
            "import": f"❌ Import Error: {error}\n💡 Tip: Make sure you're running from the correct directory\n   or install the package with: pip install -e .",
            "unexpected": f"❌ Unexpected Error: {error}\n🐛 This might be a bug. Please check the logs for details."
        }
        
        print(error_messages.get(error_type, f"❌ Error: {error}"))
        sys.exit(exit_code)

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
        _handle_startup_error("environment", e, 1)
    except ImportError as e:
        _handle_startup_error("import", e, 1)
    except Exception as e:
        _handle_startup_error("unexpected", e, 1)


if __name__ == "__main__":
    main()