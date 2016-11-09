from .cpus_cpu__general_child import CpusCpuGeneralChildEndpoint


class CpusCpuTemperatureEndpoint(CpusCpuGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/cpus/<string:cpu>/temperature"
        ]

    @classmethod
    def get_name(cls):
        return "cpu temperature measurement"

    def _get_component_metric(self) -> str:
        return "temperature"
