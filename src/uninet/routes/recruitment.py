import json
from flask import Blueprint, jsonify, request
from src.uninet.models import db, RecruitmentCandidate, RecruitmentDrive
from src.uninet.utils.auth_guards import jwt_required_role

recruitment_bp = Blueprint('recruitment', __name__)

@recruitment_bp.route('/candidates', methods=['GET'])
@jwt_required_role('society_leader')
def get_candidates():
    candidates = [c.to_dict() for c in RecruitmentCandidate.query.all()]
    return jsonify({
        "success": True,
        "data": candidates
    })

@recruitment_bp.route('/candidates', methods=['POST'])
@jwt_required_role('society_leader')
def create_candidate():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"success": False, "message": "Name and email are required"}), 400

    skills_val = data.get("skills", [])
    if isinstance(skills_val, list):
        skills_str = json.dumps(skills_val)
    else:
        skills_str = str(skills_val)

    candidate = RecruitmentCandidate(
        name=name,
        email=email,
        initials=data.get("initials", name[:2].upper() if name else "ST"),
        badge_level=data.get("badgeLevel", "Bronze"),
        points=data.get("points", 100),
        match_score=data.get("matchScore", 80),
        applied_for=data.get("appliedFor", "General ExCom Member"),
        type=data.get("type", "applicant"),
        academic_background=data.get("academicBackground", "Undergraduate"),
        skills=skills_str,
        past_contributions=data.get("pastContributions", ""),
        rating=data.get("rating", 4.0),
        status=data.get("status", "Pending")
    )
    db.session.add(candidate)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Candidate application submitted successfully",
        "data": candidate.to_dict()
    }), 201

@recruitment_bp.route('/candidates/<int:candidate_id>/status', methods=['PUT', 'POST'])
@jwt_required_role('society_leader')
def update_candidate_status(candidate_id):
    data = request.get_json() or {}
    status = data.get("status")
    allowed_statuses = ["Pending", "Under Review", "Recruited", "Ignored", "Invited"]
    if not status or status not in allowed_statuses:
        return jsonify({"success": False, "message": f"Invalid status. Must be one of {allowed_statuses}"}), 400

    candidate = RecruitmentCandidate.query.get(candidate_id)
    if not candidate:
        return jsonify({"success": False, "message": "Candidate not found"}), 404

    candidate.status = status
    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"Candidate status updated to {status}.",
        "data": candidate.to_dict()
    })

@recruitment_bp.route('/candidates/<int:candidate_id>/review', methods=['POST'])
@jwt_required_role('society_leader')
def review_candidate(candidate_id):
    candidate = RecruitmentCandidate.query.get(candidate_id)
    if not candidate:
        return jsonify({"success": False, "message": "Candidate not found"}), 404

    candidate.status = "Under Review"
    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"Candidate {candidate.name} is now Under Review.",
        "data": candidate.to_dict()
    })

@recruitment_bp.route('/candidates/<int:candidate_id>/recruit', methods=['POST'])
@jwt_required_role('society_leader')
def recruit_candidate(candidate_id):
    candidate = RecruitmentCandidate.query.get(candidate_id)
    if not candidate:
        return jsonify({"success": False, "message": "Candidate not found"}), 404

    candidate.status = "Recruited"
    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"Candidate {candidate.name} has been successfully Recruited!",
        "data": candidate.to_dict()
    })

@recruitment_bp.route('/candidates/<int:candidate_id>/ignore', methods=['POST'])
@jwt_required_role('society_leader')
def ignore_candidate(candidate_id):
    candidate = RecruitmentCandidate.query.get(candidate_id)
    if not candidate:
        return jsonify({"success": False, "message": "Candidate not found"}), 404

    candidate.status = "Ignored"
    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"Candidate {candidate.name} has been Ignored.",
        "data": candidate.to_dict()
    })

@recruitment_bp.route('/candidates/<int:candidate_id>/dispatch-invite', methods=['POST'])
@jwt_required_role('society_leader')
def dispatch_invite(candidate_id):
    candidate = RecruitmentCandidate.query.get(candidate_id)
    if candidate:
        candidate.status = "Recruited"
        db.session.commit()
        return jsonify({
            "success": True,
            "message": f"Recruitment invitation dispatched to {candidate.name}.",
            "data": candidate.to_dict()
        })

    return jsonify({"success": False, "message": "Candidate not found"}), 404

@recruitment_bp.route('/drives', methods=['GET'])
@jwt_required_role('society_leader')
def get_drives():
    drives = [d.to_dict() for d in RecruitmentDrive.query.all()]
    return jsonify({
        "success": True,
        "data": drives
    })

@recruitment_bp.route('/drives', methods=['POST'])
@jwt_required_role('society_leader')
def create_drive():
    data = request.get_json() or {}
    drive = RecruitmentDrive(
        title=data.get("title", "New Recruitment Drive"),
        role_type=data.get("roleType", "OC Recruitment"),
        target_audience=data.get("targetAudience", "All Batches"),
        deadline=data.get("deadline", "2026-09-30")
    )
    db.session.add(drive)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Recruitment drive created successfully",
        "data": drive.to_dict()
    }), 201

@recruitment_bp.route('/drives/<int:drive_id>', methods=['DELETE'])
@jwt_required_role('society_leader')
def delete_drive(drive_id):
    drive = RecruitmentDrive.query.get(drive_id)
    if drive:
        db.session.delete(drive)
        db.session.commit()
        return jsonify({"success": True, "message": "Recruitment drive removed successfully"})
    return jsonify({"success": False, "message": "Drive not found"}), 404
