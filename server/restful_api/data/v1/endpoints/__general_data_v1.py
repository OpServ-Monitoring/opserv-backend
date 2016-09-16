from abc import ABCMeta
from server.restful_api.general.endpoint import Endpoint


class GeneralEndpointDataV1(Endpoint, metaclass=ABCMeta):
    def _post_process(self):
        response_headers = self._response_holder.get_response_headers()

        response_headers['Access-Control-Allow-Origin'] = '*'
        response_headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response_headers['Access-Control-Allow-Methods'] = 'GET'

        self._response_holder.set_response_headers(response_headers)

    def _put(self):
        """
        The PUT-method is not supported by this api version, thus an response indicating a bad request is returned
        :return: A ResponseHolder holding a response with the bad request code
        """
        return self._get_bad_request_response(
            self._response_holder,
            'HTTP method PUT is not supported by this resource'
        )

    def _post(self):
        """
        The POST-method is not supported by this api version, thus an response indicating a bad request is returned
        :return: A ResponseHolder holding a response with the bad request code
        """
        return self._get_bad_request_response(
            self._response_holder,
            'HTTP method POST is not supported by this resource'
        )

    def _delete(self):
        """
        The DELETE-method is not supported by this api version, thus an response indicating a bad request is returned
        :return: A ResponseHolder holding a response with the bad request code
        """
        return self._get_bad_request_response(
            self._response_holder,
            'HTTP method DELETE is not supported by this resource'
        )
