from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.uninet.models import db, Society, WIEMentor, SocietyApplication, User

societies_bp = Blueprint('societies', __name__)

@societies_bp.route('', methods=['GET'])
@societies_bp.route('/', methods=['GET'])
def get_societies():
    search = request.args.get('search', '', type=str).lower()
    category = request.args.get('category', 'All', type=str)

    query = Society.query
    if category != 'All':
        query = query.filter_by(category=category)

    societies = query.all()
    filtered = []
    for s in societies:
        d = s.to_dict()
        match_search = (not search) or (search in d["name"].lower()) or (search in d["description"].lower())
        if match_search:
            filtered.append(d)

    mentors = [m.to_dict() for m in WIEMentor.query.all()]

    return jsonify({
        "success": True,
        "data": {
            "wieMentors": mentors,
            "societies": filtered
        }
    })


@societies_bp.route('/<society_id>/apply', methods=['POST'])
@jwt_required()
def apply_society(society_id):
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    society = Society.query.get(society_id)
    if not society:
        return jsonify({"success": False, "message": "Society not found"}), 404

    app_rec = SocietyApplication(
        society_id=society_id,
        user_id=user.id if user else None,
        applicant_name=user.full_name if user else "Anonymous",
        applicant_email=user.email if user else "",
        status="Pending"
    )
    db.session.add(app_rec)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Application sent to {society.name}!"
    })

