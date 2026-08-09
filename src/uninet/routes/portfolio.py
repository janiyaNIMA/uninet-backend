from flask import Blueprint, jsonify, request, send_file
from src.uninet.models import db, User, Badge, ResumeActivity
from src.uninet.utils.pdf_generator import generate_portfolio_pdf

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/my-badges', methods=['GET'])
def get_my_badges():
    user = User.query.get(1)

    badges = [b.to_dict() for b in Badge.query.filter_by(user_id=1).all()]
    if not badges:
        badges = [b.to_dict() for b in Badge.query.all()]

    activities = [a.to_dict() for a in ResumeActivity.query.filter_by(user_id=1).all()]
    if not activities:
        activities = [a.to_dict() for a in ResumeActivity.query.all()]

    return jsonify({
        "success": True,
        "data": {
            "currentPoints": user.total_points if user else 530,
            "badgeTier": user.badge_tier if user else "Gold",
            "nextTier": {
                "name": "Platinum",
                "pointsRequired": user.next_tier_points if user else 1000
            },
            "publicProfileEnabled": user.public_profile_enabled if user else True,
            "badges": badges,
            "resumeActivities": activities
        }
    })

@portfolio_bp.route('/public-toggle', methods=['PATCH'])
def toggle_public_profile():
    data = request.get_json() or {}
    enabled = data.get("publicProfile", True)

    user = User.query.get(1)
    if user:
        user.public_profile_enabled = enabled
        db.session.commit()

    return jsonify({
        "success": True,
        "publicProfileEnabled": enabled
    })

@portfolio_bp.route('/export-pdf', methods=['GET'])
@portfolio_bp.route('/export', methods=['GET'])
def export_pdf():
    user = User.query.get(1)
    badges = Badge.query.filter_by(user_id=1, unlocked=True).all()
    if not badges:
        badges = Badge.query.filter_by(unlocked=True).all()

    pdf_buffer = generate_portfolio_pdf({
        "name": user.full_name if user else "Jane Doe",
        "email": user.email if user else "jane@wusl.ac.lk",
        "badges": [b.title for b in badges]
    })
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="co-curricular-portfolio.pdf",
        mimetype='application/pdf'
    )

