from server.restful_api.general.endpoint import Endpoint


class DataApiVersionsEndpoint(Endpoint):
    def _get(self) -> bool:
        return True

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
        return True

    @staticmethod
    def get_paths():
        return [""]

    @staticmethod
    def _get_children():
        from server.restful_api.data.v1.data_api_v1_endpoint import DataApiV1Endpoint

        return [
            ("/current", DataApiV1Endpoint),
            ("/v1", DataApiV1Endpoint)
        ]

    @staticmethod
    def get_name():
        pass

    @staticmethod
    def _get_parent():
        from server.restful_api.api_root.endpoint_api_root import ApiRootEndpoint

        return ApiRootEndpoint
