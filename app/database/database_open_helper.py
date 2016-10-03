import sqlite3

from .tables.component_type_metrics_table_management import ComponentTypeMetricsTableManagement
from .tables.component_metrics_table_management import ComponentMetricsTableManagement
from .tables.component_types_table_management import ComponentTypesTableManagement
from .tables.measurements_table_management import MeasurementsTableManagement
from .tables.metrics_table_management import MetricsTableManagement

# TODO Decide whether the location should be configurable
location = 'opserv.db'


class DatabaseOpenHelper:
    # TODO Remove, this should be delivered by the gathering module
    __supported_component_metrics = {
        'cpu': ['info', 'usage', 'frequency', 'temperature'],
        'core': ['info', 'usage', 'frequency', 'temperature'],
        'gpu': ['info', 'gpuclock', 'memclock', 'vramusage', 'temperature', 'usage']
    }

    @staticmethod
    def on_create():
        connection = sqlite3.connect(location)

        DatabaseOpenHelper.__perform_settings(connection)
        DatabaseOpenHelper.__create_tables(connection)
        DatabaseOpenHelper.__create_triggers(connection)
        DatabaseOpenHelper.__insert_supported_component_metrics(connection)

        connection.commit()

    @staticmethod
    def __perform_settings(connection: sqlite3.Connection):
        connection.execute("PRAGMA JOURNAL_MODE=WAL")
        connection.execute("PRAGMA FOREIGN_KEYS=ON")

    @staticmethod
    def __create_tables(connection: sqlite3.Connection):
        table_managements = [
            ComponentTypesTableManagement,
            MetricsTableManagement,
            ComponentTypeMetricsTableManagement,
            ComponentMetricsTableManagement,
            MeasurementsTableManagement
        ]

        for table_management in table_managements:
            connection.execute(table_management.CREATE_TABLE_STATEMENT())

    @staticmethod
    def __create_triggers(connection: sqlite3.Connection):
        connection.execute("CREATE TRIGGER IF NOT EXISTS add_component BEFORE INSERT ON measurements_table "
                           "BEGIN "
                           "INSERT OR IGNORE INTO component_metrics_table "
                           "(component_type_fk, "
                           "component_arg, "
                           "component_metric_fk) "
                           "VALUES "
                           "(new.measurement_component_type_fk, "
                           "new.measurement_component_arg_fk, "
                           "new.measurement_metric_fk); "
                           "END;")

    @staticmethod
    def __insert_supported_component_metrics(connection: sqlite3.Connection):
        # TODO Exchange local list with gathering interface - method body could need a change aswell
        for component_type in DatabaseOpenHelper.__supported_component_metrics:
            connection.execute("INSERT OR IGNORE INTO component_types_table (component_type_name) VALUES (?)",
                               (component_type,))

            for metric in DatabaseOpenHelper.__supported_component_metrics[component_type]:
                connection.execute("INSERT OR IGNORE INTO metrics_table (metric_name) VALUES (?)", (metric,))
                connection.execute("INSERT OR IGNORE INTO component_type_metrics_table(component_type_fk, metric_fk) "
                                   "VALUES (?,?)", (component_type, metric))
