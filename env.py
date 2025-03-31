import os
from dotenv import load_dotenv

load_dotenv()

JCDECAUX = {
    "API_KEY" : os.getenv("JCDECAUX_API_KEY"),
    "CONTRACT" : "dublin",
    "URL" : "https://api.jcdecaux.com/vls/v1/stations"
}

GOOGLE_MAPS = {
    "API_KEY" : os.getenv("GOOGLE_MAPS_API_KEY")
}

OPEN_WEATHER = {
    "API_KEY" : os.getenv("OPEN_WEATHER_API_KEY"),
    "LATITUDE" : 53.39,
    "LONGITUDE" : -6.29,
    "UNITS" : "Metric",
    "URL" : {
        "ICON" : "https://openweathermap.org/img/wn/",
        "ONECALL" : "https://api.openweathermap.org/data/3.0/onecall"
    },
    "EXCLUDE" : "current,minutely,daily,alerts"
}