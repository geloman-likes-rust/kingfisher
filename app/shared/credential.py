from os import getenv
from jwt import encode
from flask import Response
from app.shared.orm import db
from app.models.user import User
from datetime import datetime, timedelta, UTC


def send_jwt(user: User) -> Response:

    jwt_secret = getenv("JWT_SECRET")
    if jwt_secret is None:
        return Response(status=500)  # 500 - INTERNAL SERVER ERROR

    token = {
        "exp": datetime.now(UTC) + timedelta(hours=1),
        "username": user.username,
        "permission": user.permission,
        "role": user.role,
    }

    access_token = encode(token, jwt_secret, algorithm="HS256")

    response = Response()

    sixty_days = 60 * 60 * 24 * 60  # seconds * minutes * hours * days

    response.set_cookie(
        secure=True,
        httponly=True,
        samesite="None",
        key="access_token",
        value=access_token,
        max_age=sixty_days,
    )

    token["exp"] = datetime.now(UTC) + timedelta(days=60)
    refresh_token = encode(token, jwt_secret, algorithm="HS256")

    # Update token and online status of user when logging in
    user.is_online = True
    user.token = refresh_token
    db.session.commit()

    response.set_cookie(
        secure=True,
        httponly=True,
        samesite="None",
        key="refresh_token",
        value=refresh_token,
        max_age=sixty_days,
    )

    response.status = 204  # 204 - NO CONTENT
    return response
