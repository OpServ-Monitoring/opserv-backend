from .disks_disk__general_child import DisksDiskGeneralChildEndpoint


class DisksDiskUsageEndpoint(DisksDiskGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/disks/<string:disk>/usage"
        ]

    @classmethod
    def get_name(cls):
        return "disk usage measurement"

    def _get_component_metric(self) -> str:
        return "usage"
