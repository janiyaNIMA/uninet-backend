import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from the backend .env file when running the app.
DOTENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv(DOTENV_PATH)

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-uninet")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-key-uninet")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is required for Neon PostgreSQL.")

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
