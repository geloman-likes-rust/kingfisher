import json
from typing import Any, Dict, List
from app.shared.redis import redis_client


def get_cache(
    endpoint: str,
) -> Dict[str, Any] | List[Dict[str, Any]] | List[str] | None:
    cached = redis_client.get(endpoint)
    match cached:
        case bytes() | str():
            deserialized = json.loads(cached)
            return deserialized
        case None | _:
            return None


def cache_response(
    endpoint: str,
    response: Dict[str, Any] | List[Dict[str, Any]] | List[str],
    ttl: int = 300,
) -> None:
    """
    Cache the `response` from the specified `endpoint` for a certain `time` period in seconds.

    Parameters:

        endpoint (`str`): The `endpoint` from which the `response` is obtained.
        response (`dict` or `list`): The `response` obtained from the `endpoint`.
        ttl (`int`, `optional`): Defaults to `300 seconds` (5 minutes).

    Returns:
        `None`
    """

    serilized = json.dumps(response)
    redis_client.setex(name=endpoint, value=serilized, time=ttl)


def delete_cache(endpoint: str) -> None:
    match ("*" in endpoint):
        case True:
            caches = redis_client.keys(endpoint)
            match caches:
                case []:
                    return None

                case list():
                    redis_client.delete(*caches)

                case _:
                    return None

        case False:
            redis_client.delete(endpoint)
