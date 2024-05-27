from typing import Literal
from app.shared.database import get_connection, release_connection


def delete_account(
    username: str | None = None,
) -> Literal["NoUsername", "Success", "Failed", "DatabaseUnavailable"]:

    if not username:
        return "NoUsername"

    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                DELETE FROM accounts
                WHERE username = %s
            """
            cursor.execute(query, (username,))
            connection.commit()

            deletion_success: bool = cursor.rowcount == 1
            if deletion_success:
                return "Success"
            return "Failed"

        finally:
            cursor.close()
            release_connection(connection)
    except:
        return "DatabaseUnavailable"
