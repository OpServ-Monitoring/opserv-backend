from .disks_disk__general_child import DisksDiskGeneralChildEndpoint


class DisksDiskStatusEndpoint(DisksDiskGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/disks/<string:disk>/status"
        ]

    @classmethod
    def get_name(cls):
        return "disk status measurement"

    @classmethod
    def _get_component_metric(cls) -> str:
        return "status"
