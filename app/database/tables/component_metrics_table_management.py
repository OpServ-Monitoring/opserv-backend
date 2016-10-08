from .component_type_metrics_table_management import ComponentTypeMetricsTableManagement
from .general_table_management import GeneralTableManagement


class ComponentMetricsTableManagement(GeneralTableManagement):
    @classmethod
    def TABLE_NAME(cls) -> str:
        return "component_metrics_table"

    __KEY_COMPONENT_TYPE_FK = "component_type_fk"
    __KEY_COMPONENT_ARG = "component_arg"
    __KEY_COMPONENT_METRIC_FK = "component_metric_fk"
    __KEY_COMPONENT_GATHERING_RATE = "component_gathering_rate"

    @staticmethod
    def KEY_COMPONENT_TYPE_FK():
        return ComponentMetricsTableManagement.__KEY_COMPONENT_TYPE_FK

    @staticmethod
    def KEY_COMPONENT_ARG():
        return ComponentMetricsTableManagement.__KEY_COMPONENT_ARG

    @staticmethod
    def KEY_COMPONENT_METRIC_FK():
        return ComponentMetricsTableManagement.__KEY_COMPONENT_METRIC_FK

    @staticmethod
    def KEY_COMPONENT_GATHERING_RATE():
        return ComponentMetricsTableManagement.__KEY_COMPONENT_GATHERING_RATE

    @staticmethod
    def _get_columns() -> list:
        # TODO improve statements!!
        greater_or_equal_500_statement = ComponentMetricsTableManagement.KEY_COMPONENT_GATHERING_RATE() + " >= 500"
        is_integer_statement = "typeof(" + ComponentMetricsTableManagement.KEY_COMPONENT_GATHERING_RATE() + ") = 'integer'"
        check_statement = "CHECK(" + ComponentMetricsTableManagement.KEY_COMPONENT_GATHERING_RATE() + " IS NULL or " + is_integer_statement + " and " + greater_or_equal_500_statement + ")"

        return [
            (ComponentMetricsTableManagement.KEY_COMPONENT_TYPE_FK(), GeneralTableManagement._type_text_not_null),
            (ComponentMetricsTableManagement.KEY_COMPONENT_ARG(), GeneralTableManagement._type_text_not_null),
            (ComponentMetricsTableManagement.KEY_COMPONENT_METRIC_FK(), GeneralTableManagement._type_text_not_null),
            (ComponentMetricsTableManagement.KEY_COMPONENT_GATHERING_RATE(), "INTEGER " + check_statement)
        ]

    @staticmethod
    def _get_primary_key() -> list:
        return [
            ComponentMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
            ComponentMetricsTableManagement.KEY_COMPONENT_ARG(),
            ComponentMetricsTableManagement.KEY_COMPONENT_METRIC_FK()
        ]

    @staticmethod
    def _get_foreign_keys() -> list:
        return [
            GeneralTableManagement._build_foreign_key(
                [
                    ComponentMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
                    ComponentMetricsTableManagement.KEY_COMPONENT_METRIC_FK()
                ],
                ComponentTypeMetricsTableManagement.TABLE_NAME(),
                [
                    ComponentTypeMetricsTableManagement.KEY_COMPONENT_TYPE_FK(),
                    ComponentTypeMetricsTableManagement.KEY_METRIC_FK()
                ]
            )
        ]
