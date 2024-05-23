from http import HTTPStatus
from flask import Response, request
from typing import Any, Dict, Callable
from app.shared.environments import jwt_secret
from jwt import decode, ExpiredSignatureError, InvalidTokenError


def jwt_required(route: Callable[..., Response]) -> Callable[..., Response]:

    def validate_token(*args, **kwargs) -> Response:

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

        # ACCESS TOKEN HAS EXPIRED
        except ExpiredSignatureError:
            return Response(status=HTTPStatus.UNAUTHORIZED)

        # INVALID ACCESS TOKEN
        except InvalidTokenError:
            return Response(status=HTTPStatus.UNAUTHORIZED)

    return validate_token


def admin_required(route: Callable[..., Response]) -> Callable[..., Response]:

    def check_role(jwt_payload: Dict[str, Any], *args, **kwargs) -> Response:

        role = jwt_payload["role"]

        if role == "admin":
            return route(*args, **kwargs)

        return Response(status=HTTPStatus.UNAUTHORIZED)

    return check_role
