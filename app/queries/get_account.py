from typing import Dict, Tuple
from collections import namedtuple
from app.shared.database import get_connection, release_connection


def get_account(username: str) -> Dict[str, str] | None:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                SELECT
                    username,
                    password,
                    role,
                    permission
                FROM accounts
                WHERE username = %s
            """
            cursor.execute(query, (username,))
            account: Tuple[str, str, str, str] | None = cursor.fetchone()
            if not account:
                return None

            User = namedtuple(
                "User", field_names=["username", "password", "role", "permission"]
            )
            user = User(*account)
            return {
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "permission": user.permission,
            }
        finally:
            cursor.close()
            release_connection(connection)
    except:
        return None
