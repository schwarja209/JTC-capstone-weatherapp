"""
Simulated weather data generation for fallback scenarios.

This module provides weather data simulation when live API data is unavailable.
Generates realistic weather patterns with randomized values within appropriate
ranges for different climate types and seasonal variations.

Classes:
    SampleWeatherGenerator: Main fallback weather data generator
"""

from typing import List, Dict, Any
import random
from datetime import datetime, timedelta

class SampleWeatherGenerator:
    """Generates simulated weather data for fallback scenarios.
    
    Creates realistic weather data when live API data is unavailable, using
    randomized values within appropriate ranges for different climate types.
    Provides consistent metric units and realistic weather patterns.
    
    Attributes:
        source_unit: Base unit system for generated data (always metric)
        temp_ranges: Temperature ranges for different climate types
        random: Random number generator for data variation
    """    
    def __init__(self) -> None:
        """Initialize the weather data generator.
        
        Sets up temperature ranges for different climate types, initializes
        random number generator, and configures base unit system for data generation.
        """
        self.source_unit = "metric"
        self.temp_ranges = {
            'default': (5, 30),      # Default range - Celsius
            'arctic': (-20, 10),     # Cold climates
            'tropical': (20, 40),    # Hot climates
            'desert': (15, 45),      # Very hot, dry climates
            'temperate': (0, 25)     # Moderate climates
        }
        self.random = random
    
    def generate(self, city: str, num_days: int = 7) -> List[Dict[str, Any]]:
        """Generate simulated weather data for a given city over a specified number of days.
        
        Creates realistic weather patterns with randomized values within appropriate
        ranges for different climate types. Uses base temperature with daily variations.
        
        Args:
            city: City name for weather data generation
            num_days: Number of days of historical data to generate (default 7)
            
        Returns:
            List[Dict[str, Any]]: List of weather data entries with date, temperature,
                                humidity, conditions, wind_speed, and pressure
        """
        data = []
        temp_min, temp_max = self.temp_ranges['default']
        base_temp = self.random.randint(temp_min, temp_max)
        for i in range(num_days):
            date = datetime.now() - timedelta(days=num_days - 1 - i)
            temp = base_temp + self.random.randint(-15, 15)
            humidity = self.random.randint(30, 90)     # %
            wind = self.random.randint(0, 10)          # %
            conditions = self.random.choice(['Sunny', 'Cloudy', 'Rainy', 'Snowy'])

            is_rainy = conditions == 'Rainy'
            is_snowy = conditions == 'Snowy'

            rain_amount = self.random.uniform(0.1, 5.0) if is_rainy else None
            snow_amount = self.random.uniform(0.1, 3.0) if is_snowy else None

            data.append({
                'date': date,
                # Original fields
                'temperature': temp,
                'humidity': humidity,
                'conditions': conditions,
                'wind_speed': wind,
                'pressure': self.random.uniform(990, 1035),  # hPa
                
                # Extended temperature metrics
                'feels_like': temp + self.random.randint(-3, 3),  # Slight variation from actual temp
                'temp_min': temp - self.random.randint(2, 8),     # Lower than current temp
                'temp_max': temp + self.random.randint(2, 8),     # Higher than current temp
                
                # Enhanced wind information
                'wind_direction': self.random.randint(0, 360),    # Random compass direction
                'wind_gust': wind + self.random.randint(0, 5) if wind > 0 else None,  # Gusts only if windy
                
                # Visibility and atmospheric conditions
                'visibility': self.random.randint(5000, 20000),   # 5-20km in meters
                'cloud_cover': self.random.randint(0, 100),       # 0-100% cloud cover
                
                # Simplified precipitation (new)
                'rain': rain_amount,
                'snow': snow_amount,
                
                # Keep detailed for completeness
                'rain_1h': rain_amount,
                'rain_3h': rain_amount * 3 if rain_amount else None,
                'snow_1h': snow_amount,
                'snow_3h': snow_amount * 3 if snow_amount else None,

                # Enhanced weather categorization
                'weather_main': conditions,
                'weather_id': self.random.choice([800, 801, 500, 600]) if conditions != 'Sunny' else 800,
                'weather_icon': self.random.choice(['01d', '02d', '10d', '13d']),

                # Add UV and Air Quality simulation
                'uv_index': self.random.randint(1, 11),  # UV index 1-11
                'air_quality_index': self.random.randint(1, 5),  # AQI 1-5
                'air_quality_description': self.random.choice(['Good', 'Fair', 'Moderate', 'Poor']),
                
                # Coordinates for consistency
                'latitude': 40.7128 + self.random.uniform(-0.1, 0.1),  # Near NYC
                'longitude': -74.0060 + self.random.uniform(-0.1, 0.1),

                # Derived comfort metrics simulation
                'heat_index': temp + self.random.uniform(0, 5) if temp > 20 else None,  # Only when warm
                'wind_chill': temp - self.random.uniform(2, 8) if temp < 10 and wind > 3 else None,  # Only when cold and windy
                'dew_point': temp - self.random.uniform(5, 15),  # Always present, typically lower than temp
                'precipitation_probability': self.random.uniform(10, 80),  # 10-80% chance
                'weather_comfort_score': self.random.uniform(30, 95)  # Comfort score 30-95
            })
        return data