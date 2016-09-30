class SqlStatementBuilder:
    @classmethod
    def __parse_columns(cls, columns):
        assert len(columns) > 0

        columns_statement = cls.__parse_column(columns[0])

        for raw_column in columns[1:]:
            columns_statement += ", "
            columns_statement += cls.__parse_column(raw_column)

        return columns_statement

    @classmethod
    def __parse_column(cls, column):
        return column[0] + " " + column[1]

    @classmethod
    def __parse_foreign_keys(cls, foreign_keys):
        foreign_keys_statement = None

        if len(foreign_keys) > 0:
            foreign_keys_statement = cls.__parse_foreign_key(foreign_keys[0])

            for raw_foreign_key in foreign_keys[1:]:
                foreign_keys_statement += ", "
                foreign_keys_statement += cls.__parse_foreign_key(raw_foreign_key)

        return foreign_keys_statement

    @classmethod
    def __parse_foreign_key(cls, foreign_key):
        assert len(foreign_key[0]) > 0
        assert len(foreign_key[0]) == len(foreign_key[2])

        foreign_key_statement = "FOREIGN KEY ("

        foreign_key_statement += foreign_key[0][0]
        for table_key in foreign_key[0][1:]:
            foreign_key_statement += ", "
            foreign_key_statement += table_key

        foreign_key_statement += ") REFERENCES "
        foreign_key_statement += foreign_key[1]
        foreign_key_statement += " ("

        foreign_key_statement += foreign_key[2][0]
        for ref_key in foreign_key[2][1:]:
            foreign_key_statement += ", "
            foreign_key_statement += ref_key

        foreign_key_statement += ")"

        return foreign_key_statement

    @classmethod
    def __parse_primary_key(cls, primary_key):
        primary_key_statement = None

        if len(primary_key) > 0:
            primary_key_statement = "PRIMARY KEY ("
            primary_key_statement += primary_key[0]

            for key_part in primary_key[1:]:
                primary_key_statement += ", "
                primary_key_statement += key_part

            primary_key_statement += ")"

        return primary_key_statement

    @classmethod
    def build_create_table_statement(cls, table_name, columns, foreign_keys, primary_key):
        # preparation
        parsed_columns = cls.__parse_columns(columns)
        parsed_foreign_keys = cls.__parse_foreign_keys(foreign_keys)
        parsed_primary_key = cls.__parse_primary_key(primary_key)

        # building
        create_statement = "CREATE TABLE IF NOT EXISTS" + " " + table_name + "("
        create_statement += parsed_columns

        if parsed_foreign_keys is not None:
            create_statement += ", "
            create_statement += parsed_foreign_keys

        if parsed_primary_key is not None:
            create_statement += ", "
            create_statement += parsed_primary_key

        create_statement += ");"

        return create_statement
