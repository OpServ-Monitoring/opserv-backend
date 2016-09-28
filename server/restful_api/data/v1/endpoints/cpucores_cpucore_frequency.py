from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class CpucoresCpucoreFrequencyEndpoint(GeneralEndpointDataV1):
    def _get(self):
        # TODO Implement endpoint
        pass

    @staticmethod
    def get_paths():
        return [
            "/cpu-cores/<string:cpu_core>/frequency",
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent():
        from server.restful_api.data.v1.endpoints.cpucores_cpucore import CpucoresCpucoreEndpoint

        return CpucoresCpucoreEndpoint

    @staticmethod
    def _get_children():
        return []
