from .endpoint_api_root import ApiRootEndpoint
from ..general.endpoint_management import EndpointManagement


class EndpointManagementRoot(EndpointManagement):
    @staticmethod
    def get_prefix():
        return ""

    @staticmethod
    def get_endpoints():
        return [
            ApiRootEndpoint
        ]
