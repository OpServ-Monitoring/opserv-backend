from .root__general_child import RootGeneralChildEndpoint
from ....general.endpoint import Endpoint


class CpusEndpoint(RootGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/cpus"
        ]

    @staticmethod
    def get_name():
        return "cpu entities"

    @staticmethod
    def _get_hardware_value_type() -> str:
        return "cpus"

    @staticmethod
    def _get_children_endpoint_type() -> Endpoint:
        from .cpus_cpu import CpusCpuEndpoint

        return CpusCpuEndpoint
