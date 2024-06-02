from typing import Dict
from http import HTTPStatus
from flask import Blueprint, Response, jsonify, request
from app.shared.cache import cache_response, delete_cache, get_cache
from app.shared.limiter import limiter


positions = Blueprint("positions", __name__, url_prefix="/api/v1")


@positions.get("/positions")
def get_positions():
    from app.queries.get_positions import get_positions

    cached = get_cache("/positions")
    match cached:
        # CACHE HIT
        case list() | dict():
            return jsonify(cached)

        # CACHE MISS
        case None:
            positions = get_positions()
            match positions:
                case list():
                    cache_response("/positions", positions)
                    return jsonify(positions)

                case None:
                    return Response(status=HTTPStatus.NOT_FOUND)


@positions.post("/positions")
@limiter.limit("50/day;25/hour")
def create_position():
    from app.queries.create_position import create_position

    payload: Dict[str, str] | None = request.json
    match payload:
        case dict():
            position = payload.get("position")
            match position:
                case str():
                    match create_position(position):
                        case "Success":
                            delete_cache("/positions")
                            return Response(status=HTTPStatus.CREATED)

                        case "NotUnique":
                            return Response(status=HTTPStatus.CONFLICT)

                        case "DatabaseUnavailable":
                            return Response(status=HTTPStatus.SERVICE_UNAVAILABLE)

                case None:
                    return Response(status=HTTPStatus.BAD_REQUEST)
        case None:
            return Response(status=HTTPStatus.BAD_REQUEST)


@positions.delete("/positions")
def delete_position():
    from app.queries.delete_position import delete_position

    payload: Dict[str, str] | None = request.json
    match payload:
        case dict():
            position = payload.get("position")
            match position:
                case str():
                    match delete_position(position):
                        case True:
                            delete_cache("/positions")
                            return Response(status=HTTPStatus.NO_CONTENT)

                        case False:
                            return Response(status=HTTPStatus.NOT_FOUND)

                case None:
                    return Response(status=HTTPStatus.BAD_REQUEST)
        case None:
            return Response(status=HTTPStatus.BAD_REQUEST)
