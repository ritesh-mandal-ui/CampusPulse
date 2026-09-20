from functools import wraps

import jwt
from flask import request

from config import Config


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return {"error": "Authentication token is required"}, 401

        token = auth_header.split(" ", 1)[1].strip()

        if not token:
            return {"error": "Authentication token is required"}, 401

        if not Config.SECRET_KEY:
            return {"error": "Server configuration error"}, 500

        try:
            payload = jwt.decode(
                token,
                Config.SECRET_KEY,
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return {"error": "Authentication token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid authentication token"}, 401

        return f(payload, *args, **kwargs)

    return decorated