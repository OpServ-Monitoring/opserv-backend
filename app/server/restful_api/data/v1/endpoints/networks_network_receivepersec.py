from .networks_network__general_child import NetworksNetworkGeneralChildEndpoint


class NetworksNetworkReceivepersecEndpoint(NetworksNetworkGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/networks/<string:network>/receivepersec"
        ]

    @staticmethod
    def get_name():
        return "network receivepersec measurement"

    def _get_component_metric(self) -> str:
        return "receivepersec"
