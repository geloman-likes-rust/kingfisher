from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.shared.environments import redis_host

limiter = Limiter(get_remote_address, storage_uri=f"redis://{redis_host}:6379")
