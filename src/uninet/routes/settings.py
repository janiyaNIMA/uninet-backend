from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.uninet.models import db, UserSettings, User

settings_bp = Blueprint('settings', __name__)


def _get_user(username):
    return User.query.filter_by(username=username).first()


@settings_bp.route('', methods=['GET'])
@settings_bp.route('/', methods=['GET'])
@jwt_required()
def get_settings():
    username = get_jwt_identity()
    user = _get_user(username)
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    s = UserSettings.query.filter_by(user_id=user.id).first()
    if not s:
        s = UserSettings(user_id=user.id)
        db.session.add(s)
        db.session.commit()

    return jsonify({
        "status": "success",
        "settings": s.to_dict()
    })


@settings_bp.route('', methods=['PUT'])
@settings_bp.route('/', methods=['PUT'])
@jwt_required()
def update_settings():
    username = get_jwt_identity()
    user = _get_user(username)
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    data = request.get_json() or {}
    s = UserSettings.query.filter_by(user_id=user.id).first()
    if not s:
        s = UserSettings(user_id=user.id)
        db.session.add(s)

    notifs = data.get("notifications", {})
    if "emailUpdates" in notifs:
        s.email_notifications = notifs["emailUpdates"]
    if "inAppAlerts" in notifs:
        s.in_app_alerts = notifs["inAppAlerts"]
    if "recruitmentNotifs" in notifs:
        s.recruitment_notifs = notifs["recruitmentNotifs"]
    if "societyBroadcasts" in notifs:
        s.society_broadcasts = notifs["societyBroadcasts"]

    if "email_notifications" in data:
        s.email_notifications = data["email_notifications"]

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Settings updated",
        "settings": s.to_dict()
    })

