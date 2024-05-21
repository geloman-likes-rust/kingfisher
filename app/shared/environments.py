from os import getenv

pg_host = getenv("PGHOST")
pg_user = getenv("PGUSER")
pg_password = getenv("PGPASSWORD")
pg_database = getenv("PGDATABASE")

redis_host = getenv("REDIS_HOST")
redis_user = getenv("REDIS_USER")
redis_password = getenv("REDIS_PASSWORD")

jwt_secret = getenv("JWT_SECRET")
allowed_origin = getenv("ALLOWED_ORIGIN")

super_admin_username = getenv("SUPER_ADMIN_USERNAME")
super_admin_password = getenv("SUPER_ADMIN_PASSWORD")
