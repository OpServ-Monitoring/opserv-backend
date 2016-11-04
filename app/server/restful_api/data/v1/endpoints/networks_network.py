from server.data_gates.default_data_gate import DefaultDataGate
from .__general_data_v1 import GeneralEndpointDataV1


class NetworksNetworkEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        network_id = self._request_holder.get_params()["network"]

        persisted_info = DefaultDataGate.get_last_measurement("network", network_id, "info")

        if persisted_info is not None:
            self._response_holder.set_body_data({
                "timestamp": persisted_info[0],
                "general-info": persisted_info[1]
            })

        return True

    @staticmethod
    def get_paths():
        return [
            "/networks/<string:network>"
        ]

    @staticmethod
    def get_name():
        return "network entity"

    @staticmethod
    def _get_parent():
        from .networks import NetworksEndpoint

        return NetworksEndpoint

    @classmethod
    def _get_children(cls):
        from .networks_network_receivepersec import NetworksNetworkReceivepersecEndpoint
        from .networks_network_transmitpersec import NetworksNetworkTransmitpersecEndpoint

        return [
            ("/receivepersec", NetworksNetworkReceivepersecEndpoint),
            ("/transmitpersec", NetworksNetworkTransmitpersecEndpoint)
        ]

    @staticmethod
    def _get_mandatory_parameters():
        return [
            NetworksNetworkEndpoint.get_network_id_validator()
        ]

    @staticmethod
    def get_network_id_validator():
        return "network", lambda x: DefaultDataGate.is_argument_valid(x, "networks")
