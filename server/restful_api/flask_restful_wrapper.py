from flask import request
from flask_restful import Api, Resource

from server.restful_api.general.requestholder import RequestHolder
from server.restful_api.rest_api_management import RestApiManagement


def init_rest_api(app):
    FlaskRestfulWrapper(app).init_rest_api()


class FlaskRestfulWrapper:
    __api = None

    def __init__(self, app):
        self.__api = Api(app)

    def init_rest_api(self):
        endpoint_managements = RestApiManagement.get_endpoint_managements()

        for endpoint_management_tuple in endpoint_managements:
            self.__init_endpoints(*endpoint_management_tuple)

    def __init_endpoints(self, endpoints_prefix, endpoint_management, is_current=False):
        if endpoint_management is not None:
            version = endpoint_management.get_prefix()
            if version is None:
                version = ""

            endpoints = endpoint_management.get_endpoints()
            for endpoint in endpoints:
                self.__init_endpoint(endpoints_prefix, endpoint, version, is_current)

    def __init_endpoint(self, endpoints_prefix, endpoint_class, version, is_current):
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

                endpoint = endpoint_class()
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

        endpoint_name = endpoints_prefix + version + endpoint_class.__name__

        paths = self.__get_api_paths(endpoints_prefix, endpoint_class.get_paths(), version, is_current)

        self.__api.add_resource(resource, *paths, endpoint=endpoint_name)

    @staticmethod
    def __get_api_paths(base_api_path, sub_paths, version, is_current):
        paths = []

        for sub_path in sub_paths:
            paths.append(base_api_path + version + sub_path)

        if is_current:
            for sub_path in sub_paths:
                paths.append(base_api_path + "/current" + sub_path)

        return tuple(paths)
