from typing import Any, Dict
from http import HTTPStatus
from flask import Blueprint, Response, request
from app.shared.environments import jwt_secret
from app.shared.credential import send_jwt, verify_refresh_token
from jwt import decode, ExpiredSignatureError, InvalidTokenError


token = Blueprint("token", __name__, url_prefix="/api/v1/token")


@token.post("/refresh")
def refresh_token():

    authorization: str | None = request.headers.get("Authorization")

    match authorization:
        case None:
            return Response(status=HTTPStatus.UNAUTHORIZED)

        case str():
            match jwt_secret:
                case None:
                    return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

                case str():

                    # ACCESS TOKEN IS STILL VALID
                    try:
                        access_token: str = authorization.split(" ")[1]

                        jwt_payload: Dict[str, Any] = decode(
                            access_token, jwt_secret, algorithms=["HS256"]
                        )

                        username: str = jwt_payload["username"]
                        permission: str = jwt_payload["permission"]
                        role: str = jwt_payload["role"]

                        # SEND NEW ACCESS TOKEN
                        return send_jwt(
                            {
                                "username": username,
                                "permission": permission,
                                "role": role,
                            }
                        )

                    # ACCESS TOKEN HAS EXPIRED
                    except ExpiredSignatureError:
                        payload: Dict[str, str] | None = request.json
                        match payload:
                            case dict():

                                refresh_token: str | None = payload.get("refresh_token")
                                if not refresh_token:
                                    return Response(status=HTTPStatus.UNAUTHORIZED)

                                try:
                                    jwt_payload: Dict[str, Any] = decode(
                                        refresh_token,
                                        jwt_secret,
                                        algorithms=["HS256"],
                                    )

                                    jwt_id: str = jwt_payload["jti"]
                                    username: str = jwt_payload["username"]

                                    match verify_refresh_token(jwt_id, username):
                                        # VALID REFRESH TOKEN
                                        case True:

                                            role: str = jwt_payload["role"]
                                            permission: str = jwt_payload["permission"]

                                            # SEND NEW ACCESS TOKEN
                                            return send_jwt(
                                                {
                                                    "username": username,
                                                    "permission": permission,
                                                    "role": role,
                                                }
                                            )

                                        # INVALID REFRESH TOKEN
                                        case False:
                                            return Response(
                                                status=HTTPStatus.UNAUTHORIZED
                                            )

                                # REFRESH TOKEN HAS EXPIRED OR INVALID REFRESH TOKEN
                                except (ExpiredSignatureError, InvalidTokenError):
                                    return Response(status=HTTPStatus.UNAUTHORIZED)

                            # REQUEST PAYLOAD IS NONE
                            case None:
                                return Response(status=HTTPStatus.UNAUTHORIZED)

                    # INVALID ACCESS TOKEN
                    except InvalidTokenError:
                        return Response(status=HTTPStatus.UNAUTHORIZED)
