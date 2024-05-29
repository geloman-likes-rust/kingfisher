from typing import List, Dict
from app.queries.get_companies import get_companies
from app.queries.get_positions import get_positions
from app.shared.database import get_connection, release_connection


def create_individuals(company: str, individuals: List[Dict[str, str]]) -> bool:
    companies = get_companies()
    positions = get_positions()

    if not companies or not positions:
        return False

    if company not in companies:
        return False

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

                if position not in positions:
                    return False

                cursor.execute(query, (firstname, lastname, position, company))
            connection.commit()

            return True

        finally:
            cursor.close()
            release_connection(connection)
    except:
        return False
