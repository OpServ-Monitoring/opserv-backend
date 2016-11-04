from database.database_open_helper import DatabaseOpenHelper

from .tables.user_preferences_table_management import UserPreferencesTableManagement


# TODO Improve methods and write tests


class UserPreferencesWriterReader:
    @staticmethod
    def get_user_preference(key):
        if key is None:
            return None

        connection = DatabaseOpenHelper.establish_database_connection()

        user_preference = connection.execute(
            """
              SELECT {0}, {1}
              FROM {2}
              WHERE {0} = ?
            """.format(
                UserPreferencesTableManagement.KEY_KEY(),
                UserPreferencesTableManagement.KEY_VALUE(),
                UserPreferencesTableManagement.TABLE_NAME()
            ),
            (
                (key,)
            )
        ).fetchone()

        connection.close()

        return user_preference

    @staticmethod
    def set_user_preference(key, value):
        if key is None:
            return None

        connection = DatabaseOpenHelper.establish_database_connection()

        connection.execute(
            "INSERT OR REPLACE INTO {0} ({1}, {2}) VALUES (?, ?)".format(
                UserPreferencesTableManagement.TABLE_NAME(),
                UserPreferencesTableManagement.KEY_KEY(),
                UserPreferencesTableManagement.KEY_VALUE()
            ),
            (
                key,
                value
            )
        )

        connection.commit()
        connection.close()

    @staticmethod
    def delete_user_preference(key):
        if key is None:
            return None

        connection = DatabaseOpenHelper.establish_database_connection()

        connection.execute(
            """
              DELETE
              FROM {0}
              WHERE {1} = ?
            """.format(
                UserPreferencesTableManagement.TABLE_NAME(),
                UserPreferencesTableManagement.KEY_KEY()
            ),
            (
                (key,)
            )
        )
        connection.commit()

        connection.close()

    @staticmethod
    def get_used_user_preference_keys() -> map:
        connection = DatabaseOpenHelper.establish_database_connection()

        user_preference = connection.execute(
            """
              SELECT {0}
              FROM {1}
            """.format(
                UserPreferencesTableManagement.KEY_KEY(),
                UserPreferencesTableManagement.TABLE_NAME()
            )
        ).fetchall()

        connection.close()

        return map(lambda row: row[0], user_preference)

    # TODO embed into db or api call
    @staticmethod
    def is_valid_json(value):
        import json

        return json.loads(value) is not None
