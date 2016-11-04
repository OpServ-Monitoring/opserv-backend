from .disks_disk__general_child import DisksDiskGeneralChildEndpoint


class DisksDiskStatusEndpoint(DisksDiskGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/disks/<string:disk>/status"
        ]

    @staticmethod
    def get_name():
        return "disk status measurement"

    def _get_component_metric(self) -> str:
        return "status"
