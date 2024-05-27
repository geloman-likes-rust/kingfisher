from typing import Literal
from psycopg2 import Error, IntegrityError
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
            cursor.execute(query, (username, password, role, permission))
            connection.commit()
            return "Success"

        except IntegrityError:
            return "AccountExists"

        finally:
            cursor.close()
            release_connection(connection)

    except Error:
        return "DatabaseUnavailable"
