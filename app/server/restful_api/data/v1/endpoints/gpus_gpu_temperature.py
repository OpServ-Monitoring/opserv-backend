from .gpus_gpu__general_child import GpusGpuGeneralChildEndpoint


class GpusGpuTemperatureEndpoint(GpusGpuGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/gpus/<string:gpu>/temperature"
        ]

    @staticmethod
    def get_name():
        return "gpu temperature measurement"

    def _get_component_metric(self) -> str:
        return "temperature"
