from .gpus_gpu__general_child import GpusGpuGeneralChildEndpoint


class GpusGpuVramusageEndpoint(GpusGpuGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/gpus/<string:gpu>/vramusage"
        ]

    @staticmethod
    def get_name():
        return "gpu vramusage measurement"

    def _get_component_metric(self) -> str:
        return "vramusage"
