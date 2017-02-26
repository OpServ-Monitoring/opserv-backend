from flask import request
from flask_basicauth import BasicAuth
from flask_restful import Api, Resource

from application_settings.app_settings import AppSettings
from .general.requestholder import RequestHolder
from .rest_api_management import RestApiManagement


class FlaskRestfulWrapper:
    __api = None

    # needed for basic authentication
    __basic_auth = None

    def __init__(self, app):
        self.__api = Api(app)

        # enable basic auth if a password is set
        password = AppSettings.get_setting(AppSettings.KEY_PASSWORD)
        if password is not None:
            app.config['BASIC_AUTH_USERNAME'] = 'opserv'
            app.config['BASIC_AUTH_PASSWORD'] = password

            self.__basic_auth = BasicAuth(app)

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
        basic_auth = self.__basic_auth  # read basic_auth from wrapper class

        class CustomResource(Resource):
            if basic_auth is not None:
                # Enable basic auth for every http api endpoint
                method_decorators = [basic_auth.required]

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
                # the uri called to obtain this endpoint
                uri = request.url

                # http request method mapped accordingly to the RequestHolder definition
                http_method = self.__get_method_code(request.method)

                # data passed as http headers
                if http_method == RequestHolder.METHOD_GET():
                    headers = request.args
                elif http_method == RequestHolder.METHOD_POST() or http_method == RequestHolder.METHOD_PUT():
                    headers = request.form
                else:
                    headers = None

                body = request.get_json()

                return RequestHolder(uri, http_method, headers, params, body)

            @classmethod
            def __get_method_code(cls, method_string):
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
        paths = self.__get_api_paths(endpoints_prefix, endpoint_class.get_paths(), version, is_current)
        endpoint_name = endpoints_prefix + version + endpoint_class.__name__

        self.__api.add_resource(resource, *paths, endpoint=endpoint_name)

    @classmethod
    def __get_api_paths(cls, base_api_path, sub_paths, version, is_current):
        paths = []

        for sub_path in sub_paths:
            paths.append(base_api_path + version + sub_path)

        if is_current:
            for sub_path in sub_paths:
                paths.append(base_api_path + "/current" + sub_path)

        return tuple(paths)


def init_rest_api(app):
    FlaskRestfulWrapper(app).init_rest_api()
