from .gpus_gpu__general_child import GpusGpuGeneralChildEndpoint


class GpusGpuGpuclockEndpoint(GpusGpuGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/gpus/<string:gpu>/gpuclock"
        ]

    @staticmethod
    def get_name():
        return "gpu gpuclock measurement"

    def _get_component_metric(self) -> str:
        return "gpuclock"
