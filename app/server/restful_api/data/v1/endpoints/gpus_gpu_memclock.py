from .gpus_gpu__general_child import GpusGpuGeneralChildEndpoint


class GpusGpuMemclockEndpoint(GpusGpuGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/gpus/<string:gpu>/memclock"
        ]

    @classmethod
    def get_name(cls):
        return "gpu memclock measurement"

    def _get_component_metric(self) -> str:
        return "memclock"
