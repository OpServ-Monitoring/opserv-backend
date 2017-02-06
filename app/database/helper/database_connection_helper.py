import logging
import sqlite3

log = logging.getLogger("opserv." + __name__)


class DatabaseConnectionHelper:
    _location = 'opserv.db'

    @classmethod
    def retrieve_database_connection(cls):
        try:
            connection = sqlite3.connect(cls._location)
        except sqlite3.Error as err:
            log.error("Could not connect to the database.")
            raise err

        connection.execute("PRAGMA JOURNAL_MODE=WAL")
        connection.commit()
        connection.execute("PRAGMA FOREIGN_KEYS=ON")
        connection.commit()

        log.debug("Database connection established.")

        return connection
