from datetime import datetime
from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.uninet.models import db, User, Badge, ResumeActivity
from src.uninet.utils.pdf_generator import generate_portfolio_pdf

portfolio_bp = Blueprint('portfolio', __name__)

DEFAULT_CATALOG_BADGES = [
    {
        "id": 1, "title": "Hackathon Hero", "category": "Innovation", "tier": "Gold",
        "unlocked": True, "points": 150, "earned_date": "2026-05-12", "icon": "🏆",
        "description": "Participated and placed in top 3 in HackElite 2025."
    },
    {
        "id": 2, "title": "Code Sprint Veteran", "category": "Technical", "tier": "Silver",
        "unlocked": True, "points": 100, "earned_date": "2026-06-20", "icon": "💻",
        "description": "Attended 3+ technical coding workshops (CMIS / IEEE / Electronic Society)."
    },
    {
        "id": 3, "title": "WIE Champion", "category": "Inclusivity", "tier": "Gold",
        "unlocked": True, "points": 120, "earned_date": "2026-07-04", "icon": "💜",
        "description": "Active participation in IEEE WIE affinity group workshops or mentorship programs."
    },
    {
        "id": 4, "title": "Lens Master", "category": "Creative", "tier": "Bronze",
        "unlocked": True, "points": 50, "earned_date": "2026-07-18", "icon": "📸",
        "description": "Contributed media coverage for a campus event via WireScope Photography."
    },
    {
        "id": 5, "title": "Tactical Mind", "category": "Sports", "tier": "Bronze",
        "unlocked": False, "points": 50, "earned_date": None, "icon": "♟️",
        "description": "Participated in university chess tournaments or inter-faculty board meets."
    },
    {
        "id": 6, "title": "Eco Warrior", "category": "Community", "tier": "Bronze",
        "unlocked": False, "points": 50, "earned_date": None, "icon": "🌿",
        "description": "Participated in ESOC environmental sustainability or green campus initiatives."
    },
    {
        "id": 7, "title": "Orator Mastery", "category": "Leadership", "tier": "Silver",
        "unlocked": False, "points": 90, "earned_date": None, "icon": "🎙️",
        "description": "Delivered a speech or completed a module in Gavel Club public speaking drives."
    },
    {
        "id": 8, "title": "Lead Organizer", "category": "Management", "tier": "Platinum",
        "unlocked": False, "points": 200, "earned_date": None, "icon": "👑",
        "description": "Served as an Organizing Committee (OC) lead for a major university event."
    }
]

DEFAULT_ACTIVITIES = [
    {
        "role": "Lead Organiser & Student Lead",
        "organization": "IEEE Student Branch Chapter",
        "event": "HackElite 2025 Hackathon",
        "category": "Leadership & Management",
        "period": "Mar 2025 – May 2025",
        "verified": True
    },
    {
        "role": "Participant & Runner-Up",
        "organization": "IEEE Computer Society",
        "event": "Cloud Computing Sprint",
        "category": "Technical Skill",
        "period": "Jun 2026",
        "verified": True
    },
    {
        "role": "WIE Ambassador",
        "organization": "IEEE Women in Engineering",
        "event": "STEM Outreach Programme",
        "category": "Community & Mentorship",
        "period": "Jul 2026",
        "verified": True
    },
    {
        "role": "Sub-Committee Member",
        "organization": "Entrepreneurship Club",
        "event": "Pitch Night Vol. 3",
        "category": "Business & Soft Skills",
        "period": "Jan 2026",
        "verified": True
    }
]


def _get_user(username):
    return User.query.filter_by(username=username).first()


def _recalculate_user_tier(user):
    points = user.total_points or 0
    if points >= 1000:
        user.badge_tier = "Platinum"
        user.next_tier_points = 1000
    elif points >= 500:
        user.badge_tier = "Gold"
        user.next_tier_points = 1000
    elif points >= 250:
        user.badge_tier = "Silver"
        user.next_tier_points = 500
    else:
        user.badge_tier = "Bronze"
        user.next_tier_points = 250


def _ensure_user_portfolio(user):
    badges = Badge.query.filter_by(user_id=user.id).all()
    if not badges:
        for b_data in DEFAULT_CATALOG_BADGES:
            b = Badge(
                user_id=user.id,
                title=b_data["title"],
                category=b_data["category"],
                tier=b_data["tier"],
                unlocked=b_data["unlocked"],
                points=b_data["points"],
                earned_date=b_data["earned_date"],
                icon=b_data["icon"],
                description=b_data["description"]
            )
            db.session.add(b)
        db.session.commit()
        badges = Badge.query.filter_by(user_id=user.id).all()

    activities = ResumeActivity.query.filter_by(user_id=user.id).all()
    if not activities:
        for act in DEFAULT_ACTIVITIES:
            a = ResumeActivity(
                user_id=user.id,
                role=act["role"],
                organization=act["organization"],
                event=act["event"],
                category=act["category"],
                period=act["period"],
                verified=act["verified"]
            )
            db.session.add(a)
        db.session.commit()
        activities = ResumeActivity.query.filter_by(user_id=user.id).all()

    return badges, activities


@portfolio_bp.route('/my-badges', methods=['GET'])
@jwt_required()
def get_my_badges():
    username = get_jwt_identity()
    user = _get_user(username)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    badges, activities = _ensure_user_portfolio(user)
    _recalculate_user_tier(user)
    db.session.commit()

    unlocked_count = len([b for b in badges if b.unlocked])
    total_count = len(badges)

    return jsonify({
        "success": True,
        "data": {
            "user": {
                "id": user.id,
                "username": user.username,
                "fullName": user.full_name,
                "email": user.email,
                "degreeStream": user.degree_stream,
                "batch": user.batch,
            },
            "currentPoints": user.total_points,
            "badgeTier": user.badge_tier,
            "nextTier": {
                "name": "Platinum",
                "pointsRequired": 1000
            },
            "publicProfileEnabled": user.public_profile_enabled,
            "unlockedBadgeCount": unlocked_count,
            "totalBadgeCount": total_count,
            "badges": [b.to_dict() for b in badges],
            "resumeActivities": [a.to_dict() for a in activities]
        }
    })


@portfolio_bp.route('/public-toggle', methods=['PATCH'])
@jwt_required()
def toggle_public_profile():
    data = request.get_json() or {}
    enabled = data.get("publicProfile", True)

    username = get_jwt_identity()
    user = _get_user(username)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    user.public_profile_enabled = enabled
    db.session.commit()

    return jsonify({
        "success": True,
        "publicProfileEnabled": enabled
    })


@portfolio_bp.route('/claim-badge', methods=['POST'])
@portfolio_bp.route('/unlock-badge', methods=['POST'])
@jwt_required()
def claim_badge():
    username = get_jwt_identity()
    user = _get_user(username)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    data = request.get_json() or {}
    badge_id = data.get("badgeId")
    badge = Badge.query.filter_by(id=badge_id, user_id=user.id).first()

    if not badge:
        return jsonify({"success": False, "message": "Badge not found"}), 444

    if badge.unlocked:
        return jsonify({"success": False, "message": "Badge is already unlocked!"}), 400

    badge.unlocked = True
    badge.earned_date = datetime.now().strftime("%Y-%m-%d")
    user.total_points = (user.total_points or 0) + badge.points
    _recalculate_user_tier(user)
    db.session.commit()

    badges = Badge.query.filter_by(user_id=user.id).all()
    return jsonify({
        "success": True,
        "message": f"Successfully claimed '{badge.title}'! +{badge.points} engagement points added.",
        "badge": badge.to_dict(),
        "currentPoints": user.total_points,
        "badgeTier": user.badge_tier,
        "badges": [b.to_dict() for b in badges]
    })


@portfolio_bp.route('/add-activity', methods=['POST'])
@jwt_required()
def add_activity():
    username = get_jwt_identity()
    user = _get_user(username)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    data = request.get_json() or {}
    role = data.get("role")
    organization = data.get("organization")
    event = data.get("event")
    category = data.get("category", "Co-Curricular")
    period = data.get("period", "2026")
    points = data.get("pointsAwarded", 50)

    if not role or not organization or not event:
        return jsonify({"success": False, "message": "Role, Organization, and Event are required"}), 400

    activity = ResumeActivity(
        user_id=user.id,
        role=role,
        organization=organization,
        event=event,
        category=category,
        period=period,
        verified=True
    )
    db.session.add(activity)

    # Award points for adding verified co-curricular activity
    user.total_points = (user.total_points or 0) + points
    _recalculate_user_tier(user)

    db.session.commit()

    activities = ResumeActivity.query.filter_by(user_id=user.id).all()
    return jsonify({
        "success": True,
        "message": f"Successfully logged new activity! +{points} engagement points added.",
        "activity": activity.to_dict(),
        "currentPoints": user.total_points,
        "badgeTier": user.badge_tier,
        "resumeActivities": [a.to_dict() for a in activities]
    })


@portfolio_bp.route('/activity/<int:activity_id>', methods=['DELETE'])
@jwt_required()
def delete_activity(activity_id):
    username = get_jwt_identity()
    user = _get_user(username)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    activity = ResumeActivity.query.filter_by(id=activity_id, user_id=user.id).first()
    if not activity:
        return jsonify({"success": False, "message": "Activity not found"}), 404

    db.session.delete(activity)
    db.session.commit()

    activities = ResumeActivity.query.filter_by(user_id=user.id).all()
    return jsonify({
        "success": True,
        "message": "Activity deleted successfully.",
        "resumeActivities": [a.to_dict() for a in activities]
    })


@portfolio_bp.route('/export-pdf', methods=['GET'])
@portfolio_bp.route('/export', methods=['GET'])
@jwt_required()
def export_pdf():
    username = get_jwt_identity()
    user = _get_user(username)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    badges = Badge.query.filter_by(user_id=user.id, unlocked=True).all()
    activities = ResumeActivity.query.filter_by(user_id=user.id).all()

    pdf_buffer = generate_portfolio_pdf({
        "name": user.full_name,
        "email": user.email,
        "id": user.id,
        "faculty": user.faculty,
        "degreeStream": user.degree_stream,
        "batch": user.batch,
        "badgeTier": user.badge_tier,
        "totalPoints": user.total_points,
        "badges": [f"{b.icon} {b.title} ({b.category}) - {b.points} pts" for b in badges],
        "activities": [a.to_dict() for a in activities]
    })
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"Co-Curricular-Portfolio-{user.username}.pdf",
        mimetype='application/pdf'
    )
