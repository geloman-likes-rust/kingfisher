from typing import Literal
from psycopg2 import IntegrityError, Error
from app.shared.database import get_connection, release_connection


def create_company(
    company: str,
) -> Literal["Success", "CompanyExists", "DatabaseUnavailable"]:
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
            return "Success"

        except IntegrityError:
            return "CompanyExists"

        finally:
            cursor.close()
            release_connection(connection)

    except Error:
        return "DatabaseUnavailable"
