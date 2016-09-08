from server.restful_api.data.endpoint_management_data import EndpointManagementData
from server.restful_api.data.v1.endpoint_management_data_v1 import EndpointManagementDataV1


class RestApiManagement:

    @staticmethod
    def get_endpoint_managements():
        base_api_path = "/api"
        data_api_path = base_api_path + "/data"
        preferences_api_path = base_api_path + "/preferences"

        return [
            # api
            (base_api_path, None),  # TODO api type overview

            # data api
            (data_api_path, EndpointManagementData),  # data version overview
            (data_api_path, EndpointManagementDataV1, True),  # data v1

            # preferences api
            (preferences_api_path, None),  # TODO preferences version overview
            (preferences_api_path, None, True)  # TODO preferences v1
        ]
