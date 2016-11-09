from ..general.endpoint import Endpoint


class DataApiVersionsEndpoint(Endpoint):
    def _get(self) -> bool:
        # no data section available
        return self.KEEP_PROCESSING()

    def _put(self) -> bool:
        self._set_bad_request_response(
            'HTTP method PUT is not supported by this resource'
        )

        return False

    def _post(self) -> bool:
        self._set_bad_request_response(
            'HTTP method POST is not supported by this resource'
        )

        return False

    def _delete(self) -> bool:
        self._set_bad_request_response(
            'HTTP method DELETE is not supported by this resource'
        )

        return False

    def _post_process(self) -> bool:
        # no post processing needed
        return self.KEEP_PROCESSING()

    @classmethod
    def get_paths(cls):
        return [""]

    @classmethod
    def _get_children(cls):
        from .v1.data_api_v1_endpoint import DataApiV1Endpoint

        return [
            ("/current", DataApiV1Endpoint),
            ("/v1", DataApiV1Endpoint)
        ]

    @classmethod
    def get_name(cls):
        return "data API versions entry"

    @classmethod
    def _get_parent(cls):
        from ..api_root.endpoint_api_root import ApiRootEndpoint

        return ApiRootEndpoint
