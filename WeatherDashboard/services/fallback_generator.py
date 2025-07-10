from typing import List, Dict, Any
import random
from datetime import datetime, timedelta

class SampleWeatherGenerator:
    """Generates simulated metric weather data."""
    
    def __init__(self) -> None:
        """Initializes the generator with default units."""
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
        """Generates simulated weather data for a given city over a specified number of days."""
        data = []
        temp_min, temp_max = self.temp_ranges['default']
        base_temp = self.random.randint(temp_min, temp_max)
        for i in range(num_days):
            date = datetime.now() - timedelta(days=num_days - 1 - i)
            data.append({
                'date': date,
                'temperature': base_temp + self.random.randint(-15, 15),
                'humidity': self.random.randint(30, 90),     # %
                # TODO: 'precipitation': self.random.uniform(0, 2),  # All precipitation values and handling is on hold for now
                'conditions': self.random.choice(['Sunny', 'Cloudy', 'Rainy', 'Snowy']),
                'wind_speed': self.random.randint(0, 10),    # m/s
                'pressure': self.random.uniform(990, 1035)   # hPa
            })
        return data