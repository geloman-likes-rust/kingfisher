from app.shared.database import get_connection, release_connection


def change_role(username: str, role: str) -> bool:
    if role not in ("admin", "user"):
        return False
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                UPDATE accounts
                SET role = %s
                WHERE username = %s
            """
            cursor.execute(query, (role, username))
            connection.commit()

            change_role_successful: bool = cursor.rowcount == 1
            return change_role_successful

        finally:
            cursor.close()
            release_connection(connection)
    except:
        return False
