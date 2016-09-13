from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class GpusGpuInfoEndpoint(GeneralEndpointDataV1):
    def _get(self):
        # TODO Implement endpoint
        pass

    @staticmethod
    def get_paths():
        return [
            "/components/gpus/<string:gpu>/info"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "gpu info endpoint"

    @staticmethod
    def _get_parent_name():
        from server.restful_api.data.v1.endpoints.components_gpus_gpu import GpusGpuEndpoint

        return GpusGpuEndpoint.get_name()

    def _get_children(self):
        return []
