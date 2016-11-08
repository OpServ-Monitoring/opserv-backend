from .root__general_child import RootGeneralChildEndpoint
from ....general.endpoint import Endpoint


class GpusEndpoint(RootGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/gpus"
        ]

    @staticmethod
    def get_name():
        return "gpu entities"

    @staticmethod
    def _get_hardware_value_type() -> str:
        return "gpus"

    @staticmethod
    def _get_children_endpoint_type() -> Endpoint:
        from .gpus_gpu import GpusGpuEndpoint

        return GpusGpuEndpoint
