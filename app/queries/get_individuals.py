from typing import List, Dict, Tuple
from app.shared.database import get_connection, release_connection


def get_individuals(company: str) -> List[Dict[str, str]] | None:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                SELECT
                    individuals.firstname
                        || ' ' ||
                    individuals.lastname as fullname,
                    positions.name as position
                FROM individuals
                INNER JOIN positions
                ON individuals.position_id = positions.id
                WHERE individuals.company_id = (SELECT id FROM companies WHERE name = %s)
            """
            cursor.execute(query, (company,))

            # [(name, position), ...] --> List[Tuple[str, str]]
            individuals: List[Tuple[str, str]] = cursor.fetchall()

            match individuals:
                case []:
                    return []

                case list():
                    return [
                        {"name": name, "position": position}
                        for name, position in individuals
                    ]

        finally:
            cursor.close()
            release_connection(connection)
    except:
        return None
