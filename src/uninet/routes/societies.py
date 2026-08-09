from flask import Blueprint, jsonify, request
from src.uninet.models import db, Society, WIEMentor, SocietyApplication

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

@societies_bp.route('/<int:society_id>/apply', methods=['POST'])
def apply_society(society_id):
    society = Society.query.get(society_id)
    name = society.name if society else "Society"

    app_rec = SocietyApplication(
        society_id=society_id,
        user_id=1,
        applicant_name="Jane Doe",
        applicant_email="jane@wusl.ac.lk",
        status="Pending"
    )
    db.session.add(app_rec)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Application sent to {name}!"
    })

