"""
Derived weather metric calculations.

This module provides functions to calculate derived weather metrics
from basic weather data including comfort indices and probability estimates.
All temperature inputs should be in the specified units per function.
"""

import math
from typing import Optional

class DerivedMetricsCalculator:
    """Calculate derived weather metrics from basic weather data.
    
    Provides comfort indices, probability estimates, and composite scores
    using standard meteorological formulas.
    """
    
    @staticmethod
    def calculate_heat_index(temp_f: float, humidity: float) -> Optional[float]:
        """Calculate heat index using the Rothfusz regression equation.
        
        Heat index represents how hot it feels when humidity is factored in.
        Only applicable when temperature >= 80°F.
        
        Args:
            temp_f: Temperature in Fahrenheit
            humidity: Relative humidity percentage (0-100)
            
        Returns:
            Heat index in Fahrenheit, or None if conditions don't warrant calculation
        """
        if temp_f < 80:
            return None
            
        # Rothfusz regression equation (NWS standard)
        hi = -42.379 + 2.04901523 * temp_f + 10.14333127 * humidity
        hi += -0.22475541 * temp_f * humidity - 6.83783e-3 * temp_f**2
        hi += -5.481717e-2 * humidity**2 + 1.22874e-3 * temp_f**2 * humidity
        hi += 8.5282e-4 * temp_f * humidity**2 - 1.99e-6 * temp_f**2 * humidity**2
        
        return hi
    
    @staticmethod
    def calculate_wind_chill(temp_f: float, wind_mph: float) -> Optional[float]:
        """Calculate wind chill using the NWS formula.
        
        Wind chill represents how cold it feels when wind is factored in.
        Only applicable when temperature <= 50°F and wind speed >= 3 mph.
        
        Args:
            temp_f: Temperature in Fahrenheit
            wind_mph: Wind speed in mph
            
        Returns:
            Wind chill in Fahrenheit, or None if conditions don't warrant calculation
        """
        if temp_f > 50 or wind_mph < 3:
            return None
            
        # NWS wind chill formula
        wc = 35.74 + 0.6215 * temp_f - 35.75 * (wind_mph ** 0.16)
        wc += 0.4275 * temp_f * (wind_mph ** 0.16)
        
        return wc
    
    @staticmethod
    def calculate_dew_point(temp_c: float, humidity: float) -> float:
        """Calculate dew point using the Magnus formula approximation.
        
        Dew point is the temperature at which air becomes saturated with moisture.
        
        Args:
            temp_c: Temperature in Celsius
            humidity: Relative humidity percentage (0-100)
            
        Returns:
            Dew point in Celsius
        """
        # Magnus formula approximation
        a = 17.27
        b = 237.7
        
        alpha = ((a * temp_c) / (b + temp_c)) + math.log(humidity / 100.0)
        dew_point = (b * alpha) / (a - alpha)
        
        return dew_point
    
    @staticmethod
    def calculate_precipitation_probability(pressure: float, humidity: float, conditions: str) -> float:
        """Estimate precipitation probability using atmospheric indicators.
        
        This is an algorithmic estimate based on pressure, humidity, and current
        conditions. Not a meteorological forecast.
        
        Args:
            pressure: Atmospheric pressure in hPa
            humidity: Relative humidity percentage (0-100)
            conditions: Current weather condition description
            
        Returns:
            Estimated precipitation probability (0-100%)
        """
        base_prob = 0
        
        # Pressure influence (lower pressure increases probability)
        if pressure < 1000:
            base_prob += (1000 - pressure) * 2
        
        # Humidity influence (higher humidity increases probability)
        if humidity > 70:
            base_prob += (humidity - 70) * 1.5
        
        # Current conditions influence
        rain_keywords = ['rain', 'drizzle', 'shower', 'thunderstorm']
        if any(keyword in conditions.lower() for keyword in rain_keywords):
            base_prob += 40
        elif 'cloud' in conditions.lower():
            base_prob += 15
        elif 'overcast' in conditions.lower():
            base_prob += 25
        
        return min(100, max(0, base_prob))
    
    @staticmethod
    def calculate_weather_comfort_score(temp_c: float, humidity: float, wind_speed: float, pressure: float) -> float:
        """Calculate composite weather comfort score.
        
        Combines temperature, humidity, wind, and pressure into a single
        comfort rating. Higher scores indicate more comfortable conditions.
        
        Args:
            temp_c: Temperature in Celsius
            humidity: Relative humidity percentage (0-100)
            wind_speed: Wind speed in m/s
            pressure: Atmospheric pressure in hPa
            
        Returns:
            Comfort score (0-100, where 100 is ideal conditions)
        """
        score = 100
        
        # Temperature comfort (ideal: 18-24°C)
        if temp_c < 18:
            score -= (18 - temp_c) * 3
        elif temp_c > 24:
            score -= (temp_c - 24) * 3
        
        # Humidity comfort (ideal: 40-60%)
        if humidity < 40:
            score -= (40 - humidity) * 1.5
        elif humidity > 60:
            score -= (humidity - 60) * 1.5
        
        # Wind comfort (ideal: light breeze)
        if wind_speed > 8:
            score -= (wind_speed - 8) * 5
        elif wind_speed < 0.5:
            score -= 10
        
        # Pressure stability (ideal: near standard atmosphere)
        pressure_diff = abs(pressure - 1013)
        if pressure_diff > 20:
            score -= (pressure_diff - 20) * 0.5
        
        return max(0, min(100, score))