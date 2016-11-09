from .cpucores_cpucore__general_child import CpucoresCpucoreGeneralChildEndpoint


class CpucoresCpucoreUsageEndpoint(CpucoresCpucoreGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/cpu-cores/<string:cpu_core>/usage"
        ]

    @classmethod
    def get_name(cls):
        return "cpu core usage measurement"

    def _get_component_metric(self) -> str:
        return "usage"
