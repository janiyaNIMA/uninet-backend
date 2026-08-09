from flask import Blueprint, jsonify, request
from src.uninet.models import db, RecruitmentCandidate, RecruitmentDrive

recruitment_bp = Blueprint('recruitment', __name__)

@recruitment_bp.route('/candidates', methods=['GET'])
def get_candidates():
    candidates = [c.to_dict() for c in RecruitmentCandidate.query.all()]
    return jsonify({
        "success": True,
        "data": candidates
    })

@recruitment_bp.route('/candidates/<int:candidate_id>/dispatch-invite', methods=['POST'])
def dispatch_invite(candidate_id):
    candidate = RecruitmentCandidate.query.get(candidate_id)
    if candidate:
        candidate.status = "Invited"
        db.session.commit()
        return jsonify({
            "success": True,
            "message": f"Recruitment invitation dispatched to {candidate.name}.",
            "data": candidate.to_dict()
        })

    return jsonify({"success": False, "message": "Candidate not found"}), 404

@recruitment_bp.route('/drives', methods=['GET'])
def get_drives():
    drives = [d.to_dict() for d in RecruitmentDrive.query.all()]
    return jsonify({
        "success": True,
        "data": drives
    })

@recruitment_bp.route('/drives', methods=['POST'])
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
def delete_drive(drive_id):
    drive = RecruitmentDrive.query.get(drive_id)
    if drive:
        db.session.delete(drive)
        db.session.commit()
        return jsonify({"success": True, "message": "Recruitment drive removed successfully"})
    return jsonify({"success": False, "message": "Drive not found"}), 404

