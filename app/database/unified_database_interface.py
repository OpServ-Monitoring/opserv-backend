class UnifiedDatabaseInterface:
    @staticmethod
    def get_measurement_insertion_transaction():
        from ._measurement_insert_transaction import MeasurementInsertTransaction

        return MeasurementInsertTransaction()

    @staticmethod
    def get_measurement_data_reader():
        from ._measurement_data_reader import MeasurementDataReader

        return MeasurementDataReader()

    @staticmethod
    def get_user_preferences_writer_reader():
        from ._user_preferences_writer_reader import UserPreferencesWriterReader

        return UserPreferencesWriterReader()

    @staticmethod
    def get_component_metrics_writer_reader():
        from ._component_metrics_writer_reader import ComponentMetricsWriterReader

        return ComponentMetricsWriterReader()

    # TODO Add method for open helper
