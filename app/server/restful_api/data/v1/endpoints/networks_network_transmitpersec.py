from .networks_network__general_child import NetworksNetworkGeneralChildEndpoint


class NetworksNetworkTransmitpersecEndpoint(NetworksNetworkGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/networks/<string:network>/transmitpersec"
        ]

    @staticmethod
    def get_name():
        return "network transmitpersec measurement"

    def _get_component_metric(self) -> str:
        return "transmitpersec"
