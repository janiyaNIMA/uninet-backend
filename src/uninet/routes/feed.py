import random
from flask import Blueprint, jsonify, request
from src.uninet.models import db, Event, EventRegistration

feed_bp = Blueprint('feed', __name__)

@feed_bp.route('', methods=['GET'])
@feed_bp.route('/', methods=['GET'])
def get_feed():
    search = request.args.get('search', '', type=str).lower()
    category = request.args.get('category', 'All', type=str)
    module = request.args.get('module', 'All Modules', type=str)

    query = Event.query

    events = query.all()
    filtered_events = []

    for ev in events:
        match_search = (not search) or (search in ev.title.lower()) or (search in ev.society_name.lower())
        match_cat = (category == 'All') or (ev.category == category)
        match_mod = (module == 'All Modules') or (ev.module == module) or (ev.module == 'All Faculties')

        if match_search and match_cat and match_mod:
            filtered_events.append({
                "id": ev.id,
                "title": ev.title,
                "society": ev.society_name,
                "category": ev.category,
                "module": ev.module,
                "date": ev.date,
                "matchScore": ev.match_score,
                "image": ev.image,
                "tags": ev.tags.split(",") if ev.tags else [],
                "description": ev.description,
                "isRegistered": False
            })

    # Sort by matchScore descending (Smart Recommendation order)
    filtered_events.sort(key=lambda x: x["matchScore"], reverse=True)

    return jsonify({
        "success": True,
        "data": filtered_events
    })

@feed_bp.route('/<int:event_id>', methods=['GET'])
def get_event_detail(event_id):
    ev = Event.query.get(event_id)
    if not ev:
        return jsonify({
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "Event not found"
            }
        }), 404

    return jsonify({
        "success": True,
        "data": {
            "id": ev.id,
            "title": ev.title,
            "society": ev.society_name,
            "category": ev.category,
            "module": ev.module,
            "date": ev.date,
            "matchScore": ev.match_score,
            "image": ev.image,
            "tags": ev.tags.split(",") if ev.tags else [],
            "description": ev.description
        }
    })

@feed_bp.route('/events/<int:event_id>/register', methods=['POST'])
@feed_bp.route('/register/<int:event_id>', methods=['POST'])
def register_event(event_id):
    ev = Event.query.get(event_id)
    if not ev:
        return jsonify({
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "Event not found"
            }
        }), 404

    reg_code = f"REG-{random.randint(10000, 99999)}"
    reg = EventRegistration(
        event_id=event_id,
        registration_code=reg_code
    )
    db.session.add(reg)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Successfully registered for {ev.title}.",
        "data": {
            "eventId": event_id,
            "registrationId": reg_code,
            "calendarSyncUrl": f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={ev.title}"
        }
    })
