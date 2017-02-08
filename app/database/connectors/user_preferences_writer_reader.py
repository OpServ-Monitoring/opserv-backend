from database.helper.base_database_connector import DatabaseConnector

from database.tables.user_preferences_table_management import UserPreferencesTableManagement


class UserPreferencesWriterReader(DatabaseConnector):
    @classmethod
    def get_user_preference(cls, key):
        connection = cls._connection_helper.retrieve_database_connection()

        user_preference = connection.execute(
            """
              SELECT {2}
              FROM {0}
              WHERE {1} = ?
            """.format(
                UserPreferencesTableManagement.TABLE_NAME(),
                UserPreferencesTableManagement.KEY_KEY(),
                UserPreferencesTableManagement.KEY_VALUE(),
            ),
            (
                (key,)
            )
        ).fetchone()

        connection.close()

        if user_preference is None:
            return None

        # TODO Change accordingly after helper extraction
        from database.connectors.component_metrics_writer_reader import ComponentMetricsWriterReader
        return ComponentMetricsWriterReader.unpack_single_element_tuple(user_preference)

    @classmethod
    def set_user_preference(cls, key, value):
        connection = cls._connection_helper.retrieve_database_connection()

        connection.execute(
            "REPLACE INTO {0} ({1}, {2}) VALUES (?, ?)".format(
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

    @classmethod
    def delete_user_preference(cls, key):
        connection = cls._connection_helper.retrieve_database_connection()

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

    @classmethod
    def get_used_user_preference_keys(cls) -> list:
        connection = cls._connection_helper.retrieve_database_connection()

        user_preference_keys = connection.execute(
            """
              SELECT {0}
              FROM {1}
            """.format(
                UserPreferencesTableManagement.KEY_KEY(),
                UserPreferencesTableManagement.TABLE_NAME()
            )
        ).fetchall()

        connection.close()

        # TODO Change accordingly after helper extraction
        from database.connectors.component_metrics_writer_reader import ComponentMetricsWriterReader
        return ComponentMetricsWriterReader.unpack_single_element_tuples(user_preference_keys)
