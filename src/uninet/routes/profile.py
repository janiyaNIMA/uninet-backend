import json
from flask import Blueprint, jsonify, request
from src.uninet.models import db, User

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('', methods=['GET'])
@profile_bp.route('/', methods=['GET'])
def get_profile():
    user = User.query.get(1)
    if not user:
        user = User(
            id=1,
            username="jane",
            email="jane@wusl.ac.lk",
            full_name="Jane Doe"
        )
        db.session.add(user)
        db.session.commit()

    return jsonify({
        "success": True,
        "data": user.to_dict()
    })

@profile_bp.route('/tags', methods=['PUT'])
@profile_bp.route('/', methods=['PUT'])
def update_profile():
    data = request.get_json() or {}
    user = User.query.get(1)
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

