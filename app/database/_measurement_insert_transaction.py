from database.database_connector import DatabaseConnector
from .database_open_helper import DatabaseOpenHelper
from .tables.measurements_table_management import MeasurementsTableManagement


class MeasurementInsertTransaction(DatabaseConnector):
    def __init__(self):
        self.__reset_variables()

    def __reset_variables(self):
        self.__insertions = []

    def insert_measurement(self, metric_name, timestamp, value, component_type, component_arg="default"):
        if component_arg is None:
            component_arg = "default"

        self.__insertions.append((component_type, component_arg, metric_name, timestamp, value))

    def commit_transaction(self):
        connection = self._connection_helper.retrieve_database_connection()

        connection.executemany(
            "INSERT INTO {0} ({1}, {2}, {3}, {4}, {5}) VALUES (?, ? ,? ,?, ?)".format(
                MeasurementsTableManagement.TABLE_NAME(),
                MeasurementsTableManagement.KEY_COMPONENT_TYPE_FK(),
                MeasurementsTableManagement.KEY_COMPONENT_ARG_FK(),
                MeasurementsTableManagement.KEY_METRIC_FK(),
                MeasurementsTableManagement.KEY_TIMESTAMP(),
                MeasurementsTableManagement.KEY_VALUE()
            ),
            self.__insertions
        )

        connection.commit()

        self.__reset_variables()

    def rollback(self):
        self.__reset_variables()
