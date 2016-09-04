from server.restful_api.data.v1.sample_data import SampleData
from server.restful_api.version_management import VersionManagement


class DataManagementV1(VersionManagement):
    def __init__(self, api, base_api_path, is_current=False):
        super(DataManagementV1, self).__init__(api, base_api_path, is_current)

    def _get_version_path(self):
        return "/v1"

    def add_version_to_api(self):
        # TODO add more paths
        # self._add_endpoint_to_api('/sample/<int:sample_id>/id/<int:sample_id2>', SampleData)

        self._add_endpoint_to_api('/components/cpu/<int:cpu>/cpu-cores/<int:cpu_core>/usage', SampleData)
