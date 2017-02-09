from .disks_disk__general_child import DisksDiskGeneralChildEndpoint


class DisksDiskTemperatureEndpoint(DisksDiskGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/disks/<string:disk>/temperature"
        ]

    @classmethod
    def get_name(cls):
        return "disk temperature measurement"

    @classmethod
    def _get_component_metric(cls) -> str:
        return "temperature"
