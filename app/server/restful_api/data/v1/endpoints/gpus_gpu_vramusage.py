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

    def _get_component_metric(self) -> str:
        return "vramusage"
