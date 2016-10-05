from .cpucores_cpucore__general_child import CpucoresCpucoreGeneralChildEndpoint


class CpucoresCpucoreUsageEndpoint(CpucoresCpucoreGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/cpu-cores/<string:cpu_core>/usage"
        ]

    @staticmethod
    def get_name():
        return "cpu core usage measurement"

    def _get_component_metric(self) -> str:
        return "usage"
