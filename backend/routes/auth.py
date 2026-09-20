from flask import Blueprint, request
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

from extensions import db
from models.user import User
from config import Config
from utils.decorators import token_required


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not data:
        return {"error": "Request body is required"}, 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    role = data.get("role", "").strip().upper()

    if not email or not password or not role:
        return {"error": "Email, password and role are required"}, 400

    if role not in ["STUDENT", "TPO"]:
        return {"error": "Registration is allowed only for STUDENT or TPO"}, 400

    if len(password) < 6:
        return {"error": "Password must contain at least 6 characters"}, 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return {"error": "Email already registered"}, 409

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    user = User(
        email=email,
        password_hash=password_hash,
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return {
        "message": "Registration successful",
        "user_id": user.user_id
    }, 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data:
        return {"error": "Request body is required"}, 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return {"error": "Email and password are required"}, 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"error": "Invalid email or password"}, 401

    try:
        password_valid = bcrypt.checkpw(
            password.encode("utf-8"),
            user.password_hash.encode("utf-8")
        )
    except (ValueError, TypeError):
        return {"error": "Invalid email or password"}, 401

    if not password_valid:
        return {"error": "Invalid email or password"}, 401

    if not Config.SECRET_KEY:
        return {"error": "Server configuration error"}, 500

    token = jwt.encode(
        {
            "user_id": user.user_id,
            "role": user.role,
            "exp": datetime.now(timezone.utc) + timedelta(hours=24)
        },
        Config.SECRET_KEY,
        algorithm="HS256"
    )

    return {
        "message": "Login successful",
        "user_id": user.user_id,
        "email": user.email,
        "role": user.role,
        "token": token
    }


@auth_bp.route("/me", methods=["GET"])
@token_required
def me(payload):
    user = User.query.get(payload["user_id"])

    if not user:
        return {"error": "User not found"}, 404

    return {
        "user_id": user.user_id,
        "email": user.email,
        "role": user.role
    }