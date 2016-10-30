from .component_metrics_table_management import ComponentMetricsTableManagement
from .general_table_management import GeneralTableManagement


class MeasurementsTableManagement(GeneralTableManagement):
    __KEY_COMPONENT_ARG_FK = "measurement_component_arg_fk"
    __KEY_COMPONENT_TYPE_FK = "measurement_component_type_fk"
    __KEY_METRIC_FK = "measurement_metric_fk"
    __KEY_TIMESTAMP = "measurement_timestamp"
    __KEY_VALUE = "measurement_value"

    @classmethod
    def TABLE_NAME(cls) -> str:
        return "measurements_table"

    @staticmethod
    def KEY_COMPONENT_ARG_FK():
        return MeasurementsTableManagement.__KEY_COMPONENT_ARG_FK

    @staticmethod
    def KEY_COMPONENT_TYPE_FK():
        return MeasurementsTableManagement.__KEY_COMPONENT_TYPE_FK

    @staticmethod
    def KEY_METRIC_FK():
        return MeasurementsTableManagement.__KEY_METRIC_FK

    @staticmethod
    def KEY_TIMESTAMP():
        return MeasurementsTableManagement.__KEY_TIMESTAMP

    @staticmethod
    def KEY_VALUE():
        return MeasurementsTableManagement.__KEY_VALUE

    @staticmethod
    def _get_columns() -> list:
        return [
            (MeasurementsTableManagement.KEY_COMPONENT_ARG_FK(), GeneralTableManagement._type_text_not_null),
            (MeasurementsTableManagement.KEY_COMPONENT_TYPE_FK(), GeneralTableManagement._type_text_not_null),
            (MeasurementsTableManagement.KEY_METRIC_FK(), GeneralTableManagement._type_text_not_null),
            (MeasurementsTableManagement.KEY_TIMESTAMP(), "INTEGER NOT NULL"),
            (MeasurementsTableManagement.KEY_VALUE(), GeneralTableManagement._type_text_not_null)
        ]

    @staticmethod
    def _get_primary_key() -> list:
        return [
            MeasurementsTableManagement.KEY_COMPONENT_TYPE_FK(),
            MeasurementsTableManagement.KEY_COMPONENT_ARG_FK(),
            MeasurementsTableManagement.KEY_METRIC_FK(),
            MeasurementsTableManagement.KEY_TIMESTAMP()
        ]

    @staticmethod
    def _get_foreign_keys() -> list:
        return [
            GeneralTableManagement._build_foreign_key(
                [
                    MeasurementsTableManagement.KEY_COMPONENT_TYPE_FK(),
                    MeasurementsTableManagement.KEY_COMPONENT_ARG_FK(),
                    MeasurementsTableManagement.KEY_METRIC_FK()
                ],
                ComponentMetricsTableManagement.TABLE_NAME(),
                [
                    ComponentMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
                    ComponentMetricsTableManagement.KEY_COMPONENT_ARG(),
                    ComponentMetricsTableManagement.KEY_COMPONENT_METRIC_FK()
                ]
            )
        ]
