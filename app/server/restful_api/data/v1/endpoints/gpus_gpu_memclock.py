from .gpus_gpu__general_child import GpusGpuGeneralChildEndpoint


class GpusGpuMemclockEndpoint(GpusGpuGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/gpus/<string:gpu>/memclock"
        ]

    @staticmethod
    def get_name():
        return "gpu memclock measurement"

    def _get_component_metric(self) -> str:
        return "memclock"
