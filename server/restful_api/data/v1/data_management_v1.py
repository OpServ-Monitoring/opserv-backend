from server.restful_api.data.v1.sample_data import SampleData
from server.restful_api.version_management import VersionManagement


class DataManagementV1(VersionManagement):
    def __init__(self, api, base_api_path, is_current=False):
        super(DataManagementV1, self).__init__(api, base_api_path, is_current)

    def _get_version_path(self):
        return "/v1"

    def add_version_to_api(self):
        # TODO add more paths
        # self._add_endpoint_to_api('/components', SampleData)

        # self._add_endpoint_to_api('/components/cpu', SampleData)
        # self._add_endpoint_to_api('/components/cpu/<int:cpu>', SampleData)
        # self._add_endpoint_to_api('/components/cpu/<int:cpu>/cpu-cores/', SampleData)
        # self._add_endpoint_to_api('/components/cpu/<int:cpu>/cpu-cores/<int:cpu_core>', SampleData)
        self._add_endpoint_to_api('/components/cpu/<int:cpu>/cpu-cores/<int:cpu_core>/usage', SampleData)

        # self._add_endpoint_to_api('/components/cpu-cores', SampleData)
        # self._add_endpoint_to_api('/components/cpu-cores/<int:cpu_core>', SampleData)
        # self._add_endpoint_to_api('/components/cpu-cores/<int:cpu_core>/usage', SampleData)

        # self._add_endpoint_to_api('/components/gpu', SampleData)
        # self._add_endpoint_to_api('/components/memory', SampleData)
        # self._add_endpoint_to_api('/components/processes', SampleData)
        # self._add_endpoint_to_api('/components/filesystem', SampleData)
