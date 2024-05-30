from http import HTTPStatus
from flask import Blueprint, Response, jsonify
from app.decorators.authorization import jwt_required
from app.shared.cache import get_cache, cache_response


individuals = Blueprint("individuals", __name__, url_prefix="/api/v1/companies")


@individuals.get("/<company>/individuals")
@jwt_required
def get_individuals(_, company: str):
    from app.queries.get_individuals import get_individuals

    company = company.replace("%20", " ").replace("+", " ")

    endpoint = f"/companies/{company}/individuals"
    cached = get_cache(endpoint)
    match cached:
        # CACHE HIT
        case list() | dict():
            return jsonify(cached)

        # CACHE MISS
        case None:
            individuals = get_individuals(company)
            match individuals:
                case list():
                    cache_response(endpoint, individuals)
                    return jsonify(individuals)
                case None:
                    return Response(status=HTTPStatus.NOT_FOUND)
