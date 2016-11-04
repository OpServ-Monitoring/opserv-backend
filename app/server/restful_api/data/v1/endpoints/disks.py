from .root__general_child import RootGeneralChildEndpoint
from ....general.endpoint import Endpoint


class DisksEndpoint(RootGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/disks"
        ]

    @staticmethod
    def get_name():
        return "disk entities"

    @staticmethod
    def _get_hardware_value_type() -> str:
        return "disks"

    @staticmethod
    def _get_component_type() -> str:
        return "disk"

    @staticmethod
    def _get_children_endpoint_type() -> Endpoint:
        from .disks_disk import DisksDiskEndpoint

        return DisksDiskEndpoint
