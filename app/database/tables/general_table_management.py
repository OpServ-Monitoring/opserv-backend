from abc import ABCMeta, abstractmethod

from database.helper.sql_statement_builder import SqlStatementBuilder


class GeneralTableManagement(metaclass=ABCMeta):
    _type_text_not_null = "TEXT NOT NULL"

    @classmethod
    def CREATE_TABLE_STATEMENT(cls):
        return SqlStatementBuilder.build_create_table_statement(
            cls.TABLE_NAME(),
            cls._get_columns(),
            cls._get_foreign_keys(),
            cls._get_primary_key()
        )

    @classmethod
    @abstractmethod
    def TABLE_NAME(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def _get_columns(cls) -> list:
        pass

    @classmethod
    @abstractmethod
    def _get_foreign_keys(cls) -> list:
        pass

    @classmethod
    @abstractmethod
    def _get_primary_key(cls) -> list:
        pass

    @classmethod
    def _build_foreign_key(cls, keys_on_table: list, ref_table_name: str, keys_on_ref_table: list) -> tuple:
        return keys_on_table, ref_table_name, keys_on_ref_table
