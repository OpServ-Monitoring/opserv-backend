from server.restful_api.data.v1.endpoints.__general_realtime_historical import GeneralEndpointRealtimeHistorical


class CpucoresCpucoreTemperatureEndpoint(GeneralEndpointRealtimeHistorical):
    def _get(self):
        # TODO Implement endpoint
        pass

    @staticmethod
    def get_paths():
        return [
            "/cpu-cores/<string:cpu_core>/temperature",
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent():
        from server.restful_api.data.v1.endpoints.cpucores_cpucore import CpucoresCpucoreEndpoint

        return CpucoresCpucoreEndpoint
