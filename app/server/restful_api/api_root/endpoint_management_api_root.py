from .endpoint_api_root import ApiRootEndpoint
from ..general.endpoint_management import EndpointManagement


class EndpointManagementRoot(EndpointManagement):
    @classmethod
    def get_prefix(cls):
        return ""

    @classmethod
    def get_endpoints(cls):
        return [
            ApiRootEndpoint
        ]
