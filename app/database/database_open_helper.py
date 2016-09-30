import sqlite3

from .sql_statement_builder import SqlStatementBuilder
from .tables.component_types_table_management import ComponentTypesTableManagement
from .tables.components_table_management import ComponentsTableManagement
from .tables.measurements_table_management import MeasurementsTableManagement
from .tables.metrics_table_management import MetricsTableManagement

# TODO Decide whether the location should be configurable
location = 'opserv.db'


class DatabaseOpenHelper:
    __create_table_metric = SqlStatementBuilder.build_create_table_statement(
        # TABLE NAME
        MetricsTableManagement.TABLE_NAME(),
        # COLUMNS
        [
            (MetricsTableManagement.KEY_NAME(), "TEXT NOT NULL")
        ],
        # FOREIGN KEYS
        [],
        # PRIMARY KEY
        [
            MetricsTableManagement.KEY_NAME()
        ]
    )

    __create_table_component_types = SqlStatementBuilder.build_create_table_statement(
        # TABLE NAME
        ComponentTypesTableManagement.TABLE_NAME(),
        # COLUMNS
        [
            (ComponentTypesTableManagement.KEY_NAME(), "TEXT NOT NULL")
        ],
        # FOREIGN KEYS
        [],
        # PRIMARY KEY
        [
            ComponentTypesTableManagement.KEY_NAME()
        ]
    )

    __create_table_components = SqlStatementBuilder.build_create_table_statement(
        # TABLE NAME
        ComponentsTableManagement.TABLE_NAME(),
        # COLUMNS
        [
            (ComponentsTableManagement.KEY_COMPONENT_ARG(), "TEXT NOT NULL"),
            (ComponentsTableManagement.KEY_COMPONENT_TYPE_FK(), "TEXT NOT NULL")
        ],
        # FOREIGN KEYS
        [
            (
                [
                    ComponentsTableManagement.KEY_COMPONENT_TYPE_FK()
                ],
                ComponentTypesTableManagement.TABLE_NAME(),
                [
                    ComponentTypesTableManagement.KEY_NAME()
                ]
            )
        ],
        # PRIMARY KEY
        [
            ComponentsTableManagement.KEY_COMPONENT_ARG(),
            ComponentsTableManagement.KEY_COMPONENT_TYPE_FK()
        ]
    )

    __create_table_measurements = SqlStatementBuilder.build_create_table_statement(
        # TABLE NAME
        MeasurementsTableManagement.TABLE_NAME(),
        # COLUMNS
        [
            (MeasurementsTableManagement.KEY_COMPONENT_ARG_FK(), "TEXT NOT NULL"),
            (MeasurementsTableManagement.KEY_COMPONENT_TYPE_FK(), "TEXT NOT NULL"),
            (MeasurementsTableManagement.KEY_METRIC_FK(), "TEXT NOT NULL"),
            (MeasurementsTableManagement.KEY_TIMESTAMP(), "INTEGER NOT NULL"),
            (MeasurementsTableManagement.KEY_VALUE(), "TEXT NOT NULL")
        ],
        # FOREIGN KEYS
        [
            (
                [
                    MeasurementsTableManagement.KEY_METRIC_FK()
                ],
                MetricsTableManagement.TABLE_NAME(),
                [
                    MetricsTableManagement.KEY_NAME()
                ]
            ),
            (
                [
                    MeasurementsTableManagement.KEY_COMPONENT_ARG_FK(),
                    MeasurementsTableManagement.KEY_COMPONENT_TYPE_FK()
                ],
                ComponentsTableManagement.TABLE_NAME(),
                [
                    ComponentsTableManagement.KEY_COMPONENT_ARG(),
                    ComponentsTableManagement.KEY_COMPONENT_TYPE_FK()
                ]
            )
        ],
        # PRIMARY KEY
        [
            MeasurementsTableManagement.KEY_COMPONENT_TYPE_FK(),
            MeasurementsTableManagement.KEY_COMPONENT_ARG_FK(),
            MeasurementsTableManagement.KEY_METRIC_FK(),
            MeasurementsTableManagement.KEY_TIMESTAMP()
        ]
    )

    def on_create(self):
        connection = sqlite3.connect(location)

        connection.execute(self.__create_table_metric)
        connection.execute(self.__create_table_component_types)
        connection.execute(self.__create_table_components)
        connection.execute(self.__create_table_measurements)

        connection.execute("PRAGMA JOURNAL_MODE=WAL")
        connection.execute("PRAGMA FOREIGN_KEYS=ON")

        connection.commit()

        # TODO Add supported metrics and component types on startup
        # TODO Add triggers to create a component in case it does not exist (foreign key constraint of measurements)
