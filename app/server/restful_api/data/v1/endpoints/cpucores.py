from .root__general_child import RootGeneralChildEndpoint
from ....general.endpoint import Endpoint


class CpucoresEndpoint(RootGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/cpu-cores"
        ]

    @classmethod
    def get_name(cls):
        return "cpu core entities"

    @classmethod
    def _get_children_endpoint_type(cls) -> Endpoint:
        from .cpucores_cpucore import CpucoresCpucoreEndpoint

        return CpucoresCpucoreEndpoint

    @classmethod
    def _get_hardware_value_type(cls) -> str:
        return "cpucores"
