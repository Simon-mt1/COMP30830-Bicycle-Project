from flask import Flask, render_template, jsonify
import requests
import datetime

app = Flask(__name__)

# API Details
API_KEY = "5c9e0c7fb93223989e7a2fc1f70f3527490cc1a6"  # Replace with actual key
CONTRACT = "dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"

# Fetch data from JCDecaux API
def fetch_data():
    try:
        response = requests.get(STATIONS_URI, params={"apiKey": API_KEY, "contract": CONTRACT})
        response.raise_for_status()
        data = response.json()
        #print("Fetched Data:", data)
        return data
    except requests.RequestException as e: 
        print(f"Error fetching data: {e}")
        return None

@app.route("/map")
def map():
    data = fetch_data()
    if not data:
        return "Error fetching data", 500
    else: 
        for station in data:
            #print(f"Before conversion: {station['last_update']} (Type: {type(station['last_update'])})")

            station['last_update'] = datetime.datetime.fromtimestamp(int(station['last_update'])/1000, tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            #print(f"after conversion: {station['last_update']} (Type: {type(station['last_update'])})")

        print("Data being sent to template:", data)

        return render_template('map.html', data=data)


@app.route("/api/data")
def api_data():
    data = fetch_data()
    if not data:
        return jsonify({"error": "Unable to fetch data"}), 500
    return jsonify(data)

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/login")
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
