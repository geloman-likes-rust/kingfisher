from redis import Redis
from app.shared.environments import redis_host, redis_user, redis_password

redis_client = Redis(host=redis_host, username=redis_user, password=redis_password)
