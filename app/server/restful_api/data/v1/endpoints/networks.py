from .root__general_child import RootGeneralChildEndpoint
from ....general.endpoint import Endpoint


class NetworksEndpoint(RootGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/networks"
        ]

    @classmethod
    def get_name(cls):
        return "network entities"

    @classmethod
    def _get_hardware_value_type(cls) -> str:
        return "networks"

    @classmethod
    def _get_children_endpoint_type(cls) -> Endpoint:
        from .networks_network import NetworksNetworkEndpoint

        return NetworksNetworkEndpoint
