class UnifiedDatabaseInterface:
    @classmethod
    def get_measurement_insertion_transaction(cls):
        from .connectors.measurement_insert_transaction import MeasurementInsertTransaction

        return MeasurementInsertTransaction()

    @classmethod
    def get_measurement_data_reader(cls):
        from .connectors.measurement_data_reader import MeasurementDataReader

        return MeasurementDataReader()

    @classmethod
    def get_user_preferences_writer_reader(cls):
        from .connectors.user_preferences_writer_reader import UserPreferencesWriterReader

        return UserPreferencesWriterReader()

    @classmethod
    def get_users_writer_reader(cls):
        from .connectors.users_writer_reader import UsersWriterReader

        return UsersWriterReader()

    @classmethod
    def get_component_metrics_writer_reader(cls):
        from .connectors.component_metrics_writer_reader import ComponentMetricsWriterReader

        return ComponentMetricsWriterReader()

    @classmethod
    def get_database_initializer(cls):
        from .connectors.database_initializer import DatabaseInitializer

        return DatabaseInitializer()
