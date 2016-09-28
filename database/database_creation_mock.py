import sqlite3

location = 'opserv.db'


class TableManagementCpusUsage:
    __TABLE_NAME = "cpu_usage_table"

    __KEY_ID = "cpu_usage_entry__id"
    __KEY_FK_CPU_ID = "cpu_usage_entry__fk_cpu_id"
    __KEY_TIMESTAMP = "cpu_usage_entry__timestamp"
    __KEY_VALUE = "cpu_usage_entry__value"

    @staticmethod
    def TABLE_NAME():
        return TableManagementCpusUsage.__TABLE_NAME

    @staticmethod
    def KEY_ID():
        return TableManagementCpusUsage.__KEY_ID

    @staticmethod
    def KEY_FK_CPU_ID():
        return TableManagementCpusUsage.__KEY_FK_CPU_ID

    @staticmethod
    def KEY_TIMESTAMP():
        return TableManagementCpusUsage.__KEY_TIMESTAMP

    @staticmethod
    def KEY_VALUE():
        return TableManagementCpusUsage.__KEY_VALUE


class DatabaseCreation:
    create_table_cpus_usage = "CREATE TABLE IF NOT EXISTS " + TableManagementCpusUsage.TABLE_NAME() + " (" + \
                              TableManagementCpusUsage.KEY_ID() + " INTEGER PRIMARY KEY AUTOINCREMENT, " + \
                              TableManagementCpusUsage.KEY_FK_CPU_ID() + " INTEGER NOT NULL, " + \
                              TableManagementCpusUsage.KEY_TIMESTAMP() + " INTEGER NOT NULL, " + \
                              TableManagementCpusUsage.KEY_VALUE() + " FLOAT NOT NULL" + \
                              ");"


sqlite_connection = sqlite3.connect(location)
cursor = sqlite_connection.cursor()

cursor.execute(DatabaseCreation().create_table_cpus_usage)
