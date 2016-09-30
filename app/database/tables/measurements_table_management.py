import sqlite3


class MeasurementsTableManagement:
    __TABLE_NAME = "measurements_table"

    __KEY_COMPONENT_ARG_FK = "measurement_component_arg_fk"
    __KEY_COMPONENT_TYPE_FK = "measurement_component_type_fk"
    __KEY_METRIC_FK = "measurement_metric_fk"
    __KEY_TIMESTAMP = "measurement_timestamp"
    __KEY_VALUE = "measurement_value"

    @staticmethod
    def TABLE_NAME():
        return MeasurementsTableManagement.__TABLE_NAME

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
    def get_inserter():
        return MeasurementsTableManagement.__InsertTransaction()

    @staticmethod
    def get_count():
        con = sqlite3.connect("opserv.db")

        with con:
            return con.execute("SELECT COUNT(*) FROM measurements_table").fetchone()[0]

    class __InsertTransaction:
        def __init__(self):
            self.__reset_variables()

        def __reset_variables(self):
            self.__insertions = []

        def insert_measurement(self, component_type, component_arg, metric_name, timestamp, value):
            self.__insertions.append((component_type, component_arg, metric_name, timestamp, value))

        def commit_transaction(self):
            connection = sqlite3.connect("opserv.db")

            # TODO Either check for foreign keys manually or add triggers to the database
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
