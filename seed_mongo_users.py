"""
Seed two demo users into MongoDB:
  - jane / student123   (role: student)
  - leader / leader123  (role: society_leader)

Run: python seed_mongo_users.py
"""
import os
import sys
import uuid

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Load .env manually so MONGODB__URL is available
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from src.uninet.mongo import get_users_collection
from werkzeug.security import generate_password_hash

DEMO_USERS = [
    {
        "_id": str(uuid.uuid4()),
        "name": "Jane Doe",
        "username": "jane",
        "email": "jane@wusl.ac.lk",
        "password_hash": generate_password_hash("student123"),
        "role": "student",
    },
    {
        "_id": str(uuid.uuid4()),
        "name": "Asel Perera",
        "username": "leader",
        "email": "leader@wusl.ac.lk",
        "password_hash": generate_password_hash("leader123"),
        "role": "society_leader",
    },
]

def seed():
    col = get_users_collection()

    # Create unique indexes
    col.create_index("username", unique=True)
    col.create_index("email", unique=True)

    for user in DEMO_USERS:
        existing = col.find_one({"username": user["username"]})
        if existing:
            print(f"⏭   User '{user['username']}' already exists — skipping.")
            continue
        col.insert_one(user)
        print(f"✅  Inserted user '{user['username']}' (role: {user['role']})")

    print("\n🎉  MongoDB users seeded!")
    print("    Demo credentials:")
    print("      student:        jane / student123")
    print("      society_leader: leader / leader123")

if __name__ == "__main__":
    seed()
