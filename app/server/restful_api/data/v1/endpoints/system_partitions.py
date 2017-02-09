from .system__general_child import SystemGeneralChildEndpoint


class SystemPartitionsEndpoint(SystemGeneralChildEndpoint):
    @classmethod
    def _get_component_metric(cls) -> str:
        return "partitions"

    @classmethod
    def get_name(cls):
        return "GIVE ME A NAME"

    @classmethod
    def get_paths(cls):
        return [
            "/system/partitions"
        ]
