"""
CSV data manager for coordinating CSV data operations.

This module provides a centralized manager for CSV data operations,
including loading, normalization, metric mapping, and state management.
Coordinates between different CSV services and provides a unified
interface for CSV data access.

Classes:
    CSVDataManager: Main manager for CSV data operations and state
"""

from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict

from WeatherDashboard.utils.logger import Logger
from WeatherDashboard.features.comparison.csv_data_service import CSVDataService
from WeatherDashboard.features.comparison.csv_normalizer import CSVNormalizer
from WeatherDashboard.features.comparison.csv_metric_mapper import CSVMetricMapper
from WeatherDashboard.features.comparison.csv_color_generator import CSVColorGenerator


class CSVDataManager:
    """Manages CSV data operations and state for the comparison feature.
    
    Coordinates between CSV data services, normalizers, metric mappers,
    and color generators. Provides a unified interface for loading,
    processing, and accessing CSV data for charting.
    
    Attributes:
        logger: Application logger instance
        data_service: CSV data loading and caching service
        normalizer: CSV data normalization service
        metric_mapper: CSV metric mapping service
        color_generator: CSV color generation service
        normalized_cache: Cache for normalized CSV data
        current_metric: Currently selected metric for filtering
        current_date_range: Currently selected date range in days
    """
    
    def __init__(self) -> None:
        """Initialize the CSV data manager.
        
        Sets up all CSV services and initializes caching structures
        for coordinated CSV data operations.
        """
        self.logger = Logger()
        
        # Initialize services
        self.data_service = CSVDataService()
        self.normalizer = CSVNormalizer()
        self.metric_mapper = CSVMetricMapper()
        self.color_generator = CSVColorGenerator()
        
        # State management
        self.normalized_cache: Dict[str, Dict[str, Any]] = {}
        self.current_metric: Optional[str] = None
        self.current_date_range: int = 30
        
    def load_all_csv_data(self, date_range_days: Optional[int] = None) -> Dict[str, Any]:
        """Load and process all available CSV files.
        
        Args:
            date_range_days: Number of days from UI (will be converted to months for CSV processing)
            
        Returns:
            Dictionary containing processed CSV data for all files
        """
        try:
            # Update date range if provided
            # Convert days to months for CSV processing
            # 7 days = 7 months, 14 days = 14 months, 30 days = 30 months
            date_range_months = date_range_days if date_range_days is not None else self.current_date_range
            self.logger.info(f"Loading CSV data with {date_range_months} months range")

            # Get available CSV files
            csv_files = self.data_service.get_available_csv_files()
            if not csv_files:
                self.logger.warn("No CSV files found in comparison directory")
                return {'files': [], 'available_metrics': [], 'data': {}}
            
            # Process each CSV file
            processed_data = {}
            all_available_metrics = set()
            
            for filename in csv_files:
                # Load raw CSV data
                raw_data = self.data_service.load_csv_data(filename)
                if not raw_data:
                    self.logger.warn(f"Failed to load CSV file: {filename}")
                    continue

                # Convert days to months for CSV processing
                date_range_months = date_range_days if date_range_days else self.current_date_range

                # Normalize data with monthly averaging
                normalized_data = self.normalizer.normalize_csv_data(
                    raw_data, date_range_months
                )

                if not normalized_data:
                    self.logger.warn(f"Failed to normalize CSV file: {filename}")
                    continue
                
                # Filter out location and date columns before metric mapping
                weather_headers = [header for header in raw_data['headers'] 
                                if not self.metric_mapper._is_date_column(header) 
                                and not self.metric_mapper._is_location_column(header)]

                # Map metrics (only weather columns)
                metric_mapping = self.metric_mapper.map_csv_columns(weather_headers)
                available_metrics = self.normalizer.get_available_metrics(normalized_data)
                
                # Store processed data
                processed_data[filename] = {
                    'raw_data': raw_data,
                    'normalized_data': normalized_data,
                    'metric_mapping': metric_mapping,
                    'available_metrics': available_metrics,
                    'color': self.color_generator.get_color_for_csv(filename)
                }
                
                # Collect all available metrics
                all_available_metrics.update(available_metrics)
            
            # Cache normalized data
            self.normalized_cache = processed_data
            
            result = {
                'files': list(processed_data.keys()),
                'available_metrics': sorted(list(all_available_metrics)),
                'data': processed_data
            }
            
            self.logger.info(f"Loaded {len(processed_data)} CSV files with {len(all_available_metrics)} available metrics")
            return result
            
        except Exception as e:
            self.logger.error(f"Error loading CSV data: {e}")
            return {'files': [], 'available_metrics': [], 'data': {}}
    
    def get_data_for_metric(self, metric: str) -> Dict[str, Any]:
        """Get CSV data filtered for a specific metric.
        
        Filters all loaded CSV data to include only files that have
        the specified metric, and returns the data ready for charting.
        Groups data by city if city information is available.
        
        Args:
            metric: Standard metric name to filter by
            
        Returns:
            Dictionary containing filtered CSV data for the metric
        """
        try:
            self.current_metric = metric
            
            if not self.normalized_cache:
                self.logger.warn("No CSV data loaded. Call load_all_csv_data() first.")
                return {'metric': metric, 'files': [], 'chart_data': {}}
            
            # Filter data for the specified metric
            chart_data = {}
            available_files = []
            
            for filename, file_data in self.normalized_cache.items():
                # Check if file has the specified metric
                if metric in file_data['available_metrics']:
                    # Filter normalized data for this metric
                    filtered_data = self.normalizer.filter_by_metric(
                        file_data['normalized_data'], metric
                    )
                    
                    if filtered_data and filtered_data['monthly_data']:
                        # Group data by city if city information is available
                        city_data = self._group_data_by_city(filtered_data['monthly_data'])
                        
                        chart_data[filename] = {
                            'data': city_data,
                            'color': file_data['color'],
                            'metric': metric,
                            'cities': list(city_data.keys())
                        }
                        available_files.append(filename)
            
            result = {
                'metric': metric,
                'files': available_files,
                'chart_data': chart_data
            }
            
            self.logger.info(f"Filtered data for metric '{metric}': {len(available_files)} files available")
            return result
            
        except Exception as e:
            self.logger.error(f"Error filtering data for metric '{metric}': {e}")
            return {'metric': metric, 'files': [], 'chart_data': {}}
    
    def _group_data_by_city(self, monthly_data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group monthly data by city.
        
        Args:
            monthly_data: List of monthly data dictionaries
            
        Returns:
            Dictionary with city names as keys and lists of monthly data as values
        """
        city_groups = defaultdict(list)
        
        for data_point in monthly_data:
            city = data_point.get('city', 'Unknown')
            city_groups[city].append(data_point)
    
        return dict(city_groups)

    def get_chart_data(self, metric: str, target_city: str, enabled_files: List[str] = None, date_range_days: Optional[int] = None) -> Tuple[List[str], List[List[float]], List[str], List[str], List[str], List[str]]:
        """Get chart-ready data for a specific metric.
        
        Prepares data in the format expected by the chart widget:
        dates, values for each city in each CSV file, and colors.
        
        Args:
            metric: Standard metric name to chart
            date_range_days: Number of days to include (optional)
            
        Returns:
            Tuple of (dates, values_list, colors) for charting
        """
        try:
            # Update date range if provided
            if date_range_days is not None:
                self.current_date_range = date_range_days
                # Reload data with new date range
                self.load_all_csv_data(date_range_days)
            
            # Get filtered data for the metric
            filtered_result = self.get_data_for_metric(metric)
            
            if not filtered_result['chart_data']:
                return [], [], [], [], [], []
            
            # Prepare chart data
            dates = []
            values_list = []
            colors = []
            labels = []
            
            # Get all unique dates from all files and cities
            all_dates = set()
            for file_data in filtered_result['chart_data'].values():
                for city_data in file_data['data'].values():
                    for entry in city_data:
                        all_dates.add(entry['date'])
            
            dates = sorted(list(all_dates))
            
            available_files = []
            missing_files = []
            
            for filename, file_data in filtered_result['chart_data'].items():
                # Only process files that are enabled (if enabled_files is provided)
                if enabled_files is not None and filename not in enabled_files:
                    continue
                if target_city in file_data['data']:
                    # Only include data for the target city
                    city_data = file_data['data'][target_city]
                    data_dict = {entry['date']: entry['value'] for entry in city_data}
                    
                    values = []
                    for date in dates:
                        values.append(data_dict.get(date, None))
                    
                    values_list.append(values)
                    # Generate unique color for each CSV file
                    file_color = self.color_generator.get_color_for_csv(filename)
                    colors.append(file_color)
                    labels.append(filename)  # Use filename as label
                    available_files.append(filename)
                    self.logger.debug(f"Added data for {filename}: {len(city_data)} data points")
                else:
                    missing_files.append(filename)
                    self.logger.debug(f"No data for {target_city} in {filename}. Available cities: {list(file_data['data'].keys())}")
            
            return dates, values_list, colors, labels, available_files, missing_files
            
        except Exception as e:
            self.logger.error(f"Error preparing chart data for metric '{metric}': {e}")
            return [], [], [], [], [], []
    
    def get_available_metrics(self) -> List[str]:
        """Get list of all available metrics across all CSV files.
        
        Returns:
            List of available standard metric names
        """
        if not self.normalized_cache:
            return []
        
        all_metrics = set()
        for file_data in self.normalized_cache.values():
            all_metrics.update(file_data['available_metrics'])
        
        return sorted(list(all_metrics))
    
    def clear_cache(self) -> None:
        """Clear all cached data.
        
        Clears both the data service cache and the normalized cache,
        forcing re-loading of all CSV data.
        """
        self.data_service.clear_cache()
        #self.color_generator.clear_cache()
        self.normalized_cache.clear()
        self.logger.info("All CSV data caches cleared")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about the current cache state.
        
        Returns:
            Dictionary containing cache statistics and state information
        """
        return {
            'data_service_cache': self.data_service.get_cache_info(),
            'color_cache': self.color_generator.get_cache_info(),
            'normalized_cache_size': len(self.normalized_cache),
            'current_metric': self.current_metric,
            'current_date_range': self.current_date_range
        }
    
    def set_date_range(self, days: int) -> None:
        """Set the date range for CSV data processing.
        
        Args:
            days: Number of days to include in data processing (converted to months for CSV)
        """
        if days > 0:
            self.current_date_range = days
            # Reload data with new date range to ensure charts update
            self.load_all_csv_data(days)
            self.logger.info(f"Updated date range to {days} days (aka months for CSV)")
        else:
            self.logger.error(f"Invalid date range: {days}. Must be positive.")
    
    def get_date_range(self) -> int:
        """Get the current date range setting.
        
        Returns:
            Current date range in days
        """
        return self.current_date_range
    
    def get_city_availability(self, target_city: str) -> Dict[str, bool]:
        """Check which CSV files contain data for the specified city.
        
        Args:
            target_city: City name to check for
            
        Returns:
            Dictionary mapping CSV filenames to boolean availability
        """
        availability = {}
        
        for filename, file_data in self.normalized_cache.items():
            # Check if any city in this file matches the target
            cities_in_file = set()
            for city_data in file_data.get('normalized_data', {}).get('monthly_data', []):
                city = city_data.get('city', 'Unknown')
                cities_in_file.add(city)
            
            availability[filename] = target_city in cities_in_file
        
        return availability