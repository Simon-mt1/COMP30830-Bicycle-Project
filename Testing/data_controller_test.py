import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import session
from app.controllers.data_controller import data_bp
from flask import Flask

# ------------------ FIXTURE SETUP ------------------

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.secret_key = "test_secret_key"
    app.register_blueprint(data_bp, url_prefix="/data")
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# ------------------ TEST: /map ------------------

@patch("app.controllers.data_controller.BikeService.getJCDecauxData")
@patch("app.controllers.data_controller.WeatherService.getWeatherData")
@patch("app.controllers.data_controller.env")
def test_map_route_success(mock_env, mock_weather, mock_bike, client):
    mock_env.GOOGLE_MAPS = {"API_KEY": "fake_api_key"}
    
    mock_bike.return_value = [
        {"address": "A Street", "last_update": 1699999999999},
        {"address": "B Street", "last_update": 1698888888888}
    ]
    mock_weather.return_value = {"temp": 20, "desc": "Clear"}

    with client.session_transaction() as sess:
        sess["user"] = "test@example.com"

    response = client.get("/data/map")
    assert response.status_code == 200
    assert b"fake_api_key" in response.data or b"map" in response.data

@patch("app.controllers.data_controller.BikeService.getJCDecauxData")
@patch("app.controllers.data_controller.WeatherService.getWeatherData")
def test_map_route_data_fetch_error(mock_weather, mock_bike, client):
    mock_bike.return_value = None
    mock_weather.return_value = {"temp": 20}

    with client.session_transaction() as sess:
        sess["user"] = "test@example.com"

    response = client.get("/data/map")
    assert response.status_code == 500
    assert b"Error fetching data" in response.data

def test_map_route_unauthenticated(client):
    response = client.get("/data/map")
    assert response.status_code == 302
    assert "/auth/login" in response.location

# ------------------ TEST: /home ------------------

def test_home_authenticated(client):
    with client.session_transaction() as sess:
        sess["user"] = "test@example.com"
    response = client.get("/data/home")
    assert response.status_code == 200
    assert b"home" in response.data or b"dashboard" in response.data

def test_home_unauthenticated(client):
    response = client.get("/data/home")
    assert response.status_code == 302
    assert response.location.endswith("/")

# ------------------ TEST: / (root) ------------------

def test_root_authenticated(client):
    with client.session_transaction() as sess:
        sess["user"] = "test@example.com"
    response = client.get("/data/")
    assert response.status_code == 302
    assert "/data/home" in response.location

def test_root_unauthenticated(client):
    response = client.get("/data/")
    assert response.status_code == 302
    assert "/auth/login" in response.location

# ------------------ TEST: /faq ------------------

def test_faq_authenticated(client):
    with client.session_transaction() as sess:
        sess["user"] = "test@example.com"
    response = client.get("/data/faq")
    assert response.status_code == 200
    assert b"FAQ" in response.data or b"faq" in response.data

def test_faq_unauthenticated(client):
    response = client.get("/data/faq")
    assert response.status_code == 302
    assert "/auth/login" in response.location
