from misc.standalone_helper import decode_string, double_decode_string
from .__general_data_v1 import GeneralEndpointDataV1


class DisksDiskEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        disk_id = self._request_holder.get_params()["disk"]
        disk_id = decode_string(disk_id)

        persisted_info = self._outbound_gate.get_last_measurement("disk", disk_id, "info")

        if persisted_info is not None:
            self._response_holder.update_body_data({
                "timestamp": persisted_info["timestamp"],
                "general-info": persisted_info["value"]
            })

        return True

    @classmethod
    def get_paths(cls):
        return [
            "/disks/<string:disk>"
        ]

    @classmethod
    def get_name(cls):
        return "disk entity"

    @classmethod
    def _get_parent(cls):
        from .disks import DisksEndpoint

        return DisksEndpoint

    @classmethod
    def _get_children(cls):
        from .disks_disk_usage import DisksDiskUsageEndpoint
        from .disks_disk_status import DisksDiskStatusEndpoint
        from .disks_disk_temperature import DisksDiskTemperatureEndpoint

        return [
            ("/usage", DisksDiskUsageEndpoint),
            ("/status", DisksDiskStatusEndpoint),
            ("/temperature", DisksDiskTemperatureEndpoint)
        ]

    @classmethod
    def _get_mandatory_parameters(cls):
        return [
            cls.get_disk_id_validator()
        ]

    @classmethod
    def get_disk_id_validator(cls):
        return "disk", lambda x: cls._outbound_gate.is_argument_valid(
            "disk", double_decode_string(x))
