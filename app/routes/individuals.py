from http import HTTPStatus
from typing import Dict, List
from flask import Blueprint, Response, jsonify, request
from app.shared.cache import delete_cache, get_cache, cache_response
from app.decorators.authorization import jwt_required, write_access_required


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


@individuals.post("/<company>/individuals")
@jwt_required
@write_access_required
def create_individuals(company: str):
    from app.queries.create_individuals import create_individuals

    company = company.replace("%20", " ").replace("+", " ")

    individuals: List[Dict[str, str]] | None = request.json
    match individuals:
        case [] | None:
            return Response(status=HTTPStatus.BAD_REQUEST)

        case list():
            match create_individuals(company, individuals):
                case "Success":
                    delete_cache(f"/companies/{company}/individuals")
                    delete_cache(f"/companies/{company}/related-individuals")
                    return Response(status=HTTPStatus.CREATED)

                case "NotUnique":
                    return Response(status=HTTPStatus.CONFLICT)

                case "CompanyNotFound":
                    return Response(status=HTTPStatus.NOT_FOUND)

                case "DatabaseUnavailable":
                    return Response(status=HTTPStatus.SERVICE_UNAVAILABLE)


@individuals.delete("/<company>/individuals")
@jwt_required
@write_access_required
def delete_individual(company: str):
    from app.queries.delete_individual import delete_individual

    company = company.replace("%20", " ").replace("+", " ")

    payload: Dict[str, str] | None = request.json
    match payload:
        case dict():
            individual = (
                payload.get("firstname"),
                payload.get("lastname"),
                payload.get("position"),
            )
            match all(field is not None for field in individual):
                case True:
                    firstname, lastname, position = (
                        payload["firstname"],
                        payload["lastname"],
                        payload["position"],
                    )

                    match delete_individual(firstname, lastname, position, company):
                        case True:
                            delete_cache(f"/companies/{company}/individuals")
                            delete_cache(f"/companies/{company}/related-individuals")
                            return Response(status=HTTPStatus.NO_CONTENT)

                        case False:
                            return Response(status=HTTPStatus.NOT_FOUND)

                case False:
                    return Response(status=HTTPStatus.BAD_REQUEST)
        case None:
            return Response(status=HTTPStatus.BAD_REQUEST)
