import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-uninet")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-key-uninet")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///uninet.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
