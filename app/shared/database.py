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


# def initialize_connection_pool(
#     retries=5,
# ) -> Tuple[Callable, Callable[..., None]]:
#     if retries == 0:
#         print("Database connection failed after multiple attempts.")
#         exit(1)
#
#     print(f"Attempting to connect to the database. Number of retries left: {retries}")
#     sleep(1)
#
#     try:
#
#         connection_pool = SimpleConnectionPool(
#             minconn=1,
#             maxconn=5,
#             host=pg_host,
#             user=pg_user,
#             dbname=pg_database,
#             password=pg_password,
#         )
#
#         def get_connection():
#             return connection_pool.getconn()
#
#         def release_connection(connection):
#             connection_pool.putconn(connection)
#
#         print("Database connection established successfully.")
#         return get_connection, release_connection
#
#     except OperationalError:
#         return initialize_connection_pool(retries - 1)


# get_connection, release_connection = initialize_connection_pool()
