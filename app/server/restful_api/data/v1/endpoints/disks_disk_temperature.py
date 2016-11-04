from .disks_disk__general_child import DisksDiskGeneralChildEndpoint


class DisksDiskTemperatureEndpoint(DisksDiskGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/disks/<string:disk>/temperature"
        ]

    @staticmethod
    def get_name():
        return "disk temperature measurement"

    def _get_component_metric(self) -> str:
        return "temperature"
