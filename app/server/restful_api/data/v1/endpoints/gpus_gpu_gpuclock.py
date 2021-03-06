from .gpus_gpu__general_child import GpusGpuGeneralChildEndpoint


class GpusGpuGpuclockEndpoint(GpusGpuGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/gpus/<string:gpu>/gpuclock"
        ]

    @classmethod
    def get_name(cls):
        return "gpu gpuclock measurement"

    @classmethod
    def _get_component_metric(cls) -> str:
        return "gpuclock"
