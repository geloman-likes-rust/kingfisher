from typing import List, Dict, Tuple
from app.shared.database import get_connection, release_connection


def get_accounts() -> List[Dict[str, str]] | None:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                SELECT
                    username,
                    role,
                    permission
                FROM accounts
            """
            cursor.execute(query)

            accounts: List[Tuple[str, str, str]] = cursor.fetchall()
            if not accounts:
                return []

            return [
                {"username": username, "role": role, "permission": permission}
                for username, role, permission in accounts
            ]
        finally:
            cursor.close()
            release_connection(connection)
    except:
        return None
