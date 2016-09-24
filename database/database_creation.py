import sqlite3

location = 'opserv.db'

create_table_cpus_usage = "CREATE TABLE IF NOT EXISTS "

sqlite_connection = sqlite3.connect(location)
cursor = sqlite_connection.cursor()


class TableManagementCpusUsage:
    __TABLE_NAME = "cpu_usage_table"

    __KEY_ID = "cpu_usage_entry__id"
    __KEY_FK_CPU_ID = "cpu_usage_entry__fk_cpu_id"
    __KEY_TIMESTAMP = "cpu_usage_entry__timestamp"
    __KEY_VALUE = "cpu_usage_entry__value"

    @staticmethod
    def get_table_name():
        return TableManagementCpusUsage.__TABLE_NAME

    @staticmethod
    def get_key_id():
        return TableManagementCpusUsage.__KEY_ID

    @staticmethod
    def get_key_fk_cpu_id():
        return TableManagementCpusUsage.__KEY_FK_CPU_ID

    @staticmethod
    def get_key_timestamp():
        return TableManagementCpusUsage.__KEY_TIMESTAMP

    @staticmethod
    def get_key_value():
        return TableManagementCpusUsage.__KEY_VALUE
