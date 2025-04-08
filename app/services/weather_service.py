"""
weather_service.py

Provides functionality to fetch and format hourly weather data from OpenWeatherMap.
"""

import requests
import datetime
import env

class WeatherService:
    """
    Service class for retrieving and formatting weather data from OpenWeatherMap.
    """

    @staticmethod
    def getWeatherData():
        """
        Fetches 24-hour weather forecast data and organizes it by date.

        Returns:
            dict or None: A dictionary containing formatted weather data, current icon, and temperature,
                          or None if an error occurs during fetch.
        """
        try:
            response = requests.get(env.OPEN_WEATHER["URL"]["ONECALL"], 
                                    params={
                                        "appid": env.OPEN_WEATHER["API_KEY"], 
                                        "lat": env.OPEN_WEATHER["LATITUDE"], 
                                        "lon": env.OPEN_WEATHER["LONGITUDE"], 
                                        "units": env.OPEN_WEATHER["UNITS"], 
                                        "exclude": env.OPEN_WEATHER["EXCLUDE"]
                                    })
            response.raise_for_status()
            data = response.json()

            data["hourly"] = data["hourly"][0:24]
            currentDate = datetime.datetime.fromtimestamp(data["hourly"][0]["dt"]).strftime('%d-%m-%Y')
            currentIcon = f'{env.OPEN_WEATHER["URL"]["ICON"]}{data["hourly"][0]["weather"][0]["icon"]}.png'
            currentTemp = int(float(data["hourly"][0]["temp"]))

            weather_data = {currentDate: []}
            for item in data["hourly"]:
                date = datetime.datetime.fromtimestamp(item["dt"]).strftime('%d-%m-%Y')
                formatted_item = {
                    "temp": int(float(item["temp"])),
                    "wind_speed": item["wind_speed"],
                    "icon": f'{env.OPEN_WEATHER["URL"]["ICON"]}{item["weather"][0]["icon"]}.png',
                    "dt": datetime.datetime.fromtimestamp(item["dt"]).strftime('%H:%M'),
                    "rain": sum(item.get("rain", {}).values()) if "rain" in item else 0
                }
                if currentDate != date:
                    currentDate = date
                    weather_data[currentDate] = []
                weather_data[currentDate].append(formatted_item)

            weatherInfo = {
                "weather_data": weather_data,
                "currentIcon": currentIcon,
                "currentTemp": currentTemp
            }
            return weatherInfo
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
