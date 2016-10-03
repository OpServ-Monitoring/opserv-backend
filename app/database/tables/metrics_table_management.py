from .general_table_management import GeneralTableManagement


class MetricsTableManagement(GeneralTableManagement):
    __KEY_NAME = "metric_name"

    @classmethod
    def TABLE_NAME(cls) -> str:
        return "metrics_table"

    @staticmethod
    def KEY_NAME():
        return MetricsTableManagement.__KEY_NAME

    @staticmethod
    def _get_columns() -> list:
        return [
            (MetricsTableManagement.KEY_NAME(), GeneralTableManagement._type_text_not_null)
        ]

    @staticmethod
    def _get_primary_key() -> list:
        return [
            MetricsTableManagement.KEY_NAME()
        ]

    @staticmethod
    def _get_foreign_keys() -> list:
        return []
