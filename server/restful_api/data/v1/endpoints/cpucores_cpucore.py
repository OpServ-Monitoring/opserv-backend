from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class CpucoresCpucoreEndpoint(GeneralEndpointDataV1):
    def _get(self):
        pass

    @staticmethod
    def get_paths():
        return [
            "/cpus/<string:cpu>/cpu-cores/<string:cpu_core>",
            "/cpu-cores/<string:cpu_core>"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent_name():
        from server.restful_api.data.v1.endpoints.cpucores import CpucoresEndpoint

        return CpucoresEndpoint.get_name()

    def _get_children(self):
        from server.restful_api.data.v1.endpoints.cpucores_cpucore_frequency import \
            CpucoresCpucoreFrequencyEndpoint
        from server.restful_api.data.v1.endpoints.cpucores_cpucore_temperature import \
            CpucoresCpucoreTemperatureEndpoint
        from server.restful_api.data.v1.endpoints.cpucores_cpucore_usage import CpucoresCpucoreUsageEndpoint

        return [
            ("/frequency", CpucoresCpucoreFrequencyEndpoint),
            ("/temperature", CpucoresCpucoreTemperatureEndpoint),
            ("/usage", CpucoresCpucoreUsageEndpoint)
        ]
