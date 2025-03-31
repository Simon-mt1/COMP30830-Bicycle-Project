import requests
import datetime
import env

class WeatherService:
    @staticmethod
    def getWeatherData():
        try:
            response = requests.get(env.OPEN_WEATHER["URL"]["ONECALL"], 
                                    params={"appid": env.OPEN_WEATHER["API_KEY"], 
                                            "lat": env.OPEN_WEATHER["LATITUDE"], 
                                            "lon": env.OPEN_WEATHER["LONGITUDE"], 
                                            "units": env.OPEN_WEATHER["UNITS"], 
                                            "exclude": env.OPEN_WEATHER["EXCLUDE"]})
            response.raise_for_status()
            data = response.json()

            weather_data = {"hourly": []}
            for item in data["hourly"]:
                formatted_item = {
                    "temp": int(float(item["temp"])),
                    "wind_speed": item["wind_speed"],
                    "icon": f'{env.OPEN_WEATHER["URL"]["ICON"]}{item["weather"][0]["icon"]}.png',
                    "dt": datetime.datetime.fromtimestamp(item["dt"]).strftime('%H:%M'),
                    "rain": sum(item.get("rain", {}).values()) if "rain" in item else 0
                }
                weather_data["hourly"].append(formatted_item)

            return weather_data
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None