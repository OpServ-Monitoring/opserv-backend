from server.restful_api.data.endpoint_management_data import EndpointManagementData
from server.restful_api.data.v1.endpoint_management_data_v1 import EndpointManagementDataV1


class RestApiManagement:

    @staticmethod
    def get_endpoint_managements():
        """
        This method returns an array of each implemented endpoint managements represented as tupels. Each tupel consists
        of a path prefix, the management class and an optional boolean indicating whether the managed endpoints are
        the newest version. For each path prefix there should only be one tupel set as newest version.
        :return: an array of tupels containing the endpoint management classes and some additional data.
        """
        base_api_path = "/api"
        data_api_path = base_api_path + "/data"
        preferences_api_path = base_api_path + "/preferences"

        return [
            # api
            (base_api_path, EndpointManagementRoot),

            # data api
            (data_api_path, EndpointManagementData),  # data version overview
            (data_api_path, EndpointManagementDataV1, True),  # data v1

            # preferences api
            (preferences_api_path, None),  # TODO preferences version overview
            (preferences_api_path, None, True)  # TODO preferences v1
        ]


from server.restful_api.general.endpoint_management import EndpointManagement


class EndpointManagementRoot(EndpointManagement):
    @staticmethod
    def get_prefix():
        return ""

    @staticmethod
    def get_endpoints():
        return [
            ApiRootEndpoint
        ]


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
    def _get_parent_name():
        return None

    def _get_children(self):
        from server.restful_api.data.data_api_versions_endpoint import DataApiVersionsEndpoint

        return [
            ("/data", DataApiVersionsEndpoint)
        ]
