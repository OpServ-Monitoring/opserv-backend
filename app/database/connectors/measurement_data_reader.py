from database.helper.base_database_connector import DatabaseConnector
from database.tables.measurements_table_management import MeasurementsTableManagement


class MeasurementDataReader(DatabaseConnector):
    @classmethod
    def get_condensed_data(cls, component_type: str, component_arg: str, metric_name: str, start_time: int,
                           end_time: int,
                           limit: float) -> list:
        connection = cls._connection_helper.retrieve_database_connection()

        result = connection.execute(
            """SELECT
                   avg({4}) AS {4},
                   min({5} * 1.0) AS minimum,
                   avg({5} * 1.0) AS average,
                   max({5} * 1.0) AS maximum
                FROM {0}
                WHERE {4} > ? AND {4} < ?
                      AND {1} = ? AND {2} = IFNULL(?, "default") AND {3} = ?
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
        connection = cls._connection_helper.retrieve_database_connection()

        result = connection.execute(
            """SELECT CAST({4} as int)
                FROM {0}
                WHERE {1} = ? and {2} = IFNULL(?, "default") and {3} = ?
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
