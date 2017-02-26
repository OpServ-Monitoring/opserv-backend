from passlib.hash import argon2

from database.helper.base_database_connector import DatabaseConnector
from database.tables.users_table_management import UsersTableManagement


class UsersWriterReader(DatabaseConnector):
    @classmethod
    def get_all_users(cls) -> list:
        connection = cls._connection_helper.retrieve_database_connection()

        users = connection.execute(
            """
              SELECT {1}, {2}
              FROM {0}
            """.format(
                UsersTableManagement.TABLE_NAME(),
                UsersTableManagement.KEY_ID(),
                UsersTableManagement.KEY_NAME(),
                UsersTableManagement.KEY_PASSWORD()
            )
        ).fetchall()

        connection.close()

        # TODO Could need some formatting
        return users

    @classmethod
    def get_user(cls, user_name):
        connection = cls._connection_helper.retrieve_database_connection()

        user = connection.execute(
            """
              SELECT {1}, {2}
              FROM {0}
              WHERE {2} = ?
            """.format(
                UsersTableManagement.TABLE_NAME(),
                UsersTableManagement.KEY_ID(),
                UsersTableManagement.KEY_NAME(),
                UsersTableManagement.KEY_PASSWORD()
            ),
            (user_name,)
        ).fetchone()

        connection.close()

        # TODO Could need some formatting
        return user

    @classmethod
    def does_user_exist(cls, user_name):
        return cls.get_user(user_name) is not None

    @classmethod
    def is_password_valid(cls, user_name: str, user_password: str) -> bool:
        connection = cls._connection_helper.retrieve_database_connection()

        hashed_user_password = connection.execute(
            """
              SELECT {3}
              FROM {0}
              WHERE {2} = ?
            """.format(
                UsersTableManagement.TABLE_NAME(),
                UsersTableManagement.KEY_ID(),
                UsersTableManagement.KEY_NAME(),
                UsersTableManagement.KEY_PASSWORD()
            ),
            (
                user_name,
            )
        ).fetchone()

        if hashed_user_password is None:
            return False
        else:
            hashed_user_password = hashed_user_password[0]

            return argon2.verify(user_password, hashed_user_password)

    @classmethod
    def add_user(cls, user_name: str, user_password: str):
        hashed_user_password = argon2.hash(user_password)

        connection = cls._connection_helper.retrieve_database_connection()
        connection.execute(
            "INSERT INTO {0} ({2}, {3}) VALUES (?, ?)".format(
                UsersTableManagement.TABLE_NAME(),
                UsersTableManagement.KEY_ID(),
                UsersTableManagement.KEY_NAME(),
                UsersTableManagement.KEY_PASSWORD()
            ),
            (
                user_name,
                hashed_user_password
            )
        )

        connection.commit()
        connection.close()

    @classmethod
    def delete_user(cls, user_name: str):
        connection = cls._connection_helper.retrieve_database_connection()
        connection.execute(
            "DELETE FROM {0} WHERE {2} = ?".format(
                UsersTableManagement.TABLE_NAME(),
                UsersTableManagement.KEY_ID(),
                UsersTableManagement.KEY_NAME(),
                UsersTableManagement.KEY_PASSWORD()
            ),
            (
                user_name,
            )
        )

        connection.commit()
        connection.close()

    @classmethod
    def change_user_password(cls, user_name: str, new_user_password: str):
        hashed_user_password = argon2.hash(new_user_password)

        connection = cls._connection_helper.retrieve_database_connection()
        connection.execute(
            "UPDATE {0} SET {3} = ? WHERE {2} = ?".format(
                UsersTableManagement.TABLE_NAME(),
                UsersTableManagement.KEY_ID(),
                UsersTableManagement.KEY_NAME(),
                UsersTableManagement.KEY_PASSWORD()
            ),
            (
                hashed_user_password,
                user_name
            )
        )

        connection.commit()
        connection.close()
