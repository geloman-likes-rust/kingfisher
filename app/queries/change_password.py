from typing import Literal
from psycopg2 import Error
from app.extensions.hasher import bcrypt
from app.queries.get_account import get_account
from app.shared.database import get_connection, release_connection


def change_password(username: str, old_pass: str, new_pass: str) -> Literal[
    "Success",
    "Failed",
    "AccountNotFound",
    "PasswordDontMatch",
    "DatabaseUnavailable",
]:

    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:

            account = get_account(username)

            match account:
                case None:
                    return "AccountNotFound"

                case dict():

                    old_password_hash = account["password"]

                    password_dont_match: bool = not bcrypt.check_password_hash(
                        old_password_hash, old_pass
                    )

                    if password_dont_match:
                        return "PasswordDontMatch"

                    new_password_hash = bcrypt.generate_password_hash(new_pass).decode()

                    query = """
                        UPDATE accounts
                        SET password = %s
                        WHERE username = %s
                        AND password = %s
                    """
                    cursor.execute(
                        query, (new_password_hash, username, old_password_hash)
                    )

                    connection.commit()

                    success: bool = cursor.rowcount == 1

                    if success:
                        return "Success"

                    return "Failed"

        finally:
            cursor.close()
            release_connection(connection)

    except Error:
        return "DatabaseUnavailable"
