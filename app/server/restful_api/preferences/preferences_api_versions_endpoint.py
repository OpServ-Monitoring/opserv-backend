from ..general.endpoint import Endpoint


class PreferencesApiVersionsEndpoint(Endpoint):
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

    @classmethod
    def _get_children(cls):
        from .v1.preferences_api_v1_endpoint import PreferencesApiV1Endpoint

        return [
            ("/current", PreferencesApiV1Endpoint),
            ("/v1", PreferencesApiV1Endpoint)
        ]

    @staticmethod
    def get_name():
        return "preferences API versions entry"

    @staticmethod
    def _get_parent():
        from ..api_root.endpoint_api_root import ApiRootEndpoint

        return ApiRootEndpoint
