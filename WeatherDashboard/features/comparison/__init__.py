"""
CSV Comparison feature for Weather Dashboard.

This module provides functionality for loading, normalizing, and displaying
CSV weather data in comparison charts. Handles CSV file monitoring,
data normalization, metric mapping, and chart integration.

Modules:
    csv_data_service: CSV file loading and caching service
    csv_data_manager: CSV data state management
    csv_normalizer: Data normalization utilities
    csv_metric_mapper: Fuzzy metric name matching
    csv_validation_utils: CSV file validation
    csv_color_generator: Random color generation for chart lines
    csv_comparison_widgets: UI widgets for CSV comparison tab
""" 