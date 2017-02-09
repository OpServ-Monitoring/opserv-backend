from .gpus_gpu__general_child import GpusGpuGeneralChildEndpoint


class GpusGpuVramusageEndpoint(GpusGpuGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/gpus/<string:gpu>/vramusage"
        ]

    @classmethod
    def get_name(cls):
        return "gpu vramusage measurement"

    @classmethod
    def _get_component_metric(cls) -> str:
        return "vramusage"
