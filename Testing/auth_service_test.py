import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Now your imports should work
from app.entities.user import User
from app.services.auth_service import AuthService

import pytest
import hashlib
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_db_session():
    """Mock db_session to avoid actual database operations during testing."""
    with patch('app.services.auth_service.db_session') as mock_session:
        yield mock_session

@pytest.fixture
def mock_user_query():
    """Mock User.query to control database query responses."""
    with patch('app.services.auth_service.User.query') as mock_query:
        yield mock_query

class TestAuthService:
    
    def test_signup_success(self, mock_db_session, mock_user_query):
        # Arrange
        mock_filter = MagicMock()
        mock_filter.first.return_value = None  # No existing user
        mock_user_query.filter.return_value = mock_filter
        
        form_data = {
            "first-name": "John",
            "last-name": "Doe",
            "email": "john.doe@example.com",
            "password": "secure_password"
        }
        
        # Act
        result = AuthService.signup(form_data)
        
        # Assert
        assert result is True
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        
    def test_signup_user_already_exists(self, mock_db_session, mock_user_query):
        # Arrange
        existing_user = User("John", "Doe", "john.doe@example.com", "hashed_password")
        mock_filter = MagicMock()
        mock_filter.first.return_value = existing_user  # User already exists
        mock_user_query.filter.return_value = mock_filter
        
        form_data = {
            "first-name": "John",
            "last-name": "Doe",
            "email": "john.doe@example.com",
            "password": "secure_password"
        }
        
        # Act
        result = AuthService.signup(form_data)
        
        # Assert
        assert result is False
        mock_db_session.add.assert_not_called()
        mock_db_session.commit.assert_not_called()
        
    def test_signup_password_hashing(self, mock_db_session, mock_user_query):
        # Arrange
        mock_filter = MagicMock()
        mock_filter.first.return_value = None
        mock_user_query.filter.return_value = mock_filter
        
        form_data = {
            "first-name": "Jane",
            "last-name": "Smith",
            "email": "jane.smith@example.com",
            "password": "test_password"
        }
        
        expected_hash = hashlib.sha256(form_data["password"].encode()).hexdigest()
        
        # Act
        AuthService.signup(form_data)
        
        # Assert
        # Get the User object that was passed to db_session.add
        called_args = mock_db_session.add.call_args[0][0]
        assert called_args.password == expected_hash
        
    def test_login_success(self, mock_user_query):
        # Arrange
        password = "test_password"
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        user = User("John", "Doe", "john.doe@example.com", hashed_password)
        mock_filter = MagicMock()
        mock_filter.first.return_value = user
        mock_user_query.filter.return_value = mock_filter
        
        form_data = {
            "email": "john.doe@example.com",
            "password": "test_password"
        }
        
        # Act
        result = AuthService.login(form_data)
        
        # Assert
        assert result == user
        
    def test_login_wrong_password(self, mock_user_query):
        # Arrange
        hashed_password = hashlib.sha256("correct_password".encode()).hexdigest()
        
        user = User("John", "Doe", "john.doe@example.com", hashed_password)
        mock_filter = MagicMock()
        mock_filter.first.return_value = user
        mock_user_query.filter.return_value = mock_filter
        
        form_data = {
            "email": "john.doe@example.com",
            "password": "wrong_password"
        }
        
        # Act
        result = AuthService.login(form_data)
        
        # Assert
        assert result is None
        
    def test_login_user_not_found(self, mock_user_query):
        # Arrange
        mock_filter = MagicMock()
        mock_filter.first.return_value = None  # User not found
        mock_user_query.filter.return_value = mock_filter
        
        form_data = {
            "email": "nonexistent@example.com",
            "password": "any_password"
        }
        
        # Act
        result = AuthService.login(form_data)
        
        # Assert
        assert result is None