"""
CSV color generation utilities.

This module provides utilities for generating random colors for CSV
chart lines, ensuring good contrast and visual distinction between
different data series.

Classes:
    CSVColorGenerator: Main color generator for CSV chart lines
"""

import random
import colorsys
from typing import List, Dict, Tuple, Any

from WeatherDashboard.utils.logger import Logger


class CSVColorGenerator:
    """Generates random colors for CSV chart lines with good contrast.
    
    Creates visually distinct colors for different CSV data series,
    ensuring good contrast and readability. Supports color caching
    and provides methods for generating color palettes.
    
    Attributes:
        logger: Application logger instance
        used_colors: Set of colors already in use
        color_cache: Dictionary mapping CSV filenames to colors
        base_colors: List of predefined base colors for consistency
    """
    
    def __init__(self) -> None:
        """Initialize the CSV color generator.
        
        Sets up base colors, color caching, and logging for
        color generation operations.
        """
        self.logger = Logger()
        
        # Track used colors to avoid duplicates
        self.used_colors: set = set()
        self.color_cache: Dict[str, str] = {}
        
        # Predefined base colors for consistency
        self.base_colors = [
            '#1f77b4',  # Blue
            '#ff7f0e',  # Orange
            '#2ca02c',  # Green
            '#d62728',  # Red
            '#9467bd',  # Purple
            '#8c564b',  # Brown
            '#e377c2',  # Pink
            '#7f7f7f',  # Gray
            '#bcbd22',  # Olive
            '#17becf',  # Cyan
        ]
    
    def get_color_for_csv(self, filename: str) -> str:
        """Get a color for a specific CSV file.
        
        Returns a cached color if the file already has one,
        otherwise generates a new color and caches it.
        
        Args:
            filename: Name of the CSV file
            
        Returns:
            Hex color string for the CSV file
        """
        # Check if color is already cached
        if filename in self.color_cache:
            return self.color_cache[filename]
        
        # Generate new color
        color = self._generate_new_color()
        
        # Cache the color
        self.color_cache[filename] = color
        self.used_colors.add(color)
        
        self.logger.debug(f"Generated color {color} for CSV file {filename}")
        return color
    
    def _generate_new_color(self) -> str:
        """Generate a new color that contrasts well with existing colors.
        
        Creates a color that is visually distinct from already
        used colors, prioritizing good contrast and readability.
        
        Returns:
            Hex color string
        """
        # Try base colors first
        for base_color in self.base_colors:
            if base_color not in self.used_colors:
                return base_color
        
        # Generate random color with good saturation and value
        attempts = 0
        max_attempts = 50
        
        while attempts < max_attempts:
            # Generate HSV color with good saturation and value
            hue = random.random()
            saturation = random.uniform(0.6, 1.0)  # Good saturation
            value = random.uniform(0.7, 1.0)       # Good brightness
            
            # Convert to RGB
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            
            # Convert to hex
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb[0] * 255),
                int(rgb[1] * 255),
                int(rgb[2] * 255)
            )
            
            # Check if color is distinct enough from used colors
            if self._is_color_distinct(hex_color):
                return hex_color
            
            attempts += 1
        
        # Fallback: generate a simple random color
        return '#{:06x}'.format(random.randint(0, 0xFFFFFF))
    
    def _is_color_distinct(self, color: str, min_distance: float = 0.3) -> bool:
        """Check if a color is distinct enough from already used colors.
        
        Calculates color distance using RGB space and ensures
        the new color is sufficiently different from existing ones.
        
        Args:
            color: Hex color string to check
            min_distance: Minimum distance threshold (0.0-1.0)
            
        Returns:
            True if color is distinct enough, False otherwise
        """
        if not self.used_colors:
            return True
        
        # Convert hex to RGB
        color_rgb = self._hex_to_rgb(color)
        
        # Check distance from all used colors
        for used_color in self.used_colors:
            used_rgb = self._hex_to_rgb(used_color)
            distance = self._color_distance(color_rgb, used_rgb)
            
            if distance < min_distance:
                return False
        
        return True
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color string to RGB tuple.
        
        Args:
            hex_color: Hex color string (e.g., '#ff0000')
            
        Returns:
            RGB tuple (r, g, b) with values 0-255
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _color_distance(self, rgb1: Tuple[int, int, int], 
                       rgb2: Tuple[int, int, int]) -> float:
        """Calculate distance between two RGB colors.
        
        Uses Euclidean distance in RGB space to measure
        color similarity.
        
        Args:
            rgb1: First RGB color tuple
            rgb2: Second RGB color tuple
            
        Returns:
            Distance value (0.0-1.0, where 0.0 is identical)
        """
        # Normalize RGB values to 0-1
        r1, g1, b1 = [x/255.0 for x in rgb1]
        r2, g2, b2 = [x/255.0 for x in rgb2]
        
        # Calculate Euclidean distance
        distance = ((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)**0.5
        
        return distance
    
    def get_color_palette(self, num_colors: int) -> List[str]:
        """Generate a color palette with the specified number of colors.
        
        Creates a set of visually distinct colors suitable for
        charting multiple data series.
        
        Args:
            num_colors: Number of colors to generate
            
        Returns:
            List of hex color strings
        """
        colors = []
        
        for i in range(num_colors):
            if i < len(self.base_colors):
                # Use base colors first
                colors.append(self.base_colors[i])
            else:
                # Generate additional colors
                color = self._generate_new_color()
                colors.append(color)
                self.used_colors.add(color)
        
        return colors
    
    def clear_cache(self) -> None:
        """Clear the color cache and used colors set.
        
        Resets the color generator to its initial state,
        allowing colors to be reassigned.
        """
        self.used_colors.clear()
        self.color_cache.clear()
        self.logger.info("Color cache cleared")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about the current color cache.
        
        Returns:
            Dictionary containing cache statistics
        """
        return {
            'cached_files': list(self.color_cache.keys()),
            'cache_size': len(self.color_cache),
            'used_colors_count': len(self.used_colors),
            'base_colors_available': len(self.base_colors)
        }
    
    def get_color_for_city(self, filename: str, city: str) -> str:
        """Get a unique color for a city within a CSV file.
        
        Args:
            filename: Name of the CSV file
            city: Name of the city
            
        Returns:
            Hex color string for the city
        """
        # Create a unique key for this city in this file
        key = f"{filename}_{city}"
        
        if key not in self.color_cache:
            # Generate a new color
            color = self._generate_new_color()
            self.color_cache[key] = color
            self.logger.debug(f"Generated color {color} for city {city} in {filename}")
        
        return self.color_cache[key]