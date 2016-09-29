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

    @staticmethod
    def get_paths():
        return [""]

    @staticmethod
    def _get_children():
        from .v1.data_api_v1_endpoint import DataApiV1Endpoint

        return [
            ("/current", DataApiV1Endpoint),
            ("/v1", DataApiV1Endpoint)
        ]

    @staticmethod
    def get_name():
        pass

    @staticmethod
    def _get_parent():
        from ..api_root.endpoint_api_root import ApiRootEndpoint

        return ApiRootEndpoint
