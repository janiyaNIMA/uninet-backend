from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(password_hash: str, password: str) -> bool:
    return check_password_hash(password_hash, password)

def generate_token(identity: str, additional_claims: dict = None) -> str:
    return create_access_token(identity=identity, additional_claims=additional_claims)
