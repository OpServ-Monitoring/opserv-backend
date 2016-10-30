from .root__general_child import RootGeneralChildEndpoint
from ....general.endpoint import Endpoint


class PartitionsEndpoint(RootGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/partitions"
        ]

    @staticmethod
    def get_name():
        return "partition entities"

    @staticmethod
    def _get_hardware_value_type() -> str:
        return "partitions"

    @staticmethod
    def _get_component_type() -> str:
        return "partition"

    @staticmethod
    def _get_children_endpoint_type() -> Endpoint:
        # TODO exchange children
        from .cpus_cpu import CpusCpuEndpoint

        return CpusCpuEndpoint
