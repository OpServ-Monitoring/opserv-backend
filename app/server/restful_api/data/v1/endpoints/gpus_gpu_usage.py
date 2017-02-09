from .gpus_gpu__general_child import GpusGpuGeneralChildEndpoint


class GpusGpuUsageEndpoint(GpusGpuGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/gpus/<string:gpu>/usage"
        ]

    @classmethod
    def get_name(cls):
        return "gpu usage measurement"

    @classmethod
    def _get_component_metric(cls) -> str:
        return "usage"
