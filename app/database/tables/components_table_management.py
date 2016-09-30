class ComponentsTableManagement:
    __TABLE_NAME = "components_table"

    __KEY_COMPONENT_ARG = "component_arg"
    __KEY_COMPONENT_TYPE_FK = "component_type_fk"

    @staticmethod
    def TABLE_NAME():
        return ComponentsTableManagement.__TABLE_NAME

    @staticmethod
    def KEY_COMPONENT_ARG():
        return ComponentsTableManagement.__KEY_COMPONENT_ARG

    @staticmethod
    def KEY_COMPONENT_TYPE_FK():
        return ComponentsTableManagement.__KEY_COMPONENT_TYPE_FK
