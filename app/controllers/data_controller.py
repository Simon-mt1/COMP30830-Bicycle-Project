from flask import Blueprint, render_template, session, redirect, url_for
from app.services.weather_service import WeatherService
from app.services.bike_service import BikeService
import env

data_bp = Blueprint('data', __name__)

@data_bp.route("/charts")
def charts():
    weatherData = WeatherService.getWeatherData()
    return render_template('charts.html', weatherData=weatherData)

@data_bp.route("/map")
def map():
    if "user" in session:
        googleMapApiKey = env.GOOGLE_MAPS["API_KEY"]
        jcdecauxData = BikeService.getJCDecauxData()
        weatherData = WeatherService.getWeatherData()
        
        if not jcdecauxData or not weatherData:
            return "Error fetching data", 500
        
        for station in jcdecauxData:
            station['last_update'] = station['last_update'] // 1000
        
        jcdecauxData.sort(key=lambda item: item["address"])
        
        return render_template('map.html', jcdecauxData=jcdecauxData, weatherData=weatherData, googleMapApiKey=googleMapApiKey)
    
    return redirect(url_for('auth.login'))

@data_bp.route("/index")
def index():
    if "user" in session:
        return render_template('index.html')
    else:
        return redirect('/')
    
@data_bp.route("/")
def start():
    return redirect(url_for("auth.login"))

@data_bp.route("/faq")
def faq():
    return render_template("faq.html")