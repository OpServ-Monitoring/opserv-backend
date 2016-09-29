from .cpucores_cpucore__general_child import CpucoresCpucoreGeneralChildEndpoint


class CpucoresCpucoreTemperatureEndpoint(CpucoresCpucoreGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/cpu-cores/<string:cpu_core>/temperature",
        ]

    @staticmethod
    def get_name():
        return "cpu core temperature measurement"
