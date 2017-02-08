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
    def _get_component_type(cls) -> str:
        return "process"

    @classmethod
    def _get_children_endpoint_type(cls) -> Endpoint:
        from .processes_process import ProcessesProcessEndpoint

        return ProcessesProcessEndpoint
