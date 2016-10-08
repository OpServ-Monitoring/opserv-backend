import sqlite3


class ComponentMetricsWriterReader:
    @staticmethod
    def _is_component_arg_persisted(component_type, component_arg):
        con = sqlite3.connect("opserv.db")  # TODO Set location globally

        query = """
                   SELECT COUNT(*)
                   FROM component_metrics_table
                   WHERE component_type_fk = ? AND component_arg = ?
                   """

        with con:
            return con.execute(query, (component_type, component_arg)).fetchone()[0] > 0

    @staticmethod
    def get_component_args(component_type):
        con = sqlite3.connect("opserv.db")  # TODO Set location globally

        query = """
           SELECT component_arg
           FROM component_metrics_table
           WHERE component_type_fk = ?
           """

        with con:
            return con.execute(query, (component_type,)).fetchall()
