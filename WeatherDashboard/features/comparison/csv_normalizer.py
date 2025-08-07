"""
CSV data normalization utilities.

This module provides utilities for normalizing CSV weather data,
including converting to monthly averages, handling null values,
and processing time-based data for weighted averages.

Classes:
    CSVNormalizer: Main normalizer for CSV data processing
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict

from WeatherDashboard.utils.logger import Logger


class CSVNormalizer:
    """Normalizes CSV weather data to monthly averages and handles null values.
    
    Processes raw CSV data to convert it into monthly averages, handles
    null values by skipping them, and provides weighted averages when
    time information is available. Supports various date formats and
    metric types.
    
    Attributes:
        logger: Application logger instance
        date_formats: List of supported date formats for parsing
    """
    
    def __init__(self) -> None:
        """Initialize the CSV normalizer.
        
        Sets up date format patterns and logging for data normalization
        operations.
        """
        self.logger = Logger()
        
        # Supported date formats
        self.date_formats = [
            '%Y-%m-%d',      # 2020-01-01
            '%m/%d/%Y',      # 01/01/2020
            '%d/%m/%Y',      # 01/01/2020
            '%Y-%m-%d %H:%M:%S',  # 2020-01-01 12:00:00
            '%m/%d/%Y %H:%M:%S',  # 01/01/2020 12:00:00
        ]
    
    def normalize_csv_data(self, csv_data: Dict[str, Any], 
                        date_range_months: int = 12) -> Optional[Dict[str, Any]]:
        """Normalize CSV data to monthly averages within a date range.
        
        Processes the raw CSV data to convert it into monthly averages,
        filters by date range, and handles null values. Groups data by city
        if a city column is present. Returns normalized data ready for charting.
        
        Args:
            csv_data: Raw CSV data dictionary from CSVDataService
            date_range_months: Number of months to include (default 12)
            
        Returns:
            Normalized data dictionary or None if processing failed
        """
        try:
            if not csv_data or 'data' not in csv_data:
                self.logger.error("Invalid CSV data structure")
                return None
            
            # Find date column
            date_column = self._find_date_column(csv_data['headers'])
            if not date_column:
                self.logger.error("No valid date column found in CSV")
                return None
            
            # Find city column (optional)
            city_column = self._find_city_column(csv_data['headers'])
            
            # Process data rows with city grouping
            monthly_data = self._process_monthly_data_by_city(
                csv_data['data'], date_column, city_column, date_range_months
            )
            if not monthly_data:
                self.logger.warn("No valid data found after normalization")
                return None
            
            return {
                'filename': csv_data['filename'],
                'headers': csv_data['headers'],
                'monthly_data': monthly_data,
                'date_column': date_column,
                'city_column': city_column,
                'available_metrics': list(monthly_data[0].keys()) if monthly_data else [],
                'cities': list(set(item.get('city', 'Unknown') for item in monthly_data))
            }
            
        except Exception as e:
            self.logger.error(f"Error normalizing CSV data: {e}")
            return None
    
    def _find_date_column(self, headers: List[str]) -> Optional[str]:
        """Find the date column in CSV headers.
        
        Searches for columns that contain date-related keywords
        and returns the first matching column name.
        
        Args:
            headers: List of CSV column headers
            
        Returns:
            Name of the date column or None if not found
        """
        date_keywords = ['date', 'time', 'datetime', 'timestamp']
        
        for header in headers:
            header_lower = header.lower()
            for keyword in date_keywords:
                if keyword in header_lower:
                    return header
        
        return None
    
    def _find_city_column(self, headers: List[str]) -> Optional[str]:
        """Find the city column in CSV headers.
        
        Searches for columns that contain city-related keywords
        and returns the first matching column name.
        
        Args:
            headers: List of CSV column headers
            
        Returns:
            Name of the city column or None if not found
        """
        city_keywords = ['city', 'location', 'place', 'town', 'station']
        
        for header in headers:
            header_lower = header.lower()
            for keyword in city_keywords:
                if keyword in header_lower:
                    return header
        
        return None
    
    def _process_monthly_data_by_city(self, rows: List[Dict[str, str]], date_column: str,
                                      city_column: Optional[str], date_range_months: int) -> List[Dict[str, Any]]:
        """Process CSV rows into monthly averages grouped by city.
        
        Groups data by city and month, calculates monthly averages for each metric,
        and filters by the specified date range (interpreted as months).
        Handles null values by skipping them in calculations.
        
        Args:
            rows: List of CSV data rows
            date_column: Name of the date column
            city_column: Name of the city column (optional)
            date_range_months: Number of months to include
            
        Returns:
            List of monthly average data dictionaries with city information
        """
        # Group data by city and month (city_YYYY-MM format)
        city_monthly_groups = defaultdict(lambda: defaultdict(list))
        
        for row in rows:
            try:
                # Parse date
                date_str = row.get(date_column, '').strip()
                if not date_str:
                    continue
                
                parsed_date = self._parse_date(date_str)
                if not parsed_date:
                    continue
                
                # Get city (default to 'Unknown' if no city column)
                city = row.get(city_column, 'Unknown').strip() if city_column else 'Unknown'
                if not city:
                    city = 'Unknown'
                
                # Add to city-monthly group
                date_key = parsed_date.strftime('%Y-%m')
                city_monthly_groups[city][date_key].append(row)
                
            except Exception as e:
                self.logger.warn(f"Error processing row: {e}")
                continue
        
        # Calculate monthly averages for each city
        monthly_averages = []
        
        for city, monthly_groups in city_monthly_groups.items():
            sorted_dates = sorted(monthly_groups.keys())
            
            # Filter by date range - take only the most recent months
            if date_range_months > 0 and len(sorted_dates) > date_range_months:
                sorted_dates = sorted_dates[-date_range_months:]
                self.logger.debug(f"Filtered {city} to {len(sorted_dates)} months from {date_range_months} requested")
            
            for date_key in sorted_dates:
                monthly_data = self._calculate_monthly_averages(monthly_groups[date_key], date_column, city_column)
                if monthly_data:
                    monthly_data['date'] = date_key
                    monthly_averages.append(monthly_data)
        
        return monthly_averages
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string using multiple formats.
        
        Attempts to parse the date string using various supported
        formats and returns a datetime object if successful.
        
        Args:
            date_str: Date string to parse
            
        Returns:
            Parsed datetime object or None if parsing failed
        """
        # Clean the date string
        date_str = date_str.strip()
        
        # Try each date format
        for date_format in self.date_formats:
            try:
                return datetime.strptime(date_str, date_format)
            except ValueError:
                continue
        
        # Try to extract just the date part if it contains time
        date_only_patterns = [
            r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
            r'(\d{1,2}/\d{1,2}/\d{4})',  # MM/DD/YYYY or DD/MM/YYYY
        ]
        
        for pattern in date_only_patterns:
            match = re.search(pattern, date_str)
            if match:
                date_part = match.group(1)
                try:
                    return datetime.strptime(date_part, '%Y-%m-%d')
                except ValueError:
                    try:
                        return datetime.strptime(date_part, '%m/%d/%Y')
                    except ValueError:
                        continue
        
        self.logger.warn(f"Could not parse date: {date_str}")
        return None
    
    def _calculate_monthly_averages(self, monthly_rows: List[Dict[str, str]], 
                                 date_column: str, city_column: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Calculate monthly averages for all metrics.
        
        Processes all rows for a single day and calculates weighted
        averages for each metric. Handles null values by skipping them.
        
        Args:
            monthly_rows: List of rows for a single day
            date_column: Name of the date column
            city_column: Name of the city column (optional)

        Returns:
            Dictionary containing monthly averages for all metrics
        """
        if not monthly_rows:
            return None
        
        # Get the date from the first row
        first_row = monthly_rows[0]
        date_str = first_row.get(date_column, '').strip()
        parsed_date = self._parse_date(date_str)
        if not parsed_date:
            return None
        
        # Get city from the first row if available
        city = None
        if city_column:
            city = first_row.get(city_column, 'Unknown').strip()
            if not city:
                city = 'Unknown'

        # Initialize metric accumulators
        metric_data = defaultdict(list)
        
        # Collect all metric values for the day
        for row in monthly_rows:
            for column, value in row.items():
                if column == date_column:
                    continue
                
                # Skip null/empty values
                if not value or value.strip() == '':
                    continue
                
                # Try to convert to numeric value
                try:
                    numeric_value = float(value)
                    metric_data[column].append(numeric_value)
                except ValueError:
                    # Skip non-numeric values
                    continue
        
        # Calculate averages for each metric
        monthly_averages = {'date': parsed_date.strftime('%Y-%m-%d')}
        
        for metric, values in metric_data.items():
            if values:  # Only include metrics with valid values
                average = sum(values) / len(values)
                monthly_averages[metric] = round(average, 2)

        # Add city information if available
        if city:
            monthly_averages['city'] = city
        
        return monthly_averages
    
    def get_available_metrics(self, normalized_data: Dict[str, Any]) -> List[str]:
        """Get list of available metrics from normalized data.
        
        Extracts the list of metrics that have valid data from
        the normalized CSV data.
        
        Args:
            normalized_data: Normalized CSV data dictionary
            
        Returns:
            List of available metric names
        """
        if not normalized_data or 'monthly_data' not in normalized_data:
            return []
        
        if not normalized_data['monthly_data']:
            return []
        
        # Get metrics from the first monthly data entry
        first_entry = normalized_data['monthly_data'][0]
        metrics = [key for key in first_entry.keys() if key != 'date']
        
        return sorted(metrics)
    
    def filter_by_metric(self, normalized_data: Dict[str, Any], 
                        target_metric: str) -> Optional[Dict[str, Any]]:
        """Filter normalized data to include only a specific metric.
        
        Creates a filtered version of the normalized data that
        includes only the specified metric and date information.
        
        Args:
            normalized_data: Normalized CSV data dictionary
            target_metric: Name of the metric to include
            
        Returns:
            Filtered data dictionary or None if metric not found
        """
        if not normalized_data or 'monthly_data' not in normalized_data:
            return None
        
        # Check if metric exists in the data
        if not normalized_data['monthly_data']:
            return None
        
        first_entry = normalized_data['monthly_data'][0]
        if target_metric not in first_entry:
            return None
        
        # Create filtered data
        filtered_data = {
            'filename': normalized_data['filename'],
            'metric': target_metric,
            'monthly_data': []
        }
        
        for entry in normalized_data['monthly_data']:
            if target_metric in entry:
                filtered_entry = {
                    'date': entry['date'],
                    'value': entry[target_metric],
                    'city': entry.get('city', 'Unknown')
                }
                filtered_data['monthly_data'].append(filtered_entry)
        
        return filtered_data if filtered_data['monthly_data'] else None 