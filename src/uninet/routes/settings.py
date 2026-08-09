from flask import Blueprint, jsonify, request
from src.uninet.models import db, UserSettings

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('', methods=['GET'])
@settings_bp.route('/', methods=['GET'])
def get_settings():
    s = UserSettings.query.filter_by(user_id=1).first()
    if not s:
        s = UserSettings(user_id=1)
        db.session.add(s)
        db.session.commit()

    return jsonify({
        "status": "success",
        "settings": s.to_dict()
    })

@settings_bp.route('', methods=['PUT'])
@settings_bp.route('/', methods=['PUT'])
def update_settings():
    data = request.get_json() or {}
    s = UserSettings.query.filter_by(user_id=1).first()
    if not s:
        s = UserSettings(user_id=1)
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

