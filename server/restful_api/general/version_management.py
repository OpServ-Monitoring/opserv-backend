import abc

from flask import request
from flask_restful import Resource

from server.restful_api.general.requestholder import RequestHolder


class VersionManagement:
    __api = None
    __base_api_path = None
    __is_current = False
    __version = None

    def __init__(self, api, base_api_path, is_current=False):
        self.__api = api
        self.__base_api_path = base_api_path
        self.__is_current = is_current

        self.__version = self._get_version_path()

    @abc.abstractmethod
    def add_version_to_api(self):
        # abstract method that every subclass should implement to add endpoints using __add_endpoint_to_api()
        return

    def _add_endpoint_to_api(self, endpoint, endpoint_name):
        class CustomResource(Resource):
            def get(self, **params):
                return self.__handle_request(**params)

            def post(self, **params):
                return self.__handle_request(**params)

            def put(self, **params):
                return self.__handle_request(**params)

            def delete(self, **params):
                return self.__handle_request(**params)

            def __handle_request(self, **params):
                request_holder = self.__get_request_holder(**params)
                response_holder = endpoint.handle_request(request_holder)

                return response_holder.get_body(), response_holder.get_status(), response_holder.get_response_headers()

            def __get_request_holder(self, **params):
                # http request method mapped accordingly to the RequestHolder definition
                http_method = self.__get_method_code(request.method)

                # data passed as http headers
                if http_method == RequestHolder.METHOD_GET():
                    headers = request.args
                elif http_method == RequestHolder.METHOD_POST() \
                        or http_method == RequestHolder.METHOD_PUT():
                    headers = request.form
                else:
                    headers = None

                # TODO Parse request-body into RequestHolder
                body = None

                return RequestHolder(http_method, headers, params, body)

            @staticmethod
            def __get_method_code(method_string):
                if method_string == "GET":
                    return RequestHolder.METHOD_GET()

                if method_string == "POST":
                    return RequestHolder.METHOD_POST()

                if method_string == "PUT":
                    return RequestHolder.METHOD_PUT()

                if method_string == "DELETE":
                    return RequestHolder.METHOD_DELETE()

                return None

        resource = CustomResource()

        paths = self.__get_api_paths(endpoint.get_paths())
        self.__api.add_resource(resource, *paths, endpoint=endpoint_name)

    def __get_api_paths(self, sub_paths):
        paths = []

        for sub_path in sub_paths:
            paths.append(self.__base_api_path + self.__version + sub_path)

        if self.__is_current:
            for sub_path in sub_paths:
                paths.append(self.__base_api_path + "/current" + sub_path)

        return tuple(paths)

    @abc.abstractmethod
    def _get_version_path(self):
        # abstract method that every subclass should implement to return its version path
        pass
