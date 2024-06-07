from http import HTTPStatus
from typing import Dict, List
from flask import Blueprint, Response, jsonify, request
from app.shared.cache import get_cache, cache_response, delete_cache
from app.decorators.authorization import jwt_required, write_access_required


parent_companies = Blueprint(
    "parent_companies", __name__, url_prefix="/api/v1/companies"
)


@parent_companies.get("/<company>/parent-companies")
@jwt_required
def get_parent_companies(_, company: str):
    from app.queries.get_parent_companies import get_parent_companies

    company = company.replace("%20", " ").replace("+", " ")

    endpoint = f"/companies/{company}/parent-companies"
    cached = get_cache(endpoint)
    match cached:
        # CACHE HIT
        case list() | dict():
            return jsonify(cached)

        # CACHE MISS
        case None:
            parent_companies = get_parent_companies(company)
            match parent_companies:
                case list():
                    cache_response(endpoint, parent_companies)
                    return jsonify(parent_companies)

                case None:
                    return Response(status=HTTPStatus.NOT_FOUND)


@parent_companies.post("/<company>/parent-companies")
@jwt_required
@write_access_required
def create_parent_companies(company: str):
    from app.queries.create_parent_companies import create_parent_companies

    company = company.replace("%20", " ").replace("+", " ")

    parent_companies: List[Dict[str, str]] | None = request.json
    match parent_companies:
        case []:
            return Response(status=HTTPStatus.BAD_REQUEST)

        case list():
            match create_parent_companies(company, parent_companies):
                case "Success":
                    delete_cache(f"/companies/{company}/parent-companies")
                    return Response(status=HTTPStatus.CREATED)

                case "Failed":
                    return Response(status=HTTPStatus.BAD_REQUEST)

                case "NotUnique":
                    return Response(status=HTTPStatus.CONFLICT)

                case "CompanyNotFound":
                    return Response(status=HTTPStatus.NOT_FOUND)

                case "DatabaseUnavailable":
                    return Response(status=HTTPStatus.SERVICE_UNAVAILABLE)

        case None:
            return Response(status=HTTPStatus.BAD_REQUEST)


@parent_companies.delete("/<company>/parent-companies")
@jwt_required
@write_access_required
def delete_parent_company(company: str):
    from app.queries.delete_parent_company import delete_parent_company

    company = company.replace("%20", " ").replace("+", " ")

    payload: Dict[str, str] | None = request.json
    match payload:
        case dict():
            parent = payload.get("company")
            match parent:
                case str():
                    match delete_parent_company(company, parent):
                        case True:
                            delete_cache(f"/companies/{company}/parent-companies")
                            return Response(status=HTTPStatus.NO_CONTENT)

                        case False:
                            return Response(status=HTTPStatus.NOT_FOUND)

                case None:
                    return Response(status=HTTPStatus.BAD_REQUEST)

        case None:
            return Response(status=HTTPStatus.BAD_REQUEST)
