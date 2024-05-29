from http import HTTPStatus
from flask import Blueprint, Response, jsonify


individuals = Blueprint("individuals", __name__, url_prefix="/api/v1/companies")


@individuals.get("/<company>/individuals")
def get_individuals(company: str):
    from app.queries.get_individuals import get_individuals

    company = company.replace("%20", " ").replace("+", " ")

    individuals = get_individuals(company)
    match individuals:
        case list():
            return jsonify(individuals)
        case None:
            return Response(status=HTTPStatus.NOT_FOUND)
