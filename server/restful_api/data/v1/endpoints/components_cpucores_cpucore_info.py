from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class CpucoresCpucoreInfoEndpoint(GeneralEndpointDataV1):
    def _get(self):
        # TODO Implement endpoint
        pass

    @staticmethod
    def get_paths():
        return [
            "/components/cpu-cores/<string:cpu_core>/info",
            "/components/cpus/<string:cpu>/cpu-cores/<string:cpu_core>/info"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent_name():
        from server.restful_api.data.v1.endpoints.components_cpucores_cpucore import CpucoresCpucoreEndpoint

        return CpucoresCpucoreEndpoint.get_name()

    def _get_children(self):
        return []
