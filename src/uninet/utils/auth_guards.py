"""
JWT role-based access control decorators.
Usage:
    from src.uninet.utils.auth_guards import jwt_required_role

    @bp.route('/secret')
    @jwt_required_role('society_leader')  # or 'student'
    def secret():
        ...
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt


def jwt_required_role(*allowed_roles):
    """
    Decorator that requires a valid JWT AND the token's 'role' claim
    to be one of the allowed_roles.

    Pass no roles (or '*') to just require any valid JWT.
    """
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role", "student")
            if allowed_roles and role not in allowed_roles:
                return jsonify({
                    "status": "error",
                    "message": "Access denied: insufficient privileges"
                }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
