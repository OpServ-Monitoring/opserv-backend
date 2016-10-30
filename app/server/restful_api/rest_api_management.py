from .api_root.endpoint_management_api_root import EndpointManagementRoot
from .data.endpoint_management_data import EndpointManagementData
from .data.v1.endpoint_management_data_v1 import EndpointManagementDataV1
from .preferences.endpoint_management_preferences import EndpointManagementPreferences
from .preferences.v1.endpoint_management_preferences_v1 import EndpointManagementPreferencesV1


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
            (preferences_api_path, EndpointManagementPreferences),
            (preferences_api_path, EndpointManagementPreferencesV1, True)
        ]
