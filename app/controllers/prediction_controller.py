from flask import Flask, request, jsonify, Blueprint
from app.services.bike_prediction_service import BikePredictionService

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST', 'GET'])
def predict():
    data = request.get_json()
    # Get data sent by the frontend
    # Call the service to get prediction
    prediction = BikePredictionService.predict_bike_availability(data)
    # Return the prediction result
    return jsonify({'prediction': prediction})


