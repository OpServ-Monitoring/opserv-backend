from server.restful_api.general.endpoint import Endpoint


class ApiRootEndpoint(Endpoint):
    def _get(self):
        pass

    def _put(self):
        return self._get_bad_request_response(
            self._response_holder,
            'HTTP method PUT is not supported by this resource'
        )

    def _post(self):
        return self._get_bad_request_response(
            self._response_holder,
            'HTTP method POST is not supported by this resource'
        )

    def _delete(self):
        return self._get_bad_request_response(
            self._response_holder,
            'HTTP method DELETE is not supported by this resource'
        )

    def _post_process(self):
        pass

    @staticmethod
    def get_paths():
        return [""]

    @staticmethod
    def get_name():
        return "api entry"

    @staticmethod
    def _get_parent():
        return None

    def _get_children(self):
        from server.restful_api.data.data_api_versions_endpoint import DataApiVersionsEndpoint

        return [
            ("/data", DataApiVersionsEndpoint)
        ]
