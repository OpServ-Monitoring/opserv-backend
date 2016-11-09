from .preferences_api_versions_endpoint import PreferencesApiVersionsEndpoint
from ..general.endpoint_management import EndpointManagement


class EndpointManagementPreferences(EndpointManagement):
    @classmethod
    def get_prefix(cls):
        return ""

    @classmethod
    def get_endpoints(cls):
        return [
            PreferencesApiVersionsEndpoint
        ]
