from typing import Dict
from http import HTTPStatus
from flask import Blueprint, Response, request
from app.shared.cache import cache_response, delete_cache, get_cache
from app.decorators.authorization import jwt_required, admin_required

accounts = Blueprint("accounts", __name__, url_prefix="/api/v1")


@accounts.post("/useradd")
@jwt_required
@admin_required
def create_account():
    from app.queries.create_account import create_account

    payload: Dict[str, str] | None = request.json

    if not payload:
        return Response(status=HTTPStatus.BAD_REQUEST)

    username = payload.get("username")
    password = payload.get("password")
    role = payload.get("role") or "user"
    permission = payload.get("permission") or "read-only"

    endpoint = f"/useradd?username={username}"
    match get_cache(endpoint):
        # CACHE HIT
        case list() | dict():
            return Response(status=HTTPStatus.CONFLICT)

        # CACHE MISS
        case None:
            match create_account(username, password, role, permission):
                case "Success":
                    cache_response(endpoint, {})
                    return Response(status=HTTPStatus.CREATED)

                case "NoUsername" | "NoPassword" | "InvalidRole" | "InvalidPermission":
                    return Response(status=HTTPStatus.BAD_REQUEST)

                case "AccountExists":
                    return Response(status=HTTPStatus.CONFLICT)

                case "DatabaseUnavailable":
                    return Response(status=HTTPStatus.SERVICE_UNAVAILABLE)


@accounts.delete("/userdel")
@jwt_required
@admin_required
def delete_account():
    from app.queries.delete_account import delete_account

    payload: Dict[str, str] | None = request.json
    if not payload:
        return Response(status=HTTPStatus.BAD_REQUEST)

    username = payload.get("username")

    match delete_account(username):
        case "Success":
            delete_cache(f"/useradd?username={username}")
            return Response(status=HTTPStatus.NO_CONTENT)

        case "Failed":
            return Response(status=HTTPStatus.NOT_FOUND)

        case "NoUsername":
            return Response(status=HTTPStatus.BAD_REQUEST)

        case "DatabaseUnavailable":
            return Response(status=HTTPStatus.SERVICE_UNAVAILABLE)


@accounts.put("/usermod")
@jwt_required
@admin_required
def edit_account():
    return Response()


@accounts.patch("/passwd")
@jwt_required
def change_password(_):
    from app.queries.change_password import change_password

    payload: Dict[str, str] | None = request.json
    if not payload:
        return Response(status=HTTPStatus.BAD_REQUEST)

    username = payload.get("username")
    oldpass = payload.get("oldpass")
    newpass = payload.get("newpass")

    if not username or not oldpass or not newpass:
        return Response(status=HTTPStatus.BAD_REQUEST)

    match change_password(username, oldpass, newpass):
        case "Success":
            return Response(status=HTTPStatus.NO_CONTENT)

        case "Failed" | "AccountNotFound" | "PasswordDontMatch":
            return Response(status=HTTPStatus.UNAUTHORIZED)

        case "DatabaseUnavailable":
            return Response(status=HTTPStatus.SERVICE_UNAVAILABLE)
