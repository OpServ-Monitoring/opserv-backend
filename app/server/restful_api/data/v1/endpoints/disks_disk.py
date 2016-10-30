from ....general.endpoint import Endpoint


# TODO Implement endpoint
class DisksDiskEndpoint(Endpoint):
    def _get(self) -> bool:
        # TODO implement endpoint
        from app.database.unified_database_interface import UnifiedDatabaseInterface
        disk_id = self._request_holder.get_params()["disk"]

        persisted_info = UnifiedDatabaseInterface.get_measurement_data_reader().get_last_value("disk", disk_id, "info")

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

    @staticmethod
    def get_disk_id_validator():
        # TODO Validate disk id
        return "disk", lambda x: True
