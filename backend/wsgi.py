"""
WSGI entry point for production deployment (Render, Gunicorn, etc.)
"""

from app import app

if __name__ == "__main__":
    app.run()
