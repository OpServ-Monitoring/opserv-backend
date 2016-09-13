import queueManager
from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class CpusCpuEndpoint(GeneralEndpointDataV1):
    def _get(self):
        pass

    @staticmethod
    def get_paths():
        return [
            "/components/cpus/<string:cpu>"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent_name():
        from server.restful_api.data.v1.endpoints.components_cpus import CpusEndpoint

        return CpusEndpoint.get_name()

    def _get_children(self):
        from server.restful_api.data.v1.endpoints.components_cpus_cpu_frequency import CpusCpuFrequencyEndpoint
        from server.restful_api.data.v1.endpoints.components_cpus_cpu_info import CpusCpuInfoEndpoint
        from server.restful_api.data.v1.endpoints.components_cpus_cpu_temperature import CpusCpuTemperatureEndpoint
        from server.restful_api.data.v1.endpoints.components_cpus_cpu_usage import CpusCpuUsageEndpoint

        return [
            ("/frequency", CpusCpuFrequencyEndpoint),
            ("/info", CpusCpuInfoEndpoint),
            ("/temperature", CpusCpuTemperatureEndpoint),
            ("/usage", CpusCpuUsageEndpoint)
        ]