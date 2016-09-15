from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class GpusGpuEndpoint(GeneralEndpointDataV1):
    def _get(self):
        # TODO general info
        pass

    @staticmethod
    def get_paths():
        return [
            "/components/gpus/<string:gpu>"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent_name():
        from server.restful_api.data.v1.endpoints.components_gpus import GpusEndpoint

        return GpusEndpoint.get_name()

    def _get_children(self):
        return [
        ]
