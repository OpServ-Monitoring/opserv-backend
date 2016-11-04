from abc import ABCMeta

from .__general_realtime_historical import GeneralEndpointRealtimeHistorical


class NetworksNetworkGeneralChildEndpoint(GeneralEndpointRealtimeHistorical, metaclass=ABCMeta):
    @staticmethod
    def _get_parent():
        from .networks_network import NetworksNetworkEndpoint

        return NetworksNetworkEndpoint

    @staticmethod
    def _get_mandatory_parameters():
        from .networks_network import NetworksNetworkEndpoint

        return [
            NetworksNetworkEndpoint.get_network_id_validator()
        ]

    @classmethod
    def _get_children(cls):
        return []

    def _get_component_type(self) -> str:
        return "network"

    def _get_component_arg(self) -> str:
        return self._request_holder.get_params()["network"]
