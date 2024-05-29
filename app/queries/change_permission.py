from app.shared.database import get_connection, release_connection


def change_permission(username: str, permission: str) -> bool:
    if permission not in ("read-write", "read-only"):
        return False
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                UPDATE accounts
                SET permission = %s
                WHERE username = %s
            """
            cursor.execute(query, (permission, username))
            connection.commit()

            change_permission_successful: bool = cursor.rowcount == 1
            return change_permission_successful
        finally:
            cursor.close()
            release_connection(connection)
    except:
        return False
