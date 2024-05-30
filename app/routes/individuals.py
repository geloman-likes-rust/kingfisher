from http import HTTPStatus
from flask import Blueprint, Response, jsonify
from app.decorators.authorization import jwt_required


individuals = Blueprint("individuals", __name__, url_prefix="/api/v1/companies")


@individuals.get("/<company>/individuals")
@jwt_required
def get_individuals(_, company: str):
    from app.queries.get_individuals import get_individuals

    company = company.replace("%20", " ").replace("+", " ")

    individuals = get_individuals(company)
    match individuals:
        case list():
            return jsonify(individuals)
        case None:
            return Response(status=HTTPStatus.NOT_FOUND)
