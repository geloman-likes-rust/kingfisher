from app.shared.database import get_connection, release_connection


def delete_parent_company(company: str, parent: str) -> bool:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                DELETE FROM parent_companies
                WHERE company_id = (SELECT id FROM companies WHERE name = %s)
                AND parent_id = (SELECT id FROM companies WHERE name = %s)
            """
            cursor.execute(query, (company, parent))
            connection.commit()

            deletion_success: bool = cursor.rowcount == 1
            return deletion_success

        finally:
            cursor.close()
            release_connection(connection)

    except:
        return False
