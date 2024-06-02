from typing import List, Tuple, Dict
from app.shared.database import get_connection, release_connection


def get_related_individuals(company: str) -> List[Dict[str, str]] | None:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                WITH company_id AS
                    (SELECT id FROM companies WHERE name = %s),
                company_individuals AS (
                    SELECT firstname, lastname
                    FROM individuals
                    WHERE company_id = (SELECT id FROM company_id)
                )
                SELECT 
                    individuals.firstname 
                    || ' ' || individuals.lastname AS fullname,
                    positions.name as position,
                    companies.name as company
                FROM individuals
                INNER JOIN positions
                ON individuals.position_id = positions.id
                INNER JOIN companies
                ON individuals.company_id = companies.id
                WHERE (firstname, lastname) IN (SELECT firstname, lastname FROM company_individuals)
                AND individuals.company_id != (SELECT id FROM company_id);
            """
            cursor.execute(query, (company,))

            # [(fullname, position, company), ...] --> List[Tuple[str, str, str]]
            related_individuals: List[Tuple[str, str, str]] = cursor.fetchall()
            match related_individuals:
                case []:
                    return []

                case list():
                    return [
                        {"fullname": fullname, "position": position, "company": company}
                        for fullname, position, company in related_individuals
                    ]

        finally:
            cursor.close()
            release_connection(connection)
    except:
        return None
