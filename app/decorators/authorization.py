from os import getenv
from app.models.user import User
from flask import Response, request
from typing import Any, Dict, Callable
from datetime import datetime, timedelta, UTC
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError


def jwt_required(route: Callable[..., Response]) -> Callable[..., Response]:

    def validate_token(*args, **kwargs) -> Response:

        jwt_secret = getenv("JWT_SECRET")
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        if jwt_secret is None:
            return Response(status=500)  # 500 - INTERNAL SERVER ERROR

        if not access_token or not refresh_token:
            return Response(status=401)  # 401 - UNAUTHORIZED

        # ACCESS TOKEN IS STILL VALID
        try:
            jwt_payload = decode(access_token, jwt_secret, algorithms=["HS256"])
            return route(jwt_payload, *args, **kwargs)

        # ACCESS TOKEN HAS EXPIRED
        except ExpiredSignatureError:

            user = User.query.filter_by(token=refresh_token).first()

            valid_refresh_token = user is not None
            if not valid_refresh_token:
                return Response(status=401)  # 401 - UNAUTHORIZED

            # REFRESH TOKEN IS STILL VALID
            try:
                jwt_payload = decode(refresh_token, jwt_secret, algorithms=["HS256"])

                jwt_payload["exp"] = datetime.now(UTC) + timedelta(hours=1)

                access_token = encode(jwt_payload, jwt_secret, algorithm="HS256")

                response = route(jwt_payload, *args, **kwargs)

                sixty_days = 60 * 60 * 24 * 60  # seconds * minutes * hours * days

                response.set_cookie(
                    secure=True,
                    httponly=True,
                    samesite="None",
                    key="access_token",
                    value=access_token,
                    max_age=sixty_days,
                )

                return response

            # REFRESH TOKEN HAS EXPIRED
            except ExpiredSignatureError:
                return Response(status=401)  # 401 - UNAUTHORIZED

            # INVALID REFRESH TOKEN
            except InvalidTokenError:
                return Response(status=401)  # 401 - UNAUTHORIZED

        # INVALID ACCESS TOKEN
        except InvalidTokenError:
            return Response(status=401)  # 401 - UNAUTHORIZED

    return validate_token


def admin_required(route: Callable[..., Response]) -> Callable:

    def check_role(jwt_payload: Dict[str, Any], *args, **kwargs) -> Response:

        role = jwt_payload.get("role")

        if role is None:
            return Response(status=401)  # 401 - UNAUTHORIZED

        if role == "admin":
            return route(*args, **kwargs)

        return Response(status=401)  # 401 - UNAUTHORIZED

    return check_role
