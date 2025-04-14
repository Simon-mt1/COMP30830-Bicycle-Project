import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, Mock
import requests
from app.services.bike_service import BikeService

class TestBikeService:
    
    @patch('app.services.bike_service.requests.get')
    def test_getJCDecauxData_success(self, mock_get):
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "number": 42,
                "name": "Test Station",
                "address": "Test Address",
                "position": {
                    "lat": 53.349562,
                    "lng": -6.278198
                },
                "bike_stands": 30,
                "available_bike_stands": 15,
                "available_bikes": 15,
                "status": "OPEN",
                "last_update": 1586948036000
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Act
        result = BikeService.getJCDecauxData()
        
        # Assert
        assert result is not None
        assert len(result) == 1
        assert result[0]['number'] == 42
        assert result[0]['name'] == "Test Station"
        assert result[0]['available_bikes'] == 15
        
    @patch('app.services.bike_service.requests.get')
    def test_getJCDecauxData_http_error(self, mock_get):
        # Arrange
        mock_get.side_effect = requests.exceptions.HTTPError("404 Client Error")
        
        # Act
        result = BikeService.getJCDecauxData()
        
        # Assert
        assert result is None
        
    @patch('app.services.bike_service.requests.get')
    def test_getJCDecauxData_connection_error(self, mock_get):
        # Arrange
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")
        
        # Act
        result = BikeService.getJCDecauxData()
        
        # Assert
        assert result is None
        
    @patch('app.services.bike_service.requests.get')
    def test_getJCDecauxData_timeout_error(self, mock_get):
        # Arrange
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        # Act
        result = BikeService.getJCDecauxData()
        
        # Assert
        assert result is None
        
    @patch('app.services.bike_service.requests.get')
    def test_getJCDecauxData_unexpected_error(self, mock_get):
        # Arrange
        mock_get.side_effect = Exception("Unexpected error")
        
        # Act
        result = BikeService.getJCDecauxData()
        
        # Assert
        assert result is None
        
    @patch('app.services.bike_service.requests.get')
    @patch('app.services.bike_service.env.JCDECAUX', {
        "URL": "https://api.jcdecaux.com/vls/v1/stations",
        "API_KEY": "test_api_key",
        "CONTRACT": "Dublin"
    })
    def test_getJCDecauxData_correct_parameters(self, mock_get):
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Act
        BikeService.getJCDecauxData()
        
        # Assert
        mock_get.assert_called_once_with(
            "https://api.jcdecaux.com/vls/v1/stations",
            params={
                "apiKey": "test_api_key",
                "contract": "Dublin"
            }
        )
        
    @patch('app.services.bike_service.requests.get')
    def test_getJCDecauxData_empty_response(self, mock_get):
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Act
        result = BikeService.getJCDecauxData()
        
        # Assert
        assert result is not None
        assert len(result) == 0
        assert isinstance(result, list)