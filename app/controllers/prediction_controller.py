"""
prediction_controller.py

Defines the route for predicting bike availability using the prediction service.

**Routes:**
- /predict: Accepts JSON input from frontend and returns bike availability prediction.
"""

from flask import Flask, request, jsonify, Blueprint
from app.services.prediction_service import PredictionService

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST', 'GET'])
def predict():
    """
    Route to handle bike availability prediction requests.

    Accepts POST or GET requests containing JSON input data,
    calls the prediction service, and returns the prediction result.

    **Returns:**
        Response: JSON object with predicted value.
    """
    data = request.get_json()
    prediction = PredictionService.predict_bike_availability(data)
    return jsonify({'prediction': prediction})
