from server.restful_api.data.v1.endpoints.cpucores_cpucore__general_child import CpucoresCpucoreGeneralChildEndpoint


class CpucoresCpucoreTemperatureEndpoint(CpucoresCpucoreGeneralChildEndpoint):
    def _get(self) -> bool:
        # TODO Implement endpoint
        return True

    @staticmethod
    def get_paths():
        return [
            "/cpu-cores/<string:cpu_core>/temperature",
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"
