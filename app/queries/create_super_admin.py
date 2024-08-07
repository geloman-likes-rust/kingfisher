from app.extensions.hasher import bcrypt
from psycopg2 import IntegrityError, Error
from app.shared.database import get_connection, release_connection
from app.shared.environments import super_admin_username as username
from app.shared.environments import super_admin_password as password


def create_super_admin():

    if not username or not password:
        if not username:
            print("SUPER_ADMIN_USERNAME hasn't been set!")
        if not password:
            print("SUPER_ADMIN_PASSWORD hasn't been set!")
        return None

    hashed_password = bcrypt.generate_password_hash(password).decode()

    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                INSERT INTO accounts
                    (username, password, role, permission)
                VALUES
                    (%s, %s, 'admin', 'read-write')
            """
            cursor.execute(query, (username, hashed_password))
            connection.commit()
            print(f"Super Admin (username: {username}) has been created..")

        except IntegrityError:
            print(
                f"IntegrityError from create_super_admin: Super Admin (username: {username}) already exists!"
            )

        finally:
            cursor.close()
            release_connection(connection)

    except Error as e:
        print("Error from create_super_admin:", e)
