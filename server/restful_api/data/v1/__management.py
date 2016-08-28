from server.restful_api.data.v1.sample_data import SampleData


def init_api(api, base_api_path):
    """
        Initializes and lists all available paths available in this version
    """

    api.add_resource(SampleData, base_api_path + '/sample/<int:sample_id>/id/<int:sample_id2>', endpoint='sample')
    # TODO Add further resources / paths
