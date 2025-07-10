import random
from datetime import datetime, timedelta

class SampleWeatherGenerator:
    """Generates simulated metric weather data."""
    
    def __init__(self):
        """Initializes the generator with default units."""
        self.source_unit = "metric"
        self.random = random
    
    def generate(self, city, num_days=7):
        """Generates simulated weather data for a given city over a specified number of days."""
        data = []
        base_temp = self.random.randint(5, 30)               # Celsius
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