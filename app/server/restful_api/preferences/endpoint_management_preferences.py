from .preferences_api_versions_endpoint import PreferencesApiVersionsEndpoint
from ..general.endpoint_management import EndpointManagement


class EndpointManagementPreferences(EndpointManagement):
    @staticmethod
    def get_prefix():
        return ""

    @staticmethod
    def get_endpoints():
        return [
            PreferencesApiVersionsEndpoint
        ]
