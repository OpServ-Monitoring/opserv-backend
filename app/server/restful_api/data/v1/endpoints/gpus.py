from .root__general_child import RootGeneralChildEndpoint
from ....general.endpoint import Endpoint


class GpusEndpoint(RootGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/gpus"
        ]

    @classmethod
    def get_name(cls):
        return "gpu entities"

    @classmethod
    def _get_hardware_value_type(cls) -> str:
        return "gpus"

    @classmethod
    def _get_children_endpoint_type(cls) -> Endpoint:
        from .gpus_gpu import GpusGpuEndpoint

        return GpusGpuEndpoint
