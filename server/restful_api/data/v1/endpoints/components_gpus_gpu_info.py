import queueManager
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
