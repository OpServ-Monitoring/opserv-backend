from .data_api_versions_endpoint import DataApiVersionsEndpoint
from ..general.endpoint_management import EndpointManagement


class EndpointManagementData(EndpointManagement):
    @staticmethod
    def get_prefix():
        return ""

    @staticmethod
    def get_endpoints():
        return [
            DataApiVersionsEndpoint
        ]
