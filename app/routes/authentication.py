from jwt import decode
from typing import Dict
from http import HTTPStatus
from app.shared.hasher import bcrypt
from flask import Blueprint, Response, request
from app.shared.environments import jwt_secret
from app.queries.get_account import get_account
from app.decorators.authorization import jwt_required
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

    account = get_account(username)
    match account:
        case dict():
            password_match = bcrypt.check_password_hash(account["password"], password)
            match password_match:
                case True:

                    username = account["username"]
                    role = account["role"]
                    permission = account["permission"]

                    refresh_token = create_refresh_token(username, role, permission)

                    return send_jwt(
                        {
                            "username": username,
                            "role": role,
                            "permission": permission,
                            "refresh_token": refresh_token,
                        }
                    )

                case False:
                    return Response(status=HTTPStatus.UNAUTHORIZED)

        case None:
            return Response(status=HTTPStatus.UNAUTHORIZED)


@authentication.get("/logout")
@jwt_required
def logout(_):
    payload: Dict[str, str] | None = request.json
    match payload:
        case dict():
            refresh_token: str | None = payload.get("refresh_token")
            match refresh_token:
                case str():
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
                case None:
                    return Response(status=HTTPStatus.BAD_REQUEST)
        case None:
            return Response(status=HTTPStatus.BAD_REQUEST)
