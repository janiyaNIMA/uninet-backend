import json
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.uninet.models import db, RecruitmentCandidate, RecruitmentDrive

recruitment_bp = Blueprint('recruitment', __name__)

DEFAULT_MOCK_CANDIDATES = [
    {
        "id": 1,
        "name": "Kavindi Bandara",
        "email": "kavindi@wusl.ac.lk",
        "initials": "KB",
        "badge_level": "Gold",
        "points": 620,
        "match_score": 96,
        "applied_for": "HackElite 2026 OC Lead",
        "type": "applicant",
        "academic_background": "BSc Hons Computer Science (3rd Year)",
        "skills": json.dumps(["Full-Stack Dev", "Event Management", "UI/UX"]),
        "past_contributions": "Sub-committee Lead for PCB Workshop 2025; 4 hackathon wins.",
        "rating": 5.0,
        "status": "Pending"
    },
    {
        "id": 2,
        "name": "Sahan Perera",
        "email": "sahan@wusl.ac.lk",
        "initials": "SP",
        "badge_level": "Silver",
        "points": 410,
        "match_score": 92,
        "applied_for": "HackElite 2026 Logistics OC",
        "type": "applicant",
        "academic_background": "BSc Industrial Management (2nd Year)",
        "skills": json.dumps(["Logistics", "Budgeting", "Vendor Relations"]),
        "past_contributions": "Coordinator for Sports Meet 2025; Active E-Club member.",
        "rating": 4.5,
        "status": "Pending"
    },
    {
        "id": 3,
        "name": "Dilini Wickramasinghe",
        "email": "dilini@wusl.ac.lk",
        "initials": "DW",
        "badge_level": "Platinum",
        "points": 890,
        "match_score": 98,
        "applied_for": "IEEE CS Vice Chair",
        "type": "ai_suggested",
        "academic_background": "BSc Hons Software Engineering (3rd Year)",
        "skills": json.dumps(["Cloud Architecture", "AI/ML", "Team Leadership"]),
        "past_contributions": "FOSS Community Lead; GSOC Contributor; WIE Senior Ambassador.",
        "rating": 5.0,
        "status": "Pending"
    },
    {
        "id": 4,
        "name": "Tharindu Fernando",
        "email": "tharindu@wusl.ac.lk",
        "initials": "TF",
        "badge_level": "Bronze",
        "points": 220,
        "match_score": 78,
        "applied_for": "HackElite 2026 Design OC",
        "type": "applicant",
        "academic_background": "BSc Applied Sciences (1st Year)",
        "skills": json.dumps(["Graphic Design", "Figma", "Video Editing"]),
        "past_contributions": "Created promotional flyers for IEEE CS Bootcamp.",
        "rating": 4.0,
        "status": "Pending"
    },
    {
        "id": 5,
        "name": "Nipuni Jayawardena",
        "email": "nipuni@wusl.ac.lk",
        "initials": "NJ",
        "badge_level": "Gold",
        "points": 580,
        "match_score": 94,
        "applied_for": "WIE Mentorship OC Lead",
        "type": "ai_suggested",
        "academic_background": "BSc Hons Computer Science (3rd Year)",
        "skills": json.dumps(["Mentorship", "Public Speaking", "Diversity Outreach"]),
        "past_contributions": "WIE Leadership Summit Lead Coordinator; Alumnae Liaison.",
        "rating": 5.0,
        "status": "Pending"
    }
]

DEFAULT_MOCK_DRIVES = [
    {
        "id": 1,
        "title": "HackElite 2026 Organizing Committee",
        "role_type": "OC Recruitment",
        "target_audience": "All Undergraduate Batches",
        "applicants_count": 34,
        "status": "Active",
        "deadline": "2026-08-30"
    },
    {
        "id": 2,
        "title": "IEEE CS Chapter Vice Chair & Secretary",
        "role_type": "ExCom Vacancy",
        "target_audience": "CS / IT Batches (2nd & 3rd Year)",
        "applicants_count": 12,
        "status": "Active",
        "deadline": "2026-09-10"
    },
    {
        "id": 3,
        "title": "WIE Mentorship Programme Coordinators",
        "role_type": "OC Recruitment",
        "target_audience": "Female Undergraduates",
        "applicants_count": 18,
        "status": "Closed",
        "deadline": "2026-08-01"
    }
]


def _ensure_recruitment_db_seeded():
    """Ensure candidate and drive records exist in database."""
    candidates = RecruitmentCandidate.query.all()
    if not candidates:
        for c in DEFAULT_MOCK_CANDIDATES:
            cand = RecruitmentCandidate(
                id=c["id"],
                name=c["name"],
                email=c["email"],
                initials=c["initials"],
                badge_level=c["badge_level"],
                points=c["points"],
                match_score=c["match_score"],
                applied_for=c["applied_for"],
                type=c["type"],
                academic_background=c["academic_background"],
                skills=c["skills"],
                past_contributions=c["past_contributions"],
                rating=c["rating"],
                status=c["status"]
            )
            db.session.add(cand)
        db.session.commit()

    drives = RecruitmentDrive.query.all()
    if not drives:
        for d in DEFAULT_MOCK_DRIVES:
            drv = RecruitmentDrive(
                id=d["id"],
                title=d["title"],
                role_type=d["role_type"],
                target_audience=d["target_audience"],
                applicants_count=d["applicants_count"],
                status=d["status"],
                deadline=d["deadline"]
            )
            db.session.add(drv)
        db.session.commit()


@recruitment_bp.route('/candidates', methods=['GET'])
@jwt_required()
def get_candidates():
    _ensure_recruitment_db_seeded()
    candidates = [c.to_dict() for c in RecruitmentCandidate.query.order_by(RecruitmentCandidate.id.desc()).all()]
    return jsonify({
        "success": True,
        "data": candidates
    })


@recruitment_bp.route('/candidates', methods=['POST'])
@jwt_required()
def create_candidate():
    _ensure_recruitment_db_seeded()
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
        "message": "Candidate application submitted successfully to database",
        "data": candidate.to_dict()
    }), 201


@recruitment_bp.route('/candidates/<int:candidate_id>', methods=['PUT'])
@recruitment_bp.route('/candidates/<int:candidate_id>/status', methods=['PUT', 'POST'])
@jwt_required()
def update_candidate_status(candidate_id):
    _ensure_recruitment_db_seeded()
    candidate = RecruitmentCandidate.query.get(candidate_id)
    if not candidate:
        return jsonify({"success": False, "message": "Candidate not found"}), 404

    data = request.get_json() or {}

    if "status" in data:
        status = data.get("status")
        allowed_statuses = ["Pending", "Under Review", "Recruited", "Ignored", "Invited"]
        if status in allowed_statuses:
            candidate.status = status

    if "rating" in data:
        try:
            candidate.rating = float(data.get("rating"))
        except (ValueError, TypeError):
            pass

    if "appliedFor" in data:
        candidate.applied_for = data.get("appliedFor")

    if "pastContributions" in data:
        candidate.past_contributions = data.get("pastContributions")

    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"Candidate '{candidate.name}' updated successfully.",
        "data": candidate.to_dict()
    })


@recruitment_bp.route('/candidates/<int:candidate_id>/review', methods=['POST'])
@jwt_required()
def review_candidate(candidate_id):
    _ensure_recruitment_db_seeded()
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
@jwt_required()
def recruit_candidate(candidate_id):
    _ensure_recruitment_db_seeded()
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
@jwt_required()
def ignore_candidate(candidate_id):
    _ensure_recruitment_db_seeded()
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
@jwt_required()
def dispatch_invite(candidate_id):
    _ensure_recruitment_db_seeded()
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


@recruitment_bp.route('/candidates/<int:candidate_id>', methods=['DELETE'])
@jwt_required()
def delete_candidate(candidate_id):
    _ensure_recruitment_db_seeded()
    candidate = RecruitmentCandidate.query.get(candidate_id)
    if not candidate:
        return jsonify({"success": False, "message": "Candidate not found"}), 404

    db.session.delete(candidate)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"Candidate record '{candidate.name}' deleted from pipeline database."
    })


@recruitment_bp.route('/drives', methods=['GET'])
@jwt_required()
def get_drives():
    _ensure_recruitment_db_seeded()
    drives = [d.to_dict() for d in RecruitmentDrive.query.all()]
    return jsonify({
        "success": True,
        "data": drives
    })


@recruitment_bp.route('/drives', methods=['POST'])
@jwt_required()
def create_drive():
    _ensure_recruitment_db_seeded()
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
@jwt_required()
def delete_drive(drive_id):
    _ensure_recruitment_db_seeded()
    drive = RecruitmentDrive.query.get(drive_id)
    if drive:
        db.session.delete(drive)
        db.session.commit()
        return jsonify({"success": True, "message": "Recruitment drive removed successfully"})
    return jsonify({"success": False, "message": "Drive not found"}), 404
