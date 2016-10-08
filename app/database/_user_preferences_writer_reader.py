from database.database_open_helper import DatabaseOpenHelper
from .tables.user_preferences_table_management import UserPreferencesTableManagement


class UserPreferencesWriterReader:
    @staticmethod
    def get_user_preference(key):
        if key is None:
            return None

        connection = DatabaseOpenHelper.establish_database_connection()

        user_preference = connection.execute(
            "SELECT {0}, {1} FROM {2} WHERE {0} = ?".format(
                UserPreferencesTableManagement.KEY_KEY(),
                UserPreferencesTableManagement.KEY_VALUE(),
                UserPreferencesTableManagement.TABLE_NAME()
            ),
            (
                key
            )
        ).fetchone()

        connection.close()

        return user_preference

    @staticmethod
    def set_user_preference(key, value):
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
