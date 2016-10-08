from database.tables.general_table_management import GeneralTableManagement


class UserPreferencesTableManagement(GeneralTableManagement):
    __KEY_KEY = "user_preference_key"
    __KEY_VALUE = "user_preference_value"

    @classmethod
    def TABLE_NAME(cls) -> str:
        return "user_preferences_table"

    @staticmethod
    def KEY_KEY():
        return UserPreferencesTableManagement.__KEY_KEY

    @staticmethod
    def KEY_VALUE():
        return UserPreferencesTableManagement.__KEY_VALUE

    @staticmethod
    def _get_columns() -> list:
        return [
            (UserPreferencesTableManagement.KEY_KEY(), GeneralTableManagement._type_text_not_null),
            (UserPreferencesTableManagement.KEY_VALUE(), "TEXT")
        ]

    @staticmethod
    def _get_foreign_keys() -> list:
        return []

    @staticmethod
    def _get_primary_key() -> list:
        return [
            UserPreferencesTableManagement.KEY_KEY()
        ]
