from .cpucores_cpucore__general_child import CpucoresCpucoreGeneralChildEndpoint


class CpucoresCpucoreFrequencyEndpoint(CpucoresCpucoreGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/cpu-cores/<string:cpu_core>/frequency",
        ]

    @classmethod
    def get_name(cls):
        return "cpu core frequency measurement"

    @classmethod
    def _get_component_metric(cls) -> str:
        return "frequency"
