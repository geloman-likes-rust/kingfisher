from typing import Literal
from psycopg2 import Error, IntegrityError
from app.extensions.hasher import bcrypt
from app.shared.database import get_connection, release_connection


def create_account(
    username: str | None = None,
    password: str | None = None,
    role="user",
    permission="read-only",
) -> Literal[
    "NoUsername",
    "NoPassword",
    "InvalidRole",
    "InvalidPermission",
    "Success",
    "AccountExists",
    "DatabaseUnavailable",
]:

    if not username:
        return "NoUsername"

    if not password:
        return "NoPassword"

    if role not in ("user", "admin"):
        return "InvalidRole"

    if permission not in ("read-only", "read-write"):
        return "InvalidPermission"

    if role == "admin":
        permission = "read-write"

    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                INSERT INTO accounts
                    (username, password, role, permission)
                VALUES
                    (%s, %s, %s, %s)
            """
            hashed_password = bcrypt.generate_password_hash(password).decode()
            cursor.execute(query, (username, hashed_password, role, permission))
            connection.commit()
            return "Success"

        except IntegrityError:
            return "AccountExists"

        finally:
            cursor.close()
            release_connection(connection)

    except Error:
        return "DatabaseUnavailable"
