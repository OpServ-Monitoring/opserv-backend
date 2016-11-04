from .disks_disk__general_child import DisksDiskGeneralChildEndpoint


class DisksDiskUsageEndpoint(DisksDiskGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/disks/<string:disk>/usage"
        ]

    @staticmethod
    def get_name():
        return "disk usage measurement"

    def _get_component_metric(self) -> str:
        return "usage"
