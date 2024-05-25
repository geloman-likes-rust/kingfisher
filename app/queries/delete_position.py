from app.shared.database import get_connection, release_connection


def delete_position(position: str):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                DELETE FROM positions
                WHERE name = %s
            """
            cursor.execute(query, (position,))
            connection.commit()

            deletion_success: bool = cursor.rowcount == 1
            return deletion_success
        finally:
            cursor.close()
            release_connection(connection)
    except:
        return False
