import sqlite3

from database.database_open_helper import DatabaseOpenHelper


class MeasurementDataReader:
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

        connection = DatabaseOpenHelper.establish_database_connection()
        cursor = connection.execute(query, params)

        result = cursor.fetchall()
        return result
