from app.shared.orm import db
from app.models.user import User
from app.shared.hasher import bcrypt
from app.shared.credential import send_jwt
from flask import Blueprint, Response, request
from app.decorators.authorization import jwt_required


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
        return send_jwt(user)

    return "", 401  # 401 - UNAUTHORIZED


@authentication.get("/logout")
@jwt_required
def logout(jwt_payload):
    if jwt_payload is None:
        return Response(status=401)

    username = jwt_payload.get("username")

    if username is None:
        return Response(status=401)

    user = User.query.filter_by(username=username).first()
    if user is None:
        return Response(status=401)

    # Update online status of currently logged in user
    user.token = ""
    user.is_online = False
    db.session.commit()

    # Delete jwt tokens
    response = Response(status=204)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return response
