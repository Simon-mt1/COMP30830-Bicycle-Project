"""
prediction_service.py

Provides prediction functionality for bike availability using weather and station data.
"""

import pickle
import pandas as pd
from app.services.weather_service import WeatherService
import os
from datetime import datetime

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
        now = datetime.now()
        day_of_week = now.isoweekday()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        full_weather_data = WeatherService.getWeatherData()

        # Get the first day's weather data
        first_day_key = next(iter(full_weather_data["weather_data"]))
        hourly_data = full_weather_data["weather_data"][first_day_key]

        prediction_dict = {}
        
        for i in range(1,len(hourly_data)):
            pred_hour = hourly_data[i]

            weather_features = {
                "max_air_temperature_celsius": pred_hour.get("temp", 0),
                "max_relative_humidity_percent": pred_hour.get("humidity", 0)
            }
            
            future_hour = hour+i

            input_data = pd.DataFrame([{'station_id': data['number'], 'num_docks_available': data['bike_stands']
                                    , 'lat':data['lat'], 'lon':data['lon'], 'capacity':data['capacity'],'stno':data['number']
                                    ,'year':year,'month':month,'day':day, 'hour':future_hour,
                                    'minute':minute, 'max_air_temperature_celsius':weather_features['max_air_temperature_celsius']
                                    ,'max_relative_humidity_percent':weather_features['max_relative_humidity_percent'],'Weekday': day_of_week}])
        
            prediction = model.predict(input_data)
            busy_flag = float(prediction)
            prediction_dict[future_hour]= busy_flag

        return prediction_dict