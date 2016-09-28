from app.server.restful_api.general.endpoint import Endpoint


class ApiRootEndpoint(Endpoint):
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
    def get_name():
        return "api entry"

    @staticmethod
    def _get_parent():
        return None

    @staticmethod
    def _get_children():
        from app.server.restful_api.data.data_api_versions_endpoint import DataApiVersionsEndpoint

        return [
            ("/data", DataApiVersionsEndpoint)
        ]
