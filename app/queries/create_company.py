from app.shared.database import get_connection, release_connection


def create_company(company: str) -> bool:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                INSERT INTO companies
                    (name)
                VALUES
                    (%s)
            """
            cursor.execute(query, (company,))
            connection.commit()
            return True
        finally:
            cursor.close()
            release_connection(connection)
    except:
        return False
