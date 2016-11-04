from .database_open_helper import DatabaseOpenHelper
from .tables.component_metrics_table_management import ComponentMetricsTableManagement


class ComponentMetricsWriterReader:
    @staticmethod
    def are_gathering_rates_set():
        connection = DatabaseOpenHelper.establish_database_connection()

        are_gathering_rates_set = connection.execute(
            "SELECT COUNT(*) FROM {0} WHERE {1} IS NOT NULL".format(
                ComponentMetricsTableManagement.TABLE_NAME(),
                ComponentMetricsTableManagement.KEY_COMPONENT_GATHERING_RATE()
            )
        ).fetchone()[0] >= 1

        connection.close()

        return are_gathering_rates_set

    @staticmethod
    def get_gathering_rates():
        connection = DatabaseOpenHelper.establish_database_connection()

        gathering_rates = connection.execute(
            "SELECT * FROM {0} WHERE {1} IS NOT NULL".format(
                ComponentMetricsTableManagement.TABLE_NAME(),
                ComponentMetricsTableManagement.KEY_COMPONENT_GATHERING_RATE()
            )
        ).fetchall()

        connection.close()

        return gathering_rates

    @staticmethod
    def insert_component_metrics(component_metrics):
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

        connection = DatabaseOpenHelper.establish_database_connection()

        connection.executemany("INSERT OR REPLACE INTO {0} ({1}, {2}, {3}, {4}) VALUES (?, ? , ?, ?)".format(
            ComponentMetricsTableManagement.TABLE_NAME(),
            ComponentMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
            ComponentMetricsTableManagement.KEY_COMPONENT_ARG(),
            ComponentMetricsTableManagement.KEY_COMPONENT_METRIC_FK(),
            ComponentMetricsTableManagement.KEY_COMPONENT_GATHERING_RATE()
        ), component_metrics)

        connection.commit()
        connection.close()

    @staticmethod
    def _is_component_arg_persisted(component_type, component_arg):
        connection = DatabaseOpenHelper.establish_database_connection()

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

    @staticmethod
    def get_component_args(component_type):
        connection = DatabaseOpenHelper.establish_database_connection()

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