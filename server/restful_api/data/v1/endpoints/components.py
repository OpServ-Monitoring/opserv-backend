from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class ComponentsEndpoint(GeneralEndpointDataV1):
    def _get(self):
        pass

    @staticmethod
    def get_paths():
        return [
            "/components"
        ]

    @staticmethod
    def get_name():
        # TODO useful name
        return "component type reference"

    @staticmethod
    def _get_parent_name():
        from server.restful_api.data.v1.data_api_v1_endpoint import DataApiV1Endpoint
        return DataApiV1Endpoint.get_name()

    def _get_children(self):
        from server.restful_api.data.v1.endpoints.components_cpus import CpusEndpoint
        from server.restful_api.data.v1.endpoints.components_cpucores import CpucoresEndpoint
        from server.restful_api.data.v1.endpoints.components_gpus import GpusEndpoint

        return [
            ("/cpus", CpusEndpoint),
            ("/cpu-cores", CpucoresEndpoint),
            ("/gpus", GpusEndpoint)
        ]
