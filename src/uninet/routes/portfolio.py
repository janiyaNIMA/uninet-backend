from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.uninet.models import db, User, Badge, ResumeActivity
from src.uninet.utils.pdf_generator import generate_portfolio_pdf

portfolio_bp = Blueprint('portfolio', __name__)


def _get_user(username):
    return User.query.filter_by(username=username).first()


@portfolio_bp.route('/my-badges', methods=['GET'])
@jwt_required()
def get_my_badges():
    username = get_jwt_identity()
    user = _get_user(username)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    badges = [b.to_dict() for b in Badge.query.filter_by(user_id=user.id).all()]
    activities = [a.to_dict() for a in ResumeActivity.query.filter_by(user_id=user.id).all()]

    return jsonify({
        "success": True,
        "data": {
            "currentPoints": user.total_points,
            "badgeTier": user.badge_tier,
            "nextTier": {
                "name": "Platinum",
                "pointsRequired": user.next_tier_points
            },
            "publicProfileEnabled": user.public_profile_enabled,
            "badges": badges,
            "resumeActivities": activities
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


@portfolio_bp.route('/export-pdf', methods=['GET'])
@portfolio_bp.route('/export', methods=['GET'])
@jwt_required()
def export_pdf():
    username = get_jwt_identity()
    user = _get_user(username)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    badges = Badge.query.filter_by(user_id=user.id, unlocked=True).all()

    pdf_buffer = generate_portfolio_pdf({
        "name": user.full_name,
        "email": user.email,
        "badges": [b.title for b in badges]
    })
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="co-curricular-portfolio.pdf",
        mimetype='application/pdf'
    )

