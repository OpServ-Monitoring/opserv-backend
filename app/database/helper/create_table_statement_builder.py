class CreateTableStatementBuilder:
    @classmethod
    def __parse_columns(cls, columns):
        return cls.__parse_list(columns, cls.__parse_column)

    @classmethod
    def __parse_column(cls, column):
        return column[0] + " " + column[1]

    @classmethod
    def __parse_foreign_keys(cls, foreign_keys):
        return cls.__parse_list(foreign_keys, cls.__parse_foreign_key)

    @classmethod
    def __parse_foreign_key(cls, foreign_key):
        if len(foreign_key[0]) > 0 and len(foreign_key[0]) == len(foreign_key[2]):
            foreign_key_statement = "FOREIGN KEY ("
            foreign_key_statement += cls.__to_string_list(foreign_key[0])

            foreign_key_statement += ") REFERENCES "
            foreign_key_statement += foreign_key[1]

            foreign_key_statement += "("
            foreign_key_statement += cls.__to_string_list(foreign_key[2])
            foreign_key_statement += ") "

            return foreign_key_statement

        return None  # TODO Log error

    @classmethod
    def __parse_primary_key(cls, primary_key):
        if len(primary_key) > 0:
            return "PRIMARY KEY (" + cls.__to_string_list(primary_key) + ")"

        return None

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
    def __append_to_string_list(cls, string_list, appendix):
        return string_list + ", " + appendix

    @classmethod
    def __parse_list(cls, a_list: list, parsing_function):
        if len(a_list) > 0:
            return cls.__to_string_list(a_list, parsing_function)

        return None  # TODO Log error
