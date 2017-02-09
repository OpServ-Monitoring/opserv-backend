from abc import ABCMeta

from .__general_realtime_historical import GeneralEndpointRealtimeHistorical


class DisksDiskGeneralChildEndpoint(GeneralEndpointRealtimeHistorical, metaclass=ABCMeta):
    @classmethod
    def _get_parent(cls):
        from .disks_disk import DisksDiskEndpoint

        return DisksDiskEndpoint

    @classmethod
    def _get_mandatory_parameters(cls):
        from .disks_disk import DisksDiskEndpoint

        return [
            DisksDiskEndpoint.get_disk_id_validator()
        ]

    @classmethod
    def _get_children(cls):
        return []

    @classmethod
    def _get_component_type(cls) -> str:
        return "disk"

    def _get_component_arg(self) -> str:
        return self._request_holder.get_params()["disk"]
