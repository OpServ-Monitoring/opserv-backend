from server.restful_api.data.v1.endpoints.cpus_cpu__general_child import CpusCpuGeneralChildEndpoint


class CpusCpuFrequencyEndpoint(CpusCpuGeneralChildEndpoint):
    def _get(self) -> bool:
        # TODO Implement endpoint
        return True

    @staticmethod
    def get_paths():
        return [
            "/cpus/<string:cpu>/frequency"
        ]

    @staticmethod
    def get_name():
        return "cpu frequency measurement"

    @staticmethod
    def _get_children():
        return []
