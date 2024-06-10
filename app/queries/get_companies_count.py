from app.shared.database import get_connection, release_connection


def get_companies_count() -> int | None:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                SELECT COUNT(*) FROM companies;
            """
            cursor.execute(query)
            (count,) = cursor.fetchone()
            return count
        finally:
            cursor.close()
            release_connection(connection)
    except:
        return None
