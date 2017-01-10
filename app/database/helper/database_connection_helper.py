import sqlite3


class DatabaseConnectionHelper:
    _location = 'opserv.db'

    @classmethod
    def retrieve_database_connection(cls):
        connection = sqlite3.connect(cls._location)

        connection.execute("PRAGMA JOURNAL_MODE=WAL")
        connection.execute("PRAGMA FOREIGN_KEYS=ON")
        connection.commit()

        return connection
