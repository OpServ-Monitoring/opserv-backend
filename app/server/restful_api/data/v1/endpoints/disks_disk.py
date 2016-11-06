from .__general_data_v1 import GeneralEndpointDataV1


class DisksDiskEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        disk_id = self._request_holder.get_params()["disk"]

        persisted_info = self._outbound_gate.get_last_measurement("disk", disk_id, "info")

        if persisted_info is not None:
            self._response_holder.set_body_data({
                "timestamp": persisted_info[0],
                "general-info": persisted_info[1]
            })

        return True

    @staticmethod
    def get_paths():
        return [
            "/disks/<string:disk>"
        ]

    @staticmethod
    def get_name():
        return "disk entity"

    @staticmethod
    def _get_parent():
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

    @staticmethod
    def _get_mandatory_parameters():
        return [
            DisksDiskEndpoint.get_disk_id_validator()
        ]

    @classmethod
    def get_disk_id_validator(cls):
        return "disk", lambda x: cls._outbound_gate.is_argument_valid(x, "disks")
