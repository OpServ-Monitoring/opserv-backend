from server.restful_api.data.v1.endpoints.cpucores_cpucore__general_child import CpucoresCpucoreGeneralChildEndpoint


class CpucoresCpucoreFrequencyEndpoint(CpucoresCpucoreGeneralChildEndpoint):
    def _get(self) -> bool:
        # TODO Implement endpoint
        return True

    @staticmethod
    def get_paths():
        return [
            "/cpu-cores/<string:cpu_core>/frequency",
        ]

    @staticmethod
    def get_name():
        return "cpu core frequency measurement"

    @staticmethod
    def _get_children():
        return []
