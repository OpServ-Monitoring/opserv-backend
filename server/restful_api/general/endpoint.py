import abc

from server.restful_api.general.requestholder import RequestHolder
from server.restful_api.general.responseholder import ResponseHolder


class Endpoint:
    _request_holder = None
    _response_holder = None

    def __init__(self):
        self._response_holder = ResponseHolder()

    def handle_request(self, request_holder):
        """
        Handles the processing of a incoming http request by executing the _pre_process() function,
        any of the processing functions _get(), _post(), _put() or _delete() and finally the _pre_process() function
        :return: The final Response object to answer the request with
        """
        self._request_holder = request_holder

        self._pre_process()

        method = self._request_holder.get_http_method()
        if method == RequestHolder.METHOD_GET():
            self._get()
        elif method == RequestHolder.METHOD_POST():
            self._post()
        elif method == RequestHolder.METHOD_PUT():
            self._put()
        elif method == RequestHolder.METHOD_DELETE():
            self._delete()
        else:
            return self._return_bad_request_response(self._response_holder)

        self._post_process()

        return self._response_holder

    def _pre_process(self):
        """
        This method is called before any of the processing functions _get(), _post(), _put() or _delete() is executed.
        Override this method in any subclass of Endpoint to manipulate the Request or Response object beforehand.
        :return: None - the output of this function is ignored
        """
        body = {
            'data': {},
            'links': self.__generate_links(self._request_holder)
        }

        self._response_holder.set_body(body)

    @abc.abstractmethod
    def _get(self):
        """
        Override this method in any subclass of Endpoint to manipulate the Response object
        in case the request is a GET request
        :return: None - the output of this function is ignored
        """
        pass

    @abc.abstractmethod
    def _post(self):
        """
        Override this method in any subclass of Endpoint to manipulate the Response object
        in case the request is a POST request
        :return: None - the output of this function is ignored
        """
        pass

    @abc.abstractmethod
    def _put(self):
        """
        Override this method in any subclass of Endpoint to manipulate the Response object
        in case the request is a PUT request
        :return: None - the output of this function is ignored
        """
        pass

    @abc.abstractmethod
    def _delete(self):
        """
        Override this method in any subclass of Endpoint to manipulate the Response object
        in case the request is a DELETE request
        :return: None - the output of this function is ignored
        """
        pass

    @abc.abstractmethod
    def _post_process(self):
        """
        This method is called after one of the processing functions _get(), _post(), _put() or _delete() is executed.
        Override this method in any subclass of Endpoint to manipulate the Response object afterwards.
        :return: None - the output of this function is ignored
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_paths():
        """
        Override this method in any subclass of Endpoint to set the paths this endpoint should operate on
        :return: A tupel of paths this endpoint should operate on
        """
        return []

    @staticmethod
    def __generate_links(request_holder):
        uri = request_holder.get_uri()

        links = {
            'self': {'href': uri, 'name': 'niy'}
        }

        # TODO Get link for parent and validate
        if True:
            links['parent'] = {'href': None, 'name': 'niy'}

        # TODO Get links for children
        if True:
            links['children'] = []

        return links

    @staticmethod
    def _return_bad_request_response(response, error_message=None):
        """
        Static helper that returns a ResponseHolder-object to indicate a bad request
        :param response: The current ResponseHolder-object
        :param error_message: An optional error message to exchange the standard message
        :return: A ResponseHolder-object indicating a bad request
        """
        if error_message is None:
            error_message = "Bad Request"
        response.set_body(
            {
                "error_message": error_message
            }
        )
        response.set_status(400)

        return response
