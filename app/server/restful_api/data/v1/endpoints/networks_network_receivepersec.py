from .networks_network__general_child import NetworksNetworkGeneralChildEndpoint


class NetworksNetworkReceivepersecEndpoint(NetworksNetworkGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/networks/<string:network>/receivepersec"
        ]

    @classmethod
    def get_name(cls):
        return "network receivepersec measurement"

    def _get_component_metric(self) -> str:
        return "receivepersec"
