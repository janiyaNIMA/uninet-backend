from flask import Blueprint, jsonify, request
from src.uninet.models import db, Society, Event, EventRegistration, RecruitmentCandidate
from src.uninet.utils.auth_guards import jwt_required_role

excom_bp = Blueprint('excom', __name__)

@excom_bp.route('/dashboard', methods=['GET'])
@jwt_required_role('society_leader')
def dashboard():
    society = Society.query.first()
    member_count = society.member_count if society else 120
    upcoming_events_count = Event.query.count()
    pending_approvals = RecruitmentCandidate.query.filter_by(status='Pending').count()

    return jsonify({
        "status": "success",
        "data": {
            "society": society.name if society else "IEEE Student Branch",
            "member_count": member_count,
            "pending_approvals": pending_approvals,
            "upcoming_events": upcoming_events_count
        }
    })

@excom_bp.route('/events', methods=['POST'])
@jwt_required_role('society_leader')
def post_event():
    data = request.get_json() or {}
    title = data.get("title", "New Community Event")
    description = data.get("description", "")
    target_modules = data.get("targetModules", [])
    required_skills = data.get("requiredSkills", [])

    module_str = ", ".join(target_modules) if isinstance(target_modules, list) else str(target_modules)
    skills_str = ", ".join(required_skills) if isinstance(required_skills, list) else str(required_skills)

    new_event = Event(
        title=title,
        society_name="IEEE Student Branch",
        category="workshop",
        module=module_str or "All Faculties",
        date="2026-09-15",
        match_score=90,
        image="https://picsum.photos/seed/event/400/200",
        tags=skills_str or "Technology,Campus",
        description=description,
        society_id="S001"
    )
    db.session.add(new_event)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Event posted successfully",
        "event": new_event.to_dict()
    }), 201

