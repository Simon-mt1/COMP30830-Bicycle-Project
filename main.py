"""
main.py

Application entry point. Initializes the database and runs the Flask app with SSL.
"""

from app.routes import create_app
from database import init_db

# Create the Flask app
app = create_app()

if __name__ == "__main__":
    # Initialize database tables and schema
    init_db()

    # Run the Flask app with SSL enabled
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        ssl_context=("cert.pem", "key.pem")
    )
