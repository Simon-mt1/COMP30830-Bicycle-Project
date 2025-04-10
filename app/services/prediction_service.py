"""
prediction_service.py

Provides prediction functionality for bike availability using weather and station data.
"""

import pickle
import pandas as pd
from app.services.weather_service import WeatherService
import os

try:
    # Load the pre-trained prediction model
    with open(os.path.join("app", "models", "bike_availability_model.pkl"), "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    print("File not found")
    
class PredictionService:
    """
    Service class for predicting bike availability at a given station.
    """

    @staticmethod
    def predict_bike_availability(data):
        """
        Predicts the number of available bikes at a station based on current weather
        and station information.

        Args:
            data (dict): Dictionary containing:
                - number (int): Station number
                - bike_stands (int): Number of docks available
                - lat (float): Latitude of the station
                - lon (float): Longitude of the station
                - capacity (int): Total capacity of the station

        Returns:
            int: Predicted number of available bikes.
        """
        full_weather_data = WeatherService.getWeatherData()

        # Get the first day's weather data
        first_day_key = next(iter(full_weather_data["weather_data"]))
        hourly_data = full_weather_data["weather_data"][first_day_key]


        # Take the first hour's data only
        first_hour = hourly_data[0]

        weather_features = {
            "max_air_temperature_celsius": first_hour.get("temp", 0),
            "max_relative_humidity_percent": first_hour.get("humidity", 0)
        }

        input_data = pd.DataFrame([{
            'station_id': data['number'],
            'num_docks_available': data['bike_stands'],
            'lat': data['lat'],
            'lon': data['lon'],
            'capacity': data['capacity'],
            'stno': data['number'],
            'year': 2025,
            'month': 4,
            'day': 7,
            'hour': 17,
            'minute': 44,
            'max_air_temperature_celsius': weather_features['max_air_temperature_celsius'],
            'max_relative_humidity_percent': weather_features['max_relative_humidity_percent'],
            'Weekday': 2
        }])

        prediction = model.predict(input_data)
        return prediction[0]
