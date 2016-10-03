from app.database.tables.general_table_management import GeneralTableManagement


class ComponentTypesTableManagement(GeneralTableManagement):
    __KEY_NAME = "component_type_name"

    @classmethod
    def TABLE_NAME(cls) -> str:
        return "component_types_table"

    @staticmethod
    def KEY_NAME():
        return ComponentTypesTableManagement.__KEY_NAME

    @staticmethod
    def _get_columns() -> list:
        return [
            (ComponentTypesTableManagement.KEY_NAME(), GeneralTableManagement._type_text_not_null)
        ]

    @staticmethod
    def _get_primary_key() -> list:
        return [
            ComponentTypesTableManagement.KEY_NAME()
        ]

    @staticmethod
    def _get_foreign_keys() -> list:
        return []
