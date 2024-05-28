from http import HTTPStatus
from typing import Dict
from flask import Blueprint, Response, request
from app.shared.credential import send_jwt
from app.shared.environments import jwt_secret
from jwt import decode, ExpiredSignatureError, InvalidTokenError


token = Blueprint("token", __name__, url_prefix="/api/v1/token")


@token.post("/refresh")
def refresh_token():

    authorization: str | None = request.headers.get("Authorization")

    match authorization:
        case None:
            return Response(status=HTTPStatus.UNAUTHORIZED)

        case str():
            try:
                access_token: str = authorization.split(" ")[1]
                jwt_payload = decode(access_token, jwt_secret, algorithms=["HS256"])

                payload = {
                    "username": jwt_payload["username"],
                    "permission": jwt_payload["permission"],
                    "role": jwt_payload["role"],
                }

                return send_jwt(payload)

            except ExpiredSignatureError:
                payload: Dict[str, str] | None = request.json
                match payload:
                    case dict():
                        refresh_token = payload.get("refresh_token")
                        match refresh_token:
                            case str():
                                try:
                                    jwt_payload = decode(
                                        refresh_token, jwt_secret, algorithms=["HS256"]
                                    )

                                    payload = {
                                        "username": jwt_payload["username"],
                                        "permission": jwt_payload["permission"],
                                        "role": jwt_payload["role"],
                                    }
                                    return send_jwt(payload)

                                except (ExpiredSignatureError, InvalidTokenError):
                                    return Response(status=HTTPStatus.UNAUTHORIZED)

                            case None:
                                return Response(status=HTTPStatus.UNAUTHORIZED)
                    case None:
                        return Response(status=HTTPStatus.UNAUTHORIZED)

            except InvalidTokenError:
                return Response(status=HTTPStatus.UNAUTHORIZED)
