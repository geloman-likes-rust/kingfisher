from typing import Literal
from psycopg2 import Error, IntegrityError
from app.shared.database import get_connection, release_connection


def create_position(
    position: str,
) -> Literal["Success", "NotUnique", "DatabaseUnavailable"]:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                INSERT INTO positions (name) VALUES (%s)
            """
            cursor.execute(query, (position,))
            connection.commit()
            return "Success"

        finally:
            cursor.close()
            release_connection(connection)

    except IntegrityError:
        return "NotUnique"

    except Error:
        return "DatabaseUnavailable"
