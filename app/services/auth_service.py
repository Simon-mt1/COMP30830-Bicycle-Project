"""
auth_service.py

Provides authentication functionality for user signup and login.
"""

from app.models.user import User
from database import db_session
import hashlib

class AuthService:
    """
    Service class for handling authentication operations like signup and login.
    """

    @staticmethod
    def signup(form_data):
        """
        Registers a new user if the email doesn't already exist.

        Args:
            form_data (dict): Dictionary containing 'first-name', 'last-name', 'email', and 'password'.

        Returns:
            bool: True if signup is successful, False if user already exists.
        """
        existing_user = User.query.filter(User.email == form_data["email"]).first()
        if existing_user:
            return False
        new_user = User(
            form_data["first-name"],
            form_data["last-name"],
            form_data["email"],
            hashlib.sha256(form_data["password"].encode()).hexdigest()
        )
        db_session.add(new_user)
        db_session.commit()
        return True

    @staticmethod
    def login(form_data):
        """
        Authenticates a user based on email and password.

        Args:
            form_data (dict): Dictionary containing 'email' and 'password'.

        Returns:
            User or None: The User object if login is successful, None otherwise.
        """
        user = User.query.filter(User.email == form_data["email"]).first()
        if user and hashlib.sha256(form_data["password"].encode()).hexdigest() == user.password:
            return user
        return None
