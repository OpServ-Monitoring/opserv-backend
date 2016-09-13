from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class CpucoresCpucoreEndpoint(GeneralEndpointDataV1):
    def _get(self):
        pass

    @staticmethod
    def get_paths():
        return [
            "/components/cpus/<string:cpu>/cpu-cores/<string:cpu_core>",
            "/components/cpu-cores/<string:cpu_core>"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent_name():
        from server.restful_api.data.v1.endpoints.components_cpucores import CpucoresEndpoint

        return CpucoresEndpoint.get_name()

    def _get_children(self):
        from server.restful_api.data.v1.endpoints.components_cpucores_cpucore_frequency import \
            CpucoresCpucoreFrequencyEndpoint
        from server.restful_api.data.v1.endpoints.components_cpucores_cpucore_info import CpucoresCpucoreInfoEndpoint
        from server.restful_api.data.v1.endpoints.components_cpucores_cpucore_temperature import \
            CpucoresCpucoreTemperatureEndpoint
        from server.restful_api.data.v1.endpoints.components_cpucores_cpucore_usage import CpucoresCpucoreUsageEndpoint

        return [
            ("/frequency", CpucoresCpucoreFrequencyEndpoint),
            ("/info", CpucoresCpucoreInfoEndpoint),
            ("/temperature", CpucoresCpucoreTemperatureEndpoint),
            ("/usage", CpucoresCpucoreUsageEndpoint)
        ]
