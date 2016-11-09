from .root__general_child import RootGeneralChildEndpoint
from ....general.endpoint import Endpoint


class DisksEndpoint(RootGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/disks"
        ]

    @classmethod
    def get_name(cls):
        return "disk entities"

    @classmethod
    def _get_hardware_value_type(cls) -> str:
        return "disks"

    @classmethod
    def _get_children_endpoint_type(cls) -> Endpoint:
        from .disks_disk import DisksDiskEndpoint

        return DisksDiskEndpoint
