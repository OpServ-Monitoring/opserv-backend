from server.restful_api.data.v1.endpoints.memory__general_child import MemoryGeneralChildEndpoint


class MemoryUsedEndpoint(MemoryGeneralChildEndpoint):
    @classmethod
    def _get_component_metric(cls) -> str:
        return "used"

    @classmethod
    def get_name(cls):
        return "GIVE ME A NAME"

    @classmethod
    def get_paths(cls):
        return [
            "/memory/used"
        ]
