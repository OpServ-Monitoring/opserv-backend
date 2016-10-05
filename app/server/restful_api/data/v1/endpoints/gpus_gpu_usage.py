from .gpus_gpu__general_child import GpusGpuGeneralChildEndpoint


class GpusGpuUsageEndpoint(GpusGpuGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/gpus/<string:gpu>/usage"
        ]

    @staticmethod
    def get_name():
        return "gpu usage measurement"

    def _get_component_metric(self) -> str:
        return "usage"
