from app.routes import create_app
from database import init_db

app = create_app()

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=("cert.pem", "key.pem"))