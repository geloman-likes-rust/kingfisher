from http import HTTPStatus
from flask import Blueprint, Response, jsonify
from app.decorators.authorization import jwt_required
from app.shared.cache import get_cache, cache_response


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
