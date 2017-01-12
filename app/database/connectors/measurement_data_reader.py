from database.helper.base_database_connector import DatabaseConnector
from database.tables.measurements_table_management import MeasurementsTableManagement


class MeasurementDataReader(DatabaseConnector):
    @classmethod
    def get_min_avg_max(cls, component_type: str, component_arg: str, metric_name: str, start_time: int, end_time: int,
                        limit: float):
        connection = cls._connection_helper.retrieve_database_connection()

        result = connection.execute(
            """SELECT measurement_component_type_fk, measurement_component_arg_fk, measurement_metric_fk,
                   avg(measurement_timestamp) AS measurement_timestamp,
                   min(measurement_value * 1.0) AS minimum,
                   avg(measurement_value * 1.0) AS average,
                   max(measurement_value * 1.0) AS maximum
                FROM measurements_table
                WHERE measurement_timestamp > ? AND measurement_timestamp < ?
                      AND measurement_component_type_fk = ? AND measurement_component_arg_fk = ? AND measurement_metric_fk = ?
                GROUP BY CAST((measurement_timestamp - ?) / ((? - ?) / CAST(? as float)) as int)
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
    def get_last_value(cls, component_type: str, component_arg: str, metric_name: str):
        connection = cls._connection_helper.retrieve_database_connection()

        result = connection.execute(
            """
            SELECT {4}, {5}
            FROM {0}
            WHERE {1} = ?
              AND {2} = ?
              AND {3} = ?
            ORDER BY {4} DESC
            LIMIT 1
            """.format(
                MeasurementsTableManagement.TABLE_NAME(),
                MeasurementsTableManagement.KEY_COMPONENT_TYPE_FK(),
                MeasurementsTableManagement.KEY_COMPONENT_ARG_FK(),
                MeasurementsTableManagement.KEY_METRIC_FK(),
                MeasurementsTableManagement.KEY_TIMESTAMP(),
                MeasurementsTableManagement.KEY_VALUE()
            ),
            (component_type, component_arg, metric_name)
        ).fetchone()

        return result
