from app.shared.database import get_connection, release_connection


def change_password(username: str, old_pass: str, new_pass: str) -> bool:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                UPDATE accounts
                SET password = %s
                WHERE username = %s
                AND password = %s
            """
            cursor.execute(query, (new_pass, username, old_pass))
            connection.commit()

            change_password_successful: bool = cursor.rowcount == 1
            return change_password_successful

        finally:
            cursor.close()
            release_connection(connection)
    except:
        return False
