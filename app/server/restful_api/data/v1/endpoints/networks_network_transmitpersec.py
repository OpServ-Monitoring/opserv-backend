from .networks_network__general_child import NetworksNetworkGeneralChildEndpoint


class NetworksNetworkTransmitpersecEndpoint(NetworksNetworkGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/networks/<string:network>/transmitpersec"
        ]

    @classmethod
    def get_name(cls):
        return "network transmitpersec measurement"

    def _get_component_metric(self) -> str:
        return "transmitpersec"
