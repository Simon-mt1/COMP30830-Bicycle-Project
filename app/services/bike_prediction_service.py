import pickle
from sklearn.preprocessing import StandardScaler
from app.services.bike_service import BikeService
from app.services.weather_service import WeatherService
import pandas as pd


with open(r"app\models\bike_availability_model.pkl", "rb") as file:
    model = pickle.load(file)
class BikePredictionService:
    def __init__(self):
        self.bike_service = BikeService()
        self.weather_service = WeatherService()
    @staticmethod
    def predict_bike_availability(data):
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

        input_data = pd.DataFrame([{'station_id': data['number'], 'num_docks_available': data['bike_stands']
                                    , 'lat':data['lat'], 'lon':data['lon'], 'capacity':data['capacity'],'stno':data['number']
                                    ,'year':2025,'month':4,'day':7, 'hour':17,
                                    'minute':44, 'max_air_temperature_celsius':weather_features['max_air_temperature_celsius']
                                    ,'max_relative_humidity_percent':weather_features['max_relative_humidity_percent'],'Weekday': 2}])
        
        prediction = model.predict(input_data)

        print(prediction[0])

        return prediction[0]
