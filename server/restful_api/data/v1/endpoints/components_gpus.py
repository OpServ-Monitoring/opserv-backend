import queueManager
from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class GpusEndpoint(GeneralEndpointDataV1):
    def _get(self):
        pass

    @staticmethod
    def get_paths():
        return [
            "/components/gpus"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent_name():
        from server.restful_api.data.v1.endpoints.components import ComponentsEndpoint

        return ComponentsEndpoint.get_name()

    def _get_children(self):
        # TODO Implement dynamic children
        return []
