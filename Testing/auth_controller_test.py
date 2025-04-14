import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import session
from app.controllers.auth_controller import auth_bp
from flask import Flask

# ------------------ FIXTURE SETUP ------------------

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.secret_key = "test_secret_key"
    app.register_blueprint(auth_bp, url_prefix="/auth")
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# ------------------ TEST: SIGNUP ------------------

@patch("app.controllers.auth_controller.AuthService.signup")
def test_signup_get(mock_signup, client):
    response = client.get("/auth/signup")
    assert response.status_code == 200
    assert b"<form" in response.data or b"signup" in response.data

@patch("app.controllers.auth_controller.AuthService.signup")
def test_signup_post_success(mock_signup, client):
    mock_signup.return_value = True
    form_data = {
        "first-name": "John",
        "last-name": "Doe",
        "email": "john@example.com",
        "password": "password"
    }
    response = client.post("/auth/signup", data=form_data)
    assert response.status_code == 302
    assert "/auth/login" in response.location

@patch("app.controllers.auth_controller.AuthService.signup")
def test_signup_post_failure(mock_signup, client):
    mock_signup.return_value = False
    form_data = {
        "first-name": "John",
        "last-name": "Doe",
        "email": "john@example.com",
        "password": "password"
    }
    response = client.post("/auth/signup", data=form_data)
    assert response.status_code == 200
    assert b"<form" in response.data or b"signup" in response.data

# ------------------ TEST: LOGIN ------------------

@patch("app.controllers.auth_controller.AuthService.login")
def test_login_get_without_session(mock_login, client):
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert b"<form" in response.data or b"login" in response.data

@patch("app.controllers.auth_controller.AuthService.login")
def test_login_get_with_session(mock_login, client, app):
    with client.session_transaction() as sess:
        sess["user"] = "john@example.com"
    response = client.get("/auth/login")
    assert response.status_code == 302
    assert "/data/home" in response.location

@patch("app.controllers.auth_controller.AuthService.login")
def test_login_post_success(mock_login, client):
    mock_user = MagicMock()
    mock_user.email = "john@example.com"
    mock_login.return_value = mock_user

    form_data = {
        "email": "john@example.com",
        "password": "password"
    }
    response = client.post("/auth/login", data=form_data)
    assert response.status_code == 302
    assert "/data/home" in response.location
    with client.session_transaction() as sess:
        assert sess["user"] == "john@example.com"

@patch("app.controllers.auth_controller.AuthService.login")
def test_login_post_failure(mock_login, client):
    mock_login.return_value = None
    form_data = {
        "email": "john@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", data=form_data)
    assert response.status_code == 200
    assert b"<form" in response.data or b"login" in response.data

# ------------------ TEST: LOGOUT ------------------

def test_logout(client):
    with client.session_transaction() as sess:
        sess["user"] = "john@example.com"
    response = client.get("/auth/logout")
    assert response.status_code == 302
    assert "/auth/login" in response.location
    with client.session_transaction() as sess:
        assert "user" not in sess
