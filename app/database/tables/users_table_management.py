from database.tables.general_table_management import GeneralTableManagement


class UsersTableManagement(GeneralTableManagement):
    __KEY_ID = "user_id"
    __KEY_NAME = "user_name"
    __KEY_PASSWORD = "user_password"

    @classmethod
    def TABLE_NAME(cls) -> str:
        return "users_table"

    @classmethod
    def KEY_ID(cls):
        return UsersTableManagement.__KEY_ID

    @classmethod
    def KEY_NAME(cls):
        return UsersTableManagement.__KEY_NAME

    @classmethod
    def KEY_PASSWORD(cls):
        return UsersTableManagement.__KEY_PASSWORD

    @classmethod
    def _get_columns(cls) -> list:
        return [
            (UsersTableManagement.KEY_ID(), "INTEGER AUTO_INCREMENT"),
            (UsersTableManagement.KEY_NAME(), "TEXT UNIQUE NOT NULL"),
            (UsersTableManagement.KEY_PASSWORD(), GeneralTableManagement._type_text_not_null)
        ]

    @classmethod
    def _get_foreign_keys(cls) -> list:
        return []

    @classmethod
    def _get_primary_key(cls) -> list:
        return [
            UsersTableManagement.KEY_ID()
        ]
