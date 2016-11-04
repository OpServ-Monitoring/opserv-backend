from .root__general_child import RootGeneralChildEndpoint
from ....general.endpoint import Endpoint


class NetworksEndpoint(RootGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/networks"
        ]

    @staticmethod
    def get_name():
        return "network entities"

    @staticmethod
    def _get_hardware_value_type() -> str:
        return "networks"

    @staticmethod
    def _get_component_type() -> str:
        return "network"

    @staticmethod
    def _get_children_endpoint_type() -> Endpoint:
        from .networks_network import NetworksNetworkEndpoint

        return NetworksNetworkEndpoint
