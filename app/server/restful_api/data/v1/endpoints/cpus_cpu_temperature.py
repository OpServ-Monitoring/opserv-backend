from .cpus_cpu__general_child import CpusCpuGeneralChildEndpoint


class CpusCpuTemperatureEndpoint(CpusCpuGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/cpus/<string:cpu>/temperature"
        ]

    @staticmethod
    def get_name():
        return "cpu temperature measurement"

    def _get_component_metric(self) -> str:
        return "temperature"
