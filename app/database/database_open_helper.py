import sqlite3

from .tables.component_metrics_table_management import ComponentMetricsTableManagement
from .tables.component_type_metrics_table_management import ComponentTypeMetricsTableManagement
from .tables.component_types_table_management import ComponentTypesTableManagement
from .tables.measurements_table_management import MeasurementsTableManagement
from .tables.metrics_table_management import MetricsTableManagement
from .tables.user_preferences_table_management import UserPreferencesTableManagement

# TODO Decide whether the location should be configurable
location = 'opserv.db'


class DatabaseOpenHelper:
    @staticmethod
    def on_create():
        connection = sqlite3.connect(location)

        DatabaseOpenHelper.__perform_settings(connection)
        DatabaseOpenHelper.__create_tables(connection)
        DatabaseOpenHelper.__create_triggers(connection)
        DatabaseOpenHelper.__insert_supported_component_metrics(connection)
        DatabaseOpenHelper.__set_gathering_rates(connection)

        connection.commit()

    @staticmethod
    def __perform_settings(connection: sqlite3.Connection):
        connection.execute("PRAGMA JOURNAL_MODE=WAL")
        connection.execute("PRAGMA FOREIGN_KEYS=ON")

    @staticmethod
    def __create_tables(connection: sqlite3.Connection):
        table_managements = [
            # measurements
            ComponentTypesTableManagement,
            MetricsTableManagement,
            ComponentTypeMetricsTableManagement,
            ComponentMetricsTableManagement,
            MeasurementsTableManagement,

            # user preferences
            UserPreferencesTableManagement
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
        component_types = []
        metrics = set()
        component_type_metrics = []

        from misc import constants
        for component_type in constants.implemented_hardware:
            component_types.append((component_type,))

            for metric in constants.implemented_hardware[component_type]:
                metrics.add((metric,))
                component_type_metrics.append((component_type, metric))

        connection.executemany("INSERT OR IGNORE INTO component_types_table (component_type_name) VALUES (?)",
                               component_types)

        connection.executemany("INSERT OR IGNORE INTO metrics_table (metric_name) VALUES (?)", metrics)

        connection.executemany("INSERT OR IGNORE INTO component_type_metrics_table(component_type_fk, metric_fk) "
                               "VALUES (?,?)", component_type_metrics)

    @staticmethod
    def __set_gathering_rates(connection):
        if connection.execute("SELECT COUNT(*) FROM component_metrics_table WHERE component_gathering_rate IS NOT NULL") \
                .fetchone()[0] == 0:
            # TODO Extract this into a separate method
            from misc import constants
            default_rates = constants.default_gathering_rates

            insert_values = []
            for component_type in default_rates:
                for component_arg in default_rates[component_type]:
                    for metric_rate_tuple in default_rates[component_type][component_arg]:
                        insert_values.append((component_type, component_arg, *metric_rate_tuple))

            # TODO Extract this into a separate method
            connection.executemany("""
                INSERT INTO component_metrics_table
                (component_type_fk, component_arg, component_metric_fk, component_gathering_rate)
                VALUES (?, ? , ?, ?)
            """, insert_values)

        # TODO Extract this into a separate method
        gathering_rates = connection.execute("""
        SELECT * FROM component_metrics_table
        WHERE component_gathering_rate IS NOT NULL
        """).fetchall()

        # TODO Extract this into a separate method
        from misc import queue_manager
        for gathering_rate in gathering_rates:
            queue_manager.setGatheringRate(
                gathering_rate[0],
                gathering_rate[2],
                gathering_rate[3],
                gathering_rate[1]
            )
