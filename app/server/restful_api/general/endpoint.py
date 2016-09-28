import re
from abc import ABCMeta, abstractmethod
from collections import Iterable

from app.server.restful_api.general.requestholder import RequestHolder
from app.server.restful_api.general.responseholder import ResponseHolder


class Endpoint(metaclass=ABCMeta):
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

        keep_processing = self._pre_process()

        if keep_processing:
            keep_processing = keep_processing and self.__main_process()

            if keep_processing:
                self._post_process()

        return self._response_holder

    def _pre_process(self) -> bool:
        """
        This method is called before any of the processing functions _get(), _post(), _put() or _delete() is executed.
        Override this method in any subclass of Endpoint to manipulate the Request or Response object beforehand.
        :return: A boolean indicating whether to carry on processing the request or not
        """
        body = {
            'data': {},
            'links': self.__generate_links()
        }

        self._response_holder.set_body(body)

        return True

    def __main_process(self):
        method = self._request_holder.get_http_method()

        if method == RequestHolder.METHOD_GET():
            return self._get()
        elif method == RequestHolder.METHOD_POST():
            return self._post()
        elif method == RequestHolder.METHOD_PUT():
            return self._put()
        elif method == RequestHolder.METHOD_DELETE():
            return self._delete()
        else:
            self._set_bad_request_response(self._response_holder)

            return False

    @abstractmethod
    def _get(self) -> bool:
        """
        Override this method in any subclass of Endpoint to manipulate the Response object
        in case the request is a GET request
        :return: A boolean indicating whether to carry on processing the request or not
        """
        pass

    @abstractmethod
    def _post(self) -> bool:
        """
        Override this method in any subclass of Endpoint to manipulate the Response object
        in case the request is a POST request
        :return: A boolean indicating whether to carry on processing the request or not
        """
        pass

    @abstractmethod
    def _put(self) -> bool:
        """
        Override this method in any subclass of Endpoint to manipulate the Response object
        in case the request is a PUT request
        :return: A boolean indicating whether to carry on processing the request or not
        """
        pass

    @abstractmethod
    def _delete(self) -> bool:
        """
        Override this method in any subclass of Endpoint to manipulate the Response object
        in case the request is a DELETE request
        :return: A boolean indicating whether to carry on processing the request or not
        """
        pass

    @abstractmethod
    def _post_process(self) -> bool:
        """
        This method is called after one of the processing functions _get(), _post(), _put() or _delete() is executed.
        Override this method in any subclass of Endpoint to manipulate the Response object afterwards.
        :return: A boolean indicating whether to carry on processing the request or not
        """
        pass

    @staticmethod
    @abstractmethod
    def get_paths():
        """
        Override this method in any subclass of Endpoint to set the paths this endpoint should operate on
        :return: A tupel of paths this endpoint should operate on
        """
        pass

    def __generate_links(self):
        links = {}

        self.__generate_self_reference(links)
        self.__generate_parent_reference(links)
        self.__generate_children_references(links)

        return links

    def __generate_self_reference(self, links):
        uri = self._request_holder.get_uri()
        name = self.get_name()
        if name is not None:
            links['self'] = self._get_link_element(uri, name)

    def __generate_parent_reference(self, links):
        parent_uri = self.__get_parent_uri()
        parent_name = self.__get_parent_name()
        if parent_uri is not None and parent_name is not None:
            links['parent'] = self._get_link_element(parent_uri, parent_name)

    def __generate_children_references(self, links):
        children = self.__get_children()
        if children is not None and isinstance(children, list) and len(children) > 0:
            links['children'] = children

    @staticmethod
    @abstractmethod
    def get_name():
        """
        Each type of endpoint should have a name which is displayed in the api as part of the links section
        :return: A string indicating the type of resource this endpoint represents
        """
        pass

    @staticmethod
    @abstractmethod
    def _get_parent():
        """
        To support HATEOAS each type of endpoint should define a parent endpoint.
        :return: A (subclass of) endpoint that is the direct api-parent of this endpoint or None
        """
        pass

    def __get_parent_uri(self):
        found_match = self.__match_for_parent_path()

        if found_match:
            return found_match.group(1)
        else:
            return None

    def __get_parent_name(self):
        parent = self._get_parent()

        parent_name = None
        if parent is not None:
            parent_name = parent.get_name()

        return parent_name

    def __get_children(self):
        """
        Returns an array holding reference objects to append as children to the link section of the response
        :return: An array holding reference objects to append as children to the response
        """
        children = []

        found_match = self.__match_for_children_base_path()
        if found_match:
            base_path = found_match.group(1)

            children_data = self._get_children()

            for child_data in children_data:
                uri = base_path + child_data[0]
                endpoint = child_data[1]

                children.append(self._get_link_element(uri, endpoint.get_name()))

        return children

    @staticmethod
    @abstractmethod
    def _get_children() -> Iterable:
        pass

    def __match_uri_with_regex(self, regex):
        uri = self._request_holder.get_uri()

        return re.match(regex, uri)

    def __match_for_children_base_path(self):
        regex = "(.+\/api.*\/*.*)(\?.*){0,1}"

        return self.__match_uri_with_regex(regex)

    def __match_for_parent_path(self):
        regex = "(.+\/api.*)\/.+(\?.*){0,1}"

        return self.__match_uri_with_regex(regex)

    @staticmethod
    def _get_link_element(uri, name):
        """
        Static helper that returns a reference dictionary object to use in the links section of the response
        :param uri: The uri of the referenced endpoint
        :param name: The name of the references endpoint
        :return: a dictionary including the passed uri and name
        """
        return {'href': uri, 'name': name}

    def __set_fault_response(self, status_code, error_message):
        """
        helper method to set an error response
        :param status_code: The http status code the response should have
        :param error_message: The error message to display as part of the response
        :return: None
        """
        self._response_holder.set_body(
            {
                "error_message": error_message
            }
        )
        self._response_holder.set_status(status_code)

    def _set_bad_request_response(self, error_message=None):
        """
        helper method to set a bad request response
        :param error_message: The error_message to display
        :return: None
        """
        if error_message is None:
            error_message = "Bad Request"

        self.__set_fault_response(400, error_message)

    def _set_internal_server_error_response(self):
        """
        helper method to set a internal server error response
        :return: None
        """
        self.__set_fault_response(500, "Internal server error")

    @staticmethod
    def KEEP_PROCESSING():
        return True

    @staticmethod
    def STOP_PROCESSING():
        return False
