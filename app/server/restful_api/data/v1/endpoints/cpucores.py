from ....general.endpoint import Endpoint
from .root__general_child import RootGeneralChildEndpoint


class CpucoresEndpoint(RootGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/cpu-cores"
        ]

    @staticmethod
    def get_name():
        return "cpu core entities"

    @staticmethod
    def _get_children_endpoint_type() -> Endpoint:
        from .cpucores_cpucore import CpucoresCpucoreEndpoint

        return CpucoresCpucoreEndpoint

    @staticmethod
    def _get_hardware_value_type() -> str:
        return "cores"

    @staticmethod
    def _get_component_type() -> str:
        return "core"
