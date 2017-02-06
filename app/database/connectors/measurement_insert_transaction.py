import logging
from sqlite3 import IntegrityError

from database.helper.base_database_connector import DatabaseConnector
from database.tables.measurements_table_management import MeasurementsTableManagement

log = logging.getLogger("database.transaction")
log.setLevel(logging.DEBUG)


class MeasurementInsertTransaction(DatabaseConnector):
    def __init__(self):
        self.__reset_variables()

    def __reset_variables(self):
        self.__insertions = []

    def insert_measurement(self, component_type, component_arg, metric_name, timestamp, value):
        self.__insertions.append((component_type, component_arg, metric_name, timestamp, value))

    def commit_transaction(self):
        connection = self._connection_helper.retrieve_database_connection()

        try:
            connection.executemany(
                """INSERT INTO {0} ({1}, {2}, {3}, {4}, {5}) VALUES (?, IFNULL(?, "default") ,? ,?, ?)
                """.format(
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
            connection.close()

        except IntegrityError as err:
            log.error(" commit of transaction, probably multiple measurements per millisecond")
            log.error(err)
            log.error("Happened with these inserts: %s", str(self.__insertions))

        self.__reset_variables()

    def rollback(self):
        self.__reset_variables()
