from typing import List, Tuple

from app.shared.database import get_connection, release_connection


def get_positions() -> List[str] | None:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                SELECT name FROM positions
            """
            cursor.execute(query)

            # [(position), ...] --> List[Tuple[str]]
            positions: List[Tuple[str]] = cursor.fetchall()

            match positions:
                case []:
                    return []
                case list():
                    return [position for (position,) in positions]
        finally:
            cursor.close()
            release_connection(connection)
    except:
        return None
