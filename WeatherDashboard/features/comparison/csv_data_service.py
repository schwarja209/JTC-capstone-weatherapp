"""
CSV data service for loading and caching CSV weather data.

This module provides services for monitoring CSV files in the comparison
directory, loading and parsing CSV data, and caching processed data
to avoid re-processing on subsequent loads.

Classes:
    CSVDataService: Main service for CSV file operations and caching
"""

import csv
import hashlib
from typing import Dict, List, Optional, Any
from pathlib import Path

from WeatherDashboard.utils.logger import Logger


class CSVDataService:
    """Service for loading, parsing, and caching CSV weather data.
    
    Monitors the comparison directory for CSV files, loads and parses
    CSV data, normalizes it to monthly averages, and caches the results
    to avoid re-processing. Handles file change detection and error
    reporting for malformed CSV files.
    
    Attributes:
        comparison_dir: Path to the comparison directory
        cache: Dictionary caching processed CSV data
        file_hashes: Dictionary tracking file modification times
        logger: Application logger instance
    """
    
    def __init__(self, comparison_dir: Optional[str] = None) -> None:
        """Initialize the CSV data service.
        
        Sets up the comparison directory path and initializes caching
        structures for processed CSV data and file modification tracking.
        
        Args:
            comparison_dir: Path to comparison directory (defaults to data/comparison)
        """
        self.logger = Logger()
        
        # Set comparison directory
        if comparison_dir:
            self.comparison_dir = Path(comparison_dir)
        else:
            # Default to data/comparison relative to project root
            project_root = Path(__file__).parent.parent.parent
            self.comparison_dir = project_root / "data" / "comparison"
        
        # Ensure directory exists
        self.comparison_dir.mkdir(parents=True, exist_ok=True)
        
        # Caching structures
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.file_hashes: Dict[str, str] = {}
        
    def get_available_csv_files(self) -> List[str]:
        """Get list of available CSV files in the comparison directory.
        
        Scans the comparison directory for CSV files and returns their
        filenames. Only includes files with .csv extension.
        
        Returns:
            List of CSV filenames found in the comparison directory
        """
        try:
            csv_files = []
            for file_path in self.comparison_dir.iterdir():
                if file_path.is_file() and file_path.suffix.lower() == '.csv':
                    csv_files.append(file_path.name)
            return sorted(csv_files)
        except Exception as e:
            self.logger.error(f"Error scanning comparison directory: {e}")
            return []
    
    def load_csv_data(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load and parse CSV data for a specific file.
        
        Loads the CSV file, parses its contents, validates the structure,
        and returns the processed data. Handles errors for malformed files
        and caches successful results.
        
        Args:
            filename: Name of the CSV file to load
            
        Returns:
            Dictionary containing parsed CSV data or None if loading failed
        """
        try:
            file_path = self.comparison_dir / filename
            
            # Check if file exists
            if not file_path.exists():
                self.logger.error(f"CSV file not found: {filename}")
                return None
            
            # Check if file has changed
            current_hash = self._get_file_hash(file_path)
            if filename in self.cache and filename in self.file_hashes:
                if self.file_hashes[filename] == current_hash:
                    # File hasn't changed, return cached data
                    return self.cache[filename]
            
            # Load and parse CSV
            data = self._parse_csv_file(file_path)
            if data is None:
                return None
            
            # Cache the result
            self.cache[filename] = data
            self.file_hashes[filename] = current_hash
            
            self.logger.info(f"Successfully loaded CSV data from {filename}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error loading CSV file {filename}: {e}")
            return None
    
    def _parse_csv_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse a CSV file and extract its data structure.
        
        Reads the CSV file, validates its structure, and extracts
        the headers and data rows. Handles various CSV formats and
        reports validation errors for malformed files.
        
        Args:
            file_path: Path to the CSV file to parse
            
        Returns:
            Dictionary containing parsed data or None if parsing failed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Get headers
                headers = reader.fieldnames
                if not headers:
                    self.logger.error(f"No headers found in CSV file: {file_path.name}")
                    return None
                
                # Read all rows
                rows = []
                for row_num, row in enumerate(reader, start=2):  # Start at 2 since row 1 is headers
                    if not self._validate_csv_row(row, headers, row_num):
                        continue
                    rows.append(row)
                
                if not rows:
                    self.logger.error(f"No valid data rows found in CSV file: {file_path.name}")
                    return None
                
                return {
                    'filename': file_path.name,
                    'headers': headers,
                    'data': rows,
                    'row_count': len(rows)
                }
                
        except UnicodeDecodeError:
            self.logger.error(f"Unicode decode error in CSV file: {file_path.name}")
            return None
        except Exception as e:
            self.logger.error(f"Error parsing CSV file {file_path.name}: {e}")
            return None
    
    def _validate_csv_row(self, row: Dict[str, str], headers: List[str], row_num: int) -> bool:
        """Validate a CSV row for required fields and data quality.
        
        Checks that the row has the expected number of columns and
        that required fields (like date) are present and valid.
        
        Args:
            row: Dictionary representing a CSV row
            headers: List of expected column headers
            row_num: Row number for error reporting
            
        Returns:
            True if row is valid, False otherwise
        """
        # Check that row has expected number of columns
        if len(row) != len(headers):
            self.logger.warn(f"Row {row_num} has {len(row)} columns, expected {len(headers)}")
            return False
        
        # Check for required date column
        date_columns = [h for h in headers if 'date' in h.lower()]
        if not date_columns:
            self.logger.warn(f"No date column found in CSV headers: {headers}")
            return False
        
        # Check that at least one date column has a value
        has_date = False
        for date_col in date_columns:
            if row.get(date_col) and row[date_col].strip():
                has_date = True
                break
        
        if not has_date:
            self.logger.warn(f"Row {row_num} has no valid date value")
            return False
        
        return True
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Generate a hash for file change detection.
        
        Creates a hash based on file modification time and size
        to detect when files have changed.
        
        Args:
            file_path: Path to the file to hash
            
        Returns:
            String hash representing file state
        """
        try:
            stat = file_path.stat()
            # Use modification time and file size for hash
            hash_data = f"{stat.st_mtime}_{stat.st_size}"
            return hashlib.md5(hash_data.encode()).hexdigest()
        except Exception as e:
            self.logger.error(f"Error generating file hash for {file_path}: {e}")
            return ""
    
    def clear_cache(self) -> None:
        """Clear all cached CSV data.
        
        Removes all cached data and file hashes, forcing
        re-loading of all CSV files on next access.
        """
        self.cache.clear()
        self.file_hashes.clear()
        self.logger.info("CSV data cache cleared")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about the current cache state.
        
        Returns:
            Dictionary containing cache statistics and file information
        """
        return {
            'cached_files': list(self.cache.keys()),
            'cache_size': len(self.cache),
            'file_hashes': list(self.file_hashes.keys())
        } 