"""
user.py

Defines the User model for the application's database using SQLAlchemy ORM.

Attributes:
    id (int): Primary key, auto-incremented.
    firstname (str): User's first name.
    lastname (str): User's last name.
    email (str): User's unique email address.
    password (str): User's hashed password.
"""

from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    """
    Represents a user of the application.

    Args:
        firstname (str): The user's first name.
        lastname (str): The user's last name.
        email (str): The user's email address.
        password (str): The user's hashed password.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(256), nullable=False)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

    def __repr__(self):
        """
        Returns a string representation of the user.

        Returns:
            str: Formatted string with the user's email.
        """
        return f'<User {self.email!r}>'
