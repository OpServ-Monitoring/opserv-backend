import sqlite3

from .component_metrics_table_management import ComponentMetricsTableManagement
from .general_table_management import GeneralTableManagement


class MeasurementsTableManagement(GeneralTableManagement):
    __KEY_COMPONENT_ARG_FK = "measurement_component_arg_fk"
    __KEY_COMPONENT_TYPE_FK = "measurement_component_type_fk"
    __KEY_METRIC_FK = "measurement_metric_fk"
    __KEY_TIMESTAMP = "measurement_timestamp"
    __KEY_VALUE = "measurement_value"

    @classmethod
    def TABLE_NAME(cls) -> str:
        return "measurements_table"

    @staticmethod
    def KEY_COMPONENT_ARG_FK():
        return MeasurementsTableManagement.__KEY_COMPONENT_ARG_FK

    @staticmethod
    def KEY_COMPONENT_TYPE_FK():
        return MeasurementsTableManagement.__KEY_COMPONENT_TYPE_FK

    @staticmethod
    def KEY_METRIC_FK():
        return MeasurementsTableManagement.__KEY_METRIC_FK

    @staticmethod
    def KEY_TIMESTAMP():
        return MeasurementsTableManagement.__KEY_TIMESTAMP

    @staticmethod
    def KEY_VALUE():
        return MeasurementsTableManagement.__KEY_VALUE

    @staticmethod
    def _get_columns() -> list:
        return [
            (MeasurementsTableManagement.KEY_COMPONENT_ARG_FK(), GeneralTableManagement._type_text_not_null),
            (MeasurementsTableManagement.KEY_COMPONENT_TYPE_FK(), GeneralTableManagement._type_text_not_null),
            (MeasurementsTableManagement.KEY_METRIC_FK(), GeneralTableManagement._type_text_not_null),
            (MeasurementsTableManagement.KEY_TIMESTAMP(), "INTEGER NOT NULL"),
            (MeasurementsTableManagement.KEY_VALUE(), GeneralTableManagement._type_text_not_null)
        ]

    @staticmethod
    def _get_primary_key() -> list:
        return [
            MeasurementsTableManagement.KEY_COMPONENT_TYPE_FK(),
            MeasurementsTableManagement.KEY_COMPONENT_ARG_FK(),
            MeasurementsTableManagement.KEY_METRIC_FK(),
            MeasurementsTableManagement.KEY_TIMESTAMP()
        ]

    @staticmethod
    def _get_foreign_keys() -> list:
        return [
            GeneralTableManagement._build_foreign_key(
                [
                    MeasurementsTableManagement.KEY_COMPONENT_TYPE_FK(),
                    MeasurementsTableManagement.KEY_COMPONENT_ARG_FK(),
                    MeasurementsTableManagement.KEY_METRIC_FK()
                ],
                ComponentMetricsTableManagement.TABLE_NAME(),
                [
                    ComponentMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
                    ComponentMetricsTableManagement.KEY_COMPONENT_ARG(),
                    ComponentMetricsTableManagement.KEY_COMPONENT_METRIC_FK()
                ]
            )
        ]

    @staticmethod
    def get_inserter():
        return MeasurementsTableManagement.__InsertTransaction()

    @staticmethod
    def get_count():
        con = sqlite3.connect("opserv.db")  # TODO Set location globally

        with con:
            return con.execute("SELECT COUNT(*) FROM measurements_table").fetchone()[0]

    class __InsertTransaction:
        def __init__(self):
            self.__reset_variables()

        def __reset_variables(self):
            self.__insertions = []

        def insert_measurement(self, metric_name, timestamp, value, component_type, component_arg="default"):
            if component_arg == None:
                component_arg = "default"
            self.__insertions.append((component_type, component_arg, metric_name, timestamp, value))

        def commit_transaction(self):
            connection = sqlite3.connect("opserv.db")  # TODO Set location globally

            connection.executemany(
                "INSERT INTO measurements_table ("
                "measurement_component_type_fk, "
                "measurement_component_arg_fk, "
                "measurement_metric_fk, "
                "measurement_timestamp, "
                "measurement_value) VALUES (?, ? ,? ,?, ?)",
                self.__insertions
            )

            connection.commit()

            self.__reset_variables()

        def rollback(self):
            self.__reset_variables()

    @staticmethod
    def get_min_avg_max(component_type: str, component_arg: str, metric_name: str, start_time: int, end_time: int,
                        limit: float):
        def triple_tuple(*base_tuple):
            return 3 * base_tuple

        query = """  SELECT
                      measurement_component_type_fk,
                      measurement_component_arg_fk,
                      measurement_metric_fk,
                      avg(measurement_timestamp) AS measurement_timestamp,
                      CAST(min(measurement_value) AS FLOAT) AS minimum,
                      avg(measurement_value) AS average,
                      CAST(max(measurement_value) AS FLOAT) AS maximum
                    FROM (
                         SELECT
                            (SELECT COUNT(*)
                              FROM measurements_table
                                  WHERE measurement_timestamp > ? AND measurement_timestamp < ?
                                  AND measurement_component_type_fk = ? AND measurement_component_arg_fk = ?
                                  AND measurement_metric_fk = ?)
                            AS row_count,

                            (SELECT COUNT(0)
                              FROM measurements_table t1
                                  WHERE t1.measurement_timestamp < t2.measurement_timestamp
                                  AND t1.measurement_timestamp > ? AND t1.measurement_timestamp < ?
                                  AND t1.measurement_component_type_fk = ? AND t1.measurement_component_arg_fk = ?
                                  AND t1.measurement_metric_fk = ?
                                  ORDER BY measurement_timestamp ASC )
                            AS row_number,

                            *
                            FROM measurements_table t2
                            WHERE t2.measurement_timestamp > ? AND t2.measurement_timestamp < ?
                                  AND t2.measurement_component_type_fk = ? AND t2.measurement_component_arg_fk = ?
                                  AND t2.measurement_metric_fk = ?

                            ORDER BY measurement_timestamp ASC)
                    GROUP BY CAST((row_number / (row_count / ?)) AS INT)
        """

        params = (
            *triple_tuple(
                start_time, end_time, component_type, component_arg, metric_name
            ),
            limit
        )

        connection = sqlite3.connect("opserv.db")
        cursor = connection.execute(query, params)

        result = cursor.fetchall()
        print(result)
        return result
