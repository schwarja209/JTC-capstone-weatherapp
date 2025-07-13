# Weather Dashboard

A comprehensive, professionally-architected weather application built with Python and Tkinter, featuring live weather data, sophisticated error handling, and a robust modular design foundation for future dual-theme satirical enhancements.

## Overview

The Weather Dashboard provides real-time weather information with a clean, tabbed interface displaying current conditions and historical trends. Built with enterprise-level architecture patterns, the application seamlessly handles both live API data and fallback scenarios while maintaining excellent user experience.

### Development History

- **GUI Foundation**: Evolved from HW 8 with significant architectural improvements
- **Error Handling & API Integration**: Enhanced from HW 10 with professional error management
- **Architecture Modernization**: Substantial refactoring and separation of concerns, as well as asynchronization
- **Documentation Expansion**: Substantial expansion of docstrings and other documentation
- **GUI Redesign**: Shifted display frames to a tabbed layout and added a status bar
- **Alert System**: Added weather alert thresholds and notification system
- **Expanded Metrics**: Substantial metric expasion, including derived metrics
- **Current State**: Production-ready application with 42+ modular files, comprehensive testing, and consistent architectural patterns

## Features

### Core Functionality
- **Live Weather Data**: Real-time data via OpenWeatherMap API with UV index and air quality
- **Fallback Data Generation**: Intelligent simulated data when API unavailable (from HW 8)
- **Dual Unit Systems**: Full support for Imperial and Metric units with seamless conversion
- **Interactive Charts**: Historical weather trend visualization with configurable date ranges and metrics
- **Weather Alerts**: Intelligent alert system with severity levels and visual indicators
- **Tabbed Interface**: Clean organization with Current Weather and Weather Trends tabs

### Advanced Functionality
- **Async Operations**: Non-blocking weather data fetching with loading states
- **Rate Limiting**: Professional API rate limiting to prevent service blocking
- **Theme-Aware Error Handling**: Sophisticated error messaging system (foundation for future themes)
- **Comprehensive Logging**: Multi-format logging (plain text and JSON Lines)
- **State Management**: Centralized application state with validation and cleanup
- **Dynamic UI**: Visibility controls for metrics with automatic chart dropdown updates
- **Memory Management**: Intelligent data cleanup with configurable retention policies

### Recent Architectural Improvements
- **Standardized Error Handling**: Consistent patterns across all application layers
- **Simplified Configuration**: Direct access patterns with single source of truth
- **Streamlined Memory Management**: Efficient cleanup without over-engineering
- **Widget State Consistency**: Safe, standardized access patterns throughout UI
- **Professional Documentation**: Balanced approach with consistent standards

## Architecture

### Project Structure
```
WeatherDashboard/
├── core/                    # Business logic and data management
│   ├── controller.py        # Main orchestration controller
│   ├── data_manager.py      # Weather data storage and processing
│   ├── data_service.py      # Service layer abstraction
│   └── view_models.py       # Display-ready data formatting
├── gui/                     # User interface components
│   ├── main_window.py       # Application window coordination
│   ├── state_manager.py     # Centralized state management
│   ├── frames.py           # Layout management
│   ├── styles.py           # Visual styling
│   └── loading_states.py   # Async operation UI handling
├── widgets/                 # Specialized UI components
│   ├── dashboard_widgets.py # Main widget coordinator
│   ├── control_widgets.py   # Input controls and buttons
│   ├── metric_widgets.py    # Weather metric displays
│   ├── chart_widgets.py     # Matplotlib chart integration
│   ├── tabbed_widgets.py    # Tab management
│   ├── status_bar_widgets.py# Status and progress indicators
|   └── title_widgets.py     # Title bar display
├── services/               # External integrations
│   ├── weather_service.py   # OpenWeatherMap API client
│   ├── error_handler.py     # Theme-aware error management
│   ├── fallback_generator.py# Simulated weather data
│   └── api_exceptions.py    # Custom exception hierarchy
├── features/               # Specialized functionality
│   ├── alerts/             # Weather alert system
│   │   ├── alert_display.py # Alert display components
│   │   └── alert_manager.py # Alert management system
│   └── theme_switcher.py   # Future theme management
├── utils/                  # Common utilities
│   ├── logger.py           # Multi-format logging
│   ├── rate_limiter.py     # API rate limiting
│   ├── unit_converter.py   # Weather unit conversions
│   ├── derived_metrics.py  # Derived metric calculations
│   └── utils.py            # General helper functions
└── tests/                  # Comprehensive test suite
    ├── test_data_manager.py
    ├── test_state_manager.py
    ├── test_unit_converter.py
    ├── test_utils.py
    └── test_runner.py
```

### Design Principles
- **Separation of Concerns**: Clear boundaries between UI, business logic, and data layers
- **Modular Architecture**: Independent, testable components with minimal coupling
- **Professional Error Handling**: Graceful degradation with standardized patterns across layers
- **State Management**: Centralized state with safe, consistent access patterns
- **Configuration Simplicity**: Direct access with single source of truth
- **Extensibility**: Foundation architecture ready for future feature expansion

### Architecture Quality
- **Consistent Error Handling**: Standardized patterns across all layers (utilities raise → services convert → controllers handle)
- **Safe State Access**: Standardized widget state access with proper error handling
- **Simplified Configuration**: Direct access patterns eliminating redundant abstraction layers
- **Streamlined Memory Management**: Efficient cleanup without over-engineering
- **Professional Documentation**: Balanced approach with consistent standards throughout

## Installation & Setup

### Prerequisites
- Python 3.8+
- tkinter (usually included with Python)
- matplotlib for chart rendering
- requests for API communication

### Required Dependencies
```bash
pip install requests matplotlib
```

### Optional Dependencies
```bash
pip install python-dotenv  # For environment variable loading
```

### API Configuration
1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Create a `.env` file in the project root:
```
OPENWEATHER_API_KEY=your_api_key_here
```
3. Or set the environment variable directly:
```bash
export OPENWEATHER_API_KEY=your_api_key_here
```

## Usage

### Running the Application
```bash
python main.py
# or
python run_dashboard.py
```

### Basic Operations
1. **Enter City**: Type any city name in the input field
2. **Select Units**: Choose between Imperial (°F, mph, inHg) or Metric (°C, m/s, hPa)
3. **Configure Metrics**: Use checkboxes to show/hide specific weather metrics
4. **View Charts**: Switch to "Weather Trends" tab for historical data visualization
5. **Update Weather**: Click "Update Weather" or press Enter in city field
6. **Monitor Alerts**: Alert indicators appear when weather conditions warrant attention

### Advanced Features
- **Chart Configuration**: Select different metrics and date ranges for trend analysis
- **Loading States**: Visual feedback during async operations with cancel capability
- **Error Recovery**: Automatic fallback to simulated data when API unavailable with visible status monitoring
- **State Persistence**: Settings maintained during session with easy reset functionality
- **Select All/Clear All**: Bulk metric visibility controls for quick configuration

## Testing

### Running Tests
```bash
python run_tests.py
```

### Test Coverage
- Unit tests for core business logic
- State management validation
- Unit conversion accuracy
- Utility function reliability
- Error handling scenarios

## Technical Implementation

### API Integration
- **Live Data**: User-triggered API calls to OpenWeatherMap with UV index and air quality
- **Chart Data**: Fully simulated historical data for trend visualization
- **Rate Limiting**: Intelligent throttling to prevent API quota exhaustion
- **Error Recovery**: Seamless fallback to simulated data with user notification

### Data Management
- **Unit Conversion**: Automatic conversion between metric and imperial systems
- **Data Validation**: Comprehensive validation with range checking and sanitization
- **Memory Management**: Automatic cleanup of old data with configurable retention
- **Logging**: Dual-format logging for both human reading and automated analysis

### UI Architecture
- **Responsive Design**: Adaptive layout with proper grid weight configuration
- **Async Operations**: Non-blocking UI with progress indicators and cancellation
- **State Synchronization**: Centralized state management with automatic UI updates
- **Error Messaging**: Theme-aware error presentation with user-friendly language

### Recent Technical Improvements
- **Error Handling Standardization**: Consistent patterns across all architectural layers
- **Configuration Simplification**: Direct access eliminating ~70 lines of redundant code
- **Memory Management Streamlining**: Simplified approach removing ~50 lines of complex logic
- **Widget State Consistency**: Safe access patterns preventing potential runtime errors
- **Import Optimization**: Clean, well-utilized imports throughout codebase

## Future Development

### Planned Enhancements
The current architecture serves as a solid foundation for a **dual-theme satirical weather application** featuring:

- **Optimistic Mode**: Cheerfully distorted weather interpretations with simplified UI
- **Pessimistic Mode**: Darkly exaggerated forecasts with deliberately degraded UX
- **Quote Integration**: Philosophical and weather-related quotes with tone alignment
- **Badge System**: Gamified achievements with inverse tone (sarcastic ↔ supportive)
- **Easter Eggs**: Hidden features triggered by specific user interactions
- **UI Evolution**: Dynamic interface changes based on theme and user behavior

### Extensibility Points
- Theme management system foundation already in place via `WeatherErrorHandler`
- Modular widget architecture ready for theme-specific behaviors
- Centralized, standardized error handling prepared for theme-aware messaging
- Alert system adaptable for satirical notifications
- State management with consistent access patterns ready for theme mode tracking
- Configuration system simplified for easy theme-based customization

### Architecture Readiness
- **Consistent Error Handling**: Standardized patterns ready for theme-aware messaging
- **Safe State Access**: Robust patterns ready for theme state integration
- **Simplified Configuration**: Direct access ready for theme-based modifications
- **Professional Foundation**: Clean, maintainable codebase ready for feature development

## Contributing

### Code Standards
- **Type Hints**: Comprehensive type annotations throughout
- **Documentation**: Balanced approach with consistent standards (detailed for complex, brief for simple)
- **Error Handling**: Standardized patterns with graceful failure handling
- **Testing**: Unit tests for all business logic components
- **Logging**: Comprehensive logging for debugging and monitoring

### Architecture Guidelines
- Maintain separation between UI, business logic, and data layers
- Use standardized error handling patterns (utilities raise → services convert → controllers handle)
- Follow consistent widget state access patterns with safe fallbacks
- Use direct configuration access rather than unnecessary abstraction layers
- Maintain the simplified, efficient memory management approach
- Follow established documentation standards (hybrid detailed/brief approach)

### Recent Architecture Decisions
- **ADR-026**: Configuration System Simplification - Direct access over abstraction layers
- **ADR-027**: Memory Management Streamlining - Single strategy over multiple approaches
- **ADR-028**: Error Handling Standardization - Consistent patterns across all layers
- **ADR-029**: Widget State Access Patterns - Safe, standardized access throughout UI
- **ADR-030**: Documentation Standards Update - Balanced hybrid approach

## License

TBD

## Acknowledgments

- Built upon foundational work from HW 8 (GUI) and HW 10 (Error Handling & API)
- Recent comprehensive architecture modernization and simplification
- OpenWeatherMap API for live weather data
- Python community for excellent libraries and tools