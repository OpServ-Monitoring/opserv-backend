from ..general.endpoint import Endpoint


class ApiRootEndpoint(Endpoint):
    def _get(self) -> bool:
        # no data section available
        return self.KEEP_PROCESSING()

    def _put(self) -> bool:
        self._response_holder.set_bad_request_response(
            'HTTP method PUT is not supported by this resource'
        )

        return False

    def _post(self) -> bool:
        self._response_holder.set_bad_request_response(
            'HTTP method POST is not supported by this resource'
        )

        return False

    def _delete(self) -> bool:
        self._response_holder.set_bad_request_response(
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
    def get_name(cls):
        return "api entry"

    @classmethod
    def _get_parent(cls):
        return None

    @classmethod
    def _get_children(cls):
        from ..data.data_api_versions_endpoint import DataApiVersionsEndpoint
        from ..preferences.preferences_api_versions_endpoint import PreferencesApiVersionsEndpoint

        return [
            ("/data", DataApiVersionsEndpoint),
            ("/preferences", PreferencesApiVersionsEndpoint)
        ]
