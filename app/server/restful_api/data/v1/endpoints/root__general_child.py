from abc import ABCMeta

from .__general_data_v1 import GeneralEndpointDataV1


class RootGeneralChildEndpoint(GeneralEndpointDataV1, metaclass=ABCMeta):
    @staticmethod
    def _get_parent():
        from ...data_api_versions_endpoint import DataApiVersionsEndpoint

        return DataApiVersionsEndpoint

    def _get(self) -> bool:
        # no data section available
        return self.KEEP_PROCESSING()
