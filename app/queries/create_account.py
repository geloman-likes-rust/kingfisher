from app.shared.database import get_connection, release_connection


def create_account(
    username: str, password: str, role="user", permission="read-only"
) -> bool:

    valid_role: bool = role in ("user", "admin")
    valid_permission: bool = permission in ("read-only", "read-write")

    if not valid_role or not valid_permission:
        return False

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
            return True

        finally:
            cursor.close()
            release_connection(connection)
    except:
        return False
