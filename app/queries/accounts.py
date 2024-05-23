from collections import namedtuple
from typing import Dict, List, Tuple
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


def get_accounts() -> List[Dict[str, str]] | None:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                SELECT
                    username,
                    role,
                    permission
                FROM accounts
            """
            cursor.execute(query)

            accounts: List[Tuple[str, str, str]] = cursor.fetchall()
            if not accounts:
                return []

            return [
                {"username": username, "role": role, "permission": permission}
                for username, role, permission in accounts
            ]
        finally:
            cursor.close()
            release_connection(connection)
    except:
        return None


def get_account(username: str) -> Dict[str, str] | None:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                SELECT
                    username,
                    password,
                    role,
                    permission
                FROM accounts
                WHERE username = %s
            """
            cursor.execute(query, (username,))
            account: Tuple[str, str, str, str] | None = cursor.fetchone()
            if not account:
                return None

            User = namedtuple(
                "User", field_names=["username", "password", "role", "permission"]
            )
            user = User(*account)
            return {
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "permission": user.permission,
            }
        finally:
            cursor.close()
            release_connection(connection)
    except:
        return None


def change_password(username: str, old_pass: str, new_pass: str) -> bool:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                UPDATE accounts
                SET password = %s
                WHERE username = %s
                AND password = %s
            """
            cursor.execute(query, (new_pass, username, old_pass))
            connection.commit()

            change_password_successful: bool = cursor.rowcount == 1
            return change_password_successful

        finally:
            cursor.close()
            release_connection(connection)
    except:
        return False


def change_role(username: str, role: str) -> bool:
    if role not in ("admin", "user"):
        return False
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                UPDATE accounts
                SET role = %s
                WHERE username = %s
            """
            cursor.execute(query, (role, username))
            connection.commit()

            change_role_successful: bool = cursor.rowcount == 1
            return change_role_successful

        finally:
            cursor.close()
            release_connection(connection)
    except:
        return False


def change_permission(username: str, permission: str) -> bool:
    if permission not in ("read-write", "read-only"):
        return False
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = """
                UPDATE accounts
                SET permission = %s
                WHERE username = %s
            """
            cursor.execute(query, (permission, username))
            connection.commit()

            change_permission_successful: bool = cursor.rowcount == 1
            return change_permission_successful
        finally:
            cursor.close()
            release_connection(connection)
    except:
        return False
