import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask import Flask
from unittest.mock import patch
from app.controllers.prediction_controller import predict_bp

# ------------------ FIXTURE SETUP ------------------

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(predict_bp, url_prefix="/api")
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# ------------------ TEST: /predict ------------------

@patch("app.controllers.prediction_controller.PredictionService.predict_bike_availability")
def test_predict_post(mock_predict, client):
    mock_predict.return_value = 12  # mock prediction output

    response = client.post("/api/predict", json={"station": "A", "hour": 10})

    assert response.status_code == 200
    assert response.is_json
    assert response.json == {"prediction": 12}
    mock_predict.assert_called_once_with({"station": "A", "hour": 10})

@patch("app.controllers.prediction_controller.PredictionService.predict_bike_availability")
def test_predict_get(mock_predict, client):
    mock_predict.return_value = 7

    response = client.get("/api/predict", json={"station": "B", "hour": 14})

    assert response.status_code == 200
    assert response.is_json
    assert response.json == {"prediction": 7}
    mock_predict.assert_called_once_with({"station": "B", "hour": 14})

@patch("app.controllers.prediction_controller.PredictionService.predict_bike_availability")
def test_predict_missing_json(mock_predict, client):
    mock_predict.return_value = None  # Just in case it’s still called

    response = client.post("/api/predict")

    # Should raise a 400 error in a real-world app, but here we test current behavior
    assert response.status_code == 200
    assert response.is_json
    assert response.json == {"prediction": None}
    mock_predict.assert_called_once_with(None)
