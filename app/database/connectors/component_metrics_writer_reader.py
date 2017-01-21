from database.helper.base_database_connector import DatabaseConnector
from database.tables.component_metrics_table_management import ComponentMetricsTableManagement


class ComponentMetricsWriterReader(DatabaseConnector):
    @classmethod
    def are_gathering_rates_set(cls):
        connection = cls._connection_helper.retrieve_database_connection()

        are_gathering_rates_set = connection.execute(
            "SELECT COUNT(*) FROM {0} WHERE {1} IS NOT NULL".format(
                ComponentMetricsTableManagement.TABLE_NAME(),
                ComponentMetricsTableManagement.KEY_COMPONENT_GATHERING_RATE()
            )
        ).fetchone()[0] >= 1

        connection.close()

        return are_gathering_rates_set

    @classmethod
    def get_gathering_rates(cls):
        connection = cls._connection_helper.retrieve_database_connection()

        gathering_rates = connection.execute(
            "SELECT * FROM {0} WHERE {1} IS NOT NULL".format(
                ComponentMetricsTableManagement.TABLE_NAME(),
                ComponentMetricsTableManagement.KEY_COMPONENT_GATHERING_RATE()
            )
        ).fetchall()

        connection.close()

        return gathering_rates

    @classmethod
    def get_gathering_rate(cls, component_type, component_arg, metric):
        connection = cls._connection_helper.retrieve_database_connection()

        # TODO Better handle this
        if component_arg is None:
            component_arg = "default"

        gathering_rate = connection.execute(
            "SELECT * FROM {0} WHERE {1} = ? AND {2} = ? AND {3} = ? AND {4} IS NOT NULL".format(
                ComponentMetricsTableManagement.TABLE_NAME(),
                ComponentMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
                ComponentMetricsTableManagement.KEY_COMPONENT_ARG(),
                ComponentMetricsTableManagement.KEY_COMPONENT_METRIC_FK(),
                ComponentMetricsTableManagement.KEY_COMPONENT_GATHERING_RATE()
            ),
            (component_type, component_arg, metric)
        ).fetchone()

        connection.close()

        return gathering_rate

    @classmethod
    def set_gathering_rate(cls, component_type, component_arg, metric, gathering_rate):
        connection = cls._connection_helper.retrieve_database_connection()

        connection.execute(
            "REPLACE INTO {0} ({1}, {2}, {3}, {4}) VALUES(?, ?, ?, ?)".format(
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
    def insert_component_metrics(cls, component_metrics):
        # TODO Change param to receive each param one by one, make None -> "default" for args
        # quick fix
        def test(component_metric):
            if component_metric[1] is None:
                return (
                    component_metric[0],
                    "default",
                    component_metric[2],
                    component_metric[3]
                )

            return component_metric

        component_metrics = map(
            lambda item: test(item),
            component_metrics
        )

        connection = cls._connection_helper.retrieve_database_connection()

        connection.executemany("INSERT OR REPLACE INTO {0} ({1}, {2}, {3}, {4}) VALUES (?, ? , ?, ?)".format(
            ComponentMetricsTableManagement.TABLE_NAME(),
            ComponentMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
            ComponentMetricsTableManagement.KEY_COMPONENT_ARG(),
            ComponentMetricsTableManagement.KEY_COMPONENT_METRIC_FK(),
            ComponentMetricsTableManagement.KEY_COMPONENT_GATHERING_RATE()
        ), component_metrics)

        connection.commit()
        connection.close()

    @classmethod
    def _is_component_arg_persisted(cls, component_type, component_arg):
        connection = cls._connection_helper.retrieve_database_connection()

        is_component_arg_persisted = connection.execute(
            "SELECT COUNT(*) FROM {0} WHERE {1} = ? AND {2} = ?".format(
                ComponentMetricsTableManagement.TABLE_NAME(),
                ComponentMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
                ComponentMetricsTableManagement.KEY_COMPONENT_ARG()
            ),
            (
                component_type,
                component_arg
            )
        ).fetchone()[0] > 0

        connection.close()

        return is_component_arg_persisted

    @classmethod
    def get_component_args(cls, component_type):
        connection = cls._connection_helper.retrieve_database_connection()

        raw_component_args = connection.execute(
            "SELECT DISTINCT {0} FROM {1} WHERE {2} = ?".format(
                ComponentMetricsTableManagement.KEY_COMPONENT_ARG(),
                ComponentMetricsTableManagement.TABLE_NAME(),
                ComponentMetricsTableManagement.KEY_COMPONENT_TYPE_FK()
            ),
            (
                component_type,
            )
        ).fetchall()

        connection.close()

        return list(
            map(
                lambda x: x[0],
                raw_component_args
            )
        )
