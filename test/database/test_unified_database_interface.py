from unittest import TestCase

from database.unified_database_interface import UnifiedDatabaseInterface


class TestUnifiedDatabaseInterface(TestCase):
    def test_get_measurement_insertion_transaction(self):
        from database.connectors.measurement_insert_transaction import MeasurementInsertTransaction

        self.assertIsInstance(
            UnifiedDatabaseInterface().get_measurement_insertion_transaction(),
            MeasurementInsertTransaction
        )

    def test_get_measurement_data_reader(self):
        from database.connectors.measurement_data_reader import MeasurementDataReader

        self.assertIsInstance(
            UnifiedDatabaseInterface().get_measurement_data_reader(),
            MeasurementDataReader
        )

    def test_get_user_preferences_writer_reader(self):
        from database.connectors.user_preferences_writer_reader import UserPreferencesWriterReader

        self.assertIsInstance(
            UnifiedDatabaseInterface().get_user_preferences_writer_reader(),
            UserPreferencesWriterReader
        )

    def test_get_component_metrics_writer_reader(self):
        from database.connectors.component_metrics_writer_reader import ComponentMetricsWriterReader

        self.assertIsInstance(
            UnifiedDatabaseInterface().get_component_metrics_writer_reader(),
            ComponentMetricsWriterReader
        )
