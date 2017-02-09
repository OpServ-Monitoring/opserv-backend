from .cpucores_cpucore__general_child import CpucoresCpucoreGeneralChildEndpoint


class CpucoresCpucoreTemperatureEndpoint(CpucoresCpucoreGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/cpu-cores/<string:cpu_core>/temperature",
        ]

    @classmethod
    def get_name(cls):
        return "cpu core temperature measurement"

    @classmethod
    def _get_component_metric(cls) -> str:
        return "temperature"
