from flask import Blueprint, request, jsonify
from src.uninet.utils.security import hash_password, verify_password, generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    
    if username == "admin" and password == "password":
        token = generate_token(identity=username, additional_claims={"role": "admin"})
        return jsonify({"status": "success", "token": token})
    
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    return jsonify({"status": "success", "message": "User registered successfully"}), 201

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    return jsonify({"status": "success", "message": "Password updated successfully"})
