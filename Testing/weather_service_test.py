import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, Mock
import requests
from app.services.weather_service import WeatherService
import env

class TestWeatherService:
    
    @patch('app.services.weather_service.requests.get')
    @patch.dict('app.services.weather_service.env.OPEN_WEATHER', {
        "URL": {"ONECALL": "https://api.openweathermap.org/data/2.5/onecall", "ICON": "https://openweathermap.org/img/wn/"},
        "API_KEY": "fake_api_key",
        "LATITUDE": 53.3498,
        "LONGITUDE": -6.2603,
        "UNITS": "metric",
        "EXCLUDE": "minutely"
    })
    def test_get_weather_data_success(self, mock_get):
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {
            "hourly": [
                {"dt": 1618317040, "temp": 15, "weather": [{"icon": "10d"}], "wind_speed": 5},
                {"dt": 1618320640, "temp": 16, "weather": [{"icon": "10d"}], "wind_speed": 6}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Act
        result = WeatherService.getWeatherData()
        
        # Assert
        assert result is not None
        assert "weather_data" in result
        assert "currentIcon" in result
        assert len(result["weather_data"]) > 0
        assert result["currentIcon"] == "https://openweathermap.org/img/wn/10d.png"
        
    @patch('app.services.weather_service.requests.get')
    @patch.dict('app.services.weather_service.env.OPEN_WEATHER', {
        "URL": {"ONECALL": "https://api.openweathermap.org/data/2.5/onecall", "ICON": "https://openweathermap.org/img/wn/"},
        "API_KEY": "fake_api_key",
        "LATITUDE": 53.3498,
        "LONGITUDE": -6.2603,
        "UNITS": "metric",
        "EXCLUDE": "minutely"
    })
    def test_get_weather_data_http_error(self, mock_get):
        # Arrange
        mock_get.side_effect = requests.exceptions.HTTPError("404 Client Error")
        
        # Act
        result = WeatherService.getWeatherData()
        
        # Assert
        assert result is None
        
    @patch('app.services.weather_service.requests.get')
    @patch.dict('app.services.weather_service.env.OPEN_WEATHER', {
        "URL": {"ONECALL": "https://api.openweathermap.org/data/2.5/onecall", "ICON": "https://openweathermap.org/img/wn/"},
        "API_KEY": "fake_api_key",
        "LATITUDE": 53.3498,
        "LONGITUDE": -6.2603,
        "UNITS": "metric",
        "EXCLUDE": "minutely"
    })
    def test_get_weather_data_connection_error(self, mock_get):
        # Arrange
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")
        
        # Act
        result = WeatherService.getWeatherData()
        
        # Assert
        assert result is None
        
    @patch('app.services.weather_service.requests.get')
    @patch.dict('app.services.weather_service.env.OPEN_WEATHER', {
        "URL": {"ONECALL": "https://api.openweathermap.org/data/2.5/onecall", "ICON": "https://openweathermap.org/img/wn/"},
        "API_KEY": "fake_api_key",
        "LATITUDE": 53.3498,
        "LONGITUDE": -6.2603,
        "UNITS": "metric",
        "EXCLUDE": "minutely"
    })
    def test_get_weather_data_timeout_error(self, mock_get):
        # Arrange
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        # Act
        result = WeatherService.getWeatherData()
        
        # Assert
        assert result is None
        
    @patch('app.services.weather_service.requests.get')
    @patch.dict('app.services.weather_service.env.OPEN_WEATHER', {
        "URL": {"ONECALL": "https://api.openweathermap.org/data/2.5/onecall", "ICON": "https://openweathermap.org/img/wn/"},
        "API_KEY": "fake_api_key",
        "LATITUDE": 53.3498,
        "LONGITUDE": -6.2603,
        "UNITS": "metric",
        "EXCLUDE": "minutely"
    })
    def test_get_weather_data_unexpected_error(self, mock_get):
        # Arrange
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = Exception("Unexpected error")
        mock_get.return_value = mock_response
        
        # Act
        result = WeatherService.getWeatherData()
        
        # Assert
        assert result is None
        
    @patch('app.services.weather_service.requests.get')
    @patch.dict('app.services.weather_service.env.OPEN_WEATHER', {
        "URL": {"ONECALL": "https://api.openweathermap.org/data/2.5/onecall", "ICON": "https://openweathermap.org/img/wn/"},
        "API_KEY": "test_api_key",
        "LATITUDE": 53.3498,
        "LONGITUDE": -6.2603,
        "UNITS": "metric",
        "EXCLUDE": "minutely"
    })
    def test_get_weather_data_correct_parameters(self, mock_get):
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {
            "hourly": [
                {"dt": 1618317040, "temp": 15, "weather": [{"icon": "10d"}], "wind_speed": 5}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Act
        WeatherService.getWeatherData()
        
        # Assert
        mock_get.assert_called_once_with(
            "https://api.openweathermap.org/data/2.5/onecall",
            params={
                "appid": "test_api_key",
                "lat": 53.3498,
                "lon": -6.2603,
                "units": "metric",
                "exclude": "minutely"
            }
        )
        
    @patch('app.services.weather_service.requests.get')
    @patch.dict('app.services.weather_service.env.OPEN_WEATHER', {
        "URL": {"ONECALL": "https://api.openweathermap.org/data/2.5/onecall", "ICON": "https://openweathermap.org/img/wn/"},
        "API_KEY": "fake_api_key",
        "LATITUDE": 53.3498,
        "LONGITUDE": -6.2603,
        "UNITS": "metric",
        "EXCLUDE": "minutely"
    })
    def test_get_weather_data_empty_response(self, mock_get):
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {"hourly": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Act
        result = WeatherService.getWeatherData()
        
        # Assert
        assert result is not None
        assert len(result["weather_data"]) == 0
        assert isinstance(result["weather_data"], dict)
