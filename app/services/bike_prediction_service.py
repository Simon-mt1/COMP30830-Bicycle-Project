import pickle
from sklearn.preprocessing import StandardScaler
from app.services.bike_service import BikeService
from app.services.weather_service import WeatherService
import pandas as pd
from datetime import datetime







with open(r"app\models\bike_availability_model.pkl", "rb") as file:
    model = pickle.load(file)
class BikePredictionService:
    def __init__(self):
        self.bike_service = BikeService()
        self.weather_service = WeatherService()
    @staticmethod
    def predict_bike_availability(data):
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        full_weather_data = WeatherService.getFullWeatherData()

        # Get the first day's weather data
        first_day_key = next(iter(full_weather_data["weather_data"]))
        hourly_data = full_weather_data["weather_data"][first_day_key]
        
        # Take the first hour's data only
        
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
                                    ,'max_relative_humidity_percent':weather_features['max_relative_humidity_percent'],'Weekday': 2}])
        
            prediction = model.predict(input_data)
            busy_flag = data['capacity']-float(prediction)
            prediction_dict[future_hour]= busy_flag


        return prediction_dict
