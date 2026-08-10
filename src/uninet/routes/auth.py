from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from src.uninet.models import db, User
from src.uninet.mongo import get_users_collection
import uuid

auth_bp = Blueprint('auth', __name__)


# ── Helper ────────────────────────────────────────────────────────────────────

def _user_to_response(user) -> dict:
    """Return profile data for the client without exposing password details."""
    return {
        "id": str(user.id),
        "name": user.full_name or user.username,
        "username": user.username,
        "email": user.email,
        "role": user.role or "student",
    }


def _get_profile_by_username(username: str):
    return User.query.filter_by(username=username).first()


# ── Routes ────────────────────────────────────────────────────────────────────

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name     = (data.get('name') or '').strip()
    username = (data.get('username') or '').strip().lower()
    email    = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not username or not email or not password:
        return jsonify({"status": "error", "message": "username, email and password are required"}), 400

    mongo_users = get_users_collection()
    if mongo_users.find_one({"username": username}):
        return jsonify({"status": "error", "message": "Username already taken"}), 409
    if mongo_users.find_one({"email": email}):
        return jsonify({"status": "error", "message": "Email already registered"}), 409

    user = User(
        username=username,
        email=email,
        role="student",
        full_name=name or username
    )
    db.session.add(user)
    db.session.commit()

    mongo_users.insert_one({
        "_id": str(uuid.uuid4()),
        "username": username,
        "email": email,
        "name": name or username,
        "password_hash": generate_password_hash(password),
        "role": "student"
    })

    token = create_access_token(
        identity=username,
        additional_claims={"role": user.role, "username": username}
    )
    return jsonify({
        "status": "success",
        "token": token,
        "user": _user_to_response(user)
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = (data.get('username') or '').strip().lower()
    password = data.get('password') or ''

    if not username or not password:
        return jsonify({"status": "error", "message": "username and password are required"}), 400

    mongo_users = get_users_collection()
    mongo_user = mongo_users.find_one({"username": username})
    if not mongo_user or not check_password_hash(mongo_user.get("password_hash", ""), password):
        return jsonify({"status": "error", "message": "Invalid username or password"}), 401

    user = _get_profile_by_username(username)
    if not user:
        user = User(
            username=username,
            email=mongo_user.get("email", ""),
            role=mongo_user.get("role", "student"),
            full_name=mongo_user.get("name", username)
        )
        db.session.add(user)
        db.session.commit()

    token = create_access_token(
        identity=username,
        additional_claims={"role": mongo_user.get("role", "student"), "username": username}
    )
    return jsonify({
        "status": "success",
        "token": token,
        "user": _user_to_response(user)
    })


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    username = get_jwt_identity()
    user = _get_profile_by_username(username)
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404
    return jsonify({"status": "success", "user": _user_to_response(user)})


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    username = get_jwt_identity()
    data = request.get_json() or {}
    current_pw = data.get('currentPassword') or ''
    new_pw = data.get('newPassword') or ''

    if not current_pw or not new_pw:
        return jsonify({"status": "error", "message": "currentPassword and newPassword are required"}), 400

    mongo_users = get_users_collection()
    mongo_user = mongo_users.find_one({"username": username})
    if not mongo_user or not check_password_hash(mongo_user.get("password_hash", ""), current_pw):
        return jsonify({"status": "error", "message": "Current password is incorrect"}), 401

    mongo_users.update_one(
        {"username": username},
        {"$set": {"password_hash": generate_password_hash(new_pw)}}
    )
    return jsonify({"status": "success", "message": "Password updated successfully"})
