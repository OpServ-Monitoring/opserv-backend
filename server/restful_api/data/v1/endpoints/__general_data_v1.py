import abc

from server.restful_api.general.endpoint import Endpoint


class GeneralEndpointDataV1(Endpoint):
    def _pre_process(self):
        pass

    def _post_process(self):
        response_headers = self._response_holder.get_response_headers()

        response_headers['Access-Control-Allow-Origin'] = '*'
        response_headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response_headers['Access-Control-Allow-Methods'] = 'GET'

        self._response_holder.set_response_headers(response_headers)

    @abc.abstractmethod
    def _get(self):
        """
        Override this method in any subclass of Endpoint to manipulate the Response object
        in case the request is a GET request
        :return: None - the output of this function is ignored
        """
        pass

    def _put(self):
        """
        The PUT-method is not supported by this api version, thus an response indicating a bad request is returned
        :return: A ResponseHolder holding a response with the bad request code
        """
        return self._return_bad_request_response(self._response_holder)

    def _post(self):
        """
        The POST-method is not supported by this api version, thus an response indicating a bad request is returned
        :return: A ResponseHolder holding a response with the bad request code
        """
        return self._return_bad_request_response(self._response_holder)

    def _delete(self):
        """
        The DELETE-method is not supported by this api version, thus an response indicating a bad request is returned
        :return: A ResponseHolder holding a response with the bad request code
        """
        return self._return_bad_request_response(self._response_holder)

    @staticmethod
    @abc.abstractmethod
    def get_paths():
        return []
