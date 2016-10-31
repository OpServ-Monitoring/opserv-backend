import sqlite3

from .tables.component_metrics_table_management import ComponentMetricsTableManagement
from .tables.component_type_metrics_table_management import ComponentTypeMetricsTableManagement
from .tables.component_types_table_management import ComponentTypesTableManagement
from .tables.measurements_table_management import MeasurementsTableManagement
from .tables.metrics_table_management import MetricsTableManagement
from .tables.user_preferences_table_management import UserPreferencesTableManagement
from .unified_database_interface import UnifiedDatabaseInterface


class DatabaseOpenHelper:
    @staticmethod
    def on_create():
        DatabaseOpenHelper.__perform_settings()
        DatabaseOpenHelper.__create_tables()
        DatabaseOpenHelper.__create_triggers()
        DatabaseOpenHelper.__insert_supported_component_metrics()
        DatabaseOpenHelper.__set_gathering_rates()

    @staticmethod  # Only used for testing
    def mock_on_create():
        DatabaseOpenHelper.__perform_settings()
        DatabaseOpenHelper.__create_tables()
        DatabaseOpenHelper.__create_triggers()
        DatabaseOpenHelper.__insert_supported_component_metrics()

    @staticmethod
    def __perform_settings():
        connection = DatabaseOpenHelper.establish_database_connection()

        connection.execute("PRAGMA JOURNAL_MODE=WAL")
        connection.execute("PRAGMA FOREIGN_KEYS=ON")

        connection.commit()
        connection.close()

    @staticmethod
    def __create_tables():
        connection = DatabaseOpenHelper.establish_database_connection()

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

        connection.commit()
        connection.close()

    @staticmethod
    def __create_triggers():
        connection = DatabaseOpenHelper.establish_database_connection()

        connection.execute(
            "CREATE TRIGGER IF NOT EXISTS add_component BEFORE INSERT ON {0} "
            "BEGIN "
            "INSERT OR IGNORE INTO {1} ({2}, {3}, {4}) VALUES (new.{5}, new.{6}, new.{7}); "
            "END;".format(
                MeasurementsTableManagement.TABLE_NAME(),
                ComponentMetricsTableManagement.TABLE_NAME(),
                ComponentMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
                ComponentMetricsTableManagement.KEY_COMPONENT_ARG(),
                ComponentMetricsTableManagement.KEY_COMPONENT_METRIC_FK(),
                MeasurementsTableManagement.KEY_COMPONENT_TYPE_FK(),
                MeasurementsTableManagement.KEY_COMPONENT_ARG_FK(),
                MeasurementsTableManagement.KEY_METRIC_FK()
            )
        )

        connection.commit()
        connection.close()

    @staticmethod
    def __insert_supported_component_metrics():
        connection = DatabaseOpenHelper.establish_database_connection()

        component_types = []
        metrics = set()
        component_type_metrics = []

        from misc import constants
        for component_type in constants.implemented_hardware:
            component_types.append((component_type,))

            for metric in constants.implemented_hardware[component_type]:
                metrics.add((metric,))
                component_type_metrics.append((component_type, metric))

        connection.executemany(
            "INSERT OR IGNORE INTO {0} ({1}) VALUES (?)".format(
                ComponentTypesTableManagement.TABLE_NAME(),
                ComponentTypesTableManagement.KEY_NAME()
            ),
            component_types
        )

        connection.executemany(
            "INSERT OR IGNORE INTO {0} ({1}) VALUES (?)".format(
                MetricsTableManagement.TABLE_NAME(),
                MetricsTableManagement.KEY_NAME()
            ),
            metrics
        )

        connection.executemany(
            "INSERT OR IGNORE INTO {0} ({1}, {2}) VALUES (?,?)".format(
                ComponentTypeMetricsTableManagement.TABLE_NAME(),
                ComponentTypeMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
                ComponentTypeMetricsTableManagement.KEY_METRIC_FK()
            ),
            component_type_metrics
        )

        connection.commit()
        connection.close()

    @staticmethod
    def __set_gathering_rates():
        from misc import queue_manager
        component_metrics_writer_reader = UnifiedDatabaseInterface.get_component_metrics_writer_reader()

        if not component_metrics_writer_reader.are_gathering_rates_set():
            DatabaseOpenHelper.__insert_default_gathering_rates()

        gathering_rates = component_metrics_writer_reader.get_gathering_rates()

        for gathering_rate in gathering_rates:
            queue_manager.set_gathering_rate(
                gathering_rate[0],
                gathering_rate[2],
                gathering_rate[3],
                gathering_rate[1]
            )

    @staticmethod
    def __insert_default_gathering_rates():
        from misc import constants
        default_rates = constants.default_gathering_rates

        insert_values = []
        for component_type in default_rates:
            for component_arg in default_rates[component_type]:
                for metric_rate_tuple in default_rates[component_type][component_arg]:
                    # Add the metric rate tuple to the comptype and compargs
                    # The line below just concatenates the tuples
                    # The * operator may not be used inside of tuples with Python < 3.5
                    insert_values.append((component_type, component_arg) + metric_rate_tuple)
        UnifiedDatabaseInterface.get_component_metrics_writer_reader().insert_component_metrics(insert_values)

    @staticmethod
    def establish_database_connection():
        # TODO Decide whether this should be configurable or not
        location = 'opserv.db'

        return sqlite3.connect(location)
