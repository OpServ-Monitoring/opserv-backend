from server.restful_api.data.v1.endpoints.overview import OverviewEndpoint
from server.restful_api.data.v1.endpoints.components_cpucore_usage import CpucoreUsageEndpoint
from server.restful_api.data.v1.endpoints.components_cpucores import CpucoresEndpoint
from server.restful_api.data.v1.endpoints.compontents import ComponentsEndpoint
from server.restful_api.general.endpoint_management import EndpointManagement


class EndpointManagementDataV1(EndpointManagement):

    @staticmethod
    def get_prefix():
        return "/v1"

    @staticmethod
    def get_endpoints():
        return [
            OverviewEndpoint,  # /v1
            ComponentsEndpoint,  # /v1/components
            CpucoresEndpoint,  # /v1/components/cpu/<int:cpu>/cpu-cores and /v1/components/cpu-cores
            CpucoreUsageEndpoint  # /v1/components/cpu/<int:cpu>/cpu-cores/usage and /v1/components/cpu-cores/usage
        ]
