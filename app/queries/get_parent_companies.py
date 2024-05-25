from typing import Dict, List, Tuple
from app.shared.database import get_connection, release_connection


def get_parent_companies(company: str) -> List[Dict[str, str]] | None:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                SELECT
                    companies.name as parent,
                    parent_companies.relation
                FROM parent_companies
                INNER JOIN companies
                ON companies.id = parent_companies.parent_id
                WHERE parent_companies.company_id = (SELECT id FROM companies WHERE name = %s)
            """
            cursor.execute(query, (company,))

            # [(company, relation), ...] --> List[Tuple[str, str]]
            companies: List[Tuple[str, str]] = cursor.fetchall()

            match companies:
                case []:
                    return []
                case list():
                    return [
                        {"company": parent, "relation": relation}
                        for parent, relation in companies
                    ]

        finally:
            cursor.close()
            release_connection(connection)
    except:
        return None
