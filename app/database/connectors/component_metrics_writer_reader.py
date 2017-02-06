from database.helper.base_database_connector import DatabaseConnector
from database.tables.component_metrics_table_management import ComponentMetricsTableManagement


class ComponentMetricsWriterReader(DatabaseConnector):
    @classmethod
    def get_gathering_rates(cls):
        """
        Retrieves all component-metric entries from the database with a set gathering rate
        :return: A list of tuples containing all gatherings rates with their respective identifiers
        """
        connection = cls._connection_helper.retrieve_database_connection()

        gathering_rates = connection.execute(
            """SELECT
                    {1},
                    CASE {2} WHEN 'default' THEN Null ELSE {2} END as {2},
                    {3},
                    {4}
                FROM {0}
                WHERE {4} IS NOT NULL
            """.format(
                ComponentMetricsTableManagement.TABLE_NAME(),
                ComponentMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
                ComponentMetricsTableManagement.KEY_COMPONENT_ARG(),
                ComponentMetricsTableManagement.KEY_COMPONENT_METRIC_FK(),
                ComponentMetricsTableManagement.KEY_COMPONENT_GATHERING_RATE()
            )
        ).fetchall()

        connection.close()

        return gathering_rates

    @classmethod
    def get_gathering_rate(cls, component_type, component_arg, metric):
        connection = cls._connection_helper.retrieve_database_connection()

        gathering_rate = connection.execute(
            """SELECT {4}
                FROM {0}
                WHERE
                  {1} = ? AND
                  {2} = IFNULL(?, "default") AND
                  {3} = ?
            """.format(
                ComponentMetricsTableManagement.TABLE_NAME(),
                ComponentMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
                ComponentMetricsTableManagement.KEY_COMPONENT_ARG(),
                ComponentMetricsTableManagement.KEY_COMPONENT_METRIC_FK(),
                ComponentMetricsTableManagement.KEY_COMPONENT_GATHERING_RATE()
            ),
            (component_type, component_arg, metric)
        ).fetchone()

        connection.close()

        if gathering_rate is not None:
            return gathering_rate[0]
        return gathering_rate

    @classmethod
    def set_gathering_rate(cls, component_type, component_arg, metric, gathering_rate):
        connection = cls._connection_helper.retrieve_database_connection()

        connection.execute(
            """REPLACE INTO {0} ({1}, {2}, {3}, {4}) VALUES(?, IFNULL(?, "default"), ?, ?)""".format(
                ComponentMetricsTableManagement.TABLE_NAME(),
                ComponentMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
                ComponentMetricsTableManagement.KEY_COMPONENT_ARG(),
                ComponentMetricsTableManagement.KEY_COMPONENT_METRIC_FK(),
                ComponentMetricsTableManagement.KEY_COMPONENT_GATHERING_RATE()
            ),
            (component_type, component_arg, metric, gathering_rate)
        )
        connection.commit()
        connection.close()

    @classmethod
    def get_component_args(cls, component_type):
        connection = cls._connection_helper.retrieve_database_connection()

        raw_component_args = connection.execute(
            """SELECT
                  DISTINCT CASE {2} WHEN 'default' THEN Null ELSE {2} END as {2}
                FROM {0}
                WHERE {1} = ?
            """.format(
                ComponentMetricsTableManagement.TABLE_NAME(),
                ComponentMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
                ComponentMetricsTableManagement.KEY_COMPONENT_ARG()
            ),
            (
                component_type,
            )
        ).fetchall()

        connection.close()

        return cls.unpack_single_element_tuples(raw_component_args)

    # HELPER METHODS - Extract those maybe
    @classmethod
    def unpack_single_element_tuple(cls, single_element_tuple: tuple):
        # TODO Should there be a length check or any sort of validation?
        return single_element_tuple[0]

    @classmethod
    def unpack_single_element_tuples(cls, single_element_tuples: list) -> list:
        return list(
            map(
                cls.unpack_single_element_tuple,
                single_element_tuples
            )
        )

    # USED FOR SETUP ONLY - may be extracted to somewhere else
    @classmethod
    def insert_component_metrics(cls, component_metrics):
        connection = cls._connection_helper.retrieve_database_connection()

        connection.executemany(
            """INSERT OR REPLACE
                INTO {0}
                ({1}, {2}, {3}, {4})
                VALUES (?, IFNULL(?, "default"), ?, ?)
            """.format(
                ComponentMetricsTableManagement.TABLE_NAME(),
                ComponentMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
                ComponentMetricsTableManagement.KEY_COMPONENT_ARG(),
                ComponentMetricsTableManagement.KEY_COMPONENT_METRIC_FK(),
                ComponentMetricsTableManagement.KEY_COMPONENT_GATHERING_RATE()
            ), component_metrics
        )

        connection.commit()
        connection.close()

    @classmethod
    def are_gathering_rates_set(cls):
        return len(cls.get_gathering_rates()) > 0
