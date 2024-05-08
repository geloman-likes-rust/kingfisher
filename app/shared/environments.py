from os import getenv

pg_host = getenv("PGHOST")
pg_user = getenv("PGUSER")
pg_password = getenv("PGPASSWORD")
pg_database = getenv("PGDATABASE")
jwt_secret = getenv("JWT_SECRET")
allowed_origin = getenv("ALLOWED_ORIGIN")
