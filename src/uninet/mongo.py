"""
MongoDB client + users collection helper.
Stores auth credentials only (username, email, hashed password, role).
All other app data stays in PostgreSQL (Neon).
"""
import os
from pathlib import Path
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import certifi

# Load environment variables from backend .env if not already loaded.
DOTENV_PATH = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(DOTENV_PATH)

# The env key has a double underscore: MONGODB__URL (fall back to MONGODB_URL if not found)
_MONGO_URL = os.environ.get("MONGODB__URL") or os.environ.get("MONGODB_URL", "")

_client: MongoClient | None = None


def get_mongo_client() -> MongoClient:
    global _client
    if not _MONGO_URL:
        raise RuntimeError("MONGODB_URL environment variable is required for MongoDB auth storage.")

    if _client is None:
        try:
            _client = MongoClient(
                _MONGO_URL,
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000,
                tls=True,
                tlsCAFile=certifi.where(),
            )
            # Validate the connection early so errors surface clearly during startup.
            _client.admin.command("ping")
        except Exception as exc:
            raise RuntimeError(
                "Unable to connect to MongoDB Atlas. "
                "Check MONGODB_URL, network access, Atlas IP allowlist, and TLS settings."
            ) from exc
    return _client


def get_users_collection():
    """Return the 'users' collection from the uninet database."""
    client = get_mongo_client()
    db = client["uninet"]
    users = db["users"]
    users.create_index("username", unique=True)
    users.create_index("email", unique=True)
    return users
