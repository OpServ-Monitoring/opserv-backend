from .__general_data_v1 import GeneralEndpointDataV1


class MemoryEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        return True

    @classmethod
    def get_paths(cls):
        return [
            "/memory"
        ]

    @classmethod
    def get_name(cls):
        return "memory entity"

    @classmethod
    def _get_parent(cls):
        from ...data_api_versions_endpoint import DataApiVersionsEndpoint

        return DataApiVersionsEndpoint

    @classmethod
    def _get_children(cls):
        # TODO children

        return [
        ]

    @classmethod
    def _get_mandatory_parameters(cls):
        return []
