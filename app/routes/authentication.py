from typing import Dict
from http import HTTPStatus
from app.shared.hasher import bcrypt
from flask import Blueprint, Response, request
from app.shared.environments import jwt_secret
from app.queries.get_account import get_account
from app.decorators.authorization import jwt_required
from app.shared.cache import cache_response, get_cache
from jwt import decode, ExpiredSignatureError, InvalidTokenError
from app.shared.credential import send_jwt, revoke_refresh_token, create_refresh_token


authentication = Blueprint("authentication", __name__, url_prefix="/api/v1")


@authentication.post("/login")
def login():
    payload: Dict[str, str] | None = request.json
    if not payload:
        return Response(status=HTTPStatus.BAD_REQUEST)

    username = payload.get("username")
    password = payload.get("password")

    if not username or not password:
        return Response(status=HTTPStatus.BAD_REQUEST)

    endpoint = f"/login?username={username}"
    cached_user = get_cache(endpoint)
    match cached_user:
        # CACHE HIT
        case dict():
            password_hash: str = cached_user["password"]
            password_match: bool = bcrypt.check_password_hash(password_hash, password)
            match password_match:
                case True:
                    username = cached_user["username"]
                    role = cached_user["role"]
                    permission = cached_user["permission"]

                    refresh_token = create_refresh_token(username, role, permission)
                    match refresh_token:
                        case str():
                            return send_jwt(
                                {
                                    "username": username,
                                    "role": role,
                                    "permission": permission,
                                    "refresh_token": refresh_token,
                                }
                            )
                        case None:
                            return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

                case False:
                    return Response(status=HTTPStatus.UNAUTHORIZED)

        # CACHE MISS
        case None | _:
            account = get_account(username)
            match account:
                case dict():
                    # 60 * 60 * 24 * 7 = 604800 (7 days in seconds)
                    seven_days = 604800
                    cache_response(endpoint, account, ttl=seven_days)

                    password_hash: str = account["password"]
                    password_match: bool = bcrypt.check_password_hash(
                        password_hash, password
                    )
                    match password_match:
                        case True:
                            username = account["username"]
                            role = account["role"]
                            permission = account["permission"]

                            refresh_token = create_refresh_token(
                                username, role, permission
                            )
                            match refresh_token:
                                case str():
                                    return send_jwt(
                                        {
                                            "username": username,
                                            "role": role,
                                            "permission": permission,
                                            "refresh_token": refresh_token,
                                        }
                                    )
                                case None:
                                    return Response(
                                        status=HTTPStatus.INTERNAL_SERVER_ERROR
                                    )

                        case False:
                            return Response(status=HTTPStatus.UNAUTHORIZED)

                case None:
                    return Response(status=HTTPStatus.UNAUTHORIZED)


@authentication.post("/logout")
@jwt_required
def logout(_):
    payload: Dict[str, str] | None = request.json
    match payload:
        case dict():
            refresh_token: str | None = payload.get("refresh_token")
            match refresh_token:
                case str():
                    try:
                        jwt_payload = decode(
                            jwt=refresh_token, key=jwt_secret, algorithms=["HS256"]
                        )

                        token_id: str = jwt_payload["jti"]
                        username: str = jwt_payload["username"]

                        match revoke_refresh_token(token_id, username):
                            case True:
                                return Response(status=HTTPStatus.NO_CONTENT)
                            case False:
                                return Response(status=HTTPStatus.NOT_FOUND)

                    except (ExpiredSignatureError, InvalidTokenError):
                        return Response(status=HTTPStatus.UNAUTHORIZED)

                case None:
                    return Response(status=HTTPStatus.BAD_REQUEST)
        case None:
            return Response(status=HTTPStatus.BAD_REQUEST)
