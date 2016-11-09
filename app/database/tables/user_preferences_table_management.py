from database.tables.general_table_management import GeneralTableManagement


class UserPreferencesTableManagement(GeneralTableManagement):
    __KEY_KEY = "user_preference_key"
    __KEY_VALUE = "user_preference_value"

    @classmethod
    def TABLE_NAME(cls) -> str:
        return "user_preferences_table"

    @classmethod
    def KEY_KEY(cls):
        return UserPreferencesTableManagement.__KEY_KEY

    @classmethod
    def KEY_VALUE(cls):
        return UserPreferencesTableManagement.__KEY_VALUE

    @classmethod
    def _get_columns(cls) -> list:
        return [
            (UserPreferencesTableManagement.KEY_KEY(), GeneralTableManagement._type_text_not_null),
            (UserPreferencesTableManagement.KEY_VALUE(), "TEXT")
        ]

    @classmethod
    def _get_foreign_keys(cls) -> list:
        return []

    @classmethod
    def _get_primary_key(cls) -> list:
        return [
            UserPreferencesTableManagement.KEY_KEY()
        ]
