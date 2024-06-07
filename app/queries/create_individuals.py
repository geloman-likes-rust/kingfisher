from typing import List, Dict, Literal
from psycopg2 import Error, IntegrityError
from app.shared.database import get_connection, release_connection


def create_individuals(
    company: str, individuals: List[Dict[str, str]]
) -> Literal["Success", "NotUnique", "CompanyNotFound", "DatabaseUnavailable"]:

    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                INSERT INTO individuals
                    (firstname, lastname, position_id, company_id)
                VALUES
                    (
                        %s, %s, -- (firstname, lastname)
                        (SELECT id FROM positions WHERE name = %s), -- position_id
                        (SELECT id FROM companies WHERE name = %s) -- company_id
                    );
            """
            for individual in individuals:
                firstname, lastname, position = (
                    individual["firstname"],
                    individual["lastname"],
                    individual["position"],
                )

                cursor.execute(query, (firstname, lastname, position, company))
            connection.commit()

            return "Success"

        finally:
            cursor.close()
            release_connection(connection)

    except IntegrityError as e:
        not_null_violation: bool = e.pgcode == "23502"
        match not_null_violation:
            case True:
                return "CompanyNotFound"

            case False:
                return "NotUnique"

    except Error:
        return "DatabaseUnavailable"
