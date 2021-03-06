import logging
import os

from application_settings.app_settings import AppSettings
from database.helper.base_database_connector import DatabaseConnector
from database.tables.component_metrics_table_management import ComponentMetricsTableManagement
from database.tables.component_type_metrics_table_management import ComponentTypeMetricsTableManagement
from database.tables.component_types_table_management import ComponentTypesTableManagement
from database.tables.measurements_table_management import MeasurementsTableManagement
from database.tables.metrics_table_management import MetricsTableManagement
from database.tables.user_preferences_table_management import UserPreferencesTableManagement
from database.tables.users_table_management import UsersTableManagement
from database.unified_database_interface import UnifiedDatabaseInterface

log = logging.getLogger("opserv." + __name__)


class DatabaseInitializer(DatabaseConnector):
    @classmethod
    def create_database(cls):
        cls.create_tables()
        cls.create_triggers()
        cls.insert_supported_component_metrics()

    @classmethod
    def create_tables(cls):
        connection = cls._connection_helper.retrieve_database_connection()

        table_managements = [
            # measurements
            ComponentTypesTableManagement,
            MetricsTableManagement,
            ComponentTypeMetricsTableManagement,
            ComponentMetricsTableManagement,
            MeasurementsTableManagement,

            # user preferences
            UserPreferencesTableManagement,

            # user management
            UsersTableManagement
        ]

        for table_management in table_managements:
            connection.execute(table_management.CREATE_TABLE_STATEMENT())

        connection.commit()
        connection.close()

    @classmethod
    def create_triggers(cls):
        connection = cls._connection_helper.retrieve_database_connection()

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

    @classmethod
    def insert_supported_component_metrics(cls):
        connection = cls._connection_helper.retrieve_database_connection()

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

    # TODO Remove this from here
    @classmethod
    def set_gathering_rates(cls):
        from misc import queue_manager
        component_metrics_writer_reader = UnifiedDatabaseInterface.get_component_metrics_writer_reader()

        if not component_metrics_writer_reader.are_gathering_rates_set():
            cls.__insert_default_gathering_rates()

        gathering_rates = component_metrics_writer_reader.get_gathering_rates()

        for gathering_rate in gathering_rates:
            arg = gathering_rate[1]

            from misc import constants
            if gathering_rate[0] in constants.HARDWARE_DEFAULTS:
                if not constants.HARDWARE_DEFAULTS[gathering_rate[0]][0]:
                    arg = None

                queue_manager.set_gathering_rate(
                    gathering_rate[0],
                    gathering_rate[2],
                    gathering_rate[3],
                    arg
                )
            else:
                log.error(
                    "Tried to set gathering rate in the queue_manager for the component_type %s which is undefined.",
                    gathering_rate[0]
                )

    # TODO Remove this from here
    @classmethod
    def __insert_default_gathering_rates(cls):
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

    @classmethod
    def configure_admin_user(cls):
        users_writer_reader = UnifiedDatabaseInterface.get_users_writer_reader()

        admin_user_name = "opserv_admin"
        admin_user_password = AppSettings.get_setting(AppSettings.KEY_PASSWORD)

        if not users_writer_reader.does_user_exist(admin_user_name):
            if admin_user_password is None:
                admin_user_password = cls.__generate_random_password(21)
                log.warning("No admin account was found in the data base. A new user \"{0}\" with the password \"{1}\" "
                            "will be created.".format(admin_user_name, admin_user_password))

            users_writer_reader.add_user(admin_user_name, admin_user_password)
        elif admin_user_password is not None:
            users_writer_reader.change_user_password(admin_user_name, admin_user_password)

    @classmethod
    def __generate_random_password(cls, length: int):
        available_chars = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
            'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '#', '.'
        ]
        password = ""

        while len(password) < length:
            # get a cryptographically random number between 0 and 63
            random_number = os.urandom(1)[0] % 64

            password += available_chars[random_number]
        return password
