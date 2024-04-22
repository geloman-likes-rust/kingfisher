from app.shared.orm import db
from app.shared.hasher import bcrypt
from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from app.models.user import User


accounts = Blueprint("accounts", __name__, url_prefix="/api/v1")


@accounts.post("/useradd")
def create_user():
    payload = request.json
    if payload is None:
        return "", 400  # 400 - BAD REQUEST

    username = payload.get("username")
    password = payload.get("password")
    if username is None or password is None:
        return "", 400  # 400 - BAD REQUEST

    hashed_password = bcrypt.generate_password_hash(password).decode()

    try:
        db.session.add(User(username=username, password=hashed_password))
        db.session.commit()
        return "", 201  # 201 - CREATED

    except IntegrityError:
        return {"error": "username has already been taken!"}, 409  # 409 - CONFLICT


@accounts.delete("/userdel")
def delete_user():
    payload = request.json
    if payload is None:
        return "", 400  # 400 - BAD REQUEST

    username = payload.get("username")
    if username is None:
        return "", 400  # 400 - BAD REQUEST

    user = User.query.filter_by(username=username).first()
    user_not_found = user is None
    if user_not_found:
        return "", 404  # 404 - NOT FOUND

    db.session.delete(user)
    db.session.commit()
    return "", 204  # 204 - NO CONTENT


@accounts.patch("/passwd")
def change_password():
    payload = request.json
    if payload is None:
        return "", 400  # 400 - BAD REQUEST

    username = payload.get("username")
    password = payload.get("password")
    if username is None or password is None:
        return "", 400  # 400 - BAD REQUEST

    user = User.query.filter_by(username=username).first()
    user_not_found = user is None
    if user_not_found:
        return "", 404  # 404 - NOT FOUND

    user.password = bcrypt.generate_password_hash(password).decode()
    db.session.commit()

    return "", 204  # 204 - NO CONTENT
