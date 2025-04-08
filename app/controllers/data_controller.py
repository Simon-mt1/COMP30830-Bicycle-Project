"""
data_controller.py

Defines routes related to maps, FAQs, and the homepage.

**Routes:**\n
- /map: Displays the Google Map with bike stations and weather info.\n
- /index: Dashboard/homepage after user login.\n
- /: Redirects to the login page.\n
- /faq: Displays the FAQ page.\n
"""

from flask import Blueprint, render_template, session, redirect, url_for
from app.services.weather_service import WeatherService
from app.services.bike_service import BikeService
import env

data_bp = Blueprint('data', __name__)

@data_bp.route("/map")
def map():
    """
    Route to display the interactive map with bike station and weather data.

    Checks if the user is authenticated, fetches JCDecaux bike data and weather
    data, formats them, and renders the map page. Redirects to login if user not in session.

    Returns:
        Response: Rendered map HTML page or redirect to login page.
    """
    if "user" in session:
        googleMapApiKey = env.GOOGLE_MAPS["API_KEY"]
        jcdecauxData = BikeService.getJCDecauxData()
        weatherData = WeatherService.getWeatherData()
        
        if not jcdecauxData or not weatherData:
            return "Error fetching data", 500
        
        for station in jcdecauxData:
            station['last_update'] = station['last_update'] // 1000
        
        jcdecauxData.sort(key=lambda item: item["address"])
        
        return render_template(
            'map.html',
            jcdecauxData=jcdecauxData,
            weatherData=weatherData,
            googleMapApiKey=googleMapApiKey
        )
    
    return redirect(url_for('auth.login'))

@data_bp.route("/index")
def index():
    """
    Route to render the main dashboard page.

    Only accessible if the user is logged in.

    Returns:
        Response: Rendered index page or redirect to root.
    """
    if "user" in session:
        return render_template('index.html')
    else:
        return redirect('/')

@data_bp.route("/")
def start():
    """
    Root route that redirects to the login page.

    Returns:
        Response: Redirect to login page.
    """
    return redirect(url_for("auth.login"))

@data_bp.route("/faq")
def faq():
    """
    Route to render the FAQ page.

    Returns:
        Response: Rendered FAQ HTML page.
    """
    return render_template("faq.html")
