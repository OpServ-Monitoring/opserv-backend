from .preference import PreferenceEndpoint
from .preferences_api_v1_endpoint import PreferencesApiV1Endpoint
from ...general.endpoint_management import EndpointManagement


class EndpointManagementPreferencesV1(EndpointManagement):
    @classmethod
    def get_prefix(cls):
        return "/v1"

    @classmethod
    def get_endpoints(cls):
        return [
            PreferencesApiV1Endpoint,  # /v1
            PreferenceEndpoint
        ]
