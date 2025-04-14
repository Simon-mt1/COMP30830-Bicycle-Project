"""
env.py

Handles environment configuration and API key management using environment variables.

Uses:
    - python-dotenv: To load environment variables from a .env file
    - os: To access environment variables in Python

Attributes:
    JCDECAUX (dict): JCDecaux API configuration
    GOOGLE_MAPS (dict): Google Maps API configuration
    OPEN_WEATHER (dict): OpenWeather API configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file in project root
load_dotenv()

# JCDecaux API configuration
JCDECAUX = {
    "API_KEY": os.getenv("JCDECAUX_API_KEY"),
    "CONTRACT": "dublin",
    "URL": "https://api.jcdecaux.com/vls/v1/stations"
}

# Google Maps API configuration
GOOGLE_MAPS = {
    "API_KEY": os.getenv("GOOGLE_MAPS_API_KEY")
}

# OpenWeather API configuration
OPEN_WEATHER = {
    "API_KEY": os.getenv("OPEN_WEATHER_API_KEY"),
    "LATITUDE": 53.39,
    "LONGITUDE": -6.29,
    "UNITS": "Metric",
    "URL": {
        "ICON": "https://openweathermap.org/img/wn/",
        "ONECALL": "https://api.openweathermap.org/data/3.0/onecall"
    },
    "EXCLUDE": "current,minutely,daily,alerts"
}
