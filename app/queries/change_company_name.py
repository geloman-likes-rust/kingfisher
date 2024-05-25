from app.shared.database import get_connection, release_connection


def change_company_name(old_name: str, new_name: str) -> bool:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                UPDATE companies
                SET name = %s
                WHERE name = %s
            """
            cursor.execute(query, (new_name, old_name))
            connection.commit()

            change_name_successful: bool = cursor.rowcount == 1
            return change_name_successful
        finally:
            cursor.close()
            release_connection(connection)
    except:
        return False
