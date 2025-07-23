"""
Color utility functions for weather dashboard styling.

Centralizes color calculation logic used across multiple widget classes.
Eliminates duplication and provides consistent color determination patterns.
"""

from typing import Any, Optional
import re

from WeatherDashboard import styles


def get_metric_color(metric_key: str, value: Any, unit_system: str) -> str:
    """Centralized color determination for metric values.
    
    Args:
        metric_key: The metric to get color for
        value: Current metric value
        unit_system: Current unit system ('metric' or 'imperial')
        
    Returns:
        str: Color name for the metric value
    """
    if value is None:
        return "darkslategray"
    
    color_config = styles.METRIC_COLOR_RANGES.get(metric_key)
    if not color_config:
        return "darkslategray"
    
    # Choose appropriate ranges based on unit system
    if color_config.get('unit_dependent', False) and unit_system == 'imperial':
        ranges = color_config.get('imperial_ranges', color_config['ranges'])
    else:
        ranges = color_config['ranges']
    
    # Find appropriate color based on value
    try:
        numeric_value = float(value)
        for threshold, color in ranges:
            if numeric_value <= threshold:
                return color
        return ranges[-1][1]
    except (ValueError, TypeError):
        return "black"


def get_enhanced_temperature_color(temp_text: str, unit_system: str) -> str:
    """Get color for enhanced temperature display based on content.
    
    Args:
        temp_text: Enhanced temperature text (e.g., "75°F (feels 78°F ↑)")
        unit_system: Current unit system
        
    Returns:
        str: Color name for the enhanced temperature display
    """
    if not temp_text or temp_text == "--":
        return "darkslategray"
    
    # Extract actual temperature for base color
    temp_match = re.search(r'^(-?\d+\.?\d*)', temp_text)
    if temp_match:
        actual_temp = float(temp_match.group())
        base_color = get_metric_color('temperature', actual_temp, unit_system)
        
        # Check for "feels like" indicators
        if 'feels' in temp_text:
            difference_match = re.search(r'feels (-?\d+\.?\d*)', temp_text)
            if difference_match:
                feels_temp = float(difference_match.group(1))
                difference = abs(feels_temp - actual_temp)
                
                # Determine enhancement based on difference and direction
                TEMP_DIFF_THRESHOLD_METRIC = 5.0  # °C
                TEMP_DIFF_THRESHOLD_IMPERIAL = 9.0 # °F
                threshold_large = TEMP_DIFF_THRESHOLD_METRIC if unit_system == 'metric' else TEMP_DIFF_THRESHOLD_IMPERIAL
                
                if '↑' in temp_text:  # Feels warmer
                    if difference >= threshold_large:
                        return styles.TEMPERATURE_DIFFERENCE_COLORS['significant_warmer']
                    else:
                        return styles.TEMPERATURE_DIFFERENCE_COLORS['slight_warmer']
                elif '↓' in temp_text:  # Feels cooler
                    if difference >= threshold_large:
                        return styles.TEMPERATURE_DIFFERENCE_COLORS['significant_cooler']
                    else:
                        return styles.TEMPERATURE_DIFFERENCE_COLORS['slight_cooler']
        
        return base_color  # Use base temperature color if no significant difference
    
    return "darkslategray"


def extract_numeric_value(formatted_text: str) -> Optional[float]:
    """Extract numeric value from formatted metric text.
    
    Args:
        formatted_text: Formatted text like "75.2°F" or "85%"
        
    Returns:
        float: Extracted numeric value, or None if extraction fails
    """
    if not formatted_text or formatted_text == "--":
        return None
    
    match = re.search(r'-?\d+\.?\d*', formatted_text)
    if match:
        try:
            return float(match.group())
        except ValueError:
            return None
    return None