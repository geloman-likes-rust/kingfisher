from typing import Dict, List, Literal
from psycopg2 import Error, IntegrityError
from app.shared.database import get_connection, release_connection


def create_parent_companies(
    company: str, parent_companies: List[Dict[str, str]]
) -> Literal[
    "Success", "Failed", "NotUnique", "CompanyNotFound", "DatabaseUnavailable"
]:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            for parent in parent_companies:
                parent_company = (
                    parent.get("company"),
                    parent.get("relation"),
                )
                match all(field is not None for field in parent_company):
                    case True:
                        query = """
                            INSERT INTO parent_companies
                                (company_id, parent_id, relation)
                            VALUES
                                (
                                    (SELECT id FROM companies WHERE name = %s),
                                    (SELECT id FROM companies WHERE name = %s), 
                                    %s
                                )
                        """
                        parent, relation = (parent["company"], parent["relation"])
                        print("parent = ", parent, "relation = ", relation)
                        cursor.execute(query, (company, parent, relation))

                    case False:
                        return "Failed"

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

    except Error as e:
        print("PGERROR = ", e.pgerror)
        print("PGCODE = ", e.pgcode)
        return "DatabaseUnavailable"
