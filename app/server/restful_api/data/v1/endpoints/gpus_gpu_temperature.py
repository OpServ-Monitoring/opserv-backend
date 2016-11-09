from .gpus_gpu__general_child import GpusGpuGeneralChildEndpoint


class GpusGpuTemperatureEndpoint(GpusGpuGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/gpus/<string:gpu>/temperature"
        ]

    @classmethod
    def get_name(cls):
        return "gpu temperature measurement"

    def _get_component_metric(self) -> str:
        return "temperature"
