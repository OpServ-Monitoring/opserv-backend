from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class CpusCpuEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        # TODO implement endpoint
        return True

    @staticmethod
    def get_paths():
        return [
            "/cpus/<string:cpu>"
        ]

    @staticmethod
    def get_name():
        return "cpu entity"

    @staticmethod
    def _get_parent():
        from server.restful_api.data.v1.endpoints.cpus import CpusEndpoint

        return CpusEndpoint

    @staticmethod
    def _get_children():
        from server.restful_api.data.v1.endpoints.cpus_cpu_frequency import CpusCpuFrequencyEndpoint
        from server.restful_api.data.v1.endpoints.cpus_cpu_temperature import CpusCpuTemperatureEndpoint
        from server.restful_api.data.v1.endpoints.cpus_cpu_usage import CpusCpuUsageEndpoint
        from server.restful_api.data.v1.endpoints.cpucores import CpucoresEndpoint

        return [
            ("/frequency", CpusCpuFrequencyEndpoint),
            ("/temperature", CpusCpuTemperatureEndpoint),
            ("/usage", CpusCpuUsageEndpoint)
        ]
