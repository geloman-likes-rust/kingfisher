from app.shared.database import get_connection, release_connection


def create_position(position: str) -> bool:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                INSERT INTO positions (name) VALUES (%s)
            """
            cursor.execute(query, (position,))
            connection.commit()
            return True
        finally:
            cursor.close()
            release_connection(connection)
    except:
        return False
