from app.shared.database import get_connection, release_connection


def delete_account(username: str) -> bool:
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
            return deletion_success

        finally:
            cursor.close()
            release_connection(connection)
    except:
        return False
