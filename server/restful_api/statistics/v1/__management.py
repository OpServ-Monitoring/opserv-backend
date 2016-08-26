from server.restful_api.statistics.v1.sample_data import SampleData


def init_api(api):
    api.add_resource(SampleData, '/sample/<int:id>', endpoint='sample')
