from server.restful_api.general.endpoint import Endpoint


class DataApiVersionsEndpoint(Endpoint):
    def _post_process(self):
        pass

    def _get(self):
        # TODO implement
        pass

    def _put(self):
        return self._return_bad_request_response(self._response_holder)

    def _post(self):
        return self._return_bad_request_response(self._response_holder)

    def _delete(self):
        return self._return_bad_request_response(self._response_holder)

    @staticmethod
    def get_paths():
        return [""]
