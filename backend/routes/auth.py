from flask import Blueprint, request
import bcrypt
import hashlib
import secrets
import resend
import jwt
from datetime import datetime, timedelta, timezone

from extensions import db
from models.user import User
from models.password_reset_token import PasswordResetToken
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


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json(silent=True)

    generic_message = (
        "If the email is registered, a password reset link has been sent."
    )

    if not data:
        return {"message": generic_message}

    email = data.get("email", "").strip().lower()

    if not email:
        return {"message": generic_message}

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"message": generic_message}

    PasswordResetToken.query.filter_by(
        user_id=user.user_id,
        used=False
    ).update({"used": True})

    raw_token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(
        raw_token.encode("utf-8")
    ).hexdigest()

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)

    reset_token = PasswordResetToken(
        user_id=user.user_id,
        token_hash=token_hash,
        expires_at=expires_at,
        used=False
    )

    db.session.add(reset_token)
    db.session.commit()

    reset_link = (
        f"{Config.FRONTEND_BASE_URL}/pages/reset-password.html"
        f"?token={raw_token}"
    )

    try:
        if not Config.RESEND_API_KEY:
            raise RuntimeError("Resend API key is not configured")

        if not Config.FRONTEND_BASE_URL:
            raise RuntimeError("Frontend base URL is not configured")

        resend.api_key = Config.RESEND_API_KEY

        email_response = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": [user.email],
            "subject": "Reset your CampusPulse password",
            "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
                    <h2>CampusPulse Password Reset</h2>

                    <p>Hello,</p>

                    <p>
                        We received a request to reset your CampusPulse password.
                    </p>

                    <p>
                        Click the button below to create a new password.
                    </p>

                    <p style="margin: 30px 0;">
                        <a
                            href="{reset_link}"
                            style="
                                background-color: #2563eb;
                                color: white;
                                padding: 12px 20px;
                                text-decoration: none;
                                border-radius: 6px;
                                display: inline-block;
                            "
                        >
                            Reset Password
                        </a>
                    </p>

                    <p>
                        This link will expire in 30 minutes and can only be used once.
                    </p>

                    <p>
                        If you did not request a password reset, you can safely ignore
                        this email.
                    </p>

                    <p>
                        Regards,<br>
                        CampusPulse Team
                    </p>
                </div>
            """
        })

        print(f"Password reset email sent: {email_response}")

    except Exception as e:
        db.session.delete(reset_token)
        db.session.commit()
        print(f"Password reset email error: {e}")

    return {"message": generic_message}


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json(silent=True)

    if not data:
        return {"error": "Request body is required"}, 400

    raw_token = data.get("token", "").strip()
    new_password = data.get("password", "")

    if not raw_token or not new_password:
        return {"error": "Token and new password are required"}, 400

    if len(new_password) < 6:
        return {"error": "Password must contain at least 6 characters"}, 400

    token_hash = hashlib.sha256(
        raw_token.encode("utf-8")
    ).hexdigest()

    reset_token = PasswordResetToken.query.filter_by(
        token_hash=token_hash,
        used=False
    ).first()

    if not reset_token:
        return {"error": "Invalid or expired reset link"}, 400

    now = datetime.now(timezone.utc)

    expires_at = reset_token.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at <= now:
        reset_token.used = True
        db.session.commit()
        return {"error": "Invalid or expired reset link"}, 400

    user = User.query.get(reset_token.user_id)

    if not user:
        reset_token.used = True
        db.session.commit()
        return {"error": "Invalid or expired reset link"}, 400

    password_hash = bcrypt.hashpw(
        new_password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    user.password_hash = password_hash

    reset_token.used = True

    PasswordResetToken.query.filter(
        PasswordResetToken.user_id == user.user_id,
        PasswordResetToken.id != reset_token.id,
        PasswordResetToken.used == False
    ).update({"used": True})

    db.session.commit()

    return {
        "message": "Password reset successful. You can now log in with your new password."
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