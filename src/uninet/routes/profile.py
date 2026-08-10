import json
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.uninet.models import db, User

profile_bp = Blueprint('profile', __name__)


def _get_profile(username):
    return User.query.filter_by(username=username).first()


@profile_bp.route('', methods=['GET'])
@profile_bp.route('/', methods=['GET'])
@jwt_required()
def get_profile():
    username = get_jwt_identity()
    user = _get_profile(username)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    return jsonify({
        "success": True,
        "data": user.to_dict()
    })


@profile_bp.route('/tags', methods=['PUT'])
@profile_bp.route('/', methods=['PUT'])
@jwt_required()
def update_profile():
    data = request.get_json() or {}
    username = get_jwt_identity()
    user = _get_profile(username)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    if "skills" in data:
        user.skills = json.dumps(data["skills"]) if isinstance(data["skills"], list) else data["skills"]
    if "interests" in data:
        user.interests = json.dumps(data["interests"]) if isinstance(data["interests"], list) else data["interests"]
    if "academicModules" in data:
        user.academic_modules = json.dumps(data["academicModules"]) if isinstance(data["academicModules"], list) else data["academicModules"]
    if "name" in data:
        user.full_name = data["name"]
    if "email" in data:
        user.email = data["email"]
    if "phone" in data:
        user.phone = data["phone"]

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Profile tags updated successfully",
        "data": user.to_dict()
    })

