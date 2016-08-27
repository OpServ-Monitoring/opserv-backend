from flask_restful import Api

import server.restful_api.statistics.__management as statistics_api_management


def init_rest_api(app):
    api = Api(app)

    statistics_api_management.init_statistics_api(api)
    # TODO init_userdata_api(api)
