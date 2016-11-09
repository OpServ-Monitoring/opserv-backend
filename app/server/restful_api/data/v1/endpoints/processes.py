from .root__general_child import RootGeneralChildEndpoint
from ....general.endpoint import Endpoint


class ProcessesEndpoint(RootGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/processes"
        ]

    @classmethod
    def get_name(cls):
        return "process entities"

    @classmethod
    def _get_hardware_value_type(cls) -> str:
        return "processes"

    @classmethod
    def _get_children_endpoint_type(cls) -> Endpoint:
        from .processes_process import ProcessesProcessEndpoint

        return ProcessesProcessEndpoint
