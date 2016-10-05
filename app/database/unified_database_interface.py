import sqlite3


class UnifiedDatabaseInterface:
    # TODO Is comp / arg vorhanden?

    @staticmethod
    def get_measurement_insertion_transaction():
        return UnifiedDatabaseInterface.__InsertTransaction()

    class __InsertTransaction:
        def __init__(self):
            self.__reset_variables()

        def __reset_variables(self):
            self.__insertions = []

        def insert_measurement(self, metric_name, timestamp, value, component_type, component_arg="default"):
            if component_arg is None:
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
    def _is_component_arg_persisted(component_type, component_arg):
        all_args = UnifiedDatabaseInterface.get_component_args(component_type)

        return component_arg in all_args

    @staticmethod
    def get_component_args(component_type):
        con = sqlite3.connect("opserv.db")  # TODO Set location globally

        query = """
        SELECT component_arg
        FROM component_metrics_table
        WHERE component_type_fk = ?
        """

        with con:
            return con.execute(query, (component_type,)).fetchall()

    @staticmethod
    def get_count():
        con = sqlite3.connect("opserv.db")  # TODO Set location globally

        with con:
            return con.execute("SELECT COUNT(*) FROM measurements_table").fetchone()[0]

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

        connection = sqlite3.connect("opserv.db") # TODO Set location globally
        cursor = connection.execute(query, params)

        result = cursor.fetchall()
        return result
