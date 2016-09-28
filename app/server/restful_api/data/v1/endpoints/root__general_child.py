from abc import ABCMeta

from app.server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class RootGeneralChildEndpoint(GeneralEndpointDataV1, metaclass=ABCMeta):
    @staticmethod
    def _get_parent():
        from app.server.restful_api.data.data_api_versions_endpoint import DataApiVersionsEndpoint

        return DataApiVersionsEndpoint
