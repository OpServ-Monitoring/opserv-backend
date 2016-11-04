from abc import ABCMeta

from .__general_realtime_historical import GeneralEndpointRealtimeHistorical


class DisksDiskGeneralChildEndpoint(GeneralEndpointRealtimeHistorical, metaclass=ABCMeta):
    @staticmethod
    def _get_parent():
        from .disks_disk import DisksDiskEndpoint

        return DisksDiskEndpoint

    @staticmethod
    def _get_mandatory_parameters():
        from .disks_disk import DisksDiskEndpoint

        return [
            DisksDiskEndpoint.get_disk_id_validator()
        ]

    @classmethod
    def _get_children(cls):
        return []

    def _get_component_type(self) -> str:
        return "disk"

    def _get_component_arg(self) -> str:
        return self._request_holder.get_params()["disk"]
