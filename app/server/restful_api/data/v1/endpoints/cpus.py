from .root__general_child import RootGeneralChildEndpoint
from ....general.endpoint import Endpoint


class CpusEndpoint(RootGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/cpus"
        ]

    @classmethod
    def get_name(cls):
        return "cpu entities"

    @classmethod
    def _get_hardware_value_type(cls) -> str:
        return "cpus"

    @classmethod
    def _get_children_endpoint_type(cls) -> Endpoint:
        from .cpus_cpu import CpusCpuEndpoint

        return CpusCpuEndpoint
