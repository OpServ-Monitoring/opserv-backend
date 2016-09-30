class SqlStatementBuilder:
    @classmethod
    def __parse_columns(cls, columns):
        assert len(columns) > 0

        columns_statement = cls.__to_string_list(columns, cls.__parse_column)

        return columns_statement

    @classmethod
    def __parse_column(cls, column):
        return column[0] + " " + column[1]

    @classmethod
    def __parse_foreign_keys(cls, foreign_keys):
        foreign_keys_statement = None

        if len(foreign_keys) > 0:
            foreign_keys_statement = cls.__to_string_list(foreign_keys, cls.__parse_foreign_key)

        return foreign_keys_statement

    @classmethod
    def __parse_foreign_key(cls, foreign_key):
        assert len(foreign_key[0]) > 0
        assert len(foreign_key[0]) == len(foreign_key[2])

        foreign_key_statement = "FOREIGN KEY ("
        foreign_key_statement += cls.__to_string_list(foreign_key[0])

        foreign_key_statement += ") REFERENCES "
        foreign_key_statement += foreign_key[1]

        foreign_key_statement += "("
        foreign_key_statement += cls.__to_string_list(foreign_key[2])
        foreign_key_statement += ") "

        return foreign_key_statement

    @classmethod
    def __parse_primary_key(cls, primary_key):
        primary_key_statement = None

        if len(primary_key) > 0:
            primary_key_statement = "PRIMARY KEY ("
            primary_key_statement += cls.__to_string_list(primary_key)
            primary_key_statement += ")"

        return primary_key_statement

    @classmethod
    def build_create_table_statement(cls, table_name, columns, foreign_keys, primary_key):
        def __append_to_string_list_if_not_none(base, appendix):
            if appendix is not None:
                return cls.__append_to_string_list(base, appendix)
            return base

        # preparation
        parsed_columns = cls.__parse_columns(columns)
        parsed_foreign_keys = cls.__parse_foreign_keys(foreign_keys)
        parsed_primary_key = cls.__parse_primary_key(primary_key)

        # building
        create_statement = "CREATE TABLE IF NOT EXISTS" + " " + table_name + "("
        create_statement += parsed_columns

        create_statement = __append_to_string_list_if_not_none(create_statement, parsed_foreign_keys)
        create_statement = __append_to_string_list_if_not_none(create_statement, parsed_primary_key)

        create_statement += ");"

        return create_statement

    @classmethod
    def __to_string_list(cls, raw_list, parsing_function=None):
        string_list = raw_list[0] if parsing_function is None else parsing_function(raw_list[0])

        for item in raw_list[1:]:
            string_list = cls.__append_to_string_list(
                string_list,
                item if parsing_function is None else parsing_function(item)
            )

        return string_list

    @classmethod
    def __append_to_string_list(cls, base, appendix):
        return base + ", " + appendix
