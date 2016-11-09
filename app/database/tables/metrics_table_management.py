from .general_table_management import GeneralTableManagement


class MetricsTableManagement(GeneralTableManagement):
    __KEY_NAME = "metric_name"

    @classmethod
    def TABLE_NAME(cls) -> str:
        return "metrics_table"

    @classmethod
    def KEY_NAME(cls):
        return MetricsTableManagement.__KEY_NAME

    @classmethod
    def _get_columns(cls) -> list:
        return [
            (MetricsTableManagement.KEY_NAME(), GeneralTableManagement._type_text_not_null)
        ]

    @classmethod
    def _get_primary_key(cls) -> list:
        return [
            MetricsTableManagement.KEY_NAME()
        ]

    @classmethod
    def _get_foreign_keys(cls) -> list:
        return []
