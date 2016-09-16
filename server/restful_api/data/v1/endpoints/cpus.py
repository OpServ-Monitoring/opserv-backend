from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class CpusEndpoint(GeneralEndpointDataV1):
    def _get(self):
        pass

    @staticmethod
    def get_paths():
        return [
            "/cpus"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent_name():
        from server.restful_api.data.v1.data_api_v1_endpoint import DataApiV1Endpoint

        return DataApiV1Endpoint.get_name()

    def _get_children(self):
        from server.restful_api.data.v1.endpoints.cpus_cpu import CpusCpuEndpoint

        children = []

        # TODO Implement dynamic children
        ids = []
        for cpu_id in ids:
            children.append(("/" + cpu_id, CpusCpuEndpoint))

        return children
