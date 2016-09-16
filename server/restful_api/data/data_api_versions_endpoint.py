from server.restful_api.general.endpoint import Endpoint


class DataApiVersionsEndpoint(Endpoint):

    def _post_process(self):
        pass

    def _get(self):
        pass

    def _put(self):
        return self._get_bad_request_response(self._response_holder)

    def _post(self):
        return self._get_bad_request_response(self._response_holder)

    def _delete(self):
        return self._get_bad_request_response(self._response_holder)

    @staticmethod
    def get_paths():
        return [""]

    def _get_children(self):
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
