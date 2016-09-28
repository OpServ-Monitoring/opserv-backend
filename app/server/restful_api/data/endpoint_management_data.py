from app.server.restful_api.data.data_api_versions_endpoint import DataApiVersionsEndpoint
from app.server.restful_api.general.endpoint_management import EndpointManagement


class EndpointManagementData(EndpointManagement):
    @staticmethod
    def get_prefix():
        return ""

    @staticmethod
    def get_endpoints():
        return [
            DataApiVersionsEndpoint
        ]
