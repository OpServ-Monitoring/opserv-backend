import server.restful_api.data.v1.__management as v1


def init_data_api(api, base_api_path):
    """
        Initializes all versions of the data api
    """

    v1.init_api(api, base_api_path + "/v1")
    # Add upcoming versions of the data api here

    # Initialize the newest supported version as "current"
    v1.init_api(api, base_api_path + "/current")
