"""
database.py

Sets up the SQLAlchemy database engine, session, and base model for ORM mapping.
Also provides a utility function to initialize the database schema.

Based on the Flask-SQLAlchemy pattern:
https://flask.palletsprojects.com/en/stable/patterns/sqlalchemy/

Modules:
    - sqlalchemy: Provides core database tools and ORM capabilities.
    - pymysql: MySQL database driver (used via SQLAlchemy connection string).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
USER = os.getenv("MYSQL_DB_USERNAME")
PASSWORD = os.getenv("MYSQL_DB_PASSWORD")
URL = os.getenv("MYSQL_DB_URL")
PORT = int(os.getenv("MYSQL_DB_PORT"))
DB = os.getenv("MYSQL_DB_NAME")

# MySQL connection string using PyMySQL driver
connect_string = f"mysql+pymysql://{USER}:{PASSWORD}@{URL}:{PORT}/{DB}"

# Create SQLAlchemy engine
engine = create_engine(connect_string, echo=True)

# Configure a thread-safe scoped session
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# Base class for all ORM models
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """
    Initializes the database schema by importing models and creating tables.

    This function should be called once at app startup to ensure that all tables
    defined in models are created in the connected database.

    Imports:
        - app.models.user: Ensures the User model is registered before table creation.
    """
    import app.models.user
    Base.metadata.create_all(bind=engine)
