from .root__general_child import RootGeneralChildEndpoint
from ....general.endpoint import Endpoint


class ProcessesEndpoint(RootGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/processes"
        ]

    @staticmethod
    def get_name():
        return "process entities"

    @staticmethod
    def _get_hardware_value_type() -> str:
        return "processes"

    @staticmethod
    def _get_component_type() -> str:
        return "process"

    @staticmethod
    def _get_children_endpoint_type() -> Endpoint:
        from .processes_process import ProcessesProcessEndpoint

        return ProcessesProcessEndpoint
