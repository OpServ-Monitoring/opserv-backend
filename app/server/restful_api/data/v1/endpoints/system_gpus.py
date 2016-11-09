from .system__general_child import SystemGeneralChildEndpoint


class SystemGpusEndpoint(SystemGeneralChildEndpoint):
    def _get_component_metric(self) -> str:
        return "gpus"

    @classmethod
    def get_name(cls):
        return "GIVE ME A NAME"

    @classmethod
    def get_paths(cls):
        return [
            "/system/gpus"
        ]
