"""
routes.py

Defines and configures the Flask application instance, including session settings
and blueprint registration.

Functions:
    create_app(): Factory function that creates and returns the Flask app.
"""

from flask import Flask
from app.controllers.auth_controller import auth_bp
from app.controllers.data_controller import data_bp
from datetime import timedelta

def create_app():
    """
    Creates and configures the Flask Flask application.

    - Sets the secret key for session management.
    - Sets session lifetime to 10 minutes.
    - Registers `auth` and `data` blueprints.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)

    app.secret_key = "hello"
    app.permanent_session_lifetime = timedelta(minutes=10)

    app.register_blueprint(auth_bp)
    app.register_blueprint(data_bp)

    return app
