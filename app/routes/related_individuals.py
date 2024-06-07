from http import HTTPStatus
from flask import Blueprint, Response, jsonify
from app.decorators.authorization import jwt_required
from app.shared.cache import get_cache, cache_response


related_individuals = Blueprint(
    "related_individuals", __name__, url_prefix="/api/v1/companies"
)


@related_individuals.get("/<company>/related-individuals")
@jwt_required
def get_related_individuals(_, company: str):
    from app.queries.get_related_individuals import get_related_individuals

    company = company.replace("%20", " ").replace("+", " ")

    endpoint = f"/companies/{company}/related-individuals"
    cached = get_cache(endpoint)
    match cached:
        # CACHE HIT
        case list() | dict():
            return jsonify(cached)

        # CACHE MISS
        case None:
            related_individuals = get_related_individuals(company)
            match related_individuals:
                case list():
                    cache_response(endpoint, related_individuals)
                    return jsonify(related_individuals)

                case None:
                    return Response(status=HTTPStatus.NOT_FOUND)
