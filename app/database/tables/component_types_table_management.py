from .general_table_management import GeneralTableManagement


class ComponentTypesTableManagement(GeneralTableManagement):
    __KEY_NAME = "component_type_name"

    @classmethod
    def TABLE_NAME(cls) -> str:
        return "component_types_table"

    @classmethod
    def KEY_NAME(cls):
        return ComponentTypesTableManagement.__KEY_NAME

    @classmethod
    def _get_columns(cls) -> list:
        return [
            (ComponentTypesTableManagement.KEY_NAME(), GeneralTableManagement._type_text_not_null)
        ]

    @classmethod
    def _get_primary_key(cls) -> list:
        return [
            ComponentTypesTableManagement.KEY_NAME()
        ]

    @classmethod
    def _get_foreign_keys(cls) -> list:
        return []
