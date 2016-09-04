from flask_restful import Api, Resource

import server.restful_api.data.__management as data_api_management
import server.restful_api.preferences.__management as preferences_api_management


def init_rest_api(app):
    """
        Initializes the restful-api including both the endpoints to the statistical data as well as the user preferences
    """
    api = Api(app)
    base_api_path = "/api"

    data_api_management.init_data_api(api, base_api_path + "/data")
    preferences_api_management.init_preferences_api(api, base_api_path + "/preferences")

    api.add_resource(ApiEndpoints, base_api_path)

    # TODO add api endpoint for base_api_path: "/api"


# TODO clean up code

class ApiEndpoints(Resource):
    def get(self):
        return {
            'data': {},
            '_links': {
                'self': "127.0.0.1:31337/api",
                '_down': [
                    {'rel': "data endpoint", 'href': "127.0.0.1:31337/api/data"},
                    {'rel': "preferences endpoint", 'href': "127.0.0.1:31337/api/preferences"}
                ]
            }
        }
