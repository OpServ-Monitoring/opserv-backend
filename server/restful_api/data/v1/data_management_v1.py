from server.restful_api.data.v1.endpoints.components_cpucore_usage import CpucoreUsageEndpoint
from server.restful_api.data.v1.endpoints.compontents import ComponentsEndpoint
from server.restful_api.general.version_management import VersionManagement


class DataManagementV1(VersionManagement):
    def __init__(self, api, base_api_path, is_current=False):
        super(DataManagementV1, self).__init__(api, base_api_path, is_current)

    def _get_version_path(self):
        return "/v1"

    def add_version_to_api(self):
        self._add_endpoint_to_api(CpucoreUsageEndpoint(), endpoint_name="testmebitch")
        self._add_endpoint_to_api(ComponentsEndpoint(), endpoint_name="somename")
