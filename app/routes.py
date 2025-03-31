from flask import Flask
from app.controllers.auth_controller import auth_bp
from app.controllers.data_controller import data_bp
from datetime import timedelta

def create_app():
    app = Flask(__name__)

    app.secret_key = "hello"
    app.permanent_session_lifetime = timedelta(minutes= 10)

    app.register_blueprint(auth_bp)
    app.register_blueprint(data_bp)

    return app