from database.helper.base_database_connector import DatabaseConnector
from database.tables.measurements_table_management import MeasurementsTableManagement


class MeasurementDataReader(DatabaseConnector):
    @classmethod
    def get_min_avg_max(cls, component_type: str, component_arg: str, metric_name: str, start_time: int, end_time: int,
                        limit: float) -> list:
        if component_type is None:
            raise TypeError("The component_type has to be a valid string.")

        if metric_name is None:
            raise TypeError("The metric_name has to be a valid string.")

        if start_time is None:
            raise TypeError("The start_time has to be a valid integer.")

        if end_time is None:
            raise TypeError("The end_time has to be a valid integer.")

        if limit is None:
            raise TypeError("The limit has to be a valid integer.")

        if component_arg is None:
            # TODO Log debug - No component_arg specified, changed to "default"
            component_arg = "default"

        connection = cls._connection_helper.retrieve_database_connection()

        result = connection.execute(
            """SELECT {1}, {2}, {3},
                   avg({4}) AS {4},
                   min({5} * 1.0) AS minimum,
                   avg({5} * 1.0) AS average,
                   max({5} * 1.0) AS maximum
                FROM {0}
                WHERE {4} > ? AND {4} < ?
                      AND {1} = ? AND {2} = ? AND {3} = ?
                GROUP BY CAST(({4} - ?) / ((? - ?) / CAST(? as float)) as int)
                """.format(
                MeasurementsTableManagement.TABLE_NAME(),
                MeasurementsTableManagement.KEY_COMPONENT_TYPE_FK(),
                MeasurementsTableManagement.KEY_COMPONENT_ARG_FK(),
                MeasurementsTableManagement.KEY_METRIC_FK(),
                MeasurementsTableManagement.KEY_TIMESTAMP(),
                MeasurementsTableManagement.KEY_VALUE()
            ),
            (
                start_time, end_time, component_type, component_arg, metric_name,
                start_time, end_time, start_time, float(limit)
            )
        ).fetchall()

        connection.close()
        return result

    @classmethod
    def get_timestamp_of_first_measurement(cls, component_type: str, component_arg: str, metric_name: str) -> int:
        if component_type is None:
            raise TypeError("The component_type has to be a valid string.")

        if metric_name is None:
            raise TypeError("The metric_name has to be a valid string.")

        if component_arg is None:
            # TODO Log debug - No component_arg specified, changed to "default"
            component_arg = "default"

        connection = cls._connection_helper.retrieve_database_connection()

        result = connection.execute(
            """SELECT CAST({4} as int)
                FROM {0}
                WHERE {1} = ? and {2} = ? and {3} = ?
                ORDER BY {4} ASC
                """.format(
                MeasurementsTableManagement.TABLE_NAME(),
                MeasurementsTableManagement.KEY_COMPONENT_TYPE_FK(),
                MeasurementsTableManagement.KEY_COMPONENT_ARG_FK(),
                MeasurementsTableManagement.KEY_METRIC_FK(),
                MeasurementsTableManagement.KEY_TIMESTAMP()
            ),
            (
                component_type, component_arg, metric_name,
            )
        ).fetchone()

        connection.close()

        if result is None:
            return 0

        return result[0]
