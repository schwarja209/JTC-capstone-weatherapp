# Weather Dashboard

A comprehensive, professionally-architected weather application built with Python and Tkinter, featuring live weather data, sophisticated error handling, and a robust modular design foundation for future dual-theme satirical enhancements.

## Overview

The Weather Dashboard provides real-time weather information with a clean, tabbed interface displaying current conditions and historical trends. Built with enterprise-level architecture patterns, the application seamlessly handles both live API data and fallback scenarios while maintaining excellent user experience.

### Development History

- **GUI Foundation**: Evolved from HW 8 with significant architectural improvements
- **Error Handling & API Integration**: Enhanced from HW 10 with professional error management
- **Current State**: Production-ready application with 42+ modular files and comprehensive testing

## Features

### Core Functionality
- **Live Weather Data**: Real-time data via OpenWeatherMap API
- **Fallback Data Generation**: Intelligent simulated data when API unavailable (from HW 8)
- **Dual Unit Systems**: Full support for Imperial and Metric units with seamless conversion
- **Interactive Charts**: Historical weather trend visualization with configurable date ranges
- **Weather Alerts**: Intelligent alert system with severity levels and visual indicators
- **Tabbed Interface**: Clean organization with Current Weather and Weather Trends tabs

### Advanced Functionality
- **Async Operations**: Non-blocking weather data fetching with loading states
- **Rate Limiting**: Professional API rate limiting to prevent service blocking
- **Theme-Aware Error Handling**: Sophisticated error messaging system (foundation for future themes)
- **Comprehensive Logging**: Multi-format logging (plain text and JSON Lines)
- **State Management**: Centralized application state with validation and cleanup
- **Dynamic UI**: Visibility controls for metrics with automatic chart dropdown updates

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
│   └── status_bar_widgets.py# Status and progress indicators
├── services/               # External integrations
│   ├── weather_service.py   # OpenWeatherMap API client
│   ├── error_handler.py     # Theme-aware error management
│   ├── fallback_generator.py# Simulated weather data
│   └── api_exceptions.py    # Custom exception hierarchy
├── features/               # Specialized functionality
│   ├── alerts/             # Weather alert system
│   └── theme_switcher.py   # Future theme management
├── utils/                  # Common utilities
│   ├── logger.py           # Multi-format logging
│   ├── rate_limiter.py     # API rate limiting
│   ├── unit_converter.py   # Weather unit conversions
│   └── utils.py            # General helper functions
└── tests/                  # Comprehensive test suite
    ├── test_data_manager.py
    ├── test_state_manager.py
    ├── test_unit_converter.py
    └── test_utils.py
```

### Design Principles
- **Separation of Concerns**: Clear boundaries between UI, business logic, and data layers
- **Modular Architecture**: Independent, testable components with minimal coupling
- **Professional Error Handling**: Graceful degradation with user-friendly messaging
- **State Management**: Centralized state with validation and backward compatibility
- **Extensibility**: Foundation architecture ready for future feature expansion

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
- **Error Recovery**: Automatic fallback to simulated data when API unavailable
- **State Persistence**: Settings maintained during session with easy reset functionality

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
- **Live Data**: User-triggered API calls to OpenWeatherMap
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
- Theme management system foundation already in place
- Modular widget architecture ready for theme-specific behaviors
- Centralized error handling prepared for theme-aware messaging
- Alert system adaptable for satirical notifications
- State management capable of tracking theme modes and user interactions

## Contributing

### Code Standards
- **Type Hints**: Comprehensive type annotations throughout
- **Documentation**: Docstrings for all classes and complex methods
- **Error Handling**: Graceful failure handling with user-friendly messaging
- **Testing**: Unit tests for all business logic components
- **Logging**: Comprehensive logging for debugging and monitoring

### Architecture Guidelines
- Maintain separation between UI, business logic, and data layers
- Use dependency injection for testability
- Follow single responsibility principle for classes and methods
- Implement comprehensive error handling with appropriate recovery strategies
- Maintain backward compatibility when possible

## License

TBD

## Acknowledgments

- Built upon foundational work from HW 8 (GUI) and HW 10 (Error Handling & API)
- OpenWeatherMap API for live weather data
- Python community for excellent libraries and tools