from http import HTTPStatus
from flask import Blueprint, Response, jsonify


parent_companies = Blueprint(
    "parent_companies", __name__, url_prefix="/api/v1/companies"
)


@parent_companies.get("/<company>/parent-companies")
def get_parent_companies(company: str):
    from app.queries.get_parent_companies import get_parent_companies

    company = company.replace("%20", " ").replace("+", " ")

    parent_companies = get_parent_companies(company)
    match parent_companies:
        case list():
            return jsonify(parent_companies)
        case None:
            return Response(status=HTTPStatus.NOT_FOUND)
