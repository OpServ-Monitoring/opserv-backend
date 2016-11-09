from .data_api_versions_endpoint import DataApiVersionsEndpoint
from ..general.endpoint_management import EndpointManagement


class EndpointManagementData(EndpointManagement):
    @classmethod
    def get_prefix(cls):
        return ""

    @classmethod
    def get_endpoints(cls):
        return [
            DataApiVersionsEndpoint
        ]
