import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, Mock
from app.services.prediction_service import PredictionService

class TestPredictionService:

    @patch('app.services.prediction_service.WeatherService.getWeatherData')
    @patch('app.services.prediction_service.model')
    def test_predict_bike_availability_success(self, mock_model, mock_get_weather):
        # Arrange
        mock_model.predict.return_value = [10.4]

        mock_get_weather.return_value = {
            "weather_data": {
                "2025-04-13": [
                    {},  # 0th index will be skipped
                    {"temp": 15, "humidity": 70},
                    {"temp": 16, "humidity": 65},
                    {"temp": 17, "humidity": 60}
                ]
            }
        }

        sample_input = {
            "number": 42,
            "bike_stands": 30,
            "lat": 53.3498,
            "lon": -6.2603,
            "capacity": 20
        }

        # Act
        result = PredictionService.predict_bike_availability(sample_input)

        # Assert
        assert "availableBikes" in result
        assert "availableSpaces" in result
        assert isinstance(result["availableBikes"], dict)
        assert isinstance(result["availableSpaces"], dict)
        assert all(isinstance(v, int) for v in result["availableBikes"].values())
        assert all(isinstance(v, int) for v in result["availableSpaces"].values())

    @patch('app.services.prediction_service.WeatherService.getWeatherData')
    @patch('app.services.prediction_service.model')
    def test_predict_bike_availability_handles_missing_weather_data(self, mock_model, mock_get_weather):
        # Arrange
        mock_model.predict.return_value = [5.0]

        mock_get_weather.return_value = {
            "weather_data": {
                "2025-04-13": [{}]  # Only one entry, no usable hourly data
            }
        }

        sample_input = {
            "number": 10,
            "bike_stands": 25,
            "lat": 53.34,
            "lon": -6.26,
            "capacity": 20
        }

        # Act
        result = PredictionService.predict_bike_availability(sample_input)

        # Assert
        # Since the loop starts from 1 and there's no data beyond index 0, should return empty dicts
        assert result["availableBikes"] == {}
        assert result["availableSpaces"] == {}
