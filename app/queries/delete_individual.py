from app.shared.database import get_connection, release_connection


def delete_individual(name: str, position: str, company: str) -> bool:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                DELETE FROM individuals
                WHERE name = %s
                AND position_id = (SELECT id FROM positions WHERE name = %s)
                AND company_id = (SELECT id FROM companies WHERE name = %s)
            """
            cursor.execute(query, (name, position, company))
            connection.commit()

            deletion_success: bool = cursor.rowcount == 1
            return deletion_success

        finally:
            cursor.close()
            release_connection(connection)
    except:
        return False
