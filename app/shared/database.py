from psycopg2.pool import SimpleConnectionPool
from app.shared.environments import pg_host, pg_user, pg_password, pg_database

connection_pool = SimpleConnectionPool(
    minconn=1,
    maxconn=5,
    host=pg_host,
    user=pg_user,
    dbname=pg_database,
    password=pg_password,
)


def get_connection():
    return connection_pool.getconn()


def release_connection(connection):
    connection_pool.putconn(connection)
