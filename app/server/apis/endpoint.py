import traceback

import tornado.escape
import tornado.web

from misc import standalone_helper
from server.data_gates.default_data_gate import DefaultDataGate


class Endpoint(tornado.web.RequestHandler):
    """
    The base class for any http endpoint to use. This assures a equal response structure and error handling
    by providing additional methods to the ones provided by `tornado.web.RequestHandler`.

    A response should be made by calling ``respond`` instead of using the build-in `write` function.
    """

    # The sole interface all api endpoints should utilize to receive and persist data
    # Also this allows for easier unit testing through dependency injection.
    _outbound_gate = DefaultDataGate

    def set_default_headers(self):
        """
        As we want to allow HEAD requests to retrieve the allowed HTTP methods of an endpoint we have to add the
        corresponding header to every response.
        In addition data returned in the body of any REST endpoint response is formatted in the JSON.
        """
        super().set_default_headers()

        self.set_header("Content-Type", "application/vnd.api+json")
        self.set_header("Allow", "HEAD")

    def head(self):
        """
        By default any request processed by the `tornado.web.RequestHandler` returns a `HTTPError` with
        code 405 "Method Not Allowed". As we want to allow HEAD requests to retrieve the allowed HTTP methods of an
        endpoint we have to override the default behaviour.
        """

    # TODO Add documentation
    def respond(self, data) -> None:
        """


        :param data:
            The data to be part of the response. Should either be a resource object in form of a dictionary or
             a list of resource object. For more information visit http://jsonapi.org.
        """
        path = self.get_path()

        self.write(
            tornado.escape.json_encode({
                "data": data,
                "links": {
                    "self": path
                }
            })
        )

    def get_path(self) -> str:
        """
        A helper method to retrieve full URL as called by the request striping a possibly trailing slash.

        :return: A string representing the URL called by the request
        """
        path = self.request.protocol + "://" + self.request.host + self.request.uri
        if path.endswith("/"):
            path = path[:-1]

        return path

    @classmethod
    def get_resource_object(cls, resource_type: str, resource_id: str, attributes: dict = None) -> dict:
        """
        A helper method that builds a resource object that may be used as part of a single resource object presentation.

        :param resource_type:
            A string that represent the type of this resource
        :param resource_id:
            A string that uniquely identifies the resource of this resource type
        :param attributes:
            A dictionary holding any information of the resource. It should not include type or id of the resource as
            both of these are treated separately

        :return:
            A dictionary object holding the passed information in form of a resource object with attributes used for
            requests that target single resources. For more information visit http://jsonapi.org.
        """
        data = {
            "type": resource_type,
            "id": resource_id
        }

        if attributes is not None and len(attributes) > 0:
            data["attributes"] = attributes

        return data

    @classmethod
    def get_resource_reference(cls, resource_type: str, resource_id: str, parent_path: str) -> dict:
        """
        A helper method that builds a resource object that may be used as part of a resource object collection.

        :param resource_type:
            A string that represent the type of this resource
        :param resource_id:
            A string that uniquely identifies the resource of this resource type
        :param parent_path:
            The URI of the endpoint that presents the list of resource objects for this resource type

        :return:
            A dictionary object holding the passed information in form of a resource object without attributes used
            for requests that target resource collections. For more information visit http://jsonapi.org.
        """
        encoded_id = standalone_helper.encode_string(resource_id)

        return {
            "type": resource_type,
            "id": resource_id,
            "links": {
                "self": parent_path + "/" + encoded_id
            }
        }

    def write_error(self, status_code, **kwargs) -> None:
        """
        Overrides the built-in function to implement custom error responses.
        If in debug mode and caused by an uncaught exception this will add the stacktrace to the error response.

        If you want to provide more detailed information you may pass a "summary" or more "details" into the kwargs
        of `send_error`.

        :param status_code:
            The status code that was passed either by a raised `HTTPError` or a call to `send_error`
        :param kwargs:
            May include additional information in case such is passed to the kwargs of ``send_error``.
            If this error was caused by an uncaught exception (including HTTPError), an ``exc_info`` triple will be
            available as ``kwargs["exc_info"]`` including the stack trace.
        """
        if "summary" in kwargs and kwargs["summary"] is not None:
            if self._reason is None:
                self._reason = ""
            self._reason += " - "
            self._reason += kwargs["summary"]

        error = {
            "status": status_code,
            "title": self._reason,
        }

        if "details" in kwargs and kwargs["details"] is not None:
            error["detail"] = kwargs["details"]

        # in debug mode, try to append the error trace
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            error_trace = []

            for line in traceback.format_exception(*kwargs["exc_info"]):
                error_trace.append(line)

            error["meta"] = {
                "stacktrace": error_trace
            }

        response = {
            "errors": [
                error
            ]
        }

        self.finish(tornado.escape.json_encode(response))
