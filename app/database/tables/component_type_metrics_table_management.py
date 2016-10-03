from app.database.tables.component_types_table_management import ComponentTypesTableManagement
from app.database.tables.general_table_management import GeneralTableManagement
from app.database.tables.metrics_table_management import MetricsTableManagement


class ComponentTypeMetricsTableManagement(GeneralTableManagement):
    __KEY_COMPONENT_TYPE_FK = "component_type_fk"
    __KEY_METRIC_FK = "metric_fk"

    @classmethod
    def TABLE_NAME(cls) -> str:
        return "component_type_metrics_table"

    @staticmethod
    def KEY_COMPONENT_TYPE_FK():
        return ComponentTypeMetricsTableManagement.__KEY_COMPONENT_TYPE_FK

    @staticmethod
    def KEY_METRIC_FK():
        return ComponentTypeMetricsTableManagement.__KEY_METRIC_FK

    @staticmethod
    def _get_columns() -> list:
        return [
            (ComponentTypeMetricsTableManagement.KEY_COMPONENT_TYPE_FK(), GeneralTableManagement._type_text_not_null),
            (ComponentTypeMetricsTableManagement.KEY_METRIC_FK(), GeneralTableManagement._type_text_not_null)
        ]

    @staticmethod
    def _get_primary_key() -> list:
        return [
            ComponentTypeMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
            ComponentTypeMetricsTableManagement.KEY_METRIC_FK()
        ]

    @staticmethod
    def _get_foreign_keys() -> list:
        return [
            GeneralTableManagement._build_foreign_key(
                [ComponentTypeMetricsTableManagement.KEY_COMPONENT_TYPE_FK()],
                ComponentTypesTableManagement.TABLE_NAME(),
                [ComponentTypesTableManagement.KEY_NAME()]
            ),
            GeneralTableManagement._build_foreign_key(
                [ComponentTypeMetricsTableManagement.KEY_METRIC_FK()],
                MetricsTableManagement.TABLE_NAME(),
                [MetricsTableManagement.KEY_NAME()]
            )
        ]
