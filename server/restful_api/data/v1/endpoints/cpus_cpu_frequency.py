from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class CpusCpuFrequencyEndpoint(GeneralEndpointDataV1):
    def _get(self):
        # TODO Implement endpoint
        pass

    @staticmethod
    def get_paths():
        return [
            "/cpus/<string:cpu>/frequency"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent_name():
        from server.restful_api.data.v1.endpoints.cpus_cpu import CpusCpuEndpoint
        return CpusCpuEndpoint.get_name()

    def _get_children(self):
        return []
