from .cpucores_cpucore__general_child import CpucoresCpucoreGeneralChildEndpoint


class CpucoresCpucoreFrequencyEndpoint(CpucoresCpucoreGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/cpu-cores/<string:cpu_core>/frequency",
        ]

    @staticmethod
    def get_name():
        return "cpu core frequency measurement"
