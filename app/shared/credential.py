from jwt import encode
from uuid import uuid4
from typing import Dict
from http import HTTPStatus
from flask import Response, jsonify
from app.shared.redis import redis_client
from datetime import datetime, timedelta, UTC
from app.shared.environments import jwt_secret


def send_jwt(payload: Dict[str, str]) -> Response:
    match jwt_secret:
        case str():
            access_token: str = encode(
                payload={
                    "exp": datetime.now(UTC) + timedelta(hours=1),
                    "username": payload["username"],
                    "permission": payload["permission"],
                    "role": payload["role"],
                },
                key=jwt_secret,
                algorithm="HS256",
            )

            return jsonify({**payload, "access_token": access_token})

        case None:
            return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


def create_refresh_token(username: str, role="user", permission="read-only"):

    current_time = datetime.now(UTC)
    token_expiration = current_time + timedelta(days=1)

    jwt_id = str(uuid4())

    refresh_token = encode(
        payload={
            "jti": jwt_id,
            "exp": token_expiration,
            "username": username,
            "permission": permission,
            "role": role,
        },
        key=jwt_secret,
        algorithm="HS256",
    )

    token_expiration_in_seconds = int(
        token_expiration.timestamp() - current_time.timestamp()
    )

    redis_client.setex(
        name=f"login-session:{username}:{jwt_id}",
        value=refresh_token,
        time=token_expiration_in_seconds,
    )

    return refresh_token


def revoke_refresh_token(token_id: str, username: str):
    deleted = redis_client.delete(f"login-session:{username}:{token_id}")
    match deleted:
        case int():
            if deleted > 0:
                return True
            return False
        case _:
            return False


def revoke_refresh_tokens(username: str) -> bool:
    sessions = redis_client.keys(f"login-session:{username}:*")
    match sessions:
        case []:
            return False

        case list():
            deleted = redis_client.delete(*sessions)
            match deleted:
                case int():
                    if deleted > 0:
                        return True
                    return False
                case _:
                    return False

        case _:
            return False
