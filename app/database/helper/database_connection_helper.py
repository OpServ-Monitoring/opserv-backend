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

        # Fix for a bug occurring in Python 3.6 on OSX, see issue #19 on Github
        old_isolation_level = connection.isolation_level  # Save the default isolation level
        connection.isolation_level = None  # Set the isolation level to None, to avoid "within transaction" bug

        connection.execute("PRAGMA JOURNAL_MODE=WAL")
        connection.commit()
        connection.execute("PRAGMA FOREIGN_KEYS=ON")
        connection.commit()

        connection.isolation_level = old_isolation_level  # Reset to the original isolation level

        log.debug("Database connection established.")

        return connection
