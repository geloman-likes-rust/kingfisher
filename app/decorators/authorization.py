from functools import wraps
from http import HTTPStatus
from flask import Response, request
from typing import Any, Dict, Callable
from app.shared.environments import jwt_secret
from jwt import decode, ExpiredSignatureError, InvalidTokenError


def jwt_required(route: Callable[..., Response]) -> Callable[..., Response]:
    @wraps(route)
    def validate_token(*args: Any, **kwargs: Any) -> Response:

        if jwt_secret is None:
            return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

        authorization = request.headers.get("Authorization")
        if authorization is None:
            return Response(status=HTTPStatus.UNAUTHORIZED)

        # ACCESS TOKEN IS STILL VALID
        try:
            access_token: str = authorization.split(" ")[1]
            jwt_payload = decode(access_token, jwt_secret, algorithms=["HS256"])
            return route(jwt_payload, *args, **kwargs)

        # ACCESS TOKEN HAS EXPIRED OR INVALID JWT TOKEN
        except (ExpiredSignatureError, InvalidTokenError):
            return Response(status=HTTPStatus.UNAUTHORIZED)

    return validate_token


def admin_required(route: Callable[..., Response]) -> Callable[..., Response]:
    @wraps(route)
    def check_role(jwt_payload: Dict[str, Any], *args: Any, **kwargs: Any) -> Response:

        role = jwt_payload["role"]

        if role == "admin":
            return route(*args, **kwargs)

        return Response(status=HTTPStatus.FORBIDDEN)

    return check_role


def write_access_required(route):
    @wraps(route)
    def check_permission(
        jwt_payload: Dict[str, Any], *args: Any, **kwargs: Any
    ) -> Response:

        permission: str = jwt_payload["permission"]
        if permission == "read-write":

            return route(*args, **kwargs)

        return Response(status=HTTPStatus.FORBIDDEN)

    return check_permission
