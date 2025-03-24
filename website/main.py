from flask import Flask, render_template, request, redirect, url_for, session
import requests
import datetime
import database
from database import db_session
from models.user import User
from datetime import timedelta
import env


app = Flask(__name__)

app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes= 10)

engine = database.init_db()

# Fetch data from JCDecaux API
def getJCDecauxData():
    jcdecaux = env.JCDECAUX

    try:
        response = requests.get(jcdecaux["URL"], params={"apiKey": jcdecaux["API_KEY"], "contract": jcdecaux["CONTRACT"]})
        response.raise_for_status()
        data = response.json()
        #print("Fetched Data:", data)
        return data
    except requests.RequestException as e: 
        print(f"Error fetching data: {e}")
        return None
    
def getWeatherData():
    openWeather = env.OPEN_WEATHER

    try:
        response = requests.get(openWeather["URL"]["DATA"], 
                                params={"appid": openWeather["API_KEY"], 
                                        "lat": openWeather["LATITUDE"], 
                                        "lon" : openWeather["LONGITUDE"], 
                                        "units" : openWeather["UNITS"]})

        response.raise_for_status()
        data = response.json()
        data["main"]["temp"] = int(str(data["main"]["temp"]).split('.')[0])
        icon = openWeather["URL"]["ICON"] + data["weather"][0]["icon"] + ".png"
        data["icon"] = icon
        print("Fetched Data:", data)
        return data
    except requests.RequestException as e: 
        print(f"Error fetching data: {e}")
        return None    

@app.route("/map")
def map():
    if "user" in session:
        googleMapApiKey = env.GOOGLE_MAPS["API_KEY"]
        jcdecauxData = getJCDecauxData()
        weatherData = getWeatherData()
        if not jcdecauxData or not weatherData:
            return "Error fetching data", 500
        else: 
            for station in jcdecauxData:
                station['last_update'] = datetime.datetime.fromtimestamp(int(station['last_update'])/1000, tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

            return render_template('map.html', jcdecauxData = jcdecauxData, weatherData = weatherData, googleMapApiKey = googleMapApiKey)
    else:
        return redirect('/')

@app.route("/index")
def index():
    if "user" in session:
        return render_template('index.html')
    else:
        return redirect('/')
    
@app.route("/signup", methods = ["POST", "GET"])
def signup():
    is_active = True
    if request.method == "POST":
        result = User.query.filter(User.email == request.form["email"]).all()
        if len(result) != 0:
            is_active = False
        else:
            u = User(request.form["first-name"], request.form["last-name"], request.form["email"], request.form["password"])
            db_session.add(u)
            db_session.commit()
            return redirect(url_for('index'))
    return render_template('signup.html', is_active = is_active)

@app.route("/login", methods = ["POST", "GET"])
def login():
    is_active = True
    if request.method == "POST":
        result = User.query.filter(User.email == request.form["email"]).first()
        if request.form["email"] != result.email or request.form["password"] != result.password:
            is_active = False
            return render_template('login.html', is_active = is_active)
        else:
            session.permanent = True
            session["user"] = result.email
            return redirect(url_for('index'))
    else:
        if "user" in session:
            return redirect(url_for('index'))
        return render_template('login.html', is_active = is_active)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/")
def start():
    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

   
    
