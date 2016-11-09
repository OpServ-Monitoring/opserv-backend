from .component_types_table_management import ComponentTypesTableManagement
from .general_table_management import GeneralTableManagement
from .metrics_table_management import MetricsTableManagement


class ComponentTypeMetricsTableManagement(GeneralTableManagement):
    __KEY_COMPONENT_TYPE_FK = "component_type_fk"
    __KEY_METRIC_FK = "metric_fk"

    @classmethod
    def TABLE_NAME(cls) -> str:
        return "component_type_metrics_table"

    @classmethod
    def KEY_COMPONENT_TYPE_FK(cls):
        return ComponentTypeMetricsTableManagement.__KEY_COMPONENT_TYPE_FK

    @classmethod
    def KEY_METRIC_FK(cls):
        return ComponentTypeMetricsTableManagement.__KEY_METRIC_FK

    @classmethod
    def _get_columns(cls) -> list:
        return [
            (ComponentTypeMetricsTableManagement.KEY_COMPONENT_TYPE_FK(), GeneralTableManagement._type_text_not_null),
            (ComponentTypeMetricsTableManagement.KEY_METRIC_FK(), GeneralTableManagement._type_text_not_null)
        ]

    @classmethod
    def _get_primary_key(cls) -> list:
        return [
            ComponentTypeMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
            ComponentTypeMetricsTableManagement.KEY_METRIC_FK()
        ]

    @classmethod
    def _get_foreign_keys(cls) -> list:
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
