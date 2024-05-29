from typing import List
from app.shared.database import get_connection, release_connection


def get_companies(limit: int = 10, offset: int = 0) -> List[str] | None:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                SELECT name
                FROM companies
                ORDER BY id
                LIMIT %s
                OFFSET %s
            """
            cursor.execute(query, (limit, offset))
            companies = cursor.fetchall()
            match companies:
                case []:
                    return []
                case list():
                    return [company for (company,) in companies]
        finally:
            cursor.close()
            release_connection(connection)
    except:
        return None
