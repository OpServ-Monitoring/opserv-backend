from .preference import PreferenceEndpoint
from .preferences_api_v1_endpoint import PreferencesApiV1Endpoint
from ...general.endpoint_management import EndpointManagement


class EndpointManagementPreferencesV1(EndpointManagement):
    @staticmethod
    def get_prefix():
        return "/v1"

    @staticmethod
    def get_endpoints():
        return [
            PreferencesApiV1Endpoint,  # /v1
            PreferenceEndpoint
        ]
