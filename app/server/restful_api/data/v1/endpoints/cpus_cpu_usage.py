from server.restful_api.data.v1.endpoints.cpus_cpu__general_child import CpusCpuGeneralChildEndpoint


class CpusCpuUsageEndpoint(CpusCpuGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/cpus/<string:cpu>/usage"
        ]

    @staticmethod
    def get_name():
        return "cpu usage measurement"
