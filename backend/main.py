"""Entry point for uvicorn - redirects to app.main."""
from app.main import app

# This allows running: uvicorn main:app --reload
# from the backend directory
