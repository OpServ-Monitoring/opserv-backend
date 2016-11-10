from sqlite3 import OperationalError
from unittest import TestCase
from unittest.mock import MagicMock

from database.connectors.database_opener import DatabaseOpener
from database.helper.database_connection_helper import DatabaseConnectionHelper


class TestDatabaseOpener(TestCase):
    def test_create_database(self):
        class DatabaseOpenerMock(DatabaseOpener):
            create_tables = MagicMock()
            create_triggers = MagicMock()
            insert_supported_component_metrics = MagicMock()

        DatabaseOpenerMock.create_database()

        DatabaseOpenerMock.create_tables.assert_called_once_with()
        DatabaseOpenerMock.create_triggers.assert_called_once_with()
        DatabaseOpenerMock.insert_supported_component_metrics.assert_called_once_with()

    def test_create_tables(self):
        database_opener = self.__build_modified_database_opener(
            "database_opener.raw.sqlite"
        )

        try:
            database_opener.create_tables()
        except OperationalError:
            self.fail("create_tables() raised OperationalError unexpectedly!")

        # TODO Check if all tables exists

    def test_create_triggers(self):
        database_opener = self.__build_modified_database_opener(
            "database_opener.after.create_tables.sqlite"
        )

        try:
            database_opener.create_triggers()
        except OperationalError:
            self.fail("create_triggers() raised OperationalError unexpectedly!")

        # TODO Check if trigger exists

    def test_insert_supported_component_metrics(self):
        database_opener = self.__build_modified_database_opener(
            "database_opener.after.create_tables.create_triggers.sqlite"
        )

        try:
            database_opener.insert_supported_component_metrics()
        except OperationalError:
            self.fail("insert_supported_component_metrics() raised OperationalError unexpectedly!")

        # TODO Check if metrics are set

    @classmethod
    def __build_modified_database_opener(cls, location):
        location = "test/database/connectors/" + location

        class ModifiedConnectionHelper(DatabaseConnectionHelper):
            _location = location

        class ModifiedDatabaseOpener(DatabaseOpener):
            _connection_helper = ModifiedConnectionHelper

        return ModifiedDatabaseOpener()
