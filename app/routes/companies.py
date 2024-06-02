from http import HTTPStatus
from typing import Dict, List
from flask.blueprints import Blueprint
from flask import Response, jsonify, request
from app.shared.cache import cache_response, get_cache, delete_cache
from app.decorators.authorization import jwt_required, write_access_required

companies = Blueprint("companies", __name__, url_prefix="/api/v1")


@companies.get("/companies")
@jwt_required
def get_companies(_):
    from app.queries.get_companies import get_companies

    limit: int = request.args.get("limit", type=int) or 10
    offset: int = request.args.get("offset", type=int) or 0

    endpoint = f"/companies?limit={limit}&offset={offset}"

    cached = get_cache(endpoint)
    match cached:
        # CACHE HIT
        case list() | dict():
            return jsonify(cached)

        # CACHE MISS
        case None:
            companies: List[str] | None = get_companies(limit, offset)
            match companies:
                case list():
                    cache_response(endpoint, response=companies)
                    return jsonify(companies)

                case None:
                    return Response(status=HTTPStatus.NOT_FOUND)


@companies.post("/companies")
@jwt_required
@write_access_required
def create_company():
    from app.queries.create_company import create_company

    payload: Dict[str, str] | None = request.json

    match payload:
        case dict():
            company = payload.get("company")
            match company:
                case str():
                    match create_company(company):
                        case "Success":
                            delete_cache("/companies?*")
                            delete_cache(f"/companies/{company}/individuals")
                            delete_cache(f"/companies/{company}/parent-companies")
                            delete_cache(f"/companies/{company}/related-individuals")
                            return Response(status=HTTPStatus.CREATED)

                        case "CompanyExists":
                            return Response(status=HTTPStatus.CONFLICT)

                        case "DatabaseUnavailable":
                            return Response(status=HTTPStatus.SERVICE_UNAVAILABLE)
                case None:
                    return Response(status=HTTPStatus.BAD_REQUEST)
        case None:
            return Response(status=HTTPStatus.BAD_REQUEST)


@companies.delete("/companies")
def delete_company():
    from app.queries.delete_company import delete_company

    payload: Dict[str, str] | None = request.json
    match payload:
        case dict():
            company: str | None = payload.get("company")
            match company:
                case str():
                    match delete_company(company):
                        case True:
                            delete_cache("/companies?*")
                            delete_cache(f"/companies/{company}/individuals")
                            delete_cache(f"/companies/{company}/parent-companies")
                            delete_cache(f"/companies/{company}/related-individuals")
                            return Response(status=HTTPStatus.NO_CONTENT)

                        case False:
                            return Response(status=HTTPStatus.NOT_FOUND)
                case None:
                    return Response(status=HTTPStatus.BAD_REQUEST)
        case None:
            return Response(status=HTTPStatus.BAD_REQUEST)


@companies.patch("/companies")
def update_company_name():
    from app.queries.change_company_name import change_company_name

    payload: Dict[str, str] | None = request.json

    match payload:
        case dict():
            old_name, new_name = payload.get("old_name"), payload.get("new_name")
            if not old_name or not new_name:
                return Response(status=HTTPStatus.BAD_REQUEST)

            match change_company_name(old_name, new_name):
                case True:
                    delete_cache(endpoint="/companies?*")
                    delete_cache(endpoint=f"/companies/{old_name}/individuals")
                    delete_cache(endpoint=f"/companies/{old_name}/parent-companies")
                    delete_cache(endpoint=f"/companies/{old_name}/related-individuals")
                    return Response(status=HTTPStatus.NO_CONTENT)

                case False:
                    return Response(status=HTTPStatus.NOT_FOUND)

        case None:
            return Response(status=HTTPStatus.BAD_REQUEST)
