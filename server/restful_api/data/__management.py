# from server.restful_api.data.v1.data_management_v1 import DataManagementV1
from server.restful_api.data.v1.data_management_v1 import DataManagementV1


def init_data_api(api, base_api_path):
    """
        Initializes all versions of the data api
    """

    # DataManagementV1(api, base_api_path, is_current=True).add_version_to_api()
    DataManagementV1(api, base_api_path, is_current=True).add_version_to_api()

    # Add upcoming versions of the data api here

    # TODO add api endpoint for base_api_path: "/api/data"
