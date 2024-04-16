from flask import Blueprint, request
from flask_login import login_required, login_user, logout_user
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
        login_user(user)
        return "", 204  # 204 - NO CONTENT

    return "", 401  # 401 - UNAUTHORIZED


@authentication.get("/logout")
@login_required
def logout():
    logout_user()
    return "", 204  # 204 - NO CONTENT
