from flask import Blueprint, request
from app.shared.hasher import bcrypt
from app.models.user import User


authentication = Blueprint("authentication", __name__, url_prefix="/api/v1")


@authentication.post("/login")
def login():
    payload = request.json
    if payload is None:
        return "", 400  # 400 - BAD REQUEST

    username = payload.get("username")
    password = payload.get("password")
    if username is None or password is None:
        return "", 400  # 400 - BAD REQUEST

    user = User.query.filter_by(username=username).first()
    if user is None:
        return "", 401  # 401 - UNAUTHORIZED

    password_did_match = bcrypt.check_password_hash(user.password, password)
    if password_did_match:

        # TODO: send both access token and refresh token as httpOnly cookie

        return "", 204  # 204 - NO CONTENT

    return "", 401  # 401 - UNAUTHORIZED


@authentication.get("/logout")
def logout():
    return "", 204  # 204 - NO CONTENT
