from .__general_data_v1 import GeneralEndpointDataV1


class MemoryEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        return True

    @staticmethod
    def get_paths():
        return [
            "/memory"
        ]

    @staticmethod
    def get_name():
        return "memory entity"

    @staticmethod
    def _get_parent():
        from ...data_api_versions_endpoint import DataApiVersionsEndpoint

        return DataApiVersionsEndpoint

    @classmethod
    def _get_children(cls):
        # TODO children

        return [
        ]

    @staticmethod
    def _get_mandatory_parameters():
        return []
