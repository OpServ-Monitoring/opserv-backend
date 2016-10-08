import sqlite3

from database.database_open_helper import DatabaseOpenHelper


class MeasurementInsertTransaction:
    def __init__(self):
        self.__reset_variables()

    def __reset_variables(self):
        self.__insertions = []

    def insert_measurement(self, metric_name, timestamp, value, component_type, component_arg="default"):
        if component_arg is None:
            component_arg = "default"

        self.__insertions.append((component_type, component_arg, metric_name, timestamp, value))

    def commit_transaction(self):
        connection = DatabaseOpenHelper.establish_database_connection()

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
