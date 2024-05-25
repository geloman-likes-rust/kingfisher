from app.shared.database import get_connection, release_connection


def delete_company(company: str) -> bool:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                DELETE FROM companies
                WHERE name = %s
            """
            cursor.execute(query, (company,))
            connection.commit()

            deletion_success = cursor.rowcount == 1
            return deletion_success
        finally:
            cursor.close()
            release_connection(connection)
    except:
        return False
