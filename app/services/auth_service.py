from app.models.user import User
from database import db_session
import hashlib

class AuthService:
    @staticmethod
    def signup(form_data):
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
        user = User.query.filter(User.email == form_data["email"]).first()
        if user and hashlib.sha256(form_data["password"].encode()).hexdigest() == user.password:
            return user
        return None