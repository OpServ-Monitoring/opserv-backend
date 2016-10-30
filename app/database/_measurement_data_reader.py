from .database_open_helper import DatabaseOpenHelper
from .tables.measurements_table_management import MeasurementsTableManagement


class MeasurementDataReader:
    @staticmethod
    def get_min_avg_max(component_type: str, component_arg: str, metric_name: str, start_time: int, end_time: int,
                        limit: float):
        connection = DatabaseOpenHelper.establish_database_connection()

        result = connection.execute(
            """SELECT
                 {1}, {2}, {3},
                 avg({4}) AS measurement_timestamp,
                 CAST(min({5}) AS FLOAT) AS minimum,
                 avg({5}) AS average,
                 CAST(max({5}) AS FLOAT) AS maximum
               FROM (
                 SELECT
                   (SELECT COUNT(*)
                    FROM {0}
                    WHERE {4} > ? AND {4} < ? AND {1} = ? AND {2} = ? AND {3} = ?
                    ) AS row_count,

                   (SELECT COUNT(0)
                    FROM {0} t1
                    WHERE t1.{4} < t2.{4} AND t1.{4} > ? AND t1.{4} < ?
                      AND t1.{1} = ? AND t1.{2} = ?  AND t1.{3} = ?
                    ORDER BY {4} ASC
                    ) AS row_number,

                    *
                    FROM {0} t2
                    WHERE t2.{4} > ? AND t2.{4} < ?
                      AND t2.{1} = ? AND t2.{2} = ? AND t2.{3} = ?
                    ORDER BY {4} ASC)
               GROUP BY CAST((row_number / (row_count / ?)) AS INT)""".format(
                MeasurementsTableManagement.TABLE_NAME(),
                MeasurementsTableManagement.KEY_COMPONENT_TYPE_FK(),
                MeasurementsTableManagement.KEY_COMPONENT_ARG_FK(),
                MeasurementsTableManagement.KEY_METRIC_FK(),
                MeasurementsTableManagement.KEY_TIMESTAMP(),
                MeasurementsTableManagement.KEY_VALUE()
            ),
            (
                start_time, end_time, component_type, component_arg, metric_name,
                start_time, end_time, component_type, component_arg, metric_name,
                start_time, end_time, component_type, component_arg, metric_name,
                limit
            )
        ).fetchall()

        connection.close()
        return result

    @staticmethod
    def get_last_value(component_type: str, component_arg: str, metric_name: str):
        connection = DatabaseOpenHelper.establish_database_connection()

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
